"""TLF Composite — corpus shape from E_g, traversal overlays E_l and E_r."""

from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))

from manim import FadeOut, Group

from loci import (
    Graph,
    PatchNodeStyle,
    Place,
    Stage,
    Vec,
    register_graph,
    register_stage,
)
from loci.ticker import SceneContext, TickerSpan
from loci.voiceover import LociVoiceoverScene, VoiceoverTickerPlayer

from _visuals import (
    BINDER,
    FAM_K_C,
    FAM_K_L,
    FILE,
    K_CORPUS,
    LECTURE,
    LINEAR,
    MUTED,
    RELATED,
    TOPIC,
    WAIT,
    add_staged,
    arc_edge,
    binder,
    contract_ring,
    dotted_directed_edge,
    emphasis,
    grow_down,
    link_then_reveal,
    math,
    note,
)

MIN_WAIT = WAIT
EG = MUTED
TRAVEL_W = 1.35
TAG = Vec(0.46, -0.02)

# Left-to-right file reading order (one possible E_l path)
FILE_CHAIN = ("f_axioms", "f_groups", "f_induction", "f_map")

NODE_TAGS = {
    "t_math": "math",
    "l_found": "found.",
    "f_axioms": "axioms",
    "t_alg": "algebra",
    "l_proofs": "proofs",
    "l_groups": "groups",
    "f_groups": "groups",
    "f_induction": "induction",
    "f_map": "map",
}


