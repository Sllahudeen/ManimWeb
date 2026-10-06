from manim import *


class PortfolioTest(Scene):

    def construct(self):

        title = Text("My Manim Portfolio")

        circle = Circle()

        self.play(Write(title))
        self.play(title.animate.to_edge(UP))

        self.play(Create(circle))

        self.play(circle.animate.scale(2))

        self.wait(2)