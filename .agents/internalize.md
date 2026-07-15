# Internalize: foundations

Semantic seed for this repo — a compact map before or after reading the docs.

**foundations** is a Cohesian knowledge corpus: papers, notebooks, and media about how ideas bind, compose, transform, and share structure across math, computation, and visualization.

---

## Read first

| Path | What it gives you |
|------|-------------------|
| `docs/README.md` | Doc index |
| `docs/COHESIAN.md` | Lens — cohesion, composition, binding, invariants, perspective |
| `docs/KGRAPH.md` | Disk layout — structure + content trees |
| `docs/PRINCIPLES.md` | How explorations are written |
| `docs/EXPLORATIONS.md` | Human index of topics/leaves |
| `README.md` | Repo entry point |

Formal TLF model: `data/documents/T-computer-science/L-composite/F-04-TLF-composite.md`.

---

## K-graph

This repo organizes knowledge as a **k-graph** — an index tree in **TLF** format (Topic / Lecture / File). Each node carries local metadata; simple rules across nodes compose the full graph. Composites (`T`, `L`) group children; leaves (`F`, `Fd`) point outward to actual content.

Every node has **edges** (`g` grouping, `l` linear, `r` related). Leaves additionally declare a **`data`** block — which content trees and extensions they hold. The index never embeds content bodies.

**Structure tree** — `k-graph/` is yaml only. Corpus shape starts at `k-graph/props.yaml`; follow `edges.g` for reading order.

**Parallel content trees** — same relative path in each:

```
k-graph/              ← structure
data/documents/       ← .md, .ipynb
data/media/scripts/   ← .py scenes
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