class TLFComposite(LociVoiceoverScene):
    def construct(self):
        self.setup_voiceover()
        self._act_corpus()
        self._fade_scene()
        self._act_categories()
        self._fade_scene()
        self._act_tmath_tree()
        self._act_overlays()
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
    def _act_corpus(self) -> None:
        stage = Stage()
        ctx = SceneContext()
        register_stage(ctx, stage)
        span = TickerSpan()

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "TLF Composite. Topic, Lecture, File — "
                "a labeled composite pattern for distributing knowledge through a corpus."
            ),
        )
        span.add(
            Place(binder(K_CORPUS), at=Vec(0, 1.4), item_id="k"),
            Place(math(r"K", color=K_CORPUS, size=34), at=Vec(0, 1.4), item_id="kl"),
            wait=MIN_WAIT,
            narration="So the full graph has vertices V, a kind label kappa, and three edge families.",
        )
        span.add(
            Place(math(r"E_g", color=EG, size=22), at=Vec(-2.6, -0.2), item_id="eg"),
            Place(math(r"E_l", color=LINEAR, size=22), at=Vec(0.0, -0.2), item_id="el"),
            Place(math(r"E_r", color=RELATED, size=22), at=Vec(2.6, -0.2), item_id="er"),
            wait=MIN_WAIT,
            narration="Grouping, linear reading, and related edges — three orthogonal roles.",
        )
        span.add(
            Place(
                math(r"shape(K)=(V,E_g)", color="#FFFFFF", size=20),
                at=Vec(0, -1.35),
                item_id="shape",
            ),
            wait=MIN_WAIT,
            narration="Only grouping defines shape — linear and related are traversal overlays.",
        )
        self._play_s(span, stage, ctx)

    # ------------------------------------------------------------------
    def _act_categories(self) -> None:
        """Two categories only — c composite, l leaf. No decorators."""

        g = Graph()
        root = g.add_node(Vec(0, 2.2), binder(K_CORPUS), label=math(r"K", color=K_CORPUS, size=32))
        c = add_staged(g, Vec(-1.8, 0.9), "cat_c", r"c", FAM_K_C)
        l_cat = add_staged(g, Vec(1.8, 0.9), "cat_l", r"l", FAM_K_L)
        t = add_staged(g, Vec(-2.8, -0.5), "tlf", r"T", TOPIC)
        lec = add_staged(g, Vec(-0.8, -0.5), "tlf", r"L", LECTURE)
        f = add_staged(g, Vec(1.8, -0.5), "tlf", r"F", FILE)

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()

        span.pause(
            wait=MIN_WAIT,
            narration="Under K, there are only two categories — composite and leaf. No decorators.",
        )
        span.add(PatchNodeStyle(root.id, emphasis(K_CORPUS)), wait=MIN_WAIT,
                  narration="Composite category c, and leaf category l.")
        link_then_reveal(span, root, c, kind="cat_c", tex=r"c", color=FAM_K_C, ew=0.32, cw=0.28,
                         narration="Squares are categories; circles are the concrete kappa labels.")
        link_then_reveal(span, root, l_cat, kind="cat_l", tex=r"l", color=FAM_K_L, ew=0.32, cw=0.28)

        link_then_reveal(span, c, t, kind="tlf", tex=r"T", color=TOPIC, ew=0.28, cw=0.24,
                         narration="Under c, the concrete composites T and L.")
        link_then_reveal(span, c, lec, kind="tlf", tex=r"L", color=LECTURE, ew=0.26, cw=0.22)
        link_then_reveal(span, l_cat, f, kind="tlf", tex=r"F", color=FILE, ew=0.28, cw=0.24,
                         narration="Under l, the concrete leaf F — files carry the readable content.")

        span.pause(
            wait=MIN_WAIT,
            narration=(
                "In grammar: K is F, or composite c of many K. "
                "Topics and lectures are composites; files are leaves — and grouping stays flexible."
            ),
        )
        self._play_g(span, g, ctx)

    # ------------------------------------------------------------------
    def _act_tmath_tree(self) -> None:
        """Paper example — κ labels as circles, E_g defines the DAG shape."""

        g = Graph()
        pos = {
            "t_math": Vec(0, 2.3),
            "l_found": Vec(-1.2, 1.0),
            "f_map": Vec(2.2, 1.0),
            "f_axioms": Vec(-2.8, -0.15),
            "t_alg": Vec(-0.8, -0.15),
            "l_proofs": Vec(0.6, -0.15),
            "l_groups": Vec(-0.8, -1.35),
            "f_groups": Vec(-0.8, -2.45),
            "f_induction": Vec(0.6, -1.35),
        }
        meta = {
            "t_math": ("tlf", r"T", TOPIC),
            "l_found": ("tlf", r"L", LECTURE),
            "f_map": ("tlf", r"F", FILE),
            "f_axioms": ("tlf", r"F", FILE),
            "t_alg": ("tlf", r"T", TOPIC),
            "l_proofs": ("tlf", r"L", LECTURE),
            "l_groups": ("tlf", r"L", LECTURE),
            "f_groups": ("tlf", r"F", FILE),
            "f_induction": ("tlf", r"F", FILE),
        }
        nodes = {
            "t_math": add_staged(g, pos["t_math"], "tlf", r"T", TOPIC, visible=True),
        }
        for key, p in pos.items():
            if key == "t_math":
                continue
            kind, tex, color = meta[key]
            nodes[key] = add_staged(g, p, kind, tex, color)

        edges = [
            ("t_math", "l_found"),
            ("t_math", "f_map"),
            ("l_found", "f_axioms"),
            ("l_found", "t_alg"),
            ("l_found", "l_proofs"),
            ("t_alg", "l_groups"),
            ("l_groups", "f_groups"),
            ("l_proofs", "f_induction"),
        ]

        ctx = SceneContext()
        register_graph(ctx, g)
        span = TickerSpan()
        span.pause(
            wait=MIN_WAIT,
            narration="Here's a concrete corpus: T dot math — nested topics, lectures, and files under E g.",
        )
        grow_down(
            span, nodes, edges, "t_math", meta,
            narration="Solid edges are E g — the grouping projection gives us the DAG shape.",
            mid=4,
        )
        span.pause(wait=MIN_WAIT * 0.5)
        self._play_g(span, g, ctx)

        self._tree_pos = pos
        self._file_pos = {k: pos[k] for k in FILE_CHAIN}

    # ------------------------------------------------------------------
    def _act_overlays(self) -> None:
        """Thin dotted F-to-F traversal edges on the tree; name tags for context."""

        stage = Stage()
        ctx = SceneContext()
        register_stage(ctx, stage)
        span = TickerSpan()
        pos = self._tree_pos

        span.pause(
            wait=MIN_WAIT,
            narration="Now, traversal overlays are leaf-only — they never change the grouping shape.",
        )

        # Tiny name tags beside each node
        for key, tag in NODE_TAGS.items():
            span.add(
                Place(
                    note(tag, color=MUTED, size=11),
                    at=pos[key] + TAG,
                    item_id=f"tag_{key}",
                ),
                wait=0.05,
            )
        span.pause(
            wait=MIN_WAIT * 0.35,
            narration="Each node keeps its name — math, foundations, axioms, and so on.",
        )

        span.add(
            Place(math(r"E_l", color=LINEAR, size=16), at=Vec(-3.35, -0.55), item_id="llbl"),
            wait=MIN_WAIT * 0.3,
            narration="Linear edges trace a simple reading path — left to right across the files.",
        )

        # Direct dotted F → F → F → F (no detour lane)
        p = self._file_pos
        for i in range(len(FILE_CHAIN) - 1):
            src, tgt = FILE_CHAIN[i], FILE_CHAIN[i + 1]
            span.add(
                Place(
                    dotted_directed_edge(p[src], p[tgt], color=LINEAR, width=TRAVEL_W),
                    item_id=f"l{i}",
                ),
                wait=MIN_WAIT * 0.42,
                narration=(
                    "Axioms, groups, induction, map — one possible sequence, and E l can vary."
                    if i == len(FILE_CHAIN) - 2
                    else None
                ),
            )

        # E_r: last F → second F in the reading chain (map → groups)
        r_arc = arc_edge(
            p["f_map"],
            p["f_groups"],
            color=RELATED,
            width=TRAVEL_W,
            angle=2.1,
            dotted=True,
        )
        span.add(
            Place(math(r"E_r", color=RELATED, size=16), at=Vec(3.15, 1.55), item_id="rlbl"),
            Place(r_arc, item_id="r1"),
            wait=MIN_WAIT,
            narration="Related edges can jump anywhere — here, from the last file back to the second.",
        )

        span.add(
            Place(
                math(r"layout(V,E_g,E_l,E_r)=layout(V,E_g)", color="#FFFFFF", size=17),
                at=Vec(0, -3.15),
                item_id="law",
            ),
            wait=MIN_WAIT * 0.7,
            narration="Fixed-node law: add l or r edges and nodes stay put — only E g moves layout.",
        )

        span.add(
            Place(math(r"\pi_g \bot \pi_l, \pi_r", color="#FFFFFF", size=19), at=Vec(3.35, 2.55), item_id="pi"),
            wait=MIN_WAIT,
            narration="Projections are views of the same corpus — traversal can change while shape stays fixed.",
        )

        span.add(
            Place(math(r"C \Rightarrow K", color=BINDER, size=20), at=Vec(0, -3.65), item_id="ck"),
            wait=MIN_WAIT,
            narration=(
                "So TLF is C implies K. This repository is itself a TLF corpus: "
                "folders give E g, links give E l and E r."
            ),
        )

        for i, fp in enumerate(p.values()):
            span.add(Place(contract_ring(K_CORPUS), at=fp, item_id=f"fr{i}"), wait=0.04)

        self._play_s(span, stage, ctx)
