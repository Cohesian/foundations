"""Starter scene — edit and render with make preview or loci-render."""

from manim import Scene

from loci import Circle, Graph, Vec


class Lesson01(Scene):
    def construct(self):
        graph = Graph()
        graph.add_node(Vec(0, 0), Circle(radius=0.5), label="A")
        graph.add_to_scene(self)
        self.wait()
