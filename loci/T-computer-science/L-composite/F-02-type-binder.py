"""F-02 · Type Binder — `T`, the binder specialized to a type universe.

Video for the L-composite lecture.

`T` is `C` specialized to types. Inside it, two orthogonal axes:
    type axis   t ::= l | c[T_1,...,T_n]   leaves {i,f,b,s} · composites {m,a}
    decorator   d ::= r | v                wrappers that stack: d{T}
Grammar:  T ::= t | d{T}.
The family unfolds as vertical decorator stacks (depth) across a horizontal
row of type-shapes (breadth) — all admitted by the one binder T.

Render:  python loci/render.py T-computer-science/L-composite/F-02-type-binder.py
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
    Transform,
    Write,
    DOWN,
    LEFT,
    RIGHT,
    UP,
    VGroup,
)

from loci import (  # noqa: E402
    Circle,
    FillStyle,
    Label,
    Rectangle,
    Vec,
    directed_segment,
    plain_segment,
    patch_circle_style,
    patch_rectangle_style,
)

import loci_theme as T  # noqa: E402


# ----------------------------------------------------------------------------- helpers
def node(center: Vec, radius: float, color: str, label: str, *, fill=0.18, fs=30):
    disc = Circle(radius=radius, style=patch_circle_style(
        stroke_color=color, stroke_width=3.2, fill=FillStyle(color, fill))).to_manim(center)
    text = Label.math(label, color=T.INK, font_size=fs, bold=True).to_manim(center)
    return {"disc": disc, "label": text, "group": VGroup(disc, text),
            "center": center, "radius": radius, "color": color}


def layer(center: Vec, w: float, h: float, color: str, label: str, *, fs=28):
    rect = Rectangle(width=w, height=h, style=patch_rectangle_style(
        stroke_color=color, stroke_width=3.2, fill=FillStyle(color, 0.18),
        corner_radius=0.12)).to_manim(center)
    text = Label.math(label, color=T.INK, font_size=fs, bold=True).to_manim(center)
    return VGroup(rect, text)


def edge(a: dict, b: dict, *, color: str = T.MUTED, width: float = 2.4, directed=True):
    start = Circle(radius=a["radius"]).boundary_toward(a["center"], b["center"])
    end = Circle(radius=b["radius"]).boundary_toward(b["center"], a["center"])
    seg = directed_segment if directed else plain_segment
    return seg(start, end, stroke_color=color, stroke_width=width).to_manim()


def header(text: str):
    return T.subtitle(text, size=32, color=T.INK).to_edge(UP, buff=0.6)


# color roles
BINDER = T.BINDER   # T
DECOR = T.CORAL     # r
VALID = T.PURPLE    # v
COMP = T.GOLD       # composites m, a
LEAF = T.GREEN      # leaves i, f, b, s


class TypeBinder(Scene):
    def construct(self):
        self.camera.background_color = T.BG
        self.intro()
        self.assignment()
        self.axes()
        self.vertical_stack()
        self.horizontal_composite()
        self.family()
        self.nesting()
        self.closing()

    def clear_all(self, run_time: float = 0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------------ 0 · title
    def intro(self):
        block = T.title_block("Type Binder", "C specialized to a type universe")
        self.play(FadeIn(block, shift=UP * 0.3), run_time=1.1)
        self.wait(1.2)
        self.play(FadeOut(block), run_time=0.7)

    # --------------------------------------------------- 1 · C  ⇒  T assignment
    def assignment(self):
        c = node(Vec(-3.2, 0.4), 0.55, T.MUTED, r"C", fill=0.12, fs=48)
        arrow = directed_segment(Vec(-2.4, 0.4), Vec(-1.1, 0.4),
                                 stroke_color=T.MUTED, stroke_width=2.6).to_manim()
        t = node(Vec(0.0, 0.4), 0.62, BINDER, r"T", fill=0.24, fs=56)
        xt = T.caption_math(r"X : T \;\;\Longleftrightarrow\;\; X \text{ is admitted by the binder}")

        self.play(GrowFromCenter(c["disc"]), FadeIn(c["label"]), run_time=0.6)
        self.play(Create(arrow), run_time=0.4)
        self.play(GrowFromCenter(t["disc"]), FadeIn(t["label"]), run_time=0.6)
        self.play(FadeIn(xt), run_time=0.5)
        self.wait(1.4)
        self.clear_all()

    # --------------------------------------------------------- 2 · two axes + grammar
    def axes(self):
        head = header("one binder T · two axes")
        type_line = MathTex(
            r"\text{type axis } t:\quad \{\,i,\;f,\;b,\;s\,\}\ \text{leaves}\quad "
            r"\{\,m,\;a\,\}\ \text{composites}", font_size=34, color=LEAF)
        dec_line = MathTex(
            r"\text{decorator axis } d:\quad \{\,r,\;v\,\}\ \text{wrappers}",
            font_size=34, color=DECOR)
        g1 = MathTex(r"T ::= t \;\mid\; d\{T\}", font_size=44, color=T.INK)
        g2 = MathTex(r"t ::= l \;\mid\; c[T_1,\dots,T_n]", font_size=44, color=T.INK)
        grammar = VGroup(g1, g2).arrange(DOWN, buff=0.4)
        block = VGroup(type_line, dec_line, grammar).arrange(DOWN, buff=0.75)
        block.move_to([0, -0.2, 0])

        self.play(FadeIn(head), run_time=0.4)
        self.play(Write(type_line), run_time=0.9)
        self.play(Write(dec_line), run_time=0.7)
        self.play(LaggedStart(Write(g1), Write(g2), lag_ratio=0.4), run_time=1.4)
        self.wait(1.6)
        self.clear_all()

    # ------------------------------------------- 3 · vertical stacking (decorator)
    def vertical_stack(self):
        head = header("vertical — decorators stack")
        cx = -1.4
        base = layer(Vec(cx, -1.15), 1.7, 0.6, LEAF, r"i", fs=32)
        mid = layer(Vec(cx, -0.4), 1.7, 0.6, VALID, r"v\{i\}", fs=26)
        top = layer(Vec(cx, 0.35), 1.7, 0.6, DECOR, r"r\{v\{i\}\}", fs=22)
        axis = directed_segment(Vec(cx + 1.55, -1.5), Vec(cx + 1.55, 0.85),
                                stroke_color=T.MUTED, stroke_width=2.4).to_manim()
        depth = T.subtitle("depth", size=24, color=T.MUTED).next_to(axis, RIGHT, buff=0.2)
        formula = T.caption_math(r"r\{v\{i\}\} : T", color=T.INK)

        self.play(FadeIn(head), run_time=0.4)
        self.play(GrowFromCenter(base), run_time=0.5)
        self.play(FadeIn(mid, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(top, shift=UP * 0.3), run_time=0.5)
        self.play(Create(axis), FadeIn(depth), run_time=0.5)
        self.play(Write(formula), run_time=0.7)
        self.wait(1.4)
        self.clear_all()

    # ------------------------------------------ 4 · horizontal composite (breadth)
    def horizontal_composite(self):
        head = header("horizontal — a composite holds many T")
        arr = node(Vec(0, 1.9), 0.5, COMP, r"a", fill=0.22, fs=40)
        kids = [
            node(Vec(-4.2, -0.4), 0.4, LEAF, r"i"),
            node(Vec(-1.4, -0.4), 0.46, VALID, r"r\{v\{f\}\}", fs=20),
            node(Vec(1.4, -0.4), 0.4, LEAF, r"b"),
            node(Vec(4.2, -0.4), 0.4, LEAF, r"s"),
        ]
        formula = T.caption_math(r"a[\,i,\; r\{v\{f\}\},\; b,\; s\,] : T", color=T.INK)

        self.play(FadeIn(head), GrowFromCenter(arr["disc"]), FadeIn(arr["label"]), run_time=0.7)
        self.play(LaggedStart(*[AnimationGroup(
            Create(edge(arr, k)), GrowFromCenter(k["disc"]), FadeIn(k["label"]))
            for k in kids], lag_ratio=0.25), run_time=1.9)
        self.play(Write(formula), run_time=0.8)
        self.wait(1.5)
        self.clear_all()

    # ------------------------------------------------ 5 · the family unfolds (money shot)
    def family(self):
        head = header("the family unfolds — stacks × breadth")
        cols = [("m", COMP), ("a", COMP), ("i", LEAF), ("f", LEAF), ("b", LEAF), ("s", LEAF)]
        xs = [-5.0, -3.0, -1.0, 1.0, 3.0, 5.0]
        y_T, y_r, y_v, y_b = 1.5, 0.55, -0.4, -1.35
        r = 0.27

        columns = []
        for (base_lbl, base_col), x in zip(cols, xs):
            nT = node(Vec(x, y_T), r, BINDER, r"T", fs=22)
            nr = node(Vec(x, y_r), r, DECOR, r"r", fs=22)
            nv = node(Vec(x, y_v), r, VALID, r"v", fs=22)
            nb = node(Vec(x, y_b), r, base_col, base_lbl, fs=24)
            e1, e2, e3 = edge(nT, nr), edge(nr, nv), edge(nv, nb)
            columns.append((nT, nr, nv, nb, e1, e2, e3))

        cap = T.caption("vertical stacks (T → r → v → base) across the whole type family")

        self.play(FadeIn(head), run_time=0.4)
        builds = []
        for (nT, nr, nv, nb, e1, e2, e3) in columns:
            builds.append(AnimationGroup(
                GrowFromCenter(nT["disc"]), FadeIn(nT["label"]),
                Create(e1), GrowFromCenter(nr["disc"]), FadeIn(nr["label"]),
                Create(e2), GrowFromCenter(nv["disc"]), FadeIn(nv["label"]),
                Create(e3), GrowFromCenter(nb["disc"]), FadeIn(nb["label"]),
                lag_ratio=0.12))
        self.play(LaggedStart(*builds, lag_ratio=0.35), run_time=3.6)
        self.play(FadeIn(cap), run_time=0.5)
        self.wait(1.8)
        self.clear_all()

    # ------------------------------- 6 · recursion: composites wrap decorated T
    def nesting(self):
        head = header("composites wrap decorated T — recursively")

        # a composite base `a`, itself wrapped by a decorator stack (v, r, T)
        a = node(Vec(0, -0.1), 0.36, COMP, r"a", fs=30)
        v = node(Vec(0, 0.8), 0.30, VALID, r"v", fs=24)
        r = node(Vec(0, 1.68), 0.30, DECOR, r"r", fs=24)
        tT = node(Vec(0, 2.55), 0.30, BINDER, r"T", fs=24)
        stack = [(v, edge(v, a)), (r, edge(r, v)), (tT, edge(tT, r))]
        note = MathTex(r"r\{v\{a\}\} : T", font_size=34, color=T.MUTED).move_to([3.9, 2.1, 0])
        tag = T.subtitle("decorated composite", size=22, color=T.MUTED).move_to([-3.8, 2.1, 0])

        # children of the composite: each is a full T hanging below
        lx = [-3.9, -1.3, 1.3, 3.9]
        llab = [r"i", r"f", r"s", r"b"]
        leaves = [node(Vec(x, -1.6), 0.36, LEAF, lab) for x, lab in zip(lx, llab)]
        e_leaves = [edge(a, k) for k in leaves]

        self.play(FadeIn(head), run_time=0.4)
        self.play(GrowFromCenter(a["disc"]), FadeIn(a["label"]), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(
            Create(e), GrowFromCenter(n["disc"]), FadeIn(n["label"]))
            for n, e in stack], lag_ratio=0.3), run_time=1.4)
        self.play(FadeIn(note), FadeIn(tag), run_time=0.5)
        self.play(LaggedStart(*[AnimationGroup(
            Create(e), GrowFromCenter(k["disc"]), FadeIn(k["label"]))
            for e, k in zip(e_leaves, leaves)], lag_ratio=0.2), run_time=1.7)
        self.wait(0.9)

        # recursion: decorate one leaf, and expand another into a nested composite
        head2 = header("any child T may be decorated — or another composite")
        f = leaves[1]
        ring = Circle(radius=0.56, style=patch_circle_style(
            stroke_color=VALID, stroke_width=3.0, fill=FillStyle(VALID, 0.08))
        ).to_manim(f["center"])
        vlab = Label.math(r"v", color=VALID, font_size=22, bold=True).to_manim(
            f["center"] + Vec(0, 0.82))

        s = leaves[2]
        m = node(s["center"], 0.36, COMP, r"m")
        gc = [node(Vec(0.4, -3.05), 0.30, LEAF, r"i"),
              node(Vec(2.2, -3.05), 0.30, LEAF, r"f")]
        e_gc = [edge(m, g) for g in gc]

        self.play(Transform(head, head2), run_time=0.6)
        self.play(Create(ring), FadeIn(vlab), run_time=0.6)
        self.play(FadeOut(s["group"]), FadeIn(m["group"]), run_time=0.6)
        self.play(LaggedStart(*[AnimationGroup(
            Create(e), GrowFromCenter(g["disc"]), FadeIn(g["label"]))
            for e, g in zip(e_gc, gc)], lag_ratio=0.2), run_time=1.2)
        self.wait(1.9)
        self.clear_all()

    # ------------------------------------------------------------------ 7 · closing
    def closing(self):
        g1 = T.caption_math(r"T ::= t \;\mid\; d\{T\}", color=T.INK, size=46)
        g2 = T.caption_math(r"t ::= l \;\mid\; c[T_1,\dots,T_n]", color=T.INK, size=46)
        grammar = VGroup(g1, g2).arrange(DOWN, buff=0.45).shift(UP * 0.5)
        tag = T.caption_math(r"\text{one binder} \;\Rightarrow\; \text{two orthogonal axes}",
                             color=T.MUTED, size=34).next_to(grammar, DOWN, buff=0.8)
        self.play(LaggedStart(Write(g1), Write(g2), lag_ratio=0.4), run_time=1.6)
        self.play(FadeIn(tag), run_time=0.6)
        self.wait(1.8)
        self.play(FadeOut(grammar), FadeOut(tag), run_time=0.9)
