#!/usr/bin/env python3
"""Render a loci/manim scene and drop the mp4 at its mirrored k-graph path.

Two trees share the same k-graph **relative path**; only the **origin** (root)
differs. Roots are configured in ``render.toml`` (``src_root``, ``dst_root``).

    <src_root>/…/F-01-carbon-binder.py      ← scene script
    <dst_root>/…/F-01-carbon-binder.mp4     ← render output

Resolution order: CLI flags > render.toml > built-in defaults.

Usage
-----
    python render.py T-computer-science/L-composite/F-01-carbon-binder.py
    python render.py scene.py --dst-root ../videos --src-root .

If no Scene class is given, the first `class X(...Scene)` in the file is used.
Quality defaults to high (-q h); use -q m or -q l while iterating.
"""
from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
from pathlib import Path

try:
    import tomllib
except ModuleNotFoundError:
    sys.exit("Python 3.11+ (tomllib) required")

HERE = Path(__file__).resolve().parent
CONFIG = HERE / "render.toml"
BUILD = HERE / ".build"

_SCENE_RE = re.compile(r"^\s*class\s+([A-Za-z_]\w*)\s*\(([^)]*)\)\s*:", re.MULTILINE)


def load_render_config() -> dict[str, str]:
    if not CONFIG.exists():
        return {}
    with CONFIG.open("rb") as fh:
        return tomllib.load(fh)


def resolve_root(path: str | Path, *, anchor: Path) -> Path:
    p = Path(path)
    return p.resolve() if p.is_absolute() else (anchor / p).resolve()


def configured_roots(cfg: dict) -> tuple[Path, Path]:
    src = resolve_root(cfg.get("src_root", "."), anchor=HERE)
    dst = resolve_root(cfg.get("dst_root", "../renders"), anchor=HERE)
    return src, dst


def find_scene(script: Path) -> str:
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


def resolve_script(path: Path, src_root: Path) -> Path:
    script = path if path.is_absolute() else (src_root / path).resolve()
    if not script.exists():
        raise SystemExit(f"Scene file not found: {script}")
    try:
        script.relative_to(src_root.resolve())
    except ValueError as exc:
        raise SystemExit(
            f"Scene {script} is not under src_root {src_root} "
            "(adjust src_root in render.toml or pass --src-root)"
        ) from exc
    return script


def render_dest(script: Path, src_root: Path, dst_root: Path) -> Path:
    rel = script.relative_to(src_root.resolve()).with_suffix(".mp4")
    return dst_root.resolve() / rel


def main() -> int:
    cfg = load_render_config()
    cfg_src, cfg_dst = configured_roots(cfg)

    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "script",
        help="scene .py — relative to src_root, or absolute",
    )
    parser.add_argument("scene", nargs="?", help="Scene class (default: first found)")
    parser.add_argument(
        "--src-root",
        type=Path,
        default=None,
        help=f"scene tree root (default: render.toml → {cfg_src})",
    )
    parser.add_argument(
        "--dst-root",
        type=Path,
        default=None,
        help=f"output tree root (default: render.toml → {cfg_dst})",
    )
    parser.add_argument(
        "-q", "--quality", default="h", choices=["l", "m", "h", "p", "k"],
        help="manim quality: l=480p m=720p h=1080p p=1440p k=4k (default h)",
    )
    args = parser.parse_args()

    src_root = args.src_root.resolve() if args.src_root else cfg_src
    dst_root = args.dst_root.resolve() if args.dst_root else cfg_dst
    script = resolve_script(Path(args.script), src_root)
    dest = render_dest(script, src_root, dst_root)
    scene = args.scene or find_scene(script)
    stem = script.stem

    print(f"  config:   {CONFIG.name}")
    print(f"  src_root: {src_root}")
    print(f"  src:      {script}")
    print(f"  dst_root: {dst_root}")
    print(f"  dst:      {dest}")

    cmd = [
        sys.executable, "-m", "manim", "render",
        f"-q{args.quality}",
        "--media_dir", str(BUILD),
        "-o", stem,
        str(script),
        scene,
    ]
    print("»", " ".join(cmd))
    result = subprocess.run(cmd, cwd=str(src_root))
    if result.returncode != 0:
        return result.returncode

    produced = newest_mp4(stem)
    if produced is None:
        raise SystemExit(f"Render finished but no mp4 named {stem}.mp4 was found.")

    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(produced, dest)
    print(f"\n✓ {scene}  ->  {dest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
