"""F-01 · Carbon Binder — the binder as a glue interface that scales.

Video for the L-composite lecture (abstract introduction).

Idea: a single bonding surface `C` admits many concretions through ONE
interface, and structure then scales along orthogonal axes —
    horizontal  = composite  (breadth: one contains many)
    vertical    = decorator  (depth:   wrappers stack around one)
    n-axes      = each domain adds its own independent directions
— while everything keeps returning to `C`.

Render:  python loci/render.py T-computer-science/L-composite/F-01-carbon-binder.py
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from manim import (  # noqa: E402
    AnimationGroup,
    Create,
    Dot,
    FadeIn,
    FadeOut,
    GrowFromCenter,
    LaggedStart,
    Scene,
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
def node(center: Vec, radius: float, color: str, label: str, *, fill=0.18, fs=34):
    disc = Circle(radius=radius, style=patch_circle_style(
        stroke_color=color, stroke_width=3.5, fill=FillStyle(color, fill))).to_manim(center)
    text = Label.math(label, color=T.INK, font_size=fs, bold=True).to_manim(center)
    return {"disc": disc, "label": text, "group": VGroup(disc, text),
            "center": center, "radius": radius, "color": color}


def layer(center: Vec, w: float, h: float, color: str, label: str, *, fs=30):
    rect = Rectangle(width=w, height=h, style=patch_rectangle_style(
        stroke_color=color, stroke_width=3.2, fill=FillStyle(color, 0.18),
        corner_radius=0.12)).to_manim(center)
    text = Label.math(label, color=T.INK, font_size=fs, bold=True).to_manim(center)
    return VGroup(rect, text)


def edge(a: dict, b: dict, *, color: str = T.MUTED, width: float = 2.6, directed=True):
    start = Circle(radius=a["radius"]).boundary_toward(a["center"], b["center"])
    end = Circle(radius=b["radius"]).boundary_toward(b["center"], a["center"])
    seg = directed_segment if directed else plain_segment
    return seg(start, end, stroke_color=color, stroke_width=width).to_manim()


def header(text: str):
    return T.subtitle(text, size=32, color=T.INK).to_edge(UP, buff=0.6)


class CarbonBinder(Scene):
    def construct(self):
        self.camera.background_color = T.BG
        self.intro()
        self.glue_interface()
        self.horizontal()
        self.vertical()
        self.n_axes()
        self.closure()
        self.closing()

    def clear_all(self, run_time: float = 0.55):
        if self.mobjects:
            self.play(*[FadeOut(m) for m in self.mobjects], run_time=run_time)

    # ------------------------------------------------------------------ 0 · title
    def intro(self):
        block = T.title_block("Carbon Binder", "one glue interface · many structures")
        self.play(FadeIn(block, shift=UP * 0.3), run_time=1.1)
        self.wait(1.3)
        self.play(FadeOut(block), run_time=0.7)

    # -------------------------------------------------- 1 · the glue interface C
    def glue_interface(self):
        head = header("a glue interface")
        c = node(Vec(0, 0.35), 0.62, T.BINDER, r"C", fill=0.22, fs=60)
        cap = T.caption("C — every interaction happens through one surface")
        self.play(FadeIn(head), GrowFromCenter(c["disc"]), FadeIn(c["label"]), run_time=0.9)
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(0.7)

        centers = [Vec(-3.0, 1.9), Vec(3.0, 1.9), Vec(-3.0, -1.2), Vec(3.0, -1.2)]
        colors = [T.GOLD, T.GREEN, T.PURPLE, T.CORAL]
        kids = [node(p, 0.44, col, rf"C_{i+1}")
                for i, (p, col) in enumerate(zip(centers, colors))]
        cap2 = T.caption("many concretions comply — x : C")
        self.play(FadeOut(cap), FadeIn(cap2), run_time=0.4)
        self.play(LaggedStart(*[AnimationGroup(
            Create(edge(c, k)), GrowFromCenter(k["disc"]), FadeIn(k["label"]), lag_ratio=0.25)
            for k in kids], lag_ratio=0.32), run_time=2.3)
        self.wait(1.2)
        self.clear_all()

    # ------------------------------------------------ 2 · horizontal = composite
    def horizontal(self):
        head = header("scale horizontally — composite")
        c = node(Vec(0, 1.95), 0.5, T.BINDER, r"C", fill=0.22, fs=42)
        xs = [-4.4, -2.2, 0.0, 2.2, 4.4]
        cols = [T.GOLD, T.GREEN, T.PURPLE, T.CORAL, T.GOLD]
        labels = [r"C_1", r"C_2", r"C_3", r"C_4", r"C_n"]
        kids = [node(Vec(x, -0.4), 0.36, col, lab)
                for x, col, lab in zip(xs, cols, labels)]
        formula = T.caption_math(r"\mathrm{Comp}(C_1,\dots,C_n) : C", color=T.INK)

        self.play(FadeIn(head), GrowFromCenter(c["disc"]), FadeIn(c["label"]), run_time=0.7)
        self.play(LaggedStart(*[AnimationGroup(
            Create(edge(c, k)), GrowFromCenter(k["disc"]), FadeIn(k["label"]))
            for k in kids], lag_ratio=0.22), run_time=1.9)
        self.play(Write(formula), run_time=0.8)
        self.wait(1.4)
        self.clear_all()

    # -------------------------------------------------- 3 · vertical = decorator
    def vertical(self):
        head = header("scale vertically — decorator")
        cx = -1.2
        base = layer(Vec(cx, -0.7), 2.0, 0.66, T.BINDER, r"C", fs=34)
        mid = layer(Vec(cx, 0.1), 2.0, 0.66, T.GOLD, r"v\{C\}", fs=28)
        top = layer(Vec(cx, 0.9), 2.0, 0.66, T.CORAL, r"r\{v\{C\}\}", fs=24)

        axis = directed_segment(Vec(cx + 1.75, -1.05), Vec(cx + 1.75, 1.4),
                                stroke_color=T.MUTED, stroke_width=2.4).to_manim()
        depth = T.subtitle("depth", size=24, color=T.MUTED).next_to(axis, RIGHT, buff=0.2)
        formula = T.caption_math(r"\mathrm{Dec}(C) : C \qquad d\{d\{C\}\} : C", color=T.INK)

        self.play(FadeIn(head), run_time=0.4)
        self.play(GrowFromCenter(base), run_time=0.5)
        self.play(FadeIn(mid, shift=UP * 0.3), run_time=0.5)
        self.play(FadeIn(top, shift=UP * 0.3), run_time=0.5)
        self.play(Create(axis), FadeIn(depth), run_time=0.6)
        self.play(Write(formula), run_time=0.8)
        self.wait(1.4)
        self.clear_all()

    # --------------------------------------------------------- 4 · n orthogonal axes
    def n_axes(self):
        head = header("orthogonal axes combine")
        o = Vec(-2.2, -1.6)
        hx = directed_segment(o, o + Vec(5.2, 0), stroke_color=T.GREEN,
                              stroke_width=2.6).to_manim()
        vy = directed_segment(o, o + Vec(0, 3.4), stroke_color=T.CORAL,
                              stroke_width=2.6).to_manim()
        hlab = T.subtitle("composite · breadth", size=24, color=T.GREEN)
        hlab.next_to(hx, DOWN, buff=0.2).align_to(hx, RIGHT)
        vlab = T.subtitle("decorator · depth", size=24, color=T.CORAL)
        vlab.next_to(vy, UP, buff=0.2)

        grid = VGroup(*[
            Dot((o + Vec(0.9 * i, 0.85 * j)).to_manim(), radius=0.06, color=T.BINDER)
            for i in range(1, 5) for j in range(1, 4)
        ])
        cap = T.caption("…and each domain adds its own axes — an n-axis binder")

        self.play(FadeIn(head), run_time=0.4)
        self.play(Create(hx), Create(vy), run_time=0.8)
        self.play(FadeIn(hlab), FadeIn(vlab), run_time=0.5)
        self.play(LaggedStart(*[GrowFromCenter(d) for d in grid], lag_ratio=0.06),
                  run_time=1.3)
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(1.4)
        self.clear_all()

    # ------------------------------------------------------------ 5 · returns to C
    def closure(self):
        forms = VGroup(
            T.caption_math(r"\text{leaf} : C"),
            T.caption_math(r"\mathrm{Comp}(C_1,\dots,C_n) : C"),
            T.caption_math(r"\mathrm{Dec}(C) : C"),
        )
        for m in forms:
            m.set_color(T.INK)
        forms.arrange(DOWN, buff=0.7, aligned_edge=LEFT).scale(0.85)
        forms.move_to([-3.0, 0.15, 0])
        hub = node(Vec(3.9, 0.15), 0.72, T.BINDER, r"C", fill=0.24, fs=64)
        cap = T.caption("every form returns to the same surface — C")

        self.play(LaggedStart(*[Write(m) for m in forms], lag_ratio=0.35), run_time=1.7)
        self.play(GrowFromCenter(hub["disc"]), FadeIn(hub["label"]), run_time=0.6)
        arrows = []
        for m in forms:
            start = Vec.from_manim(m.get_right()) + Vec(0.2, 0)
            end = Circle(radius=hub["radius"]).boundary_toward(hub["center"], start)
            arrows.append(directed_segment(start, end, stroke_color=T.MUTED,
                                           stroke_width=2.4).to_manim())
        self.play(LaggedStart(*[Create(a) for a in arrows], lag_ratio=0.22), run_time=1.1)
        self.play(FadeIn(cap), run_time=0.4)
        self.wait(1.6)
        self.clear_all()

    # ------------------------------------------------------------------ 6 · closing
    def closing(self):
        line = T.caption_math(r"C \;\Rightarrow\; \text{cohesion} \,+\, \text{flexibility}",
                              color=T.INK, size=52).shift(UP * 0.4)
        bridge = T.caption_math(
            r"\text{specialize the surface:}\quad C \Rightarrow T \quad C \Rightarrow Q \quad C \Rightarrow K",
            color=T.MUTED, size=34).next_to(line, DOWN, buff=0.7)
        self.play(Write(line), run_time=1.3)
        self.play(FadeIn(bridge), run_time=0.7)
        self.wait(1.8)
        self.play(FadeOut(line), FadeOut(bridge), run_time=0.9)
