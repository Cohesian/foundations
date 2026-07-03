"""F-03 · Query Binder — `Q`, the binder specialized to a predicate universe.

Video for the L-composite lecture.

`Q` is `C` specialized to queries. The SAME two axes reappear:
    tests (leaves)   l in {e, g, h}    equals · greater · has
    composites       c in {a, o}       and · or           (breadth)
    decorator        d = n             not                (depth)
Grammar:  q ::= l | n{q} | c[q_1,...,q_n].
Worked query:
    chi = a[ e(status,"open"), n{e(archived)}, o[ e(priority), g(score) ] ] : Q

Render:  python loci/render.py T-computer-science/L-composite/F-03-query-binder.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (  # noqa: E402
    AnimationGroup,
    Create,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    MathTex,
    Scene,
    Write,
    DOWN,
    UP,
    VGroup,
)

from loci import (  # noqa: E402
    Circle,
    FillStyle,
    Label,
    Vec,
    directed_segment,
    plain_segment,
    patch_circle_style,
)

import loci_theme as T  # noqa: E402


# ----------------------------------------------------------------------------- helpers
def node(center: Vec, radius: float, color: str, label: str, *, fill=0.18, fs=30):
    disc = Circle(radius=radius, style=patch_circle_style(
        stroke_color=color, stroke_width=3.2, fill=FillStyle(color, fill))).to_manim(center)
    text = Label.math(label, color=T.INK, font_size=fs, bold=True).to_manim(center)
    return {"disc": disc, "label": text, "group": VGroup(disc, text),
            "center": center, "radius": radius, "color": color}


def edge(a: dict, b: dict, *, color: str = T.MUTED, width: float = 2.4, directed=True):
    start = Circle(radius=a["radius"]).boundary_toward(a["center"], b["center"])
    end = Circle(radius=b["radius"]).boundary_toward(b["center"], a["center"])
    seg = directed_segment if directed else plain_segment
    return seg(start, end, stroke_color=color, stroke_width=width).to_manim()


def header(text: str):
    return T.subtitle(text, size=32, color=T.INK).to_edge(UP, buff=0.6)


def sublabel(text: str, at: Vec):
    return T.subtitle(text, size=18, color=T.MUTED).move_to(at.to_manim())


# color roles
BINDER = T.BINDER   # Q
COMP = T.GOLD       # composites a, o
DECOR = T.CORAL     # decorator n
LEAF = T.GREEN      # tests e, g, h


class QueryBinder(Scene):
    def construct(self):
        self.camera.background_color = T.BG
        self.intro()
        self.assignment()
        self.symbols()
        self.worked_query()
        self.closing()

    def clear_all(self, run_time: float = 0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------------ 0 · title
    def intro(self):
        block = T.title_block("Query Binder", "C specialized to a predicate universe")
        self.play(FadeIn(block, shift=UP * 0.3), run_time=1.1)
        self.wait(1.2)
        self.play(FadeOut(block), run_time=0.7)

    # --------------------------------------------------- 1 · C  ⇒  Q assignment
    def assignment(self):
        c = node(Vec(-3.2, 0.4), 0.55, T.MUTED, r"C", fill=0.12, fs=48)
        arrow = directed_segment(Vec(-2.4, 0.4), Vec(-1.1, 0.4),
                                 stroke_color=T.MUTED, stroke_width=2.6).to_manim()
        q = node(Vec(0.0, 0.4), 0.62, BINDER, r"Q", fill=0.24, fs=56)
        qt = T.caption_math(r"q : Q \;\;\Longleftrightarrow\;\; q \text{ is a valid predicate form}")

        self.play(GrowFromCenter(c["disc"]), FadeIn(c["label"]), run_time=0.6)
        self.play(Create(arrow), run_time=0.4)
        self.play(GrowFromCenter(q["disc"]), FadeIn(q["label"]), run_time=0.6)
        self.play(FadeIn(qt), run_time=0.5)
        self.wait(1.4)
        self.clear_all()

    # ------------------------------------------------------- 2 · symbols + grammar
    def symbols(self):
        head = header("one binder Q · the same two axes")
        tests = MathTex(
            r"\text{tests } \ell \in \{\,e,\;g,\;h\,\}\ :\ "
            r"\text{equals}\,\cdot\,\text{greater}\,\cdot\,\text{has}",
            font_size=34, color=LEAF)
        comps = MathTex(
            r"\text{composites } c \in \{\,a,\;o\,\}\ :\ \text{and}\,\cdot\,\text{or}",
            font_size=34, color=COMP)
        deco = MathTex(
            r"\text{decorator } d = n\ :\ \text{not}", font_size=34, color=DECOR)
        grammar = MathTex(
            r"q ::= \ell \;\mid\; n\{q\} \;\mid\; c[\,q_1,\dots,q_n\,]",
            font_size=44, color=T.INK)
        block = VGroup(tests, comps, deco, grammar).arrange(DOWN, buff=0.6)
        block.move_to([0, -0.2, 0])

        self.play(FadeIn(head), run_time=0.4)
        self.play(Write(tests), run_time=0.7)
        self.play(Write(comps), run_time=0.6)
        self.play(Write(deco), run_time=0.5)
        self.play(Write(grammar), run_time=0.9)
        self.wait(1.7)
        self.clear_all()

    # ------------------------------------------------ 3 · the worked query (money shot)
    def worked_query(self):
        head = header("one query — and/or grow breadth · not stacks depth")
        q = node(Vec(0, 2.55), 0.30, BINDER, r"Q", fs=24)
        a = node(Vec(0, 1.45), 0.34, COMP, r"a", fs=30)
        e1 = node(Vec(-4.3, 0.15), 0.30, LEAF, r"e", fs=26)
        n = node(Vec(-0.3, 0.15), 0.30, DECOR, r"n", fs=26)
        o = node(Vec(3.8, 0.15), 0.34, COMP, r"o", fs=30)
        e2 = node(Vec(-0.3, -1.45), 0.30, LEAF, r"e", fs=26)
        e3 = node(Vec(2.6, -1.45), 0.30, LEAF, r"e", fs=26)
        g = node(Vec(5.0, -1.45), 0.30, LEAF, r"g", fs=26)

        subs = VGroup(
            sublabel("status = open", Vec(-4.3, -0.4)),
            sublabel("archived", Vec(-0.3, -2.0)),
            sublabel("priority", Vec(2.6, -2.0)),
            sublabel("score > 90", Vec(5.0, -2.0)),
        )

        self.play(FadeIn(head), run_time=0.4)
        self.play(GrowFromCenter(q["disc"]), FadeIn(q["label"]), run_time=0.5)
        self.play(Create(edge(q, a)), GrowFromCenter(a["disc"]), FadeIn(a["label"]),
                  run_time=0.6)
        # a's three children (breadth)
        self.play(LaggedStart(*[AnimationGroup(
            Create(edge(a, ch)), GrowFromCenter(ch["disc"]), FadeIn(ch["label"]))
            for ch in (e1, n, o)], lag_ratio=0.25), run_time=1.6)
        # not wraps a test (depth)
        self.play(Create(edge(n, e2)), GrowFromCenter(e2["disc"]), FadeIn(e2["label"]),
                  run_time=0.6)
        # or fans to two tests (breadth)
        self.play(LaggedStart(*[AnimationGroup(
            Create(edge(o, ch)), GrowFromCenter(ch["disc"]), FadeIn(ch["label"]))
            for ch in (e3, g)], lag_ratio=0.25), run_time=1.1)
        self.play(FadeIn(subs), run_time=0.6)

        chi = T.caption_math(
            r"\chi = a[\,e(\text{status}),\; n\{e(\text{archived})\},\; "
            r"o[\,e(\text{priority}),\,g(\text{score})\,]\,] : Q", color=T.INK, size=34)
        chi.scale_to_fit_width(12.2).to_edge(DOWN, buff=0.4)
        self.play(Write(chi), run_time=1.1)
        self.wait(1.9)
        self.clear_all()

    # ------------------------------------------------------------------ 4 · closing
    def closing(self):
        c = node(Vec(0, 1.95), 0.62, T.BINDER, r"C", fill=0.24, fs=54)
        t = node(Vec(-3.7, -1.7), 0.52, T.GREEN, r"T", fill=0.20, fs=44)
        q = node(Vec(0.0, -1.7), 0.52, T.PURPLE, r"Q", fill=0.20, fs=44)
        k = node(Vec(3.7, -1.7), 0.52, T.GOLD, r"K", fill=0.20, fs=44)
        e_t, e_q = edge(c, t), edge(c, q)
        e_k = edge(c, k, color="#4A515C")
        cap = T.caption("one surface, many domains — types · queries · corpus (next: TLF)")

        self.play(GrowFromCenter(c["disc"]), FadeIn(c["label"]), run_time=0.6)
        self.play(
            AnimationGroup(Create(e_t), GrowFromCenter(t["disc"]), FadeIn(t["label"])),
            AnimationGroup(Create(e_q), GrowFromCenter(q["disc"]), FadeIn(q["label"])),
            run_time=1.0)
        self.play(Create(e_k), GrowFromCenter(k["disc"]), FadeIn(k["label"]), run_time=0.7)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(1.9)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=0.9)
