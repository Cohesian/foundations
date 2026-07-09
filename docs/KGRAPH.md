# K-graph layout

How the **foundations** repository organizes explorations on disk.

The **k-graph** (knowledge graph) uses **TLF** — **Topic / Lecture / File** — a labeled composite pattern for knowledge. It's not a strict tree or a perfect DAG: the grouping axis (`g`) reads tree-like, but the linear (`l`) and related (`r`) axes add cross-links. The formal (filesystem-agnostic) model is in [F-04-TLF-composite.md](../data/documents/T-computer-science/L-composite/F-04-TLF-composite.md). **This document** is the **disk realization** for **foundations**.

---

## Structure + data trees

The k-graph is split into one **structure** dir and three **content trees** under `data/`:

```text
foundations/
  k-graph/              ← structure: yaml nodes only (the TLF tree)
  data/
    documents/          ← .md and .ipynb
    media/
      loci/             ← .py scene scripts (source of truth, committed)
      videos/           ← .mp4 builds (gitignored); hash maps live in maps/ at repo root
```

All trees share the **same relative path** as the node inside `k-graph/`. A node's content is found by convention:

```
<tree-root>/<same relative path>/<node-id>.<ext>
```

So `k-graph/T-math/L-division/F-01-introduction.yaml` has its document at
`data/documents/T-math/L-division/F-01-introduction.md`, and (once produced) its
render at `data/media/videos/T-math/L-division/F-01-introduction.mp4`.

Content files carry **no frontmatter or metadata** — they are pure content. All metadata lives in `k-graph/`.

---

## Node kinds

| Kind | Role | In `k-graph/` |
|------|------|------------|
| `T` | Topic (composite) | Directory `T-<slug>/` + `props.yaml` |
| `L` | Lecture (composite) | Directory `L-<slug>/` + `props.yaml` |
| `F` | File (leaf, production) | `F-<slug>.yaml` |
| `Fd` | File (leaf, draft) | `Fd-<slug>.yaml` |

- **Composites** (`T`, `L`) may nest any mixture of `T`, `L`, `F`, and `Fd`.
- **Leaves** (`F`, `Fd`) are data-agnostic — id is `F-01-function`, not `F-01-function.md`. The same node can hold documents, a loci scene, and a render.

---

## Node files

Every node carries the three TLF edge axes under `edges`:

- **`g` — grouping:** ordered direct children (composites).
- **`l` — linear:** the reading chain, as a `prev` / `next` pair.
- **`r` — related:** cross-links to other nodes.

All edge targets are **data-agnostic ids** (`F-01-function`, or a directory name). Use `null` / `[]` where empty.

### Leaf — `<id>.yaml`

A leaf adds a `data` block — which trees it holds and which extensions exist in each:

```yaml
title: Execution
description: Execution as the interface admitting many executable forms.
kind: F
data:
  documents:
    - md
edges:
  g: []
  l:
    prev: F-01-function
    next: F-03-function-network
  r: []
```

A leaf with documents, a loci scene, and a video:

```yaml
data:
  media:
    loci:
      - py
    videos:
      - mp4
```

- Each tree lists **extensions** present for that node (`md`, `py`, `mp4`, …).
- Leaf yaml never names a concrete host (YouTube, S3, …) — only abstract data.
- Add a tree when content is produced; routing lives in `k-graph.toml`.

### Composite — `props.yaml`

A composite lists its children under `edges.g`, in the order you want them read:

```yaml
title: Functions
description: Functions as bounded nodes — composition, execution, networks, and wrappers.
kind: L
edges:
  g:
    - F-01-function
    - F-02-execution
    - F-03-function-network
    - F-04-function-natural-wrappers
    - Fd-function-orchestration
  l:
    prev: null
    next: null
  r: []
```

Children are leaf ids or sub-directory names. Order is pedagogical, not alphabetical — `L-functions` may come before `L-composite`.

---

## Resolution config — `k-graph.toml`

`k-graph/` leaves stay origin-agnostic. [`k-graph.toml`](../k-graph.toml) defines
**infrastructure sources** (origin + mapping) and which sources each data tree can reach:

```toml
[infrastructure.local]
mapping = "path"

# [infrastructure.s3bucket]
# origin = "https://media.cohesian.org"
# mapping = "path"
# pattern = "{path}"

[infrastructure.youtube]
origin = "https://www.youtube.com"
mapping = "hash"
pattern = "/watch?v={hash}"
mapper = "maps/youtube.toml"

[data.documents]
sources = ["local"]  # , "s3bucket"

[data.media.loci]
sources = ["local"]

[data.media.videos]
sources = ["local", "youtube"]
serve = "youtube"
```

**Mapping**

| Kind | Resolve | Example |
|------|---------|---------|
| `path` | `origin` + `pattern` with `{path}` | local: repo file |
| `hash` | lookup key in infra `mapper` → `origin` + `pattern` with `{hash}` | YouTube watch URL |

Path segment is always `<tree-root>/<k-graph-key>.<ext>` (tree root derived from tree name).

Hash map (`maps/youtube.toml`, referenced by `[infrastructure.youtube]`):

```toml
["T-computer-science/L-composite/F-01-carbon-binder"]
hash = "dQw4w9WgXcQ"
```

Change `hash` when a video moves — leaf yaml untouched.

```bash
python tools/resolve_kgraph.py media.videos T-computer-science/L-composite/F-01-carbon-binder
python tools/resolve_kgraph.py media.videos T-computer-science/L-composite/F-01-carbon-binder --source local
```

---

## Validation

`tools/validate_kgraph.py` checks the whole k-graph:

- every `edges.g` / `edges.l` / `edges.r` target resolves to a real sibling node;
- path + local source: local files on disk (videos/mp4 optional — gitignored builds);
- hash source: map file contains `hash` (or `ref`) for each key that declares the tree.

```bash
python tools/validate_kgraph.py   # requires pyyaml
```

---

## Repository metadata (not k-graph nodes)

- `README.md` — entry point (renders on GitHub)
- `docs/` — project documentation
- `k-graph.toml` — infrastructure sources + per-tree reachable sources
- `tools/` — validator + `resolve_kgraph.py`
- `LICENSE`, `LICENSE-CONTENT`, `NOTICE`, `ATTRIBUTION.md` — legal and attribution

---

## Reading philosophy

Each exploration is a single leaf node (`F` or `Fd`) that may expose the same idea in several trees, listed in its `data` block.

- **Documents** (`data/documents/`) — `.md` papers readable without running code; `.ipynb` notebooks for interactive work.
- **Loci** (`data/media/loci/`) — `.py` scene scripts: the lazy source of a video.
- **Videos** (`data/media/videos/`) — `.mp4` local builds (path mapping) or infra-projected URLs (hash mapping via `maps/youtube.toml`).

Prefer **`F-*`** for production-ready material; use **`Fd-*`** for intentional drafts. Data is additive: a node starts with whatever exists and gains more over time.
