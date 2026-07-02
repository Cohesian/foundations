# Corpus layout

How the **foundations** repository organizes explorations on disk.

The corpus uses **TLF** — **Topic / Lecture / File** — a labeled composite pattern for knowledge. The formal (filesystem-agnostic) model is in [F-04-TLF-composite.md](../papers/T-computer-science/L-composite/F-04-TLF-composite.md). **This document** is the **disk realization** for **foundations**.

---

## Three sibling dirs

The corpus is split into one **structure** dir and one dir per **content domain**:

```text
foundations/
  tree/       ← structure: yaml nodes only (the TLF tree)
  papers/     ← content: .md and .ipynb
  media/      ← content: .mp4
```

All three share the **same relative paths**. A node's content is found by convention:

```
<domain>/<same relative path>/<node-id>.<ext>
```

So `tree/T-math/L-division/F-01-introduction.yaml` has its paper at
`papers/T-math/L-division/F-01-introduction.md`, and (once produced) its video at
`media/T-math/L-division/F-01-introduction.mp4`.

Content files carry **no frontmatter or metadata** — they are pure content. All metadata lives in `tree/`.

---

## Node kinds

| Kind | Role | In `tree/` |
|------|------|------------|
| `T` | Topic (composite) | Directory `T-<slug>/` + `props.yaml` |
| `L` | Lecture (composite) | Directory `L-<slug>/` + `props.yaml` |
| `F` | File (leaf, production) | `F-<slug>.yaml` |
| `Fd` | File (leaf, draft) | `Fd-<slug>.yaml` |

- **Composites** (`T`, `L`) may nest any mixture of `T`, `L`, `F`, and `Fd`.
- **Leaves** (`F`, `Fd`) are format-agnostic — id is `F-01-function`, not `F-01-function.md`. The same node can carry a paper, a notebook, and a video.

---

## Node files

Every node carries the three TLF edge axes under `edges`:

- **`g` — grouping:** ordered direct children (composites).
- **`l` — linear:** the reading chain, as a `prev` / `next` pair.
- **`r` — related:** cross-links to other nodes.

All edge targets are **format-agnostic ids** (`F-01-function`, or a directory name). Use `null` / `[]` where empty.

### Leaf — `<id>.yaml`

A leaf adds a `formats` list (which content extensions exist, in order):

```yaml
title: Execution
description: Execution as the interface admitting many executable forms.
kind: F
formats:
  - md
edges:
  g: []
  l:
    prev: F-01-function
    next: F-03-function-network
  r: []
```

- A format is present **iff** it is listed — consumers never probe `papers/` or `media/` to discover formats.
- Add a format when it is produced (e.g. add `mp4` once a video exists), remove it if it goes away.

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

## Format → domain map

| Format | Lives in |
|--------|----------|
| `md` | `papers/` |
| `ipynb` | `papers/` |
| `mp4` | `media/` |

Notebooks group with papers (written / executable material); videos are the media domain. New domains can be added by extending this map.

---

## Validation

`tools/validate_corpus.py` checks the whole corpus:

- every `edges.g` / `edges.l` / `edges.r` target resolves to a real sibling node;
- every leaf `formats` entry has its content file present in the right domain dir.

```bash
python tools/validate_corpus.py   # requires pyyaml
```

---

## Repository metadata (not corpus nodes)

- `README.md` — entry point (renders on GitHub)
- `docs/` — project documentation
- `tools/` — corpus tooling (validator)
- `LICENSE`, `LICENSE-CONTENT`, `NOTICE`, `ATTRIBUTION.md` — legal and attribution

---

## Reading philosophy

Each exploration is a single leaf node (`F` or `Fd`) that may expose the same idea in several formats, listed in its `formats`.

- **Paper** (`md` in `papers/`) — readable without running code.
- **Notebook** (`ipynb` in `papers/`) — interactive: code, diagrams, plots, experiments.
- **Video** (`mp4` in `media/`) — a relatable, narrated take on the same node.

Prefer **`F-*`** for production-ready material; use **`Fd-*`** for intentional drafts. Formats are additive: a node starts with whatever exists and gains more over time.
