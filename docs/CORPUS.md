# Corpus layout

How the **foundations** repository organizes explorations on disk.

The corpus uses **TLF** — **Topic / Lecture / File** — a labeled composite pattern for knowledge. The formal model (grouping vs linear vs related edges, projections, and laws) is in [F-04-TLF-composite.md](../T-computer-science/L-composite/F-04-TLF-composite.md).

---

## Node kinds

- **Topics (`T`)** and **lectures (`L`)** are **composites** (directories). Either may contain topics, lectures, or files in any mixture. There is no required chain `T → L → F`; grouping is a tree (or forest) of containment.
- **Files (`F`)** are **leaves** (readable content): papers, notes, and production notebooks.
- **Draft files (`Fd`)** are the same role as `F`, marked as work in progress — useful when material should stay in the repo but is not ready for production reading.

The filesystem path is the structural index: directories define grouping; filenames declare node kind.

[README.md](../README.md) at the repository root is the public entry point. Exploration content lives under `T-*` topics. There is no separate `INDEX.md` layer — navigation follows the TLF tree.

---

## Typical layout

    foundations/
      README.md
      docs/
        CORPUS.md
        …

      T-math/
        L-exponential-phase/
          F-01-branching-depth-resolution.md
          F-02-discrete-phase-rulers.md
          F-03-hidden-generators.md
          Fd-exponential-phase-visual-notebook.ipynb
        T-linear-algebra/
          T-vectors/
            L-basis/
              F-01-introduction.md

      T-computer-science/
        L-functions/
          F-01-function.md
          Fd-function-orchestration.md
        L-composite/
          F-04-TLF-composite.md
        T-mechanics/
          L-sparse-ticker-state/
            F-sparse_ticker_state_ledger.md
            Fd-sparse_ticker_state_ledger.ipynb

---

## Naming conventions

Explorations follow **TLF prefixes** on disk. The prefix encodes node kind; the slug after it describes the content (usually kebab-case; some legacy slugs use underscores).

| Kind | Role | On disk | Example |
|------|------|---------|---------|
| `T` | Topic (composite) | Directory `T-<slug>/` | `T-math/`, `T-linear-algebra/` |
| `L` | Lecture (composite) | Directory `L-<slug>/` | `L-exponential-phase/`, `L-functions/` |
| `F` | File (leaf, production) | File `F-<slug>.<ext>` | `F-01-function.md`, `F-sparse_ticker_state_ledger.md` |
| `Fd` | File (leaf, draft) | File `Fd-<slug>.<ext>` | `Fd-function-orchestration.md`, `Fd-sparse_ticker_state_ledger.ipynb` |

**Composites** (`T`, `L`) may nest any combination of `T`, `L`, and `F` / `Fd` children. **Leaves** (`F`, `Fd`) do not contain other corpus nodes.

Within a lecture, ordered papers often use a numeric segment after `F-` (for example `F-01-…`, `F-02-…`) to suggest a default reading sequence. That order is a traversal hint on leaves; it does not change the grouping tree.

**Repository metadata** (not TLF corpus nodes) keeps conventional names:

- `README.md` — entry point at the repository root (renders on GitHub)
- `docs/` — internal project documentation ([COHESIAN](COHESIAN.md), [CORPUS](CORPUS.md), [EXPLORATIONS](EXPLORATIONS.md), [PRINCIPLES](PRINCIPLES.md), [CONTRIBUTING](CONTRIBUTING.md))
- `LICENSE`, `LICENSE-CONTENT`, `NOTICE`, `ATTRIBUTION.md` — legal and attribution

---

## Reading philosophy

Each exploration is a leaf (`F` or `Fd`) and can be read in two ways.

### As a paper

Markdown leaves (`F-*.md`) are meant to be readable without running code.

They should explain the main idea, motivation, definitions, examples, perspectives, invariants, and conclusions.

### As an executable notebook

Notebook leaves (`F-*.ipynb` or `Fd-*.ipynb`) make the idea interactive.

They may include code, diagrams, plots, experiments, examples, counterexamples, simulations, or visual explanations.

The notebook is not only an implementation detail.

It is part of the thinking process.

Prefer **`F-*`** for material you treat as production-ready. Use **`Fd-*`** when the artifact is intentionally draft — same leaf role, different maturity.
