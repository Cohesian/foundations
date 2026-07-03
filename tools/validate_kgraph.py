#!/usr/bin/env python3
"""Validate the k-graph: k-graph/ (structure) + content resolved via k-graph.toml.

Layout:
- k-graph/ yaml-only. Every node carries `edges` with three axes:
             g = grouping (ordered children; composites),
             l = linear   (prev / next reading chain),
             r = related  (cross-links).
           Leaves also carry a `formats` list.
- content  resolved per format by k-graph.toml:
             local  -> <base>/<relative path>/<id>.<ext>  (checked on disk)
             remote -> <base>/<relative path>/<id>.<ext>  (trusted; e.g. bucket)

Checks per node:
- composite edges.g children exist (subdir or <id>.yaml);
- leaf edges.l prev/next and edges.r targets exist among siblings;
- leaf `formats` are configured in k-graph.toml, and local formats have their file present.

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

problems: list[str] = []


def err(where: Path, msg: str):
    problems.append(f"{where.relative_to(ROOT)}: {msg}")


def load_formats() -> dict:
    if not CONFIG.exists():
        sys.exit(f"config not found: {CONFIG}")
    with CONFIG.open("rb") as fh:
        cfg = tomllib.load(fh)
    return cfg.get("formats", {})


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


def check_formats(leaf: Path, node: dict, rel: Path, fmt_cfg: dict):
    formats = node.get("formats") or []
    if not formats:
        err(leaf, "no formats listed")
    node_id = leaf.stem
    for fmt in formats:
        spec = fmt_cfg.get(fmt)
        if spec is None:
            err(leaf, f"format '{fmt}' not configured in k-graph.toml")
            continue
        if spec.get("origin") == "local":
            target = ROOT / spec.get("base", "") / rel / f"{node_id}.{fmt}"
            if not target.exists():
                err(leaf, f"format '{fmt}' -> missing {target.relative_to(ROOT)}")
        # remote formats are trusted (resolved at read time against the base URL)


def main():
    if not TREE.exists():
        sys.exit(f"k-graph dir not found: {TREE}")
    fmt_cfg = load_formats()

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
            check_formats(leaf, node, rel, fmt_cfg)

    if problems:
        print(f"FAIL: {len(problems)} problem(s):\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"OK: {n_composites} composites + {n_leaves} leaves valid; edges + content resolve.")


if __name__ == "__main__":
    main()
