# K-graph layout

How the **foundations** repository organizes explorations on disk.

The **k-graph** (knowledge graph) uses **TLF** — **Topic / Lecture / File** — a labeled composite pattern for knowledge. It's not a strict tree or a perfect DAG: the grouping axis (`g`) reads tree-like, but the linear (`l`) and related (`r`) axes add cross-links. The formal (filesystem-agnostic) model is in [F-04-TLF-composite.md](../papers/T-computer-science/L-composite/F-04-TLF-composite.md). **This document** is the **disk realization** for **foundations**.

---

## Three sibling dirs

The k-graph is split into one **structure** dir and one dir per **content domain**:

```text
foundations/
  k-graph/    ← structure: yaml nodes only (the TLF tree)
  papers/     ← content: .md and .ipynb
  loci/       ← content: .py (loci/manim scene scripts)
  media/      ← content: .mp4 (rendered from loci/)
```

All three share the **same relative paths**. A node's content is found by convention:

```
<domain>/<same relative path>/<node-id>.<ext>
```

So `k-graph/T-math/L-division/F-01-introduction.yaml` has its paper at
`papers/T-math/L-division/F-01-introduction.md`, and (once produced) its video at
`media/T-math/L-division/F-01-introduction.mp4`.

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
- **Leaves** (`F`, `Fd`) are format-agnostic — id is `F-01-function`, not `F-01-function.md`. The same node can carry a paper, a notebook, a scene, and a video.

---

## Node files

Every node carries the three TLF edge axes under `edges`:

- **`g` — grouping:** ordered direct children (composites).
- **`l` — linear:** the reading chain, as a `prev` / `next` pair.
- **`r` — related:** cross-links to other nodes.

All edge targets are **format-agnostic ids** (`F-01-function`, or a directory name). Use `null` / `[]` where empty.

### Leaf — `<id>.yaml`

A leaf adds a `formats` list (which content domains it has, in order):

```yaml
title: Execution
description: Execution as the interface admitting many executable forms.
kind: F
formats:
  - papers
edges:
  g: []
  l:
    prev: F-01-function
    next: F-03-function-network
  r: []
```

- Formats are named after the **content domain** that holds them (`papers`, `loci`, `media`) — not the bare extension — so the list reads as "there is something in that space".
- A format is present **iff** it is listed — consumers never probe `papers/`, `loci/`, or `media/` to discover formats.
- Add a format when it is produced (e.g. add `loci` + `media` once a scene and its video exist), remove it if it goes away.

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

`k-graph/` nodes stay origin-agnostic (a leaf only declares *which* formats it has).
Where each format resolves is defined once in [`k-graph.toml`](../k-graph.toml):

```toml
[formats.papers]
origin = "local"    # resolved against the repo root
base = "papers"
ext = "md"

[formats.ipynb]
origin = "local"
base = "papers"
ext = "ipynb"

[formats.loci]
origin = "local"    # pure-python scene scripts (committed)
base = "loci"
ext = "py"

[formats.media]
origin = "remote"   # bucket / CDN; not stored in git
base = "https://media.cohesian.org"
ext = "mp4"
```

A node's content is located as `<base>/<relative path>/<id>.<ext>`, where each format
declares both its `base` domain dir and its file `ext`:

| Format | Origin | Ext | Example for `T-computer-science/L-functions/F-01-function` |
|--------|--------|-----|-----------------------------------------------------------|
| `papers` | local | `md` | `papers/T-computer-science/L-functions/F-01-function.md` |
| `ipynb` | local | `ipynb` | `papers/T-computer-science/L-functions/F-01-function.ipynb` |
| `loci` | local | `py` | `loci/T-computer-science/L-functions/F-01-function.py` |
| `media` | remote | `mp4` | `https://media.cohesian.org/T-computer-science/L-functions/F-01-function.mp4` |

- **Local** origins are checked on disk by the validator.
- **Remote** origins are trusted (declaring the format is enough; the binary lives in the bucket and is gitignored).
- Add a new format (e.g. `pdf`, `slides`) by adding a `[formats.<name>]` block with its `base` + `ext` — no tree changes needed.

---

## Validation

`tools/validate_kgraph.py` checks the whole k-graph:

- every `edges.g` / `edges.l` / `edges.r` target resolves to a real sibling node;
- every leaf `formats` entry has its content file present in the right domain dir.

```bash
python tools/validate_kgraph.py   # requires pyyaml
```

---

## Repository metadata (not k-graph nodes)

- `README.md` — entry point (renders on GitHub)
- `docs/` — project documentation
- `k-graph.toml` — format resolution config (origins / bases)
- `tools/` — k-graph tooling (validator)
- `LICENSE`, `LICENSE-CONTENT`, `NOTICE`, `ATTRIBUTION.md` — legal and attribution

---

## Reading philosophy

Each exploration is a single leaf node (`F` or `Fd`) that may expose the same idea in several formats, listed in its `formats`.

- **Paper** (`papers`, `.md`) — readable without running code.
- **Notebook** (`ipynb`, `.ipynb` in `papers/`) — interactive: code, diagrams, plots, experiments.
- **Scene** (`loci`, `.py` in `loci/`) — the lazy source of a video: a tiny, versioned loci/manim script.
- **Video** (`media`, `.mp4`) — a relatable, narrated take, rendered from the loci scene.

Prefer **`F-*`** for production-ready material; use **`Fd-*`** for intentional drafts. Formats are additive: a node starts with whatever exists and gains more over time.
