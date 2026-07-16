"""Shared visuals for L-composite lecture scenes."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from loci import (
    Circle,
    ConnectNodes,
    FillStyle,
    Graph,
    Label,
    PatchNodeStyle,
    Place,
    Rectangle,
    Vec,
    directed_segment,
    patch_circle_style,
    patch_label_style,
    patch_rectangle_style,
)
from loci.systems.graph.state import get_node, node_address, patch_node_style
from loci.ticker import Change, Command, SceneContext, TickerSpan

# Uniform geometry — keeps graph edges attached cleanly
R = 0.26
WH = 0.52
SW = 3.0
WAIT = 0.45
BG = "#000000"

# Roles
BINDER = "#6CB6FF"
LEAF = "#7EE787"
COMPOSITE = "#D2A8FF"
DECORATOR = "#E07A5F"
TYPE_B = "#A8C7FA"
QUERY_B = "#F9C86B"
CORPUS = "#C9D1D9"
K_CORPUS = CORPUS
FAM_K_C = COMPOSITE   # category c — composite
FAM_K_L = LEAF        # category l — leaf
TOPIC = COMPOSITE
LECTURE = "#B392F0"
FILE = LEAF

LINEAR = "#79C0FF"
RELATED = "#E07A5F"
MUTED = "#888888"
VALIDATOR = "#F9C86B"

NodeMeta = tuple[str, str, str]  # kind, tex, color


def math(tex: str, *, color: str = "#FFFFFF", size: int = 28) -> Label:
    return Label.math(tex, color=color, font_size=size)


def note(tex: str, *, color: str = "#CCCCCC", size: int = 22) -> Label:
    return Label(tex, style=patch_label_style(color=color, font_size=size))


def _fill(color: str, opacity: float = 0.28) -> FillStyle:
    return FillStyle(color, opacity)


def _concealed_fill() -> FillStyle:
    return FillStyle(BG, 0)


def concrete_square(color: str) -> Rectangle:
    """Square concrete — used where a box is intentional (e.g. carbon composite)."""
    return Rectangle(
        width=WH,
        height=WH,
        style=patch_rectangle_style(stroke_color=color, stroke_width=SW, fill=_fill(color)),
    )


def concrete_disk(color: str) -> Circle:
    """Concrete component — circle (κ labels i, f, e, g, …)."""
    return Circle(
        radius=R,
        style=patch_circle_style(stroke_color=color, stroke_width=SW, fill=_fill(color)),
    )


def category_box(color: str) -> Rectangle:
    """TLF category node — square."""
    return Rectangle(
        width=WH,
        height=WH,
        style=patch_rectangle_style(stroke_color=color, stroke_width=SW, fill=_fill(color, 0.12)),
    )


def tlf_concrete(color: str) -> Circle:
    """TLF concrete κ label (T, L, or F) — circle."""
    return concrete_disk(color)


def leaf() -> Circle:
    return Circle(
        radius=R,
        style=patch_circle_style(stroke_color=LEAF, stroke_width=SW, fill=_fill(LEAF)),
    )


def composite_box() -> Rectangle:
    return Rectangle(
        width=WH,
        height=WH,
        style=patch_rectangle_style(stroke_color=COMPOSITE, stroke_width=SW, fill=_fill(COMPOSITE)),
    )


def composite_disk() -> Circle:
    return Circle(
        radius=R,
        style=patch_circle_style(stroke_color=COMPOSITE, stroke_width=SW, fill=_fill(COMPOSITE)),
    )


def binder(color: str = BINDER) -> Circle:
    return Circle(
        radius=R,
        style=patch_circle_style(stroke_color=color, stroke_width=SW, fill=_fill(color)),
    )


def decorator_node() -> Circle:
    return Circle(
        radius=R,
        style=patch_circle_style(stroke_color=DECORATOR, stroke_width=SW, fill=_fill(DECORATOR, 0.18)),
    )


def concealed(kind: str) -> Circle | Rectangle:
    hidden = patch_circle_style(stroke_width=0, fill=_concealed_fill())
    rect_hidden = patch_rectangle_style(stroke_width=0, fill=_concealed_fill())
    if kind in ("composite_box", "cat_c", "cat_l", "grouping"):
        return Rectangle(width=WH, height=WH, style=rect_hidden)
    if kind in ("concrete", "topic", "lecture", "tlf", "file", "decorator"):
        return Circle(radius=R, style=hidden)
    return Circle(radius=R, style=hidden)


def concealed_label(tex: str, *, color: str, size: int = 28) -> Label:
    return math(tex, color=BG, size=size)


def visible_style(kind: str, color: str) -> dict[str, Any]:
    category_kinds = ("composite_box", "cat_c", "cat_l", "grouping")
    if kind in category_kinds:
        return {
            "stroke_width": SW,
            "stroke_color": color,
            "fill": FillStyle(color, 0.12),
        }
    fill_opacity = 0.18 if kind == "decorator" else 0.28
    return {
        "stroke_width": SW,
        "stroke_color": color,
        "fill": FillStyle(color, fill_opacity),
    }


def emphasis(color: str, *, fill_opacity: float = 0.42) -> dict[str, Any]:
    """Highlight a node in its own color — never borrow a parent edge color."""
    return {"stroke_width": SW + 1.5, "fill": FillStyle(color, fill_opacity)}


@dataclass
class RevealNode(Command):
    """Show a concealed node after its incoming edge lands."""

    node_id: str
    style: dict[str, Any]
    label: Label | str | None

    def apply(self, ctx: SceneContext) -> list[Change]:
        graph = ctx.system("graph")
        node = get_node(graph, self.node_id)
        old_style = node.shape.style
        old_label = node.label
        node.shape.style = patch_node_style(node, **self.style)
        node.label = self.label
        return [
            Change(
                system="graph",
                address=node_address(self.node_id),
                prop="shape.style",
                old=old_style,
                new=node.shape.style,
            ),
            Change(
                system="graph",
                address=node_address(self.node_id),
                prop="label",
                old=old_label,
                new=self.label,
            ),
        ]


def add_staged(
    graph: Graph,
    position: Vec,
    kind: str,
    tex: str,
    color: str,
    *,
    visible: bool = False,
):
    shape = {
        "leaf": leaf,
        "binder": lambda: binder(color),
        "grouping": lambda: category_box(color),
        "cat_c": lambda: category_box(color),
        "cat_l": lambda: category_box(color),
        "tlf": lambda: tlf_concrete(color),
        "topic": lambda: tlf_concrete(color),
        "lecture": lambda: tlf_concrete(color),
        "file": lambda: tlf_concrete(color),
        "concrete": lambda: concrete_disk(color),
        "composite_box": lambda: concrete_square(color),
        "composite_disk": lambda: concrete_disk(color),
        "decorator": lambda: concrete_disk(color),
    }[kind]()
    if not visible:
        shape = concealed(kind)
    label = math(tex, color=color) if visible else concealed_label(tex, color=color)
    return graph.add_node(position, shape, label=label)


def reveal(
    span: TickerSpan,
    node,
    kind: str,
    tex: str,
    color: str,
    *,
    wait: float = WAIT,
    narration: str | None = None,
) -> None:
    span.add(
        RevealNode(node.id, visible_style(kind, color), math(tex, color=color)),
        wait=wait,
        narration=narration,
    )


def link_then_reveal(
    span: TickerSpan,
    source,
    target,
    *,
    kind: str,
    tex: str,
    color: str,
    ew: float = WAIT * 0.8,
    cw: float = WAIT * 0.65,
    narration: str | None = None,
) -> None:
    """Edge grows first; the target node pops in its own color afterward."""
    span.add(ConnectNodes(source.id, target.id, directed=True), wait=ew)
    reveal(span, target, kind, tex, color, wait=cw, narration=narration)


def branch_out(
    span: TickerSpan,
    root,
    children: list,
    meta: list[NodeMeta],
    *,
    root_color: str,
    ew: float = WAIT * 0.75,
    cw: float = WAIT * 0.55,
    narrations: list[str | None] | None = None,
) -> None:
    span.add(PatchNodeStyle(root.id, emphasis(root_color)), wait=WAIT * 0.7)
    narrations = narrations or [None] * len(children)
    for child, (kind, tex, color), narration in zip(children, meta, narrations):
        link_then_reveal(
            span,
            root,
            child,
            kind=kind,
            tex=tex,
            color=color,
            ew=ew,
            cw=cw,
            narration=narration,
        )


def grow_down(
    span: TickerSpan,
    nodes: dict,
    edges: list[tuple[str, str]],
    root: str,
    meta: dict[str, NodeMeta],
    *,
    ew: float = WAIT * 0.75,
    cw: float = WAIT * 0.55,
    narration: str | None = None,
    mid: int | None = None,
) -> None:
    """Root first, then each parent→child edge, then child pops in its own color."""
    _, _, root_color = meta[root]
    span.add(PatchNodeStyle(nodes[root].id, emphasis(root_color)), wait=WAIT * 0.7)
    for idx, (src, tgt) in enumerate(edges):
        kind, tex, color = meta[tgt]
        n = narration if idx == mid and narration else None
        link_then_reveal(
            span,
            nodes[src],
            nodes[tgt],
            kind=kind,
            tex=tex,
            color=color,
            ew=ew,
            cw=cw,
            narration=n,
        )


def boundary(center: Vec, toward: Vec, radius: float = R) -> Vec:
    d = toward - center
    if d.length() < 1e-6:
        return center
    return center + d.normalized() * radius


def contract_ring(color: str = TYPE_B, *, radius: float | None = None) -> Circle:
    """Faint ring — node still satisfies the binder contract."""
    r = radius if radius is not None else R + 0.1
    return Circle(
        radius=r,
        style=patch_circle_style(
            stroke_color=color,
            stroke_width=1.8,
            fill=FillStyle(color, 0.06),
        ),
    )


def family_box(width: float, height: float, *, color: str) -> Rectangle:
    """Unfilled family bracket — visible stroke + faint tint."""
    return Rectangle(
        width=width,
        height=height,
        style=patch_rectangle_style(
            stroke_color=color,
            stroke_width=3.0,
            fill=FillStyle(color, 0.07),
        ),
    )


def outline_box(width: float, height: float, *, color: str = MUTED) -> Rectangle:
    return family_box(width, height, color=color)


def grouping_node(color: str) -> Rectangle:
    """Category / union node — square."""
    return category_box(color)


def legend_panel(*, grouping: str, concrete: str) -> list[tuple[Any, Vec, str]]:
    """Return stage placements for the category-vs-concrete legend."""
    return [
        (note(grouping, color=MUTED, size=16), Vec(0.0, -2.55), "leg_g"),
        (note(concrete, color=CORPUS, size=16), Vec(0.0, -3.05), "leg_c"),
    ]


# Family colors — squares for categories, circles for concretes
FAM_T = TYPE_B       # binder T, and t / l / c categories
FAM_D = DECORATOR    # d category
FAM_Q = QUERY_B      # binder Q, and ℓ / c categories


def decorator_rings() -> tuple[Circle, Circle]:
    """r inner, v outer — concrete decorator layers."""
    r_ring = Circle(
        radius=0.42,
        style=patch_circle_style(
            stroke_color=DECORATOR, stroke_width=2.2, fill=FillStyle(DECORATOR, 0.08),
        ),
    )
    v_ring = Circle(
        radius=0.56,
        style=patch_circle_style(
            stroke_color=VALIDATOR, stroke_width=2.2, fill=FillStyle(VALIDATOR, 0.08),
        ),
    )
    return r_ring, v_ring


def not_ring(color: str = DECORATOR) -> Circle:
    """Single negation ring — concrete decorator n in Q."""
    return Circle(
        radius=0.48,
        style=patch_circle_style(
            stroke_color=color,
            stroke_width=2.2,
            fill=FillStyle(color, 0.08),
        ),
    )


MINI_R = 0.15


def mini_shape(kind: str, color: str):
    """Small shape for stacked T examples."""
    sw = 2.2
    fill = FillStyle(color, 0.22)
    if kind == "composite_box":
        s = MINI_R * 2
        return Rectangle(
            width=s,
            height=s,
            style=patch_rectangle_style(stroke_color=color, stroke_width=sw, fill=fill),
        )
    if kind == "decorator":
        return Circle(
            radius=MINI_R,
            style=patch_circle_style(stroke_color=color, stroke_width=sw, fill=FillStyle(color, 0.14)),
        )
    return Circle(
        radius=MINI_R,
        style=patch_circle_style(stroke_color=color, stroke_width=sw, fill=fill),
    )


def stack_row(
    span: TickerSpan,
    origin: Vec,
    rows: list[tuple[str, str, str]],
    *,
    prefix: str,
    dy: float = 0.46,
    wait: float = 0.14,
    narration: str | None = None,
) -> None:
    """Vertical stack of mini nodes on the stage (no edges)."""
    for i, (kind, tex, color) in enumerate(rows):
        pos = Vec(origin.x, origin.y - i * dy)
        span.add(
            Place(mini_shape(kind, color), at=pos, item_id=f"{prefix}s{i}"),
            Place(math(tex, color=color, size=20), at=pos, item_id=f"{prefix}l{i}"),
            wait=wait,
            narration=narration if i == 0 else None,
        )


@dataclass
class DottedDirectedLine:
    """Thin dashed segment with arrow — traversal overlay."""

    start: Vec
    end: Vec
    stroke_color: str = LINEAR
    stroke_width: float = 1.4

    def resolved_style(self) -> Any:
        from loci.resources.lines.style import LINE_STYLE

        return LINE_STYLE

    def to_manim(self, *args: Any, **kwargs: Any) -> Any:
        from manim import Arrow, DashedVMobject

        arrow = Arrow(
            self.start.to_manim(),
            self.end.to_manim(),
            buff=0.06,
            color=self.stroke_color,
            stroke_width=self.stroke_width,
            max_tip_length_to_length_ratio=0.14,
        )
        return DashedVMobject(arrow, num_dashes=14, dashed_ratio=0.55)


@dataclass
class CurvedDirectedLine:
    """Quadratic-style arc with arrow — Drawable for stage overlays."""

    start: Vec
    end: Vec
    angle: float = -2.2
    stroke_color: str = "#FFFFFF"
    stroke_width: float = 2.5
    dotted: bool = False

    def resolved_style(self) -> Any:
        from loci.resources.lines.style import LINE_STYLE

        return LINE_STYLE

    def to_manim(self, *args: Any, **kwargs: Any) -> Any:
        from manim import CurvedArrow, DashedVMobject

        arc = CurvedArrow(
            self.start.to_manim(),
            self.end.to_manim(),
            color=self.stroke_color,
            stroke_width=self.stroke_width,
            angle=self.angle,
        )
        if self.dotted:
            return DashedVMobject(arc, num_dashes=12, dashed_ratio=0.55)
        return arc


def dotted_directed_edge(start: Vec, end: Vec, *, color: str, width: float = 1.4):
    """Dashed directed edge between node centers (boundary-aware)."""
    return DottedDirectedLine(
        boundary(start, end),
        boundary(end, start),
        stroke_color=color,
        stroke_width=width,
    )


def arc_edge(
    start: Vec,
    end: Vec,
    *,
    color: str,
    width: float = 2.5,
    angle: float = -2.2,
    dotted: bool = False,
):
    """Curved directed edge between node centers (boundary-aware)."""
    return CurvedDirectedLine(
        boundary(start, end),
        boundary(end, start),
        angle=angle,
        stroke_color=color,
        stroke_width=width,
        dotted=dotted,
    )


