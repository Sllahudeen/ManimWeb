
from manim import *
import numpy as np
from scipy.integrate import solve_ivp


# ============================================================
# 1. PHYSICAL PARAMETERS
# ============================================================

m1 = 1.0          # Mass of first bob (kg)
m2 = 1.0          # Mass of second bob (kg)

L1 = 2.0          # Length of first rod (m)
L2 = 2.0          # Length of second rod (m)

g = 9.81          # Gravitational acceleration (m/s^2)


# ============================================================
# 2. INITIAL CONDITIONS
# ============================================================

# Initial angles measured from the downward vertical.
# Enter angles in degrees here.

theta1_0 = -30.0
theta2_0 = 90.0

# Initial angular velocities in radians per second.
omega1_0 = 0.0
omega2_0 = 0.0


# ============================================================
# 3. DURATION AND NUMERICAL INTEGRATION
# ============================================================

SIMULATION_TIME = 20.0   # Physical time in seconds
FPS = 60                 # Animation frame rate
SLOW_MOTION = 1.0        # 1.0 = real-time physical speed

# Numerical sampling interval
DT = 1.0 / 240.0


# ============================================================
# 4. EQUATIONS OF MOTION
# ============================================================

def equations_of_motion(t, state):
    """
    State vector:
        state[0] = theta1
        state[1] = omega1
        state[2] = theta2
        state[3] = omega2

    Angles are measured from the downward vertical.
    """

    theta1, omega1, theta2, omega2 = state

    delta = theta1 - theta2

    denominator = (
        2 * m1 + m2
        - m2 * np.cos(2 * delta)
    )

    alpha1 = (
        -g * (2 * m1 + m2) * np.sin(theta1)
        - m2 * g * np.sin(theta1 - 2 * theta2)
        - 2 * m2 * np.sin(delta) * (
            omega2**2 * L2
            + omega1**2 * L1 * np.cos(delta)
        )
    ) / (L1 * denominator)

    alpha2 = (
        2 * np.sin(delta) * (
            omega1**2 * L1 * (m1 + m2)
            + g * (m1 + m2) * np.cos(theta1)
            + omega2**2 * L2 * m2 * np.cos(delta)
        )
    ) / (L2 * denominator)

    return [
        omega1,
        alpha1,
        omega2,
        alpha2
    ]


# ============================================================
# 5. SOLVE THE EQUATIONS BEFORE ANIMATION
# ============================================================

initial_state = [
    np.deg2rad(theta1_0),
    omega1_0,
    np.deg2rad(theta2_0),
    omega2_0
]

time_points = np.arange(
    0,
    SIMULATION_TIME + DT / 2,
    DT
)

solution = solve_ivp(
    equations_of_motion,
    (0, SIMULATION_TIME),
    initial_state,
    t_eval=time_points,
    method="DOP853",
    rtol=1e-10,
    atol=1e-12,
    max_step=DT
)

if not solution.success:
    raise RuntimeError(solution.message)

times = solution.t
theta1_values = solution.y[0]
theta2_values = solution.y[2]


def get_angles(t):
    """Interpolate the numerically calculated angles."""

    t = np.clip(t, times[0], times[-1])

    theta1 = np.interp(t, times, theta1_values)
    theta2 = np.interp(t, times, theta2_values)

    return theta1, theta2


# ============================================================
# 6. MANIM ANIMATION
# ============================================================

