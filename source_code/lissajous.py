

from manim import *
import numpy as np


class Lissajous3D(ThreeDScene):

    def construct(self):

        # -----------------------------
        # Parameters of the oscillation
        # -----------------------------
        Ax, Ay, Az = 3, 2.5, 2.5

        wx = 3
        wy = 4
        wz = 5

        phix = 0
        phiy = PI / 3
        phiz = PI / 2

        # Time range
        T = 2 * PI

        def position(t):
            x = Ax * np.sin(wx * t + phix)
            y = Ay * np.sin(wy * t + phiy)
            z = Az * np.sin(wz * t + phiz)

            return np.array([x, y, z])

        # -----------------------------
        # Camera orientation
        # -----------------------------
        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=0 * DEGREES,
            zoom=0.70
        )

        # Title
        title = Text(
            "Lissajous Curve",
            font_size=36,
            color=WHITE
        )
        title.to_edge(UP, buff=0.3)

        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1)

        # -----------------------------
        # Full Lissajous trajectory
        # -----------------------------
        curve = ParametricFunction(
            position,
            t_range=[0, T],
            color=BLUE,
            stroke_width=3,
        )

        # Moving particle
        particle = Sphere(
            radius=0.09,
            resolution=(12, 24),
            color=YELLOW
        )
        particle.move_to(position(0))

        # Trace drawn as time progresses
        trace = VMobject(
            color=BLUE,
            stroke_width=3
        )
        trace.set_points_as_corners([position(0)])

        tracker = ValueTracker(0)

        def update_particle(mob):
            t = tracker.get_value()
            mob.move_to(position(t))

        def update_trace(mob):
            t = tracker.get_value()

            points = np.array([
                position(s)
                for s in np.linspace(0, t, 500)
            ])

            mob.set_points_as_corners(points)

        particle.add_updater(update_particle)
        trace.add_updater(update_trace)

        self.add(trace, particle)

        # -----------------------------
        # Stage 1: Trace the curve
        # -----------------------------
        self.begin_ambient_camera_rotation(rate=0.50)

        self.play(
            tracker.animate.set_value(T),
            run_time=3.5,
            rate_func=linear
        )

        # Stop camera and particle motion
        self.stop_ambient_camera_rotation()

        particle.clear_updaters()
        trace.clear_updaters()

        # Remove particle: retain only the completed curve
        self.remove(particle)

        # -----------------------------
        # Stage 2: Rotate the curve itself
        # -----------------------------
        def rotate_curve(mob, dt):
            mob.rotate(
                1.5 * dt,
                axis=RIGHT,
                about_point=ORIGIN
            )
            mob.rotate(
                1.0 * dt,
                axis=UP,
                about_point=ORIGIN
            )
            mob.rotate(
                2.0 * dt,
                axis=OUT,
                about_point=ORIGIN
            )

        trace.add_updater(rotate_curve)

        # Observe the completed curve tumbling in 3D
        self.wait(6.5)

        trace.clear_updaters()