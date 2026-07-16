# scripts

Loci animation project. Pinned to loci v1.0.3 (same version as the loci-seed that created this project).

## Setup

Requires [Manim](https://docs.manim.community/) and loci (library + `loci-render` CLI).

```bash
loci-seed scripts --venv --install    # or run these steps manually:
python3 -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -U pip
pip install "loci[voiceover] @ git+ssh://git@github.com/Cohesian/loci.git@v1.0.3"
```

Copy `.env.example` → `.env` if you use paid TTS (OpenAI, Azure, …).

## Render

`loci-render` reads `loci.toml` and invokes manim. Plain `manim` also works.

```bash
make preview
loci-render scenes/lesson_01.py Lesson01 -vq l -p
loci-render scenes/lesson_01.py Lesson01 -vq l -as gtts -p   # narrated
manim -pql scenes/lesson_01.py Lesson01
```

Defaults live in `loci.toml`. See [loci docs](https://github.com/Cohesian/loci/tree/main/docs).
