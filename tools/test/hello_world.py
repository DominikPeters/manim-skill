"""Simple Hello World animation with colorful shapes for testing."""

from manim import *


class HelloWorld(Scene):
    def construct(self):
        # Create title
        title = Text("Hello World", font_size=72, color=BLUE)

        # Create colorful shapes
        circle = Circle(color=RED, fill_opacity=0.7)
        square = Square(color=GREEN, fill_opacity=0.7)
        triangle = Triangle(color=YELLOW, fill_opacity=0.7)

        # Arrange shapes
        circle.shift(LEFT * 2)
        square.shift(RIGHT * 2)
        triangle.shift(DOWN * 2)

        shapes = VGroup(circle, square, triangle)

        # Animate title
        self.play(Write(title), run_time=2)
        self.wait(0.5)

        # Animate shapes appearing
        self.play(FadeIn(circle), FadeIn(square), FadeIn(triangle), run_time=1.5)
        self.wait(0.5)

        # Animate shapes rotating and moving
        self.play(
            Rotate(circle, angle=PI),
            Rotate(square, angle=PI),
            Rotate(triangle, angle=PI),
            run_time=2
        )
        self.wait(0.5)

        # Scale shapes
        self.play(
            circle.animate.scale(1.5),
            square.animate.scale(1.5),
            triangle.animate.scale(1.5),
            run_time=1
        )
        self.wait(0.5)

        # Fade everything out
        self.play(FadeOut(title), FadeOut(shapes), run_time=1.5)
