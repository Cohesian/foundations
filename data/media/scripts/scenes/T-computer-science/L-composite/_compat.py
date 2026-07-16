"""Compatibility shims for restored scenes — maps old helpers to _visuals."""

from __future__ import annotations

from loci import Circle, FillStyle, Graph, Label, Rectangle, Vec, patch_rectangle_style

from _visuals import (
    BINDER,
    COMPOSITE,
    DECORATOR,
    LEAF,
    MUTED,
    QUERY_B,
    TYPE_B,
    add_staged,
    binder,
    composite_box,
    composite_disk,
    concealed,
    decorator_node,
    leaf,
)

TYPE_AXIS = TYPE_B
TOPIC = COMPOSITE
LECTURE = COMPOSITE
FILE = LEAF
REMOVER = DECORATOR
VALIDATOR = QUERY_B
GROUP = MUTED


def _binder(radius: float = 0.26, *, color: str = TYPE_B) -> Circle:
    return binder(color)


def _topic(radius: float = 0.26) -> Circle:
    return composite_disk()


def _lecture() -> Rectangle:
    return composite_box()


def _file() -> Circle:
    return leaf()


def _invisible_anchor(graph: Graph, pos: Vec, label: Label | str):
    return graph.add_node(pos, concealed("binder"), label=label)


EQ_COLOR = LEAF
GT_COLOR = LEAF
HAS_COLOR = LEAF
NOT_COLOR = DECORATOR


def _leaf(name: str, *, color: str = LEAF) -> Circle:
    return leaf()


def _composite(name: str):
    return composite_box() if name == "a" else composite_disk()

