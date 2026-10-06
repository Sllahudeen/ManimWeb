from manim import *
import numpy as np
from pyglet.font.directwrite import white


class bc(Scene):
    def construct(self):
        # Define two fixed points
        start = np.array([np.pi, 2, 0])  # Start point (higher)
        end = np.array([3 * np.pi / 2 + 1, 1, 0])  # End point (lower)

        # Define the function for the sinusoidal arc
        def func(x):
            return -0.2 * np.sin(4 * x) - ((2 * (0.2 * np.sin(8) + 1)) / (np.pi + 2)) * (x - np.pi) + 2

        # Define the sinusoidal arc
        sinosidal_arc = ParametricFunction(
            lambda t: np.array([t, func(t), 0]),
            t_range=[np.pi, (3 * np.pi / 2) + 1],  # Domain of the function
            color=GREEN
        )

        # Define the straight line
        straight_line = Line(start, end, color=BLUE)  # Straight path

        # Define the brachistochrone path (cycloid)
        brachistochrone_path = ParametricFunction(
            lambda t: np.array([
                (t - np.sin(t)),
                (1 - np.cos(t)),
                0
            ]),
            t_range=[np.pi, 3 * np.pi / 2],  # Cycloid defined with parametric t
            color=RED
        )

        # Add vertical lines
        left_vertical_line = Line(
            start,  # Start at (π, 2)
            np.array([np.pi, -1, 0]),  # Extend downward (length = 4)
            color=WHITE
        )
        right_vertical_line = Line(
            end,  # Start at (3π/2 + 1, 1)
            np.array([3 * np.pi / 2 + 1, -1, 0]),  # Extend downward (length = 5)
            color=WHITE
        )

        # Connect the bases of the two vertical lines
        connecting_line = Line(
            np.array([np.pi, -1, 0]),  # Base of the left vertical line
            np.array([3 * np.pi / 2 + 1, -1, 0]),  # Base of the right vertical line
            color=WHITE
        )

        # Group all elements, including the endpoints, to scale them together
        scene_elements = VGroup(
            straight_line,
            sinosidal_arc,
            brachistochrone_path,
            left_vertical_line,
            right_vertical_line,
            connecting_line
        )

        # Shift the group and endpoints to the left
        scene_elements.shift(LEFT * 2)

        # Scale the entire scene elements by 1.5
        scene_elements.scale(1.5)

        scene_elements.shift(DOWN * 2)
        # Add paths, lines, and scaled endpoints to the scene
        self.add(scene_elements)

        # Add moving balls (one for each path)
        ball_a = Dot(start, color=WHITE).scale(1)
        ball_b = Dot(start, color=WHITE).scale(1)
        ball_c = Dot(start, color=WHITE).scale(1)

        # Define motion for each ball under gravity
        def ball_a_update(m, dt):
            alpha = m.alpha if hasattr(m, 'alpha') else 0
            alpha += dt / 3  # Adjust speed for slower travel
            alpha = min(alpha, 1)
            m.alpha = alpha
            m.move_to(straight_line.point_from_proportion(alpha))

        def ball_b_update(m, dt):
            alpha = m.alpha if hasattr(m, 'alpha') else 0
            alpha += dt / 2  # Adjust speed for medium travel
            alpha = min(alpha, 1)
            m.alpha = alpha
            m.move_to(sinosidal_arc.point_from_proportion(alpha))

        def ball_c_update(m, dt):
            alpha = m.alpha if hasattr(m, 'alpha') else 0
            alpha += dt  # Adjust speed for fastest travel (brachistochrone)
            alpha = min(alpha, 1)
            m.alpha = alpha
            m.move_to(brachistochrone_path.point_from_proportion(alpha))

        ball_a.add_updater(ball_a_update)
        ball_b.add_updater(ball_b_update)
        ball_c.add_updater(ball_c_update)

        # Add balls to the scene
        self.add(ball_a, ball_b, ball_c)

        # Create the title text
        title = Text("Brachistochrone: The least time path", font_size=36, color=WHITE)
        title.shift(UP * 3 + LEFT * 3)  # Position explicitly relative to the scene

        # Add larger equations for parametric curves
        equations = VGroup(
            MathTex(r"x(t) = a(t - \sin(t))", font_size=40, color=WHITE),  # Increased font size
            MathTex(r"y(t) = a(1 - \cos(t))", font_size=46, color=WHITE)   # Increased font size
        )
        equations.arrange(DOWN, aligned_edge=LEFT)  # Arrange equations vertically
        equations.next_to(title, DOWN, buff=0.5)

        # Add a box around the equations
        box = SurroundingRectangle(equations, color=ORANGE, buff=0.3)

        # Animate the text, equations, and box appearing letter by letter
        self.play(Write(title), run_time=6)  # Extended time for the title
        self.play(Write(equations), run_time=6)  # Extended time for equations
        self.play(Create(box), run_time=2)  # Animate the box appearing around the equations

        # Keep the scene visible longer
        self.wait()  # Extended wait time for full visibility
