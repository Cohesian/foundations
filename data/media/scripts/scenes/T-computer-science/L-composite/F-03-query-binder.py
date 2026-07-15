"""Query Binder — Q as predicate binder with composite and decorator categories."""

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
    FAM_Q,
    MUTED,
    QUERY_B,
    WAIT,
    add_staged,
    binder,
    contract_ring,
    emphasis,
    legend_panel,
    link_then_reveal,
    math,
    not_ring,
    note,
)

MIN_WAIT = WAIT


class QueryBinder(LociVoiceoverScene):
    def construct(self):
        self.setup_voiceover()
        self._act_specialization()
        self._fade_scene()
        self._act_two_axes()
        self._fade_scene()
        self._act_decorator_views()
        self._fade_scene()
        self._act_query_axis()
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
        q = add_staged(g, Vec(0.9, 0), "binder", r"Q", QUERY_B)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Query Binder. The binder pattern is not limited to types. "
                "Here we specialize C to the query universe Q."
            ),
        )
        span.add(PatchNodeStyle(c.id, emphasis(BINDER)), wait=MIN_WAIT)
        link_then_reveal(
            span, c, q, kind="binder", tex=r"Q", color=QUERY_B,
            narration="C specializes to Q — the binder of predicates and query structure.",
        )
        span.pause(
            wait=MIN_WAIT,
            narration="Any valid predicate form is written q colon Q. Q is the grouping surface.",
        )
        self._play_g(span, g, ctx)

    # ------------------------------------------------------------------
    def _act_two_axes(self) -> None:
        g = Graph()
        root = g.add_node(Vec(0, 1.7), binder(QUERY_B), label=math(r"Q", color=QUERY_B, size=38))
        c_hub = add_staged(g, Vec(-2.6, 0.1), "grouping", r"c", FAM_Q)
        d_hub = add_staged(g, Vec(2.6, 0.1), "grouping", r"d", FAM_D)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration="Inside Q, two categories stay distinct — yet both belong to the same binder.",
        )
        span.add(PatchNodeStyle(root.id, emphasis(QUERY_B)), wait=MIN_WAIT,
                  narration="Composite category c: group many predicates.")
        link_then_reveal(span, root, c_hub, kind="grouping", tex=r"c", color=FAM_Q, ew=0.35, cw=0.3)
        link_then_reveal(
            span, root, d_hub, kind="grouping", tex=r"d", color=FAM_D,
            narration="Decorator category d: wrap one inner predicate.",
        )
        self._play_g(span, g, ctx)

        self._fade_scene()
        stage = Stage()
        sctx = SceneContext()
        register_stage(sctx, stage)
        ax = TickerSpan()
        o = Vec(-3.2, -1.6)
        cx = directed_segment(o, o + Vec(4.5, 0), stroke_color=QUERY_B, stroke_width=2.8)
        dy = directed_segment(o + Vec(2.2, 0), o + Vec(2.2, 2.2), stroke_color=DECORATOR, stroke_width=2.8)
        ax.pause(
            wait=MIN_WAIT,
            narration=(
                "c gives grouping geometry. d gives wrapper geometry. "
                "They are orthogonal — independent ranks. "
                "Direction is only our drawing choice."
            ),
        )
        ax.add(Place(cx, item_id="cx"), wait=MIN_WAIT, narration="Composite axis: and or or.")
        ax.add(Place(note("c", color=QUERY_B, size=22), at=Vec(-0.6, -2.0), item_id="cxl"), wait=0.3)
        ax.add(Place(dy, item_id="dy"), wait=MIN_WAIT, narration="Decorator axis: not wraps one Q.")
        ax.add(Place(note("d", color=DECORATOR, size=22), at=Vec(2.55, 0.5), item_id="dyl"), wait=MIN_WAIT)
        ax.pause(wait=MIN_WAIT, narration="Orthogonal axes over one binder Q.")
        self._play_s(ax, stage, sctx)

    # ------------------------------------------------------------------
    def _act_decorator_views(self) -> None:
        """Brief note: n as radial ring or vertical stack — layout only."""
        stage = Stage()
        ctx = SceneContext()
        register_stage(ctx, stage)
        span = TickerSpan()
        ring = not_ring(FAM_D)

        span.pause(
            wait=MIN_WAIT,
            narration="Category d wraps one inner Q — same structure, many layouts.",
        )
        span.add(
            Place(note("radial", color=FAM_D, size=18), at=Vec(-2.8, 1.45), item_id="lbl"),
            Place(binder(FAM_Q), at=Vec(-2.8, 0.0), item_id="core"),
            Place(math(r"e", color=FAM_Q, size=28), at=Vec(-2.8, 0.0), item_id="core_l"),
            wait=MIN_WAIT * 0.7,
        )
        span.add(Place(ring, at=Vec(-2.8, 0.0), item_id="nr"), wait=MIN_WAIT * 0.6,
                 narration="Radial: n as a ring around the inner predicate.")

        px = 2.6
        e1 = plain_segment(Vec(px, 0.45), Vec(px, -0.35), stroke_color=FAM_D, stroke_width=2.5)
        span.add(
            Place(note("vertical stack", color=FAM_D, size=18), at=Vec(px, 1.45), item_id="plbl"),
            wait=MIN_WAIT * 0.5,
            narration="Or stacked — radial, vertical, horizontal: direction is just notation.",
        )
        span.add(
            Place(note("n", color=FAM_D, size=22), at=Vec(px + 0.55, 0.45), item_id="pn"),
            Place(e1, item_id="pe1"), wait=0.18,
        )
        span.add(
            Place(binder(FAM_Q), at=Vec(px, -0.35), item_id="pt"),
            Place(math(r"e", color=FAM_Q, size=22), at=Vec(px, -0.85), item_id="ptl"),
            wait=MIN_WAIT * 0.6,
        )
        span.pause(wait=MIN_WAIT * 0.7, narration="Layout only — the nesting stays n of Q.")
        self._play_s(span, stage, ctx)

    # ------------------------------------------------------------------
    def _act_query_axis(self) -> None:
        self._act_query_tree()
        self._fade_scene()
        self._act_chi_matrix()

    def _act_query_tree(self) -> None:
        """Classification tree — squares for categories, circles for concretes."""

        Q_P = Vec(0.0, 3.15)
        L_P = Vec(-3.8, 1.95)
        C_P = Vec(0.0, 1.95)
        D_P = Vec(3.8, 1.95)
        E_P = Vec(-5.0, 0.75)
        G_P = Vec(-3.8, 0.75)
        H_P = Vec(-2.6, 0.75)
        A_P = Vec(-0.65, 0.75)
        O_P = Vec(0.65, 0.75)
        N_P = Vec(3.8, 0.75)

        g = Graph()
        stage = Stage()
        root = g.add_node(Q_P, binder(QUERY_B), label=math(r"Q", color=QUERY_B, size=36))
        ell = add_staged(g, L_P, "grouping", r"\ell", FAM_Q)
        c = add_staged(g, C_P, "grouping", r"c", FAM_Q)
        d = add_staged(g, D_P, "grouping", r"d", FAM_D)
        e = add_staged(g, E_P, "concrete", r"e", FAM_Q)
        g_leaf = add_staged(g, G_P, "concrete", r"g", FAM_Q)
        h = add_staged(g, H_P, "concrete", r"h", FAM_Q)
        a = add_staged(g, A_P, "concrete", r"a", FAM_Q)
        o = add_staged(g, O_P, "concrete", r"o", FAM_Q)
        n = add_staged(g, N_P, "concrete", r"n", FAM_D)

        ctx = SceneContext()
        register_graph(ctx, g)
        register_stage(ctx, stage)
        span = TickerSpan()

        span.pause(
            wait=MIN_WAIT,
            narration="The binder Q has a classification tree — categories, then concretes.",
        )
        span.add(
            Place(note("□ category   ○ concrete", color=MUTED, size=17), at=Vec(4.3, 2.75), item_id="key"),
            wait=MIN_WAIT * 0.5,
        )
        span.add(PatchNodeStyle(root.id, emphasis(QUERY_B)), wait=MIN_WAIT,
                  narration="Three categories under Q — leaf, composite, and decorator.")

        link_then_reveal(span, root, ell, kind="grouping", tex=r"\ell", color=FAM_Q, ew=0.34, cw=0.3,
                         narration="ℓ — leaf predicates: atomic tests.")
        link_then_reveal(span, root, c, kind="grouping", tex=r"c", color=FAM_Q, ew=0.34, cw=0.3,
                         narration="c — composite grouping: and and or.")
        link_then_reveal(span, root, d, kind="grouping", tex=r"d", color=FAM_D, ew=0.34, cw=0.3,
                         narration="d — decorator wrapping: not.")

        link_then_reveal(span, ell, e, kind="concrete", tex=r"e", color=FAM_Q, ew=0.28, cw=0.24,
                         narration="e equality, g greater-than, h contains.")
        link_then_reveal(span, ell, g_leaf, kind="concrete", tex=r"g", color=FAM_Q, ew=0.26, cw=0.22)
        link_then_reveal(span, ell, h, kind="concrete", tex=r"h", color=FAM_Q, ew=0.26, cw=0.22)

        link_then_reveal(span, c, a, kind="concrete", tex=r"a", color=FAM_Q, ew=0.28, cw=0.24,
                         narration="a for and, o for or — each holds many Q.")
        link_then_reveal(span, c, o, kind="concrete", tex=r"o", color=FAM_Q, ew=0.26, cw=0.22)

        link_then_reveal(span, d, n, kind="concrete", tex=r"n", color=FAM_D, ew=0.28, cw=0.24,
                         narration="n negates exactly one inner predicate.")

        for asset, pos, item_id in legend_panel(
            grouping="categories (□):  ℓ, c, d",
            concrete="concretes (○):  e, g, h, a, o, n",
        ):
            span.add(Place(asset, at=pos, item_id=item_id), wait=0.12)

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "Categories are grouping unions in the grammar. "
                "Concretes are the operators we actually pick."
            ),
        )

        ring_positions = [Q_P, L_P, C_P, D_P, E_P, G_P, H_P, A_P, O_P, N_P]
        for i, pos in enumerate(ring_positions):
            span.add(Place(contract_ring(QUERY_B), at=pos, item_id=f"ring{i}"), wait=0.07,
                      narration=(
                          "Every node — category or concrete — still satisfies q colon Q."
                          if i == 0 else None
                      ))

        self._play_gs(span, ctx)

    def _act_chi_matrix(self) -> None:
        """Concrete query χ — tree shape with parallel category paths."""

        AX = -1.8
        FX = 3.0
        Y = {
            "a": 2.85,
            "e1": 1.85,
            "n": 1.85,
            "o": 1.85,
            "e2": 0.75,
            "e3": 0.75,
            "g1": 0.75,
        }

        g = Graph()
        stage = Stage()
        a_root = g.add_node(Vec(AX, Y["a"]), binder(QUERY_B), label=math(r"a", color=QUERY_B, size=30))
        e_status = add_staged(g, Vec(AX - 1.5, Y["e1"]), "concrete", r"e", FAM_Q)
        n_wrap = add_staged(g, Vec(AX, Y["n"]), "concrete", r"n", FAM_D)
        o_grp = add_staged(g, Vec(AX + 1.5, Y["o"]), "concrete", r"o", FAM_Q)
        e_arch = add_staged(g, Vec(AX, Y["e2"]), "concrete", r"e", FAM_Q)
        e_prio = add_staged(g, Vec(AX + 1.0, Y["e3"]), "concrete", r"e", FAM_Q)
        g_score = add_staged(g, Vec(AX + 2.0, Y["g1"]), "concrete", r"g", FAM_Q)

        ctx = SceneContext()
        register_graph(ctx, g)
        register_stage(ctx, stage)
        span = TickerSpan()

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "One concrete query — shape on the left, "
                "category path on the right. Every step still binds to Q."
            ),
        )
        span.add(
            Place(note("shape", color=MUTED, size=18), at=Vec(AX, 3.45), item_id="hsh"),
            Place(note("category path", color=MUTED, size=18), at=Vec(FX - 0.35, 3.45), item_id="hfam"),
            wait=MIN_WAIT * 0.6,
        )
        span.add(
            Place(math(r"Q \to c", color=FAM_Q, size=19), at=Vec(FX, Y["a"]), item_id="f0"),
            wait=MIN_WAIT * 0.4,
        )
        span.add(PatchNodeStyle(a_root.id, emphasis(QUERY_B)), wait=MIN_WAIT,
                  narration="Chi: and of three branches — test, negation, and grouped alternative.")

        link_then_reveal(span, a_root, e_status, kind="concrete", tex=r"e", color=FAM_Q, ew=0.28, cw=0.22)
        span.add(
            Place(math(r"Q \to \ell", color=FAM_Q, size=19), at=Vec(FX, Y["e1"]), item_id="f1"),
            wait=MIN_WAIT * 0.7,
            narration="Status equals open — a leaf predicate in category ℓ.",
        )

        link_then_reveal(span, a_root, n_wrap, kind="concrete", tex=r"n", color=FAM_D, ew=0.28, cw=0.22)
        span.add(
            Place(math(r"Q \to d", color=FAM_D, size=19), at=Vec(FX, Y["n"]), item_id="f2"),
            wait=MIN_WAIT * 0.6,
            narration="Not archived — decorator category d.",
        )
        link_then_reveal(span, n_wrap, e_arch, kind="concrete", tex=r"e", color=FAM_Q, ew=0.26, cw=0.2)
        span.add(
            Place(math(r"Q \to \ell", color=FAM_Q, size=19), at=Vec(FX, Y["e2"]), item_id="f3"),
            wait=MIN_WAIT * 0.6,
        )

        link_then_reveal(span, a_root, o_grp, kind="concrete", tex=r"o", color=FAM_Q, ew=0.28, cw=0.22)
        span.add(
            Place(math(r"Q \to c", color=FAM_Q, size=19), at=Vec(FX, Y["o"]), item_id="f4"),
            wait=MIN_WAIT,
            narration="Or branch — priority high, or score greater than ninety.",
        )
        link_then_reveal(span, o_grp, e_prio, kind="concrete", tex=r"e", color=FAM_Q, ew=0.24, cw=0.2)
        link_then_reveal(span, o_grp, g_score, kind="concrete", tex=r"g", color=FAM_Q, ew=0.24, cw=0.2)
        span.add(
            Place(math(r"Q \to \ell", color=FAM_Q, size=19), at=Vec(FX, Y["e3"]), item_id="f5"),
            wait=MIN_WAIT * 0.5,
        )
        span.add(
            Place(math(r"Q \to \ell", color=FAM_Q, size=19), at=Vec(FX, Y["g1"]), item_id="f6"),
            wait=MIN_WAIT * 0.4,
        )

        span.add(
            Place(math(r"\chi : Q", color="#FFFFFF", size=24), at=Vec(0.2, -1.85), item_id="eq"),
            Place(
                note(
                    r'e(status,"open")  ·  n{e(archived,true)}  ·  o[e(priority,"high"), g(score,90)]',
                    color=MUTED,
                    size=14,
                ),
                at=Vec(0.2, -2.45),
                item_id="detail",
            ),
            wait=MIN_WAIT,
            narration="The whole expression chi is still Q — one binder end to end.",
        )

        all_pos = [
            Vec(AX, Y["a"]), Vec(AX - 1.5, Y["e1"]), Vec(AX, Y["n"]),
            Vec(AX + 1.5, Y["o"]), Vec(AX, Y["e2"]),
            Vec(AX + 1.0, Y["e3"]), Vec(AX + 2.0, Y["g1"]),
        ]
        span.add(Place(contract_ring(QUERY_B, radius=2.1), at=Vec(AX + 0.25, 1.85), item_id="big"),
                 wait=MIN_WAIT,
                 narration=(
                     "Query Binder: same pattern as T — orthogonal categories, "
                     "one surface, every form q colon Q."
                 ))

        for j, pos in enumerate(all_pos):
            span.add(Place(contract_ring(QUERY_B), at=pos, item_id=f"mr{j}"), wait=0.05)

        self._play_gs(span, ctx)
