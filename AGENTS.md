# Foundations agent guidance

Read this file before modifying repository structure, corpus content, or tooling.

**foundations** is a Cohesian knowledge corpus: papers, notebooks, and media about how ideas bind, compose, transform, and share structure across math, computation, and visualization.

This file is an orientation guide, not the complete specification. Use the task-specific reading routes below.

## Core inheritance

Foundations follows [Cohesian Core principles v0.1.0](../core/PRINCIPLES.md).
Here, the structural lens guides relations across the knowledge graph without
collapsing distinct fields into one model. [`docs/COHESIAN.md`](docs/COHESIAN.md)
is this repository's local interpretation, not a replacement for Core.

---

## Read first

| Path | What it gives you |
|------|-------------------|
| `README.md` | Repo entry point |
| `docs/README.md` | Doc index |
| `docs/COHESIAN.md` | Lens — cohesion, composition, binding, invariants, perspective |
| `docs/KGRAPH.md` | Disk layout — structure + content trees |
| `docs/EXPLORATIONS.md` | Human index of topics/leaves (no need to read each file on the k-graph and parallel data trees)|

---

## K-graph

This repo organizes knowledge as a **k-graph** — an index tree in **TLF** format (Topic / Lecture / File). Each node carries local metadata; simple rules across nodes compose the full graph. Composites (`T`, `L`) group children; leaves (`F`, `Fd`) point outward to actual content.

Every node has **edges** (`g` grouping, `l` linear, `r` related). Leaves additionally declare a **`data`** block — which content trees and extensions they hold. The index never embeds content bodies.

**Structure tree** — `k-graph/` is yaml only. Corpus shape starts at `k-graph/props.yaml`; follow `edges.g` for reading order.

**Parallel content trees** — same relative path in each:

```
k-graph/              ← structure
data/documents/       ← .md, .ipynb
data/media/scripts/scenes/  ← .py scenes (media.scripts.scenes in leaf yaml)
data/media/videos/    ← .mp4 (gitignored; routed via maps/)
```

```
<tree-root>/<k-graph-path>/<node-id>.<ext>
```

Content files are pure (no frontmatter). All node metadata stays in `k-graph/`. Where content resolves (local path, YouTube hash, etc.): `k-graph.toml`.

| Kind | On disk |
|------|---------|
| `T` topic | `T-<slug>/props.yaml` |
| `L` lecture | `L-<slug>/props.yaml` |
| `F` leaf | `F-<slug>.yaml` |
| `Fd` draft leaf | `Fd-<slug>.yaml` |

Node ids are data-agnostic (`F-01-function`, not `.md`). Full edge semantics and traversal: `docs/KGRAPH.md`.

---

Update this file when repo semantics change. Source of truth: `docs/KGRAPH.md`, `k-graph.toml`.
