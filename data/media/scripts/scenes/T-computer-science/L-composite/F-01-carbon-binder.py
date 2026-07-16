"""Carbon Binder — abstract interface C, graph composition, orthogonal axes."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import FadeOut, Group

from loci import (
    Circle,
    ConnectNodes,
    FillStyle,
    Graph,
    PatchNodeStyle,
    Place,
    Restyle,
    Stage,
    Vec,
    directed_segment,
    patch_circle_style,
    plain_segment,
    register_graph,
    register_stage,
)
from loci.ticker import SceneContext, TickerSpan
from loci.voiceover import LociVoiceoverScene, VoiceoverTickerPlayer

from _visuals import (
    BINDER,
    COMPOSITE,
    DECORATOR,
    LEAF,
    MUTED,
    QUERY_B,
    TYPE_B,
    WAIT,
    add_staged,
    binder,
    branch_out,
    composite_box,
    composite_disk,
    decorator_node,
    emphasis,
    grow_down,
    leaf,
    link_then_reveal,
    math,
    note,
)

MIN_WAIT = WAIT

_ISO_O = Vec(0.0, -0.15)
_ISO_SX = 0.82
_ISO_SY = 0.44
_ISO_SZ = 0.95

_CUBE_EDGES = [
    (0, 1), (1, 2), (2, 3), (3, 0),
    (4, 5), (5, 6), (6, 7), (7, 4),
    (0, 4), (1, 5), (2, 6), (3, 7),
]

# Cross-links — entrelazamiento, not a tree
_CUBE_CROSS = [(0, 6), (1, 7), (2, 4), (3, 5)]


def _iso(x: float, y: float, z: float) -> Vec:
    return _ISO_O + Vec(_ISO_SX * (x - y), _ISO_SY * (x + y) + _ISO_SZ * z)


class CarbonBinder(LociVoiceoverScene):
    def construct(self):
        self.setup_voiceover()
        self._act_interface()
        self._fade_scene()
        self._act_graph_shapes()
        self._fade_scene()
        self._act_axes_and_mixed()
        self._fade_scene()
        self._act_under_c()
        self._fade_scene()
        self._act_decorator()
        self._fade_scene()
        self._act_entrelazamientos()
        self._fade_scene()
        self._act_specialization()
        self.wait(0.8)

    def _fade_scene(self) -> None:
        if not self.mobjects:
            return
        self.play(FadeOut(Group(*self.mobjects)), run_time=0.6)
        self.wait(0.1)

    def _play_g(self, span: TickerSpan, graph: Graph, ctx: SceneContext) -> None:
        VoiceoverTickerPlayer.from_span(span, ctx).play(self)

    def _play_s(self, span: TickerSpan, stage: Stage, ctx: SceneContext) -> None:
        VoiceoverTickerPlayer.from_span(span, ctx).play(self, system="stage")

    # ------------------------------------------------------------------
    def _act_interface(self) -> None:
        g = Graph()
        hub = g.add_node(Vec(0, 1.4), binder(), label=math(r"C", color=BINDER, size=40))
        slots = [
            (Vec(-3.2, -0.6), r"C_1"),
            (Vec(-1.1, -0.6), r"C_2"),
            (Vec(1.1, -0.6), r"C_3"),
            (Vec(3.2, -0.6), r"C_4"),
        ]
        kids = [add_staged(g, p, "binder", t, BINDER) for p, t in slots]
        meta = [("binder", t, BINDER) for _, t in slots]

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Carbon Binder. Here, C is our common binder — "
                "an abstract interface that many concrete forms can implement."
            ),
        )
        span.add(PatchNodeStyle(hub.id, emphasis(BINDER)), wait=MIN_WAIT,
                  narration="Whenever we admit a form, we write it as x colon C.")
        branch_out(
            span, hub, kids, meta, root_color=BINDER,
            narrations=[
                "Each concretion, in turn, implements the same interface locally.",
                None, None, None,
            ],
        )
        span.pause(
            wait=MIN_WAIT,
            narration="So one contract, many concretions — and the interface itself stays fixed.",
        )
        self._play_g(span, g, ctx)

    # ------------------------------------------------------------------
    def _act_graph_shapes(self) -> None:
        """Composition is a graph — nodes and edges. Shapes vary; not always a DAG or tree."""
        g = Graph()

        pipe = [g.add_node(Vec(-4.0, -0.4), binder(), label=math(r"C", color=BINDER, size=24))]
        for x in (-2.6, -1.2, 0.2):
            pipe.append(add_staged(g, Vec(x, -0.4), "binder", r"C", BINDER))

        t_root = g.add_node(Vec(3.6, 1.6), binder(), label=math(r"C", color=BINDER, size=26))
        t_mid = add_staged(g, Vec(2.4, 0.0), "binder", r"C", BINDER)
        t_r = add_staged(g, Vec(5.0, 0.0), "binder", r"C", BINDER)
        t_end = add_staged(g, Vec(5.0, -1.4), "binder", r"C", BINDER)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Composition is built from nodes and edges — a graph. "
                "It need not be a tree or a DAG. "
                "On the left, a pipeline; on the right, something that branches."
            ),
        )
        for i in range(1, len(pipe)):
            link_then_reveal(
                span, pipe[i - 1], pipe[i], kind="binder", tex=r"C", color=BINDER,
                ew=0.32, cw=0.28,
                narration="On the left, a chain — each step has one successor." if i == 2 else None,
            )
        link_then_reveal(span, t_root, t_mid, kind="binder", tex=r"C", color=BINDER, ew=0.32, cw=0.28)
        link_then_reveal(span, t_root, t_r, kind="binder", tex=r"C", color=BINDER, ew=0.32, cw=0.28,
                         narration="On the right, a branch — one node with several neighbours.")
        link_then_reveal(span, t_r, t_end, kind="binder", tex=r"C", color=BINDER, ew=0.32, cw=0.28,
                         narration="And every node here is still a concretion of C.")
        self._play_g(span, g, ctx)

    # ------------------------------------------------------------------
    def _act_axes_and_mixed(self) -> None:
        g = Graph()
        root = g.add_node(Vec(0, 2.35), composite_box(), label=math(r"Comp", color=COMPOSITE, size=28))

        d1 = add_staged(g, Vec(-2.9, 1.0), "decorator", r"n_1", DECORATOR)
        d2 = add_staged(g, Vec(-2.9, -0.05), "decorator", r"n_2", DECORATOR)
        core_v = add_staged(g, Vec(-2.9, -1.15), "binder", r"C", BINDER)

        h1 = add_staged(g, Vec(1.0, 1.0), "binder", r"C", BINDER)
        h2 = add_staged(g, Vec(3.0, 1.0), "binder", r"C", BINDER)
        h3 = add_staged(g, Vec(3.0, -0.55), "binder", r"C", BINDER)

        edges = [
            ("root", "d1"), ("d1", "d2"), ("d2", "core_v"),
            ("root", "h1"), ("h1", "h2"), ("h2", "h3"),
        ]
        nodes = {
            "root": root, "d1": d1, "d2": d2, "core_v": core_v,
            "h1": h1, "h2": h2, "h3": h3,
        }
        meta = {
            "root": ("composite_box", r"Comp", COMPOSITE),
            "d1": ("decorator", r"n_1", DECORATOR),
            "d2": ("decorator", r"n_2", DECORATOR),
            "core_v": ("binder", r"C", BINDER),
            "h1": ("binder", r"C", BINDER),
            "h2": ("binder", r"C", BINDER),
            "h3": ("binder", r"C", BINDER),
        }

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Now, two orthogonal ranks — independent growth directions. "
                "We draw depth on one branch and breadth on another; "
                "what matters is orthogonality, not the drawing orientation."
            ),
        )
        grow_down(span, nodes, edges, "root", meta,
                  narration="One graph shape, with two independent directions.", mid=2)
        self._play_g(span, g, ctx)

        self._fade_scene()
        stage = Stage()
        sctx = SceneContext()
        register_stage(sctx, stage)
        ax = TickerSpan()
        o = Vec(-3.5, -1.8)
        hx = directed_segment(o, o + Vec(5.0, 0), stroke_color=COMPOSITE, stroke_width=2.8)
        vy = directed_segment(o + Vec(2.5, 0), o + Vec(2.5, 2.4), stroke_color=DECORATOR, stroke_width=2.8)
        ax.pause(
            wait=MIN_WAIT,
            narration=(
                "Composite and decorator are orthogonal axes — "
                "they grow in different directions. "
                "Horizontal and vertical are simply our choice for this video."
            ),
        )
        ax.add(Place(hx, item_id="hx"), wait=MIN_WAIT,
               narration="Composite is breadth — one-to-many containment.")
        ax.add(Place(note("Comp", color=COMPOSITE, size=22), at=Vec(-0.8, -2.2), item_id="hxl"), wait=0.3)
        ax.add(Place(vy, item_id="vy"), wait=MIN_WAIT,
               narration="Decorator is depth — one-around-one wrapping.")
        ax.add(Place(note("Dec", color=DECORATOR, size=22), at=Vec(0.5, 0.35), item_id="vyl"), wait=MIN_WAIT)
        ax.pause(
            wait=MIN_WAIT,
            narration="Two independent ranks, both living over the same binder C.",
        )
        self._play_s(ax, stage, sctx)

    # ------------------------------------------------------------------
    def _act_under_c(self) -> None:
        g = Graph()
        iface = g.add_node(Vec(0, 2.0), binder(), label=math(r"C", color=BINDER, size=38))
        leaf_n = add_staged(g, Vec(-2.4, 0.3), "leaf", r"L", LEAF)
        comp_n = add_staged(g, Vec(2.0, 0.3), "composite_box", r"Comp", COMPOSITE)
        c1 = add_staged(g, Vec(1.0, -1.15), "binder", r"C", BINDER)
        c2 = add_staged(g, Vec(3.2, -1.15), "binder", r"C", BINDER)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "C is the abstract interface. "
                "A concrete form may present as a leaf L, or as a composite Comp — "
                "and both are admitted as x colon C."
            ),
        )
        span.add(PatchNodeStyle(iface.id, emphasis(BINDER)), wait=MIN_WAIT)
        link_then_reveal(span, iface, leaf_n, kind="leaf", tex=r"L", color=LEAF,
                         narration="A leaf: L colon C.")
        link_then_reveal(span, iface, comp_n, kind="composite_box", tex=r"Comp", color=COMPOSITE,
                         narration="A composite: Comp of children — still colon C.")
        link_then_reveal(span, comp_n, c1, kind="binder", tex=r"C", color=BINDER, ew=0.3, cw=0.28)
        link_then_reveal(span, comp_n, c2, kind="binder", tex=r"C", color=BINDER, ew=0.3, cw=0.28,
                         narration="Different shapes, but the same admission contract.")
        self._play_g(span, g, ctx)

    # ------------------------------------------------------------------
    def _act_decorator(self) -> None:
        stage = Stage()
        ctx = SceneContext()
        register_stage(ctx, stage)
        span = TickerSpan()

        inner = binder()
        ring1 = Circle(radius=0.48, style=patch_circle_style(
            stroke_color=DECORATOR, stroke_width=2, fill=FillStyle(DECORATOR, 0.06)))
        ring2 = Circle(radius=0.66, style=patch_circle_style(
            stroke_color=DECORATOR, stroke_width=2, fill=None))

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Decorator growth wraps one component. "
                "The result is still typed as C. "
                "We'll show two equivalent pictures — the axis need not be vertical."
            ),
        )
        span.add(
            Place(inner, at=Vec(-3.2, 0.0), item_id="core"),
            Place(math(r"C", color=BINDER, size=32), at=Vec(-3.2, 0.0), item_id="core_l"),
            wait=MIN_WAIT,
        )
        span.add(Place(ring1, at=Vec(-3.2, 0.0), item_id="r1"), wait=MIN_WAIT,
                 narration="Concentric rings — radius grows outward.")
        span.add(Restyle("r1", {"stroke_width": 4}), wait=0.3)
        span.add(Place(ring2, at=Vec(-3.2, 0.0), item_id="r2"), wait=MIN_WAIT,
                 narration="Dec of C — still colon C.")
        span.add(Restyle("r2", {"stroke_width": 4}), wait=MIN_WAIT)

        pipe_x = 2.8
        n1 = decorator_node()
        n2 = decorator_node()
        n3 = binder()
        e12 = plain_segment(Vec(pipe_x, 0.85), Vec(pipe_x, 0.05), stroke_color=DECORATOR, stroke_width=2.5)
        e23 = plain_segment(Vec(pipe_x, 0.05), Vec(pipe_x, -0.75), stroke_color=DECORATOR, stroke_width=2.5)

        span.add(
            Place(n1, at=Vec(pipe_x, 0.85), item_id="n1"),
            Place(math(r"n_1", color=DECORATOR, size=24), at=Vec(pipe_x, 1.35), item_id="n1l"),
            wait=MIN_WAIT,
            narration="Or, alternatively, a vertical stack — one layout for depth.",
        )
        span.add(Place(e12, item_id="e12"), wait=0.28)
        span.add(
            Place(n2, at=Vec(pipe_x, 0.05), item_id="n2"),
            Place(math(r"n_2", color=DECORATOR, size=24), at=Vec(pipe_x + 0.55, 0.05), item_id="n2l"),
            wait=0.28,
        )
        span.add(Place(e23, item_id="e23"), wait=0.28)
        span.add(
            Place(n3, at=Vec(pipe_x, -0.75), item_id="n3"),
            Place(math(r"C", color=BINDER, size=24), at=Vec(pipe_x, -1.25), item_id="n3l"),
            wait=MIN_WAIT,
            narration="The innermost node is C. Orthogonality matters — the drawing direction does not.",
        )
        span.add(
            Place(math(r"Dec(C) : C", color="#FFFFFF", size=26), at=Vec(0, -2.35), item_id="eq"),
            wait=MIN_WAIT,
        )
        self._play_s(span, stage, ctx)

    # ------------------------------------------------------------------
    def _act_entrelazamientos(self) -> None:
        """Interwoven cube — every vertex is C; structure from a shared contract, not a hub."""
        verts = [_iso(0, 0, 0), _iso(1, 0, 0), _iso(1, 1, 0), _iso(0, 1, 0),
                 _iso(0, 0, 1), _iso(1, 0, 1), _iso(1, 1, 1), _iso(0, 1, 1)]
        center = _iso(0.5, 0.5, 0.5)

        stage = Stage()
        ctx = SceneContext()
        register_stage(ctx, stage)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Structure can also emerge through intertwinings — "
                "not necessarily a tree. "
                "Here, a cube drawn in two dimensions."
            ),
        )

        for i, (a, b) in enumerate(_CUBE_EDGES):
            seg = plain_segment(verts[a], verts[b], stroke_color=MUTED, stroke_width=2.2)
            span.add(Place(seg, item_id=f"e{i}"), wait=0.16,
                     narration="Edges define the graph." if i == 0 else None)

        for i, (a, b) in enumerate(_CUBE_CROSS):
            cross = plain_segment(verts[a], verts[b], stroke_color=BINDER, stroke_width=1.6)
            span.add(Place(cross, item_id=f"x{i}"), wait=0.14,
                     narration="Cross-links entwine the solid — so this is not a tree." if i == 0 else None)

        # faint contract ring at each vertex — implicit interface wrap
        wrap = Circle(radius=0.34, style=patch_circle_style(
            stroke_color=BINDER, stroke_width=1.5, fill=FillStyle(BINDER, 0.06)))

        for i, v in enumerate(verts):
            outward = v - center
            lbl = v + outward.normalized() * 0.4 if outward.length() > 1e-6 else v + Vec(0, 0.4)
            span.add(
                Place(wrap, at=v, item_id=f"w{i}"),
                Place(binder(), at=v, item_id=f"v{i}"),
                Place(math(r"C", color=BINDER, size=22), at=lbl, item_id=f"vl{i}"),
                wait=0.2,
                narration=(
                    "Each vertex is a concrete C — "
                    "like an implementation behind an interface."
                    if i == 0 else None
                ),
            )

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "There is no central hub. "
                "Each node answers the same contract locally, in a decentralized way — "
                "and you may interact with any of them."
            ),
        )
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "So the graph emerges from a common C contract — "
                "whether pipeline, branch, composite, decorator, or entwined solid."
            ),
        )
        self._play_s(span, stage, ctx)

    # ------------------------------------------------------------------
    def _act_specialization(self) -> None:
        g = Graph()
        c = g.add_node(Vec(-3.2, 0), binder(), label=math(r"C", color=BINDER, size=40))
        t = add_staged(g, Vec(0.6, 1.3), "binder", r"T", TYPE_B)
        q = add_staged(g, Vec(0.6, -1.3), "binder", r"Q", QUERY_B)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(wait=MIN_WAIT, narration="In practice, domains may specialize the same abstract binder.")
        span.add(PatchNodeStyle(c.id, emphasis(BINDER)), wait=MIN_WAIT)
        link_then_reveal(span, c, t, kind="binder", tex=r"T", color=TYPE_B,
                         narration="C specializes to T — the type universe.")
        link_then_reveal(span, c, q, kind="binder", tex=r"Q", color=QUERY_B,
                         narration="And C specializes to Q — the query universe.")
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Carbon Binder in short: abstract C as interface. "
                "Graphs compose from nodes and edges. "
                "Orthogonal axes for composite and decorator. "
                "And every concretion honours the same contract."
            ),
        )
        self._play_g(span, g, ctx)
