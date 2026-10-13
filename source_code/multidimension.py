
from manim import *
import numpy as np


class HopfFibration(ThreeDScene):

    def construct(self):

        # =====================================================
        # PARAMETERS
        # =====================================================

        # S^3 has unit radius before stereographic projection.
        # eta labels the Clifford tori inside S^3.
        eta_values = [0.38, 0.68, 0.96]

        # Fiber counts on the three tori.
        fiber_counts = [7, 9, 11]

        # Number of points used to draw each fiber.
        curve_samples = 160

        # =====================================================
        # MATHEMATICAL MAPS
        # =====================================================

        def stereographic_point(eta, alpha, beta):

            # Coordinates in C^2:
            # z1 = cos(eta) exp(i alpha)
            # z2 = sin(eta) exp(i beta)

            x1 = np.cos(eta) * np.cos(alpha)
            x2 = np.cos(eta) * np.sin(alpha)
            x3 = np.sin(eta) * np.cos(beta)
            x4 = np.sin(eta) * np.sin(beta)

            denominator = 1.0 - x4

            # The chosen eta values stay away from the
            # stereographic projection pole.
            return np.array([
                x1 / denominator,
                x2 / denominator,
                x3 / denominator,
            ])

        def fiber_point(eta, delta, t):

            # A Hopf fiber:
            # alpha = t, beta = t - delta.
            return stereographic_point(
                eta,
                t,
                t - delta
            )

        def make_fiber(eta, delta, color, width=2.5):

            return ParametricFunction(
                lambda t: fiber_point(eta, delta, t),
                t_range=[0, TAU],
                color=color,
                stroke_width=width,
                use_smoothing=True,
            )

        def make_torus(eta, color):

            # Fix eta and allow alpha and beta to vary
            # independently. This gives a Clifford torus
            # in S^3, projected into ordinary R^3.

            return Surface(
                lambda alpha, beta: stereographic_point(
                    eta,
                    alpha,
                    beta
                ),
                u_range=[0, TAU],
                v_range=[0, TAU],
                resolution=(32, 32),
                checkerboard_colors=[color, color],
                fill_opacity=0.075,
                stroke_color=color,
                stroke_width=0.45,
                stroke_opacity=0.32,
            )

        # =====================================================
        # SCENE 1: INTRODUCTION
        # =====================================================

        title = Tex(
            r"The Hopf Fibration"
        ).scale(1.15)

        subtitle = Tex(
            r"How circles fill the three-sphere $S^3$"
        ).scale(0.65)

        equation = MathTex(
            r"S^3=\left\{(z_1,z_2)\in\mathbb{C}^2:"
            r"|z_1|^2+|z_2|^2=1\right\}"
        ).scale(0.65)

        subtitle.next_to(title, DOWN, buff=0.35)
        equation.next_to(subtitle, DOWN, buff=0.55)

        self.play(Write(title), run_time=1.5)
        self.play(FadeIn(subtitle, shift=UP * 0.15))
        self.play(Write(equation), run_time=2)
        self.wait(2)

        self.play(
            FadeOut(title),
            FadeOut(subtitle),
            FadeOut(equation),
            run_time=1
        )

        # =====================================================
        # SCENE 2: PARAMETERIZATION
        # =====================================================

        parameter_title = Tex(
            r"Complex coordinates on $S^3$"
        ).scale(0.75)

        parameter_title.to_edge(UP, buff=0.35)

        parameter_equations = MathTex(
            r"z_1=\cos\eta\,e^{i\alpha},",
            r"\qquad",
            r"z_2=\sin\eta\,e^{i\beta}"
        ).scale(0.72)

        parameter_equations.next_to(
            parameter_title,
            DOWN,
            buff=0.45
        )

        normalization = MathTex(
            r"|z_1|^2+|z_2|^2"
            r"=\cos^2\eta+\sin^2\eta=1"
        ).scale(0.65)

        normalization.next_to(
            parameter_equations,
            DOWN,
            buff=0.45
        )

        self.add_fixed_in_frame_mobjects(
            parameter_title,
            parameter_equations,
            normalization
        )

        self.play(FadeIn(parameter_title))
        self.play(Write(parameter_equations))
        self.play(Write(normalization))
        self.wait(3)

        self.play(
            FadeOut(parameter_title),
            FadeOut(parameter_equations),
            FadeOut(normalization),
            run_time=1
        )

        # =====================================================
        # SCENE 3: STEREOGRAPHIC PROJECTION
        # =====================================================

        projection_title = Tex(
            r"Projecting $S^3$ into $\mathbb{R}^3$"
        ).scale(0.68)

        projection_title.to_edge(UP, buff=0.3)

        projection_equation = MathTex(
            r"(X,Y,Z)=",
            r"\frac{(x_1,x_2,x_3)}{1-x_4}"
        ).scale(0.7)

        projection_equation.next_to(
            projection_title,
            DOWN,
            buff=0.35
        )

        projection_note = Tex(
            r"The fourth coordinate is encoded by the projection."
        ).scale(0.47)

        projection_note.next_to(
            projection_equation,
            DOWN,
            buff=0.25
        )

        self.add_fixed_in_frame_mobjects(
            projection_title,
            projection_equation,
            projection_note
        )

        self.play(FadeIn(projection_title))
        self.play(Write(projection_equation))
        self.play(FadeIn(projection_note))
        self.wait(3)

        self.play(
            FadeOut(projection_title),
            FadeOut(projection_equation),
            FadeOut(projection_note),
            run_time=1
        )

        # =====================================================
        # SCENE 4: NESTED TORI
        # =====================================================

        self.set_camera_orientation(
            phi=68 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.95,
        )

        # Faint shells reveal the nested toroidal structure.
        torus_colors = [
            BLUE_D,
            PURPLE,
            TEAL,
        ]

        tori = VGroup()

        for eta, color in zip(eta_values, torus_colors):

            torus = make_torus(eta, color)
            tori.add(torus)

        self.play(
            LaggedStart(
                *[Create(torus) for torus in tori],
                lag_ratio=0.3
            ),
            run_time=4
        )

        shell_title = Tex(
            r"Constant $\eta$: a torus inside $S^3$"
        ).scale(0.57)

        shell_title.to_edge(UP, buff=0.3)

        shell_equation = MathTex(
            r"|z_1|=\cos\eta,\qquad |z_2|=\sin\eta"
        ).scale(0.55)

        shell_equation.to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(
            shell_title,
            shell_equation
        )

        self.play(
            FadeIn(shell_title),
            FadeIn(shell_equation)
        )

        self.wait(3)

        self.play(
            FadeOut(shell_title),
            FadeOut(shell_equation),
            run_time=0.8
        )

        # =====================================================
        # SCENE 5: HOPF FIBERS
        # =====================================================

        fiber_colors = [
            RED,
            ORANGE,
            YELLOW,
            GREEN,
            TEAL,
            BLUE,
            PURPLE,
            PINK,
            GOLD,
            MAROON,
            BLUE_B,
        ]

        fibers = VGroup()

        # Several different fibers on each torus.
        # At a given eta, delta selects the fiber.
        for shell_index, eta in enumerate(eta_values):

            count = fiber_counts[shell_index]

            for j in range(count):

                delta = TAU * j / count

                color = fiber_colors[
                    (j + 2 * shell_index) % len(fiber_colors)
                ]

                fiber = make_fiber(
                    eta,
                    delta,
                    color,
                    width=2.1
                )

                fibers.add(fiber)

        # Highlight one fiber on the middle torus.
        highlighted_eta = eta_values[1]
        highlighted_delta = 0.0

        highlighted_fiber = make_fiber(
            highlighted_eta,
            highlighted_delta,
            WHITE,
            width=4.2
        )

        fiber_title = Tex(
            r"Each colored curve is a Hopf fiber"
        ).scale(0.58)

        fiber_title.to_edge(UP, buff=0.3)

        fiber_equation = MathTex(
            r"z_1=\cos(\eta)e^{it}",
            r"\quad",
            r"z_2=\sin(\eta)e^{i(t-\delta)}",
        ).scale(0.55)

        fiber_equation.to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(
            fiber_title,
            fiber_equation
        )

        self.play(FadeIn(fiber_title))
        self.play(
            LaggedStart(
                *[Create(fiber) for fiber in fibers],
                lag_ratio=0.025
            ),
            run_time=7
        )

        self.play(
            Create(highlighted_fiber),
            run_time=2
        )

        self.play(FadeIn(fiber_equation))
        self.wait(3)

        self.play(
            FadeOut(fiber_title),
            FadeOut(fiber_equation),
            run_time=1
        )

        # =====================================================
        # SCENE 6: THE HOPF MAP
        # =====================================================

        hopf_title = Tex(
            r"The Hopf map $S^3\longrightarrow S^2$"
        ).scale(0.62)

        hopf_title.to_edge(UP, buff=0.3)

        hopf_equation = MathTex(
            r"h(z_1,z_2)=",
            r"\left(",
            r"2z_1\overline{z}_2,",
            r"|z_1|^2-|z_2|^2",
            r"\right)"
        ).scale(0.55)

        hopf_equation.next_to(
            hopf_title,
            DOWN,
            buff=0.3
        )

        hopf_note = Tex(
            r"Each point of $S^2$ labels one circular fiber."
        ).scale(0.48)

        hopf_note.to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(
            hopf_title,
            hopf_equation,
            hopf_note
        )

        self.play(FadeIn(hopf_title))
        self.play(Write(hopf_equation))
        self.play(FadeIn(hopf_note))
        self.wait(4)

        self.play(
            FadeOut(hopf_title),
            FadeOut(hopf_equation),
            FadeOut(hopf_note),
            run_time=1
        )

        # =====================================================
        # SCENE 7: ROTATING THREE-DIMENSIONAL VIEW
        # =====================================================

        # Remove the shells to make the interlinking more visible.
        # Keep all fibers in place.
        self.play(
            FadeOut(tori),
            run_time=1.5
        )

        # Bring the highlighted fiber to the foreground visually.
        # Geometry remains unchanged; only the camera moves.
        self.begin_ambient_camera_rotation(
            rate=0.25,
            about="theta"
        )

        final_title = Tex(
            r"The Hopf fibration"
        ).scale(0.7)

        final_title.to_edge(UP, buff=0.3)

        final_note = Tex(
            r"Distinct fibers are linked, yet never intersect."
        ).scale(0.48)

        final_note.to_edge(DOWN, buff=0.3)

        self.add_fixed_in_frame_mobjects(
            final_title,
            final_note
        )

        self.play(
            FadeIn(final_title),
            FadeIn(final_note)
        )

        self.wait(12)

        self.stop_ambient_camera_rotation()

        self.wait(2)

        self.play(
            FadeOut(final_title),
            FadeOut(final_note),
            run_time=1
        )

        self.wait(1)
