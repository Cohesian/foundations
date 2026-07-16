"""Type Binder — T as type-universe binder with orthogonal type and decorator axes."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import FadeOut, Group, VGroup

from loci import (
    Graph,
    PatchNodeStyle,
    Place,
    Stage,
    Vec,
    directed_segment,
    plain_segment,
    register_graph,
    register_stage,
)
from loci.ticker import SceneContext, TickerPlayer, TickerSpan
from loci.voiceover import LociVoiceoverScene, VoiceoverTickerPlayer

from _visuals import (
    BINDER,
    DECORATOR,
    FAM_D,
    FAM_T,
    MUTED,
    TYPE_B,
    WAIT,
    add_staged,
    binder,
    contract_ring,
    decorator_rings,
    emphasis,
    legend_panel,
    link_then_reveal,
    math,
    note,
)

MIN_WAIT = WAIT

# Concrete decorator kinds (squares, d-family color)
REMOVER = DECORATOR
VALIDATOR = "#F9C86B"


class TypeBinder(LociVoiceoverScene):
    def construct(self):
        self.setup_voiceover()
        self._act_specialization()
        self._fade_scene()
        self._act_two_axes()
        self._fade_scene()
        self._act_decorator_views()
        self._fade_scene()
        self._act_type_axis()
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

    def _play_gs(self, span: TickerSpan, ctx: SceneContext) -> None:
        """Play a span that may update graph and stage in the same timeline."""
        player = TickerPlayer(span, ctx)
        systems: list[str] = []
        for name in ("graph", "stage"):
            try:
                ctx.system(name)
            except KeyError:
                continue
            systems.append(name)

        groups = {name: ctx.render(name) for name in systems}
        for name, group in groups.items():
            ctx.set_mobject(name, group)
        self.add(VGroup(*groups.values()))

        for index, tick in enumerate(span.ticks):
            narration = getattr(tick, "narration", None)

            def _step() -> None:
                player.apply_tick(index)
                for name in systems:
                    old = ctx.mobject(name)
                    new = ctx.render(name)
                    self.remove(old)
                    self.add(new)
                    ctx.set_mobject(name, new)

            if narration:
                with self.voiceover(text=narration) as tracker:
                    _step()
                    self.wait(max(tick.wait, tracker.duration))
            else:
                _step()
                self.wait(tick.wait)

    # ------------------------------------------------------------------
    def _act_specialization(self) -> None:
        g = Graph()
        c = g.add_node(Vec(-2.8, 0), binder(BINDER), label=math(r"C", color=BINDER, size=34))
        t = add_staged(g, Vec(0.9, 0), "binder", r"T", TYPE_B)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Type Binder. Carbon Binder gave us abstract C — "
                "and here, we specialize it to the type universe T."
            ),
        )
        span.add(PatchNodeStyle(c.id, emphasis(BINDER)), wait=MIN_WAIT)
        link_then_reveal(
            span, c, t, kind="binder", tex=r"T", color=TYPE_B,
            narration="So C specializes to T: the binder of the type system.",
        )
        span.pause(
            wait=MIN_WAIT,
            narration="Any admitted form is written X colon T — T is the grouping surface.",
        )
        self._play_g(span, g, ctx)

    # ------------------------------------------------------------------
    def _act_two_axes(self) -> None:
        g = Graph()
        root = g.add_node(Vec(0, 1.7), binder(TYPE_B), label=math(r"T", color=TYPE_B, size=38))
        t_hub = add_staged(g, Vec(-2.6, 0.1), "grouping", r"t", FAM_T)
        d_hub = add_staged(g, Vec(2.6, 0.1), "grouping", r"d", FAM_D)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration="Inside T, two categories stay distinct — yet both still belong to the same binder.",
        )
        span.add(PatchNodeStyle(root.id, emphasis(TYPE_B)), wait=MIN_WAIT,
                  narration="First, the type axis t: what shape — leaf or composite?")
        link_then_reveal(span, root, t_hub, kind="grouping", tex=r"t", color=FAM_T, ew=0.35, cw=0.3)
        link_then_reveal(
            span, root, d_hub, kind="grouping", tex=r"d", color=FAM_D,
            narration="And the decorator axis d: what wrapper layers sit on top?",
        )
        self._play_g(span, g, ctx)

        self._fade_scene()
        stage = Stage()
        sctx = SceneContext()
        register_stage(sctx, stage)
        ax = TickerSpan()
        o = Vec(-3.2, -1.6)
        tx = directed_segment(o, o + Vec(4.5, 0), stroke_color=TYPE_B, stroke_width=2.8)
        dy = directed_segment(o + Vec(2.2, 0), o + Vec(2.2, 2.2), stroke_color=DECORATOR, stroke_width=2.8)
        ax.pause(
            wait=MIN_WAIT,
            narration=(
                "t gives us type geometry; d gives us wrapper geometry. "
                "They are orthogonal — independent ranks. "
                "Left-right and up-down are only how we chose to draw it."
            ),
        )
        ax.add(Place(tx, item_id="tx"), wait=MIN_WAIT, narration="Type axis: leaf or composite.")
        ax.add(Place(note("t", color=TYPE_B, size=22), at=Vec(-0.6, -2.0), item_id="txl"), wait=0.3)
        ax.add(Place(dy, item_id="dy"), wait=MIN_WAIT, narration="Decorator axis: wrap one inner T.")
        ax.add(Place(note("d", color=DECORATOR, size=22), at=Vec(2.55, 0.5), item_id="dyl"), wait=MIN_WAIT)
        ax.pause(wait=MIN_WAIT, narration="Two orthogonal axes, one binder T.")
        self._play_s(ax, stage, sctx)

    # ------------------------------------------------------------------
    def _act_decorator_views(self) -> None:
        """Brief note: d as radial or stacked — direction is layout only."""
        stage = Stage()
        ctx = SceneContext()
        register_stage(ctx, stage)
        span = TickerSpan()
        r_ring, v_ring = decorator_rings()

        span.pause(
            wait=MIN_WAIT,
            narration="The d category wraps one inner T — same structure, many possible layouts.",
        )
        span.add(
            Place(note("radial", color=FAM_D, size=18), at=Vec(-2.8, 1.45), item_id="lbl"),
            Place(binder(TYPE_B), at=Vec(-2.8, 0.0), item_id="core"),
            Place(math(r"t", color=FAM_T, size=28), at=Vec(-2.8, 0.0), item_id="core_l"),
            wait=MIN_WAIT * 0.7,
        )
        span.add(Place(r_ring, at=Vec(-2.8, 0.0), item_id="rr"), wait=MIN_WAIT * 0.6)
        span.add(Place(v_ring, at=Vec(-2.8, 0.0), item_id="vr"), wait=MIN_WAIT * 0.6,
                 narration="Rings around the core — one way to draw d.")

        px = 2.6
        e1 = plain_segment(Vec(px, 0.85), Vec(px, 0.05), stroke_color=FAM_D, stroke_width=2.5)
        e2 = plain_segment(Vec(px, 0.05), Vec(px, -0.75), stroke_color=FAM_D, stroke_width=2.5)
        span.add(
            Place(note("vertical stack", color=FAM_D, size=18), at=Vec(px, 1.45), item_id="plbl"),
            wait=MIN_WAIT * 0.5,
            narration="Or stacked vertically — all of that is just notation, not the nesting itself.",
        )
        span.add(
            Place(note("r", color=FAM_D, size=22), at=Vec(px + 0.55, 0.85), item_id="pr"),
            Place(e1, item_id="pe1"), wait=0.18,
        )
        span.add(
            Place(note("v", color=VALIDATOR, size=22), at=Vec(px + 0.55, 0.05), item_id="pv"),
            Place(e2, item_id="pe2"), wait=0.18,
        )
        span.add(
            Place(binder(FAM_T), at=Vec(px, -0.75), item_id="pt"),
            Place(math(r"t", color=FAM_T, size=22), at=Vec(px, -1.2), item_id="ptl"),
            wait=MIN_WAIT * 0.6,
        )
        span.pause(wait=MIN_WAIT * 0.7,
                   narration="What matters is the nesting — it stays d of T.")
        self._play_s(span, stage, ctx)

    # ------------------------------------------------------------------
    def _act_type_axis(self) -> None:
        self._act_type_tree()
        self._fade_scene()
        self._act_category_matrix()

    def _act_type_tree(self) -> None:
        """Classification tree — squares for categories, circles for concretes."""

        T_P = Vec(0.0, 3.15)
        T_P2 = Vec(-3.4, 2.05)
        D_P = Vec(3.4, 2.05)
        L_P = Vec(-5.15, 0.95)
        C_P = Vec(-1.75, 0.95)
        V_P = Vec(2.55, 0.95)
        R_P = Vec(4.15, 0.95)
        LEAF_P = {
            "i": Vec(-6.15, -0.45),
            "f": Vec(-5.05, -0.45),
            "b": Vec(-3.95, -0.45),
            "s": Vec(-2.85, -0.45),
        }
        M_P = Vec(-2.05, -0.45)
        A_P = Vec(-0.85, -0.45)

        g = Graph()
        stage = Stage()
        root = g.add_node(T_P, binder(TYPE_B), label=math(r"T", color=TYPE_B, size=36))
        t = add_staged(g, T_P2, "grouping", r"t", FAM_T)
        d = add_staged(g, D_P, "grouping", r"d", FAM_D)
        l = add_staged(g, L_P, "grouping", r"l", FAM_T)
        c = add_staged(g, C_P, "grouping", r"c", FAM_T)
        leaves = {k: add_staged(g, p, "concrete", k, FAM_T) for k, p in LEAF_P.items()}
        m = add_staged(g, M_P, "concrete", r"m", FAM_T)
        a = add_staged(g, A_P, "concrete", r"a", FAM_T)
        v = add_staged(g, V_P, "concrete", r"v", FAM_D)
        r = add_staged(g, R_P, "concrete", r"r", FAM_D)

        ctx = SceneContext()
        register_graph(ctx, g)
        register_stage(ctx, stage)
        span = TickerSpan()

        span.pause(
            wait=MIN_WAIT,
            narration="Now, the binder T has a classification tree — first categories, then concretes.",
        )
        span.add(
            Place(note("□ category   ○ concrete", color=MUTED, size=17), at=Vec(4.3, 2.75), item_id="key"),
            wait=MIN_WAIT * 0.5,
        )
        span.add(PatchNodeStyle(root.id, emphasis(TYPE_B)), wait=MIN_WAIT,
                  narration="From T, two main branches — type t and decorator d.")

        link_then_reveal(span, root, t, kind="grouping", tex=r"t", color=FAM_T, ew=0.34, cw=0.3,
                         narration="t groups type-shaped forms.")
        link_then_reveal(span, root, d, kind="grouping", tex=r"d", color=FAM_D, ew=0.34, cw=0.3,
                         narration="d groups wrapper-shaped forms.")

        span.add(Place(note(r"|", color=MUTED, size=20), at=Vec(-2.35, 1.45), item_id="u1"),
                 wait=0.18, narration="Under t, a union: leaf l or composite c.")

        link_then_reveal(span, t, l, kind="grouping", tex=r"l", color=FAM_T, ew=0.32, cw=0.28,
                         narration="l — the leaf category.")
        link_then_reveal(span, t, c, kind="grouping", tex=r"c", color=FAM_T, ew=0.32, cw=0.28,
                         narration="c — the composite category.")

        for idx, key in enumerate(["i", "f", "b", "s"]):
            link_then_reveal(
                span, l, leaves[key], kind="concrete", tex=key, color=FAM_T,
                ew=0.26, cw=0.22,
                narration="And the concrete leaves: integer, float, bool, string." if idx == 0 else None,
            )

        link_then_reveal(span, c, m, kind="concrete", tex=r"m", color=FAM_T, ew=0.26, cw=0.22,
                         narration="m — a map of T.")
        link_then_reveal(span, c, a, kind="concrete", tex=r"a", color=FAM_T, ew=0.26, cw=0.22,
                         narration="a — an array of T.")

        link_then_reveal(span, d, v, kind="concrete", tex=r"v", color=FAM_D, ew=0.28, cw=0.24,
                         narration="Under d, we find v the validator and r the remover.")
        link_then_reveal(span, d, r, kind="concrete", tex=r"r", color=FAM_D, ew=0.28, cw=0.24)

        for asset, pos, item_id in legend_panel(
            grouping="categories (□):  t, c, l, d",
            concrete="concretes (○):  i, f, b, s, m, a, r, v",
        ):
            span.add(Place(asset, at=pos, item_id=item_id), wait=0.12)

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "So categories are grouping unions in the grammar — "
                "and concretes are the components we actually instantiate."
            ),
        )

        ring_positions = [
            T_P, T_P2, D_P, L_P, C_P, *LEAF_P.values(), M_P, A_P, V_P, R_P,
        ]
        for i, pos in enumerate(ring_positions):
            span.add(Place(contract_ring(TYPE_B), at=pos, item_id=f"ring{i}"), wait=0.07,
                      narration=(
                          "And every node — category or concrete — still satisfies X colon T."
                          if i == 0 else None
                      ))

        self._play_gs(span, ctx)

    def _act_category_matrix(self) -> None:
        """Shape spine + parallel category-path column — every link is still T."""

        SX = -2.4
        FX = 3.1
        Y = {
            "T": 2.85,
            "r1": 2.05,
            "v1": 1.25,
            "m": 0.45,
            "r2": -0.55,
            "v2": -1.35,
            "i": -2.15,
        }
        NEST = 0.4

        g = Graph()
        stage = Stage()
        top = g.add_node(Vec(SX, Y["T"]), binder(TYPE_B), label=math(r"T", color=TYPE_B, size=32))
        r1 = add_staged(g, Vec(SX, Y["r1"]), "concrete", r"r", FAM_D)
        v1 = add_staged(g, Vec(SX, Y["v1"]), "concrete", r"v", FAM_D)
        m = add_staged(g, Vec(SX, Y["m"]), "concrete", r"m", FAM_T)
        r2 = add_staged(g, Vec(SX + NEST, Y["r2"]), "concrete", r"r", FAM_D)
        v2 = add_staged(g, Vec(SX + NEST, Y["v2"]), "concrete", r"v", FAM_D)
        i = add_staged(g, Vec(SX + NEST, Y["i"]), "concrete", r"i", FAM_T)

        ctx = SceneContext()
        register_graph(ctx, g)
        register_stage(ctx, stage)
        span = TickerSpan()

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Let's read one composed T shape — concretes on the left, "
                "category path on the right. Every step still binds to T."
            ),
        )
        span.add(
            Place(note("shape", color=MUTED, size=18), at=Vec(SX, 3.45), item_id="hsh"),
            Place(note("category path", color=MUTED, size=18), at=Vec(FX - 0.35, 3.45), item_id="hfam"),
            wait=MIN_WAIT * 0.6,
        )
        span.add(PatchNodeStyle(top.id, emphasis(TYPE_B)), wait=MIN_WAIT,
                  narration="Think of a decorated map holding a decorated integer — all as T.")

        link_then_reveal(span, top, r1, kind="concrete", tex=r"r", color=FAM_D, ew=0.26, cw=0.22)
        span.add(
            Place(math(r"T \to d", color=FAM_D, size=20), at=Vec(FX, Y["r1"]), item_id="f1"),
            wait=MIN_WAIT * 0.7,
            narration="Here, r and v sit in the d category.",
        )
        link_then_reveal(span, r1, v1, kind="concrete", tex=r"v", color=FAM_D, ew=0.24, cw=0.2)

        link_then_reveal(span, v1, m, kind="concrete", tex=r"m", color=FAM_T, ew=0.26, cw=0.22)
        span.add(
            Place(math(r"T \to t \to c", color=FAM_T, size=19),
                  at=Vec(FX, Y["m"]), item_id="f2"),
            wait=MIN_WAIT,
            narration="So m sits in the composite category under t.",
        )

        link_then_reveal(span, m, r2, kind="concrete", tex=r"r", color=FAM_D, ew=0.28, cw=0.22)
        span.add(
            Place(math(r"T \to d", color=FAM_D, size=20), at=Vec(FX, Y["r2"]), item_id="f3"),
            wait=MIN_WAIT * 0.7,
            narration="Inside m, we nest another decorated value — again in category d.",
        )
        link_then_reveal(span, r2, v2, kind="concrete", tex=r"v", color=FAM_D, ew=0.24, cw=0.2)
        link_then_reveal(span, v2, i, kind="concrete", tex=r"i", color=FAM_T, ew=0.26, cw=0.22)
        span.add(
            Place(math(r"T \to t \to l", color=FAM_T, size=19),
                  at=Vec(FX, Y["i"]), item_id="f4"),
            wait=MIN_WAIT,
            narration="And down to i — a concrete leaf in category l.",
        )

        span.add(
            Place(
                math(r"m[d\{r\{v\{i\}\}\}]:T", color="#FFFFFF", size=22),
                at=Vec(0.35, -3.05),
                item_id="eq",
            ),
            wait=MIN_WAIT,
            narration="Each node binds to the next T — one contract, end to end.",
        )

        all_pos = [Vec(SX, Y[k]) for k in ("T", "r1", "v1", "m")] + [
            Vec(SX + NEST, Y[k]) for k in ("r2", "v2", "i")
        ]
        span.add(Place(contract_ring(TYPE_B, radius=2.35), at=Vec(SX + 0.15, 0.35), item_id="big"),
                 wait=MIN_WAIT,
                 narration="Type Binder in short: orthogonal categories, one surface — every form X colon T.")

        for j, pos in enumerate(all_pos):
            span.add(Place(contract_ring(TYPE_B), at=pos, item_id=f"mr{j}"), wait=0.05)

        self._play_gs(span, ctx)
