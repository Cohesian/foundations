"""F-04 · TLF Composite — `K`, a corpus as a labeled composite graph.

Video for the L-composite lecture (capstone).

TLF = Topic / Lecture / File. The corpus is
    G_K = (V, E_g ⊔ E_l ⊔ E_r, κ),  κ : V → {T, L, F}
where only grouping defines shape:  shape(K) = (V, E_g).
T and L are composites, F is a leaf:  K ::= F | c[K_1,...,K_n], c ∈ {T,L}.
E_l (linear reading) and E_r (related) are leaf-only overlays drawn on the
SAME fixed nodes — adding them never moves a node.

Render:  python loci/render.py T-computer-science/L-composite/F-04-TLF-composite.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (  # noqa: E402
    AnimationGroup,
    Create,
    DashedLine,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    Indicate,
    LaggedStart,
    MathTex,
    Scene,
    Transform,
    Write,
    DOWN,
    RIGHT,
    UP,
    VGroup,
)

from loci import (  # noqa: E402
    Circle,
    FillStyle,
    Label,
    Vec,
    plain_segment,
    patch_circle_style,
)

import loci_theme as T  # noqa: E402


# color roles
TOP = T.BINDER     # Topic   (composite)
LEC = T.PURPLE     # Lecture (composite)
FILE = T.GREEN     # File    (leaf)
LIN = T.GOLD       # E_l — linear reading overlay
REL = T.CORAL      # E_r — related overlay
GROUP = T.MUTED    # E_g — grouping (structure)


# ----------------------------------------------------------------------------- helpers
def kind_node(center: Vec, color: str, kind: str, name: str, r: float = 0.32):
    disc = Circle(radius=r, style=patch_circle_style(
        stroke_color=color, stroke_width=3.2, fill=FillStyle(color, 0.20))).to_manim(center)
    lab = Label.math(kind, color=T.INK, font_size=26, bold=True).to_manim(center)
    nm = T.subtitle(name, size=15, color=T.MUTED)
    nm.next_to(disc, DOWN, buff=0.05)
    return {"disc": disc, "group": VGroup(disc, lab, nm), "center": center, "radius": r}


def boundary(a: dict, b: dict):
    s = Circle(radius=a["radius"]).boundary_toward(a["center"], b["center"])
    e = Circle(radius=b["radius"]).boundary_toward(b["center"], a["center"])
    return s, e


def link(a: dict, b: dict):
    """Grouping edge E_g — a solid line (containment / structure)."""
    s, e = boundary(a, b)
    return plain_segment(s, e, stroke_color=GROUP, stroke_width=2.6).to_manim()


def flow(a: dict, b: dict, color: str):
    """Traversal overlay (E_l / E_r) — a dashed, directed line."""
    s, e = boundary(a, b)
    ln = DashedLine(s.to_manim(), e.to_manim(), color=color,
                    stroke_width=2.8, dash_length=0.13, dashed_ratio=0.55)
    ln.add_tip(tip_length=0.2)
    return ln


def header(text: str):
    return T.subtitle(text, size=32, color=T.INK).to_edge(UP, buff=0.55)


class TLFComposite(Scene):
    def construct(self):
        self.camera.background_color = T.BG
        self.intro()
        self.kinds()
        self.corpus()
        self.closing()

    def clear_all(self, run_time: float = 0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------------ 0 · title
    def intro(self):
        block = T.title_block("TLF Composite", "Topic · Lecture · File — a corpus as a graph")
        self.play(FadeIn(block, shift=UP * 0.3), run_time=1.1)
        self.wait(1.2)
        self.play(FadeOut(block), run_time=0.7)

    # ------------------------------------------------------------- 1 · node kinds
    def kinds(self):
        head = header("node kinds — Topic · Lecture · File")
        badges = []
        for x, color, kind, meaning in [
            (-4.2, TOP, "T", "topic"), (0.0, LEC, "L", "lecture"), (4.2, FILE, "F", "file")
        ]:
            disc = Circle(radius=0.55, style=patch_circle_style(
                stroke_color=color, stroke_width=3.5, fill=FillStyle(color, 0.22))
            ).to_manim(Vec(x, 1.3))
            lab = Label.math(kind, color=T.INK, font_size=48, bold=True).to_manim(Vec(x, 1.3))
            mean = T.subtitle(meaning, size=24, color=color).next_to(disc, DOWN, buff=0.2)
            badges.append(VGroup(disc, lab, mean))

        grammar = MathTex(r"K ::= F \;\mid\; c[\,K_1,\dots,K_n\,]\quad c\in\{T,L\}",
                          font_size=42, color=T.INK)
        note = MathTex(r"T,\,L:\ \text{composite (they contain)}\qquad F:\ \text{leaf (content)}",
                       font_size=30, color=T.MUTED)
        block = VGroup(grammar, note).arrange(DOWN, buff=0.5).move_to([0, -1.7, 0])

        self.play(FadeIn(head), run_time=0.4)
        self.play(LaggedStart(*[GrowFromCenter(b) for b in badges], lag_ratio=0.3), run_time=1.6)
        self.play(Write(grammar), run_time=0.9)
        self.play(FadeIn(note), run_time=0.6)
        self.wait(1.7)
        self.clear_all()

    # ---------------------------------- 2 · shape (E_g) + overlays (E_l,E_r) + projections
    def corpus(self):
        head = header("grouping edges  —  the shape")

        t0 = kind_node(Vec(0.0, 2.8), TOP, "T", "math")
        l0 = kind_node(Vec(-2.3, 1.5), LEC, "L", "foundations")
        f3 = kind_node(Vec(3.4, 1.5), FILE, "F", "map")
        f0 = kind_node(Vec(-5.4, 0.2), FILE, "F", "axioms")
        t1 = kind_node(Vec(-2.9, 0.2), TOP, "T", "algebra")
        l2 = kind_node(Vec(-0.5, 0.2), LEC, "L", "proofs")
        l1 = kind_node(Vec(-2.9, -1.1), LEC, "L", "groups")
        f2 = kind_node(Vec(-0.5, -1.1), FILE, "F", "induction")
        f1 = kind_node(Vec(-2.9, -2.4), FILE, "F", "groups")

        # child -> parent (grouping)
        pairs = [(l0, t0), (f3, t0), (f0, l0), (t1, l0), (l2, l0), (l1, t1), (f2, l2), (f1, l1)]
        g_edges = {id(ch): link(p, ch) for ch, p in pairs}
        grouping = VGroup(*g_edges.values())

        # --- reveal the grouping shape, parent before child
        self.play(FadeIn(head), run_time=0.4)
        self.play(GrowFromCenter(t0["group"]), run_time=0.5)
        steps = [AnimationGroup(Create(g_edges[id(ch)]), GrowFromCenter(ch["group"]), lag_ratio=0.25)
                 for ch, _ in pairs]
        self.play(LaggedStart(*steps, lag_ratio=0.3), run_time=3.4)
        self.wait(0.9)

        # --- traversal overlays on the SAME fixed nodes
        head2 = header("reading & related  —  overlays on the same fixed nodes")
        linear = VGroup(flow(f0, f2, LIN), flow(f2, f1, LIN))     # axioms → induction → groups
        related = VGroup(flow(f1, f0, REL))                        # groups → axioms
        lin_tag = T.subtitle("linear reading", size=20, color=LIN).to_edge(DOWN, buff=0.9).shift(RIGHT * 3.2)
        rel_tag = T.subtitle("related", size=20, color=REL).next_to(lin_tag, DOWN, buff=0.2)

        self.play(Transform(head, head2), run_time=0.6)
        self.play(LaggedStart(*[Create(e) for e in linear], lag_ratio=0.5),
                  FadeIn(lin_tag), run_time=1.5)
        self.play(Create(related[0]), FadeIn(rel_tag), run_time=0.9)
        self.wait(1.3)

        # --- projections: same corpus, three views
        head3 = header("one corpus  ·  three projections")
        plabels = VGroup(
            MathTex(r"\pi_g=(V,E_g)", font_size=30, color=GROUP),
            MathTex(r"\pi_l=(V_F,E_l)", font_size=30, color=LIN),
            MathTex(r"\pi_r=(V_F,E_r)", font_size=30, color=REL),
        ).arrange(RIGHT, buff=0.8).to_edge(DOWN, buff=0.35)

        self.play(Transform(head, head3), FadeOut(lin_tag), FadeOut(rel_tag), run_time=0.6)
        self.play(FadeIn(plabels[0]), run_time=0.4)
        self.play(Indicate(grouping, color=T.INK, scale_factor=1.06), run_time=1.0)
        self.play(FadeIn(plabels[1]), run_time=0.4)
        self.play(Indicate(linear, color=LIN, scale_factor=1.12), run_time=1.0)
        self.play(FadeIn(plabels[2]), run_time=0.4)
        self.play(Indicate(related, color=REL, scale_factor=1.12), run_time=1.0)
        self.wait(1.6)
        self.clear_all()

    # ------------------------------------------------------------------ 3 · closing
    def closing(self):
        l1 = MathTex(r"G_{\mathcal{K}} = (\,V,\; E_g \sqcup E_l \sqcup E_r,\; \kappa\,)",
                     font_size=46, color=T.INK)
        l2 = MathTex(r"\operatorname{shape}(\mathcal{K}) = (V,\,E_g)",
                     font_size=42, color=T.MUTED)
        l3 = MathTex(r"K ::= F \;\mid\; c[\,K_1,\dots,K_n\,]\quad c\in\{T,L\}",
                     font_size=40, color=T.INK)
        box = VGroup(l1, l2, l3).arrange(DOWN, buff=0.5).shift(UP * 0.4)
        tag = MathTex(r"C \;\Rightarrow\; K \qquad \text{the binder becomes a corpus}",
                      font_size=34, color=T.BINDER).next_to(box, DOWN, buff=0.7)

        self.play(Write(l1), run_time=1.1)
        self.play(FadeIn(l2), FadeIn(l3), run_time=0.9)
        self.play(FadeIn(tag), run_time=0.6)
        self.wait(2.0)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
