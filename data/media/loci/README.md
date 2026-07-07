# loci — k-graph render project

Pure-python [loci](https://github.com/Cohesian/library) + [Manim](https://www.manim.community/)
scene scripts that animate k-graph leaf nodes. This tree holds **only the
scripts**; rendered videos land in the sibling **`data/media/renders/`** tree.

Three content trees mirror the same k-graph path:

```
k-graph/…/F-01-carbon-binder.yaml              ← node (metadata)
data/documents/…/F-01-carbon-binder.md         ← readable content
data/media/loci/…/F-01-carbon-binder.py        ← scene source   (committed)
data/media/renders/…/F-01-carbon-binder.mp4    ← render output  (gitignored)
```

The **`.py` is the source of truth**: tiny, diff-able, lazily runnable. The
**`.mp4` is a build artifact** — regenerated on demand and served from the
remote renders origin (`k-graph.toml` → `data.media.renders.remote_origin`).
Only the paths we actually animate are mirrored.

## Setup

Managed with [uv](https://docs.astral.sh/uv/). Needs a LaTeX install for
`MathTex`; Manim's encoder rides on PyAV, so **no system ffmpeg needed**. Python
3.12 (pinned in `.python-version`) is provisioned by uv automatically.

Dependencies are declared in `pyproject.toml`. The private `loci` library is
pulled straight from git over SSH (no PyPI/registry) — this needs (1) your SSH
key to have read access to `Cohesian/library`, and (2) the pinned tag (`v0.1.0`)
to exist on that repo. The tag marks a whole-repo commit; `subdirectory = "loci"`
in `pyproject.toml` selects the package folder. To cut it:

```bash
git -C ../../../../library tag v0.1.0 && git -C ../../../../library push origin v0.1.0
```

Then, from this folder:

```bash
cd data/media/loci
uv sync          # creates .venv, resolves deps, writes uv.lock (commit it)
```

To develop `loci` itself, point the source at a local editable checkout (see the
commented line in `pyproject.toml`) and re-run `uv sync`.

## Render

Output paths live in **`render.toml`** at this project root — edit `dst_root`
when the output tree moves or is renamed. Paths are relative to
`data/media/loci/` unless absolute.

**Priority:** `--src-root` / `--dst-root` (CLI) → `render.toml` → built-in default.

```toml
# render.toml
src_root = "."              # scene scripts tree root
dst_root = "../renders"     # output tree root (rename freely, e.g. "../videos")
```

Then just:

```bash
uv run render.py T-computer-science/L-composite/F-01-carbon-binder.py
```

One-off override:

```bash
uv run render.py scene.py --dst-root ../videos
```

Before manim runs, the script prints src + dst:

```
  config:   render.toml
  src_root: …/data/media/loci
  src:      …/F-01-carbon-binder.py
  dst_root: …/data/media/renders
  dst:      …/F-01-carbon-binder.mp4
```

Manim scratch goes to `./.build/` (gitignored); only the final mp4 is copied to `dst_root`.

## Convention

- One scene file per animated leaf, named exactly like the node id.
- One `Scene` class per file (the render target).
- Shared palette / caption helpers live in `loci_theme.py`.
- Prefer loci systems (graph / plane / stage) first; drop to raw Manim when
  loci has no primitive.
