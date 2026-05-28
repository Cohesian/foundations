# Corpus layout

How the **foundations** repository organizes explorations on disk.

The corpus uses **TLF** — **Topic / Lecture / File** — a labeled composite pattern for knowledge. The formal (filesystem-agnostic) model is in [F-04-TLF-composite.md](../T-knowledge/T-computer-science/L-composite/F-04-TLF-composite.md). **This document** is the **disk realization** for **foundations**: `T-knowledge/` root, `props.yaml`, frontmatter, and **TLF+** edge constraints. Rollout plan: [PLAN-tlf-extensions.md](PLAN-tlf-extensions.md).

---

## Corpus root

All exploration content lives under **`T-knowledge/`** — a top-level topic that acts as the TLF root ρ.

Repo metadata (`README.md`, `docs/`, `LICENSE`, …) stays **outside** the corpus tree.

```text
foundations/
  README.md
  docs/
  T-knowledge/                  ← TLF root ρ
    props.yaml
    T-math/
      props.yaml
      L-exponential-phase/
        props.yaml
        F-01-branching-depth-resolution.md
        …
    T-computer-science/
      …
```

[README.md](../README.md) at the repository root is the public entry point. There is no `INDEX.md` layer — navigation follows the TLF tree plus `props.yaml` ordering.

---

## Node kinds

| Kind | Role | On disk |
|------|------|---------|
| `T` | Topic (composite) | Directory `T-<slug>/` |
| `L` | Lecture (composite) | Directory `L-<slug>/` |
| `F` | File (leaf, production) | File `F-<slug>.<ext>` |
| `Fd` | File (leaf, draft) | File `Fd-<slug>.<ext>` |

- **Composites** (`T`, `L`) may nest any mixture of `T`, `L`, `F`, and `Fd`. There is no required chain `T → L → F`.
- **Leaves** (`F`, `Fd`) carry readable content and do not contain other corpus nodes.
- The **filesystem path** defines grouping ($E_g$); **props** declare preferred child order and traversal overlays.

---

## Node props (all nodes)

Every node uses the same semantic shape — stored in **`props.yaml`** (composites) or YAML **frontmatter** (leaves):

```yaml
title: string
description: string
kind: T | L | F | Fd
edges:
  g: []    # grouping — ordered direct children (composites only)
  l:       # linear — $E_l$ as prev / next (same-type targets only)
    prev: null
    next: null
  r: []    # related — same-type targets only
```

| Node | Storage |
|------|---------|
| Composite `T`, `L` | `props.yaml` at the directory root |
| Leaf `F`, `Fd` | YAML frontmatter at the top of the file (`.md`; notebooks later) |

### `edges.g` (grouping order)

Lists **direct children** in the order you want them shown or read — basenames only (e.g. `L-functions`, `F-01-function.md`).

- Does **not** move files on disk; it overrides naive alphanumeric sort.
- A generator command can seed `edges.g` from directory listings; you reorder by hand for pedagogy.

### `edges.l` and `edges.r` (TLF+)

F-04 defines linear and related edges on **files only**. TLF+ adds **same-kind** `l` / `r` for composites.

**Linear (`l`)** is always a **pair** — not a list:

```yaml
l:
  next: …   # forward neighbor along $E_l$; null if none
  prev: …   # backward neighbor; null if none
```

| Kind | `edges.g` | `l.next` / `l.prev` targets | `edges.r` |
|------|-----------|-----------------------------|-----------|
| **T** | ✓ | other **T** nodes (paths from `T-knowledge/`) | other **T** |
| **L** | ✓ | other **L** nodes | other **L** |
| **F** / **Fd** | ✗ | sibling **F** / **Fd** basenames in the same lecture | **F** / **Fd** |

**v1 constraint:** no cross-kind links (e.g. no `T → L` or `T → F` in `l` / `r` yet).

On **files**, `next` / `prev` are usually basenames in the same directory (e.g. `F-02-execution.md`). Use `null` when there is no neighbor. Draft leaves (`Fd`) participate in the same chains as `F`.

Changing props or frontmatter does **not** change filesystem grouping (F-04 stability law).

---

## Example: composite props

`T-knowledge/T-computer-science/props.yaml`:

```yaml
title: Computer science
description: Computation, functions, semantics, and mechanics.
kind: T
edges:
  g:
    - L-functions
    - L-composite
    - L-inference
    - L-semantics
    - T-mechanics
  l:
    prev: null
    next: null
  r: []
```

`L-functions` before `L-composite` — pedagogical order, not alphabetical.

---

## Example: leaf frontmatter

```yaml
---
title: Execution
description: Execution as the interface admitting many executable forms.
kind: F
edges:
  g: []
  l:
    prev: F-01-function.md
    next: F-03-function-network.md
  r: []
---
# Execution
…
```

Numeric `F-01-` prefixes remain optional; `edges.l.next` / `edges.l.prev` define reading sequence without renaming files.

---

## TLF vs TLF+

| | F-04 (core) | TLF+ (this repo) |
|---|-------------|------------------|
| Shape | $E_g$ from directory paths | same |
| Child order | implicit (filesystem) | explicit in `edges.g` |
| File `l` / `r` | $V_F \times V_F$ | frontmatter `edges.l` / `edges.r` |
| Composite `l` / `r` | not specified | same-kind T→T, L→L |
| Draft leaves | — | `Fd` kind |
| Corpus root | forest at repo root | **`T-knowledge/`** topic |

---

## Repository metadata (not corpus nodes)

- `README.md` — entry point (renders on GitHub)
- `docs/` — project documentation
- `LICENSE`, `LICENSE-CONTENT`, `NOTICE`, `ATTRIBUTION.md` — legal and attribution

---

## Reading philosophy

Each exploration is a leaf (`F` or `Fd`) and can be read in two ways.

### As a paper

Markdown leaves (`F-*.md`) are meant to be readable without running code — main idea, motivation, definitions, examples, perspectives, invariants, and conclusions.

### As an executable notebook

Notebook leaves (`F-*.ipynb` or `Fd-*.ipynb`) make the idea interactive: code, diagrams, plots, experiments, and visual explanations.

Prefer **`F-*`** for production-ready material. Use **`Fd-*`** for intentional drafts — same leaf role, different maturity.