class DoublePendulum(Scene):

    def construct(self):

        # ----------------------------------------------------
        # VISUAL SETTINGS
        # ----------------------------------------------------

        scale = 1.0

        pivot_position = np.array([0.0, 2.0, 0.0])

        rod_color = GREY_B
        bob1_color = BLUE_C
        bob2_color = RED_C

        bob_radius = 0.14

        # ----------------------------------------------------
        # TITLE
        # ----------------------------------------------------

        title = Text(
            "Double Pendulum",
            font_size=32
        ).to_edge(UP, buff=0.25)

        subtitle = Text(
            "Nonlinear dynamics from equations of motion",
            font_size=17,
            color=GREY_B
        ).next_to(title, DOWN, buff=0.08)

        self.add(title, subtitle)

        # ----------------------------------------------------
        # FIXED PIVOT
        # ----------------------------------------------------

        pivot = Dot(
            pivot_position,
            radius=0.075,
            color=WHITE
        )

        support = Line(
            pivot_position + LEFT * 0.45,
            pivot_position + RIGHT * 0.45,
            color=GREY_B,
            stroke_width=5
        )

        self.add(support, pivot)

        # ----------------------------------------------------
        # PENDULUM BOBS
        # ----------------------------------------------------

        bob1 = Dot(
            radius=bob_radius,
            color=bob1_color
        )

        bob2 = Dot(
            radius=bob_radius,
            color=bob2_color
        )

        # ----------------------------------------------------
        # RODS
        # ----------------------------------------------------

        rod1 = Line(
            pivot_position,
            pivot_position + DOWN,
            color=rod_color,
            stroke_width=4
        )

        rod2 = Line(
            pivot_position + DOWN,
            pivot_position + 2 * DOWN,
            color=rod_color,
            stroke_width=4
        )

        # ----------------------------------------------------
        # TIME TRACKER
        # ----------------------------------------------------

        clock = ValueTracker(0.0)

        def positions(t):
            theta1, theta2 = get_angles(t)

            x1 = L1 * np.sin(theta1)
            y1 = -L1 * np.cos(theta1)

            x2 = x1 + L2 * np.sin(theta2)
            y2 = y1 - L2 * np.cos(theta2)

            p1 = pivot_position + scale * np.array(
                [x1, y1, 0.0]
            )

            p2 = pivot_position + scale * np.array(
                [x2, y2, 0.0]
            )

            return p1, p2

        def update_rod1(mob):
            p1, _ = positions(clock.get_value())
            mob.put_start_and_end_on(
                pivot_position, p1
            )

        def update_rod2(mob):
            p1, p2 = positions(clock.get_value())
            mob.put_start_and_end_on(p1, p2)

        def update_bob1(mob):
            p1, _ = positions(clock.get_value())
            mob.move_to(p1)

        def update_bob2(mob):
            _, p2 = positions(clock.get_value())
            mob.move_to(p2)

        rod1.add_updater(update_rod1)
        rod2.add_updater(update_rod2)

        bob1.add_updater(update_bob1)
        bob2.add_updater(update_bob2)

        # ----------------------------------------------------
        # TRAILS OF BOTH MASSES
        # ----------------------------------------------------

        trail2 = TracedPath(
            bob2.get_center,
            stroke_color=RED_C,
            stroke_width=2.5
        )

        # ----------------------------------------------------
        # TIME DISPLAY
        # ----------------------------------------------------

        time_label = always_redraw(
            lambda: Text(
                f"Time: {clock.get_value():.2f} s",
                font_size=20
            ).to_corner(UL, buff=0.35).shift(
                DOWN * 0.55
            )
        )

        # ----------------------------------------------------
        # INITIALIZE AT THE GIVEN ANGLES
        # ----------------------------------------------------

        p1, p2 = positions(0)

        bob1.move_to(p1)
        bob2.move_to(p2)

        self.add(
            rod1,
            rod2,
            trail2,
            bob1,
            bob2,
            time_label
        )

        # ----------------------------------------------------
        # RUN THE ACTUAL DYNAMICS
        # ----------------------------------------------------

        self.play(
            clock.animate.set_value(SIMULATION_TIME),
            run_time=SIMULATION_TIME / SLOW_MOTION,
            rate_func=linear
        )

        # Stop all dynamic updates cleanly.
        rod1.clear_updaters()
        rod2.clear_updaters()
        bob1.clear_updaters()
        bob2.clear_updaters()