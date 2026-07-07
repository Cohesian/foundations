#!/usr/bin/env python3
"""Validate the k-graph: k-graph/ (structure) + content resolved via k-graph.toml.

Layout:
- k-graph/ yaml-only. Every node carries `edges` with three axes:
             g = grouping (ordered children; composites),
             l = linear   (prev / next reading chain),
             r = related  (cross-links).
           Leaves also carry a `data` block (which trees / extensions exist).
- content  resolved per tree by k-graph.toml:
             local_origin  -> <path>/<relative>/<id>.<ext>  (checked on disk)
             remote_origin -> trusted for build artifacts (e.g. renders on CDN)

Checks per node:
- composite edges.g children exist (subdir or <id>.yaml);
- leaf edges.l prev/next and edges.r targets exist among siblings;
- leaf `data` trees are configured in k-graph.toml; local trees have files present.

Non-zero exit on any problem. Stdlib + pyyaml.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    sys.exit("Python 3.11+ (tomllib) required")

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("pyyaml is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
TREE = ROOT / "k-graph"
CONFIG = ROOT / "k-graph.toml"

# Trees whose local files are optional (build artifacts / gitignored).
TRUST_LOCAL_OPTIONAL = frozenset({"data.media.renders"})

problems: list[str] = []


def err(where: Path, msg: str):
    problems.append(f"{where.relative_to(ROOT)}: {msg}")


def load_data_cfg() -> dict:
    if not CONFIG.exists():
        sys.exit(f"config not found: {CONFIG}")
    with CONFIG.open("rb") as fh:
        return tomllib.load(fh).get("data", {})


def tree_spec(cfg: dict, tree_key: str) -> dict | None:
    """Resolve e.g. 'data.media.loci' -> config dict (without 'data.' prefix in walk)."""
    node = cfg
    for part in tree_key.removeprefix("data.").split("."):
        if not isinstance(node, dict):
            return None
        node = node.get(part)
        if node is None:
            return None
    return node if isinstance(node, dict) else None


def iter_data_entries(data: dict) -> list[tuple[str, list[str]]]:
    """Yield (tree_key, extensions) from a leaf's `data` block."""
    if not data:
        return []
    out: list[tuple[str, list[str]]] = []
    docs = data.get("documents")
    if docs is not None:
        exts = docs if isinstance(docs, list) else [docs]
        out.append(("data.documents", exts))
    media = data.get("media") or {}
    if not isinstance(media, dict):
        return out
    for branch in ("loci", "renders"):
        exts = media.get(branch)
        if exts is not None:
            out.append((f"data.media.{branch}", exts if isinstance(exts, list) else [exts]))
    return out


def sibling_ids(tree_dir: Path) -> set[str]:
    ids = {p.stem for p in tree_dir.glob("*.yaml") if p.name != "props.yaml"}
    ids |= {p.name for p in tree_dir.iterdir() if p.is_dir()}
    return ids


def check_edges(where: Path, node: dict, siblings: set[str], composite: bool):
    e = node.get("edges") or {}
    if composite:
        for child in e.get("g") or []:
            if child not in siblings:
                err(where, f"edges.g child '{child}' not found")
    l = e.get("l") or {}
    for side in ("prev", "next"):
        t = l.get(side)
        if t is not None and t not in siblings:
            err(where, f"edges.l.{side} '{t}' not found among siblings")
    for t in e.get("r") or []:
        if t not in siblings:
            err(where, f"edges.r '{t}' not found among siblings")


def check_data(leaf: Path, node: dict, rel: Path, data_cfg: dict):
    data = node.get("data")
    if not data:
        err(leaf, "no data block")
        return
    node_id = leaf.stem
    entries = iter_data_entries(data)
    if not entries:
        err(leaf, "data block is empty")
        return
    for tree_key, exts in entries:
        spec = tree_spec(data_cfg, tree_key)
        if spec is None:
            err(leaf, f"tree '{tree_key}' not configured in k-graph.toml")
            continue
        local = (spec.get("local_origin") or "").strip()
        if not local:
            continue
        for ext in exts:
            target = ROOT / local / rel / f"{node_id}.{ext}"
            if target.exists():
                continue
            if tree_key in TRUST_LOCAL_OPTIONAL:
                continue  # renders are gitignored; declaration is enough
            err(leaf, f"data.{tree_key} [{ext}] -> missing {target.relative_to(ROOT)}")


def main():
    if not TREE.exists():
        sys.exit(f"k-graph dir not found: {TREE}")
    data_cfg = load_data_cfg()

    n_leaves = n_composites = 0
    for dir_path in [TREE, *[p for p in TREE.rglob("*") if p.is_dir()]]:
        rel = dir_path.relative_to(TREE)
        siblings = sibling_ids(dir_path)

        props = dir_path / "props.yaml"
        if props.exists():
            n_composites += 1
            node = yaml.safe_load(props.read_text()) or {}
            if node.get("kind") not in ("T", "L"):
                err(props, f"composite kind must be T/L, got {node.get('kind')}")
            check_edges(props, node, siblings, composite=True)

        for leaf in sorted(dir_path.glob("*.yaml")):
            if leaf.name == "props.yaml":
                continue
            n_leaves += 1
            node = yaml.safe_load(leaf.read_text()) or {}
            if node.get("kind") not in ("F", "Fd"):
                err(leaf, f"leaf kind must be F/Fd, got {node.get('kind')}")
            check_edges(leaf, node, siblings, composite=False)
            check_data(leaf, node, rel, data_cfg)

    if problems:
        print(f"FAIL: {len(problems)} problem(s):\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"OK: {n_composites} composites + {n_leaves} leaves valid; edges + content resolve.")


if __name__ == "__main__":
    main()
