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
      renders/          ← .mp4 outputs (build artifacts, gitignored / remote)
```

All trees share the **same relative path** as the node inside `k-graph/`. A node's content is found by convention:

```
<tree-root>/<same relative path>/<node-id>.<ext>
```

So `k-graph/T-math/L-division/F-01-introduction.yaml` has its document at
`data/documents/T-math/L-division/F-01-introduction.md`, and (once produced) its
render at `data/media/renders/T-math/L-division/F-01-introduction.mp4`.

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

A leaf with documents, a loci scene, and a render:

```yaml
data:
  media:
    loci:
      - py
    renders:
      - mp4
  documents:
    - md
```

- Each tree (`documents`, `media.loci`, `media.renders`) lists the **extensions** present for that node — there can be more than one per tree (e.g. `documents: [md, ipynb]`).
- Data is present **iff** it is listed — consumers never probe `data/` to discover what exists.
- Add a tree when content is produced (e.g. add `media.loci` + `media.renders` once a scene and its video exist), remove it if it goes away.

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

`k-graph/` nodes stay origin-agnostic (a leaf only declares *what* data it holds).
Where each tree resolves is defined once in [`k-graph.toml`](../k-graph.toml):

```toml
[data.media.loci]
local_origin = "data/media/loci"
remote_origin = ""

[data.media.renders]
local_origin = "data/media/renders"
remote_origin = "https://media.cohesian.org"

[data.documents]
local_origin = "data/documents"
remote_origin = ""
```

A node's content is located as `<origin>/<relative path>/<id>.<ext>`:

| Tree | Local origin | Remote origin | Example ext |
|------|--------------|---------------|-------------|
| `data.documents` | `data/documents/` | — | `md`, `ipynb` |
| `data.media.loci` | `data/media/loci/` | — | `py` |
| `data.media.renders` | `data/media/renders/` | `https://media.cohesian.org` | `mp4` |

- **Local** origins are checked on disk by the validator (except renders — mp4s are gitignored build artifacts).
- **Remote** origins are trusted at read time (declaring `media.renders` is enough; the binary lives on the CDN).
- Add a new extension under the appropriate tree in the leaf's `data` block; add a new tree by adding a `[data.<path>]` block in `k-graph.toml`.

---

## Validation

`tools/validate_kgraph.py` checks the whole k-graph:

- every `edges.g` / `edges.l` / `edges.r` target resolves to a real sibling node;
- every leaf `data` entry has its content file present under the tree's `local_origin` (renders optional).

```bash
python tools/validate_kgraph.py   # requires pyyaml
```

---

## Repository metadata (not k-graph nodes)

- `README.md` — entry point (renders on GitHub)
- `docs/` — project documentation
- `k-graph.toml` — data tree resolution config (local / remote origins)
- `tools/` — k-graph tooling (validator)
- `LICENSE`, `LICENSE-CONTENT`, `NOTICE`, `ATTRIBUTION.md` — legal and attribution

---

## Reading philosophy

Each exploration is a single leaf node (`F` or `Fd`) that may expose the same idea in several trees, listed in its `data` block.

- **Documents** (`data/documents/`) — `.md` papers readable without running code; `.ipynb` notebooks for interactive work.
- **Loci** (`data/media/loci/`) — `.py` scene scripts: the lazy source of a video.
- **Renders** (`data/media/renders/`) — `.mp4` narrated takes, built from the loci scene (same k-graph path, different tree root).

Prefer **`F-*`** for production-ready material; use **`Fd-*`** for intentional drafts. Data is additive: a node starts with whatever exists and gains more over time.
