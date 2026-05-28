# Plan: TLF+ props, `T-knowledge` root, and edge extensions

Revise the corpus model: one **`T-knowledge/`** tree as the TLF root, unified **node props** everywhere, and a small **TLF+** variant on who may use `l` / `r` edges.

---

## Layout (simple)

```text
foundations/
  README.md
  docs/
  T-knowledge/                  ← TLF root ρ (all corpus content lives here)
    props.yaml                  ← orders / describes top-level topics
    T-math/
      props.yaml
      L-exponential-phase/
        props.yaml
        F-01-branching-depth-resolution.md
        …
    T-computer-science/
      props.yaml
      L-functions/
        …
```

- **`T-knowledge/`** is the **only** corpus root — a top-level topic that holds the whole tree.
- Repo metadata (`README.md`, `docs/`, `LICENSE`, …) stays **outside** `T-knowledge/`.
- Each **composite** (`T-*`, `L-*`) carries **`props.yaml`** at the **root of that directory**.
- Each **leaf** (`F-*`, `Fd-*`) carries the **same fields** in YAML **frontmatter** (`.md`) or notebook metadata (`.ipynb`, later).

**Config filename:** `props.yaml` (alias `cfg.yaml` acceptable; pick one — **`props.yaml`** recommended).

---

## Unified node props (all nodes)

Every node — composite or leaf — uses the same semantic shape:

```yaml
title: string
description: string
kind: T | L | F | Fd
edges:
  g: []    # grouping — ordered children (composites only)
  l:       # linear — $E_l$ as prev / next (same-type only)
    prev: null
    next: null
  r: []    # related — same-type targets only
```

### Where props live

| Node class | Kinds | Storage |
|------------|-------|---------|
| Composite **C** | `T`, `L` | `props.yaml` at directory root |
| Leaf **L** | `F`, `Fd` | YAML frontmatter at top of file |

(`L` as leaf class = leaf node, not lecture — use “composite” vs “leaf” in prose to avoid confusion with lecture `L`.)

---

## Edge rules (TLF core + TLF+ extension)

F-04 defines three edge families on the corpus graph: **g** (grouping), **l** (linear), **r** (related).

**Unchanged from F-04**

- **Shape** = **g** only: directory containment, a rooted tree/forest.
- **g** does not move nodes; it only lists **direct children** in preferred order.

**TLF+ extension (this plan)**

Original F-04 restricts **l** and **r** to **file → file** (`F × F`). We keep that for files, and **add same-kind edges for composites**:

| Kind | `edges.g` | `l.next` / `l.prev` | `edges.r` |
|------|-----------|---------------------|-----------|
| **T** | ordered children | other **T** (path from `T-knowledge/`) | other **T** |
| **L** | ordered children | other **L** | other **L** |
| **F** / **Fd** | *(none)* | sibling **F** / **Fd** basename | **F** / **Fd** |

**Explicit constraints (v1 — intentional simplification)**

- **No cross-kind `l` / `r`** for now (e.g. a topic cannot `l`-link to a lecture or file). Cross-scope references stay future work.
- **g** remains the only edge that defines containment; **l** / **r** are overlays (F-04 stability law still applies).
- **`Fd`** is the same leaf class as **`F`** for edge typing; `kind: Fd` marks draft maturity only.
- **`l`** is always `{ next, prev }`; use `null` when a direction is absent.

**Reference format:** composite `l` / `r` use paths relative to **`T-knowledge/`**. File `l.next` / `l.prev` use sibling basenames in the same lecture.

```yaml
# T-math/props.yaml — related topic (r), no linear chain yet
edges:
  l:
    prev: null
    next: null
  r:
    - T-computer-science
```

```yaml
# L-functions/props.yaml — linear to sibling lecture (example)
edges:
  l:
    prev: null
    next: ../L-composite
  r: []
```

---

## Example files

### `T-knowledge/props.yaml` (corpus root ρ)

```yaml
title: Knowledge
description: Root grouping for all TLF topics in the foundations corpus.
kind: T
edges:
  g:
    - T-math
    - T-computer-science
  l:
    prev: null
    next: null
  r: []
```

### `T-knowledge/T-math/props.yaml`

```yaml
title: Math
description: Mathematical explorations.
kind: T
edges:
  g:
    - L-division
    - L-exponential-phase
    - T-linear-algebra
  l:
    prev: null
    next: null
  r: []
```

### `T-knowledge/T-computer-science/L-functions/F-01-function.md`

```yaml
---
title: Functions
description: One lens on functions as bounded executable nodes.
kind: F
edges:
  g: []
  l:
    prev: null
    next: F-02-execution.md
  r: []
---
# Functions
…
```

Linear chains on files: set **`l.next`** and **`l.prev`** from the lecture’s `edges.g` order (including `Fd` leaves).

---

## Scaffolding workflow

