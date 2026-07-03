# loci — k-graph render project

Pure-python [loci](https://github.com/Cohesian/library) + [Manim](https://www.manim.community/)
scene scripts that animate k-graph leaf nodes. This directory holds **only the
scripts**; rendered videos land in the sibling **`media/`** domain.

Two content domains mirror the same k-graph tree (just like `papers/`):

```
k-graph/T-computer-science/L-composite/F-01-carbon-binder.yaml   ← node (metadata)
papers/ T-computer-science/L-composite/F-01-carbon-binder.md     ← md content
loci/   T-computer-science/L-composite/F-01-carbon-binder.py     ← scene source   (committed)
media/  T-computer-science/L-composite/F-01-carbon-binder.mp4    ← render output  (gitignored)
```

The **`.py` is the source of truth**: tiny, diff-able, lazily runnable. The
**`.mp4` is a build artifact** — regenerated on demand and served from the media
bucket (`k-graph.toml` declares the `media` format as a `remote` origin). Only
the paths we actually animate are mirrored.

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
git -C ../../library tag v0.1.0 && git -C ../../library push origin v0.1.0
```

Then, from this folder:

```bash
cd loci
uv sync          # creates .venv, resolves deps, writes uv.lock (commit it)
```

To develop `loci` itself, point the source at a local editable checkout (see the
commented line in `pyproject.toml`) and re-run `uv sync`.

## Render

```bash
uv run render.py T-computer-science/L-composite/F-01-carbon-binder.py       # -q h (1080p) default
uv run render.py T-computer-science/L-composite/F-01-carbon-binder.py -q m  # 720p, faster iteration
```

`render.py` renders into `./.build/` (gitignored) and copies the final mp4 to
the sibling `media/` domain at the **same relative path** as the script. If a
file has one `Scene` subclass it is picked automatically; otherwise pass the
class name explicitly.

## Convention

- One scene file per animated leaf, named exactly like the node id.
- One `Scene` class per file (the render target).
- Shared palette / caption helpers live in `loci_theme.py`.
- Prefer loci systems (graph / plane / stage) first; drop to raw Manim when
  loci has no primitive.
