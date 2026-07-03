#!/usr/bin/env python3
"""Render a loci/manim scene and drop the mp4 at its mirrored k-graph path.

Two sibling content domains mirror the same k-graph tree:

    loci/   ← pure-python scene scripts   (source of truth, committed)
    media/  ← rendered mp4 outputs        (build artifacts, gitignored)

So a scene authored at

    loci/T-computer-science/L-composite/F-01-carbon-binder.py

renders to

    media/T-computer-science/L-composite/F-01-carbon-binder.mp4

The script is the lazy, tiny source of truth; the mp4 is a build artifact
(regenerated on demand, or pushed to the media bucket).

Usage
-----
    python render.py T-computer-science/L-composite/F-01-carbon-binder.py
    python render.py <script.py> [SceneClass] [-q l|m|h|k]

If no SceneClass is given, the first `class X(...Scene)` found in the file is
rendered. Quality defaults to high (-q h); use -q m or -q l while iterating.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent          # the loci/ scripts project
BUILD = HERE / ".build"                          # manim scratch tree (gitignored)
MEDIA = HERE.parent / "media"                     # sibling mp4 domain (mirrors paths)

_SCENE_RE = re.compile(r"^\s*class\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*:", re.MULTILINE)


def find_scene(script: Path) -> str:
    """Return the first class whose bases mention a *Scene."""
    source = script.read_text(encoding="utf-8")
    for name, bases in _SCENE_RE.findall(source):
        if "Scene" in bases:
            return name
    raise SystemExit(f"No Scene subclass found in {script}")


def newest_mp4(stem: str) -> Path | None:
    candidates = sorted(
        BUILD.glob(f"videos/**/{stem}.mp4"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    return candidates[0] if candidates else None


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("script", help="scene .py, relative to loci/ or absolute")
    parser.add_argument("scene", nargs="?", help="Scene class (default: first found)")
    parser.add_argument(
        "-q", "--quality", default="h", choices=["l", "m", "h", "p", "k"],
        help="manim quality: l=480p m=720p h=1080p p=1440p k=4k (default h)",
    )
    args = parser.parse_args()

    script = Path(args.script)
    if not script.is_absolute():
        script = (HERE / script).resolve()
    if not script.exists():
        raise SystemExit(f"Scene file not found: {script}")

    scene = args.scene or find_scene(script)
    stem = script.stem

    cmd = [
        sys.executable, "-m", "manim", "render",
        f"-q{args.quality}",
        "--media_dir", str(BUILD),
        "-o", stem,
        str(script),
        scene,
    ]
    print("»", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(HERE))
    if result.returncode != 0:
        return result.returncode

    produced = newest_mp4(stem)
    if produced is None:
        raise SystemExit(f"Render finished but no mp4 named {stem}.mp4 was found.")

    # mirror the script's path under loci/ into the media/ domain
    rel = script.relative_to(HERE).with_suffix(".mp4")
    dest = MEDIA / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(produced, dest)
    print(f"\n✓ {scene}  ->  {dest.relative_to(HERE.parent)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