Problem: manually maintaining `edges.g` lists is tedious.

**Step 1 — generator command** (future script, e.g. `python -m corpus.props` or `make props`):

1. Walk `T-knowledge/` composites.
2. For each composite dir, list **direct children** (dirs matching `T-*` / `L-*`, files matching `F-*` / `Fd-*`; skip `props.yaml`).
3. Emit or merge `props.yaml` with:
   - existing `title`, `description`, `kind`, `edges.l`, `edges.r` preserved
   - `edges.g` refreshed as **alphabetical** sibling list (or append-only new entries)

**Step 2 — human pass:** reorder `edges.g` (and fill `l` / `r`) by hand for pedagogy.

This keeps the system simple: **filesystem = shape**, **props = order + overlays**.

---

## Relation to F-04

| Topic | F-04 | TLF+ (this plan) |
|-------|------|------------------|
| Shape | $E_g$ from paths | same; `edges.g` mirrors / overrides display order |
| File linear | $E_l \subseteq V_F \times V_F$ | same; declared in frontmatter `edges.l` |
| File related | $E_r \subseteq V_F \times V_F$ | same; frontmatter `edges.r` |
| Composite linear/related | not in F-04 | **new:** $E_l, E_r$ on $V_T$ and $V_L$ (same-kind only) |
| Draft leaves | not in F-04 | `Fd` kind |
| Node metadata | not specified | unified `title`, `description`, `kind`, `edges` |
| Corpus root | repo root or forest | **`T-knowledge/`** is ρ |

Document TLF+ in [CORPUS.md](CORPUS.md) only — F-04 stays the core, filesystem-agnostic TLF paper.

---

## Implementation phases (one commit each)

### Commit 1 — `docs: revise TLF+ plan (T-knowledge root, props.yaml, edges)`

- Replace this file with the agreed model (done in working tree).
- Update [CORPUS.md](CORPUS.md): `T-knowledge/` root, `props.yaml`, frontmatter schema, edge matrix, TLF+ vs F-04.
- Update [docs/README.md](README.md) link to plan.

**No corpus moves yet.**

---

### Commit 2 — *(skipped)* F-04 stays core TLF only

[F-04-TLF-composite.md](../T-knowledge/T-computer-science/L-composite/F-04-TLF-composite.md) remains the **filesystem-agnostic** TLF spec ($E_l$, $E_r$ on files only). **TLF+** constraints and disk conventions live in [CORPUS.md](CORPUS.md) only — do not extend F-04.

---

### Commit 3 — `refactor(corpus): move TLF tree under T-knowledge/`

- `git mv T-math T-computer-science → T-knowledge/`
- Fix links in `docs/`, root `README.md`, `docs/EXPLORATIONS.md`, cross-paper links if any break.

---

### Commit 4 — `feat(corpus): add props.yaml to composites`

- Add `T-knowledge/props.yaml` (top-level topic order).
- Run scaffold (manual first pass OK): one `props.yaml` per composite with `edges.g` listing siblings.
- Hand-tune orders (e.g. `L-functions` before `L-composite` under `T-computer-science`).

---

### Commit 5 — `feat(corpus): add frontmatter props to markdown leaves`

- Same schema: `title`, `description`, `kind`, `edges`.
- Batch by lecture; wire `edges.l` / `edges.r` where reading order exists today (`F-01` chains).

---

### Commit 6 — `docs: update paths and props conventions in EXPLORATIONS`

- All corpus links prefixed with `T-knowledge/`.
- Note: navigation order = `props.yaml` `edges.g`, not locale sort.

---

### Commit 7 (optional) — `feat(tools): scaffold props.yaml from directory listing`

- Small script + README snippet in CORPUS or CONTRIBUTING.

---

## Verification checklist

- [ ] All corpus content under `T-knowledge/` only
- [ ] Every composite has `props.yaml`; every `edges.g` ⊇ actual children (modulo generator rules)
- [ ] No `l`/`r` entry crosses kind constraints (T→T, L→L, F→F/Fd only)
- [ ] Frontmatter validates; Markdown renders on GitHub
- [ ] `docs/` and root README links use `T-knowledge/…`

---

## Decisions locked in

| Question | Answer |
|----------|--------|
| Corpus root | **`T-knowledge/`** at repo root (TLF topic, not a generic folder name) |
| Composite config | `props.yaml` at composite dir root |
| Leaf config | frontmatter, same schema |
| Cross-kind links | **not in v1** |
| File `l`/`r` | **F / Fd only** (F-04) |
| Composite `l`/`r` | **T→T, L→L only** (TLF+ extension) |
| `F-01-` prefixes | keep for now; optional strip once `edges.l` is populated |

---

## After v1

- Validator: props ↔ filesystem consistency
- Sidebar / site generator reads `props.yaml` + frontmatter
- Relax cross-kind `r` (e.g. T → specific L) when needed
