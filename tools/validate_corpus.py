#!/usr/bin/env python3
"""Validate the 3-dir corpus: tree/ (structure) + papers/ + media/ (content).

Layout:
- tree/    yaml-only. Every node carries `edges` with three axes:
             g = grouping (ordered children; composites),
             l = linear   (prev / next reading chain),
             r = related  (cross-links).
           Leaves also carry a `formats` list.
- papers/  md + ipynb content, mirrored path, named <id>.<ext>.
- media/   mp4 content, mirrored path, named <id>.mp4.

Content locator is implicit: <domain>/<same relative path>/<id>.<ext>.

Checks per node:
- composite edges.g children exist (subdir or <id>.yaml);
- leaf edges.l prev/next and edges.r targets exist among siblings;
- leaf `formats` are known and each content file is present in its domain dir.

Non-zero exit on any problem. Pure stdlib + pyyaml.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ModuleNotFoundError:
    sys.exit("pyyaml is required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
TREE = ROOT / "tree"
DOMAIN = {"md": ROOT / "papers", "ipynb": ROOT / "papers", "mp4": ROOT / "media"}
KNOWN_FMTS = set(DOMAIN)

problems: list[str] = []


def err(where: Path, msg: str):
    problems.append(f"{where.relative_to(ROOT)}: {msg}")


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


def main():
    if not TREE.exists():
        sys.exit(f"tree not found: {TREE}")

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
            node_id = leaf.stem
            if node.get("kind") not in ("F", "Fd"):
                err(leaf, f"leaf kind must be F/Fd, got {node.get('kind')}")
            check_edges(leaf, node, siblings, composite=False)

            formats = node.get("formats") or []
            if not formats:
                err(leaf, "no formats listed")
            for fmt in formats:
                if fmt not in KNOWN_FMTS:
                    err(leaf, f"unknown format '{fmt}'")
                    continue
                content = DOMAIN[fmt] / rel / f"{node_id}.{fmt}"
                if not content.exists():
                    err(leaf, f"format '{fmt}' -> missing {content.relative_to(ROOT)}")

    if problems:
        print(f"FAIL: {len(problems)} problem(s):\n")
        for p in problems:
            print(f"  - {p}")
        sys.exit(1)
    print(f"OK: {n_composites} composites + {n_leaves} leaves valid; edges + content resolve.")


if __name__ == "__main__":
    main()
