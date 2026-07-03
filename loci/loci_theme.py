"""Shared visual language for foundations scenes.

A tiny palette + caption/title helpers so every k-graph video feels like one
series. Scenes stay format-agnostic loci/manim; this only fixes colors and a
couple of recurring layout moves.
"""
from __future__ import annotations

from manim import DOWN, UP, MathTex, Text, VGroup

# Palette (tuned for the dark #0E1116 background set in manim.cfg).
BG = "#0E1116"
INK = "#E6EDF3"      # primary text
MUTED = "#9BA6B2"    # secondary text / edges
BINDER = "#6CB6FF"   # the binder surface C
GOLD = "#E3B341"
GREEN = "#7EE787"
PURPLE = "#D2A8FF"
CORAL = "#E07A5F"

ACCENTS = [BINDER, GOLD, GREEN, PURPLE, CORAL]


def caption(text: str, *, color: str = MUTED, size: float = 30) -> Text:
    """A plain-text line pinned near the bottom of the frame."""
    return Text(text, font_size=size, color=color).to_edge(DOWN, buff=0.55)


def caption_math(tex: str, *, color: str = MUTED, size: float = 40) -> MathTex:
    """A LaTeX line pinned near the bottom of the frame."""
    return MathTex(tex, font_size=size, color=color).to_edge(DOWN, buff=0.55)


def title(text: str, *, color: str = INK, size: float = 54) -> Text:
    return Text(text, font_size=size, color=color, weight="BOLD")


def subtitle(text: str, *, color: str = MUTED, size: float = 30) -> Text:
    return Text(text, font_size=size, color=color)


def title_block(main: str, sub: str | None = None) -> VGroup:
    """Centered title with an optional subtitle beneath it."""
    t = title(main)
    if sub is None:
        return VGroup(t)
    s = subtitle(sub).next_to(t, DOWN, buff=0.3)
    return VGroup(t, s)
