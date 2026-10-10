
from manim import *
import numpy as np

from scipy.integrate import solve_ivp
from qiskit.quantum_info import Statevector, Pauli


# ==================================================
# QUANTUM MECHANICS: hbar = 1
# ==================================================

SIGMA_X = np.array([[0, 1], [1, 0]], dtype=complex)
SIGMA_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=complex)

PAULI = [Pauli("X"), Pauli("Y"), Pauli("Z")]


def hamiltonian(B):
    """H(t) = -1/2 B(t).sigma, with hbar = 1."""
    Bx, By, Bz = B

    return -0.5 * (
        Bx * SIGMA_X
        + By * SIGMA_Y
        + Bz * SIGMA_Z
    )


def bloch_vector(state):
    """Return (<sigma_x>, <sigma_y>, <sigma_z>)."""

    state = Statevector(
        np.ascontiguousarray(state.data, dtype=np.complex128)
    )

    return np.array([
        np.real(state.expectation_value(P))
        for P in PAULI
    ])


def rotating_field_trajectory(
    state,
    B_perp,
    Bz,
    drive_omega,
    duration,
    samples=600,
):
    """
    Numerically solve the time-dependent Schrodinger equation.

    B(t) = (
        B_perp cos(drive_omega*t),
        B_perp sin(drive_omega*t),
        Bz
    )
    """

    def B_of_t(t):
        return np.array([
            B_perp * np.cos(drive_omega * t),
            B_perp * np.sin(drive_omega * t),
            Bz,
        ])

    def schrodinger_rhs(t, psi):
        return -1j * hamiltonian(B_of_t(t)) @ psi

    times = np.linspace(0, duration, samples)

    solution = solve_ivp(
        schrodinger_rhs,
        (0, duration),
        state.data,
        t_eval=times,
        rtol=1e-9,
        atol=1e-11,
    )

    if not solution.success:
        raise RuntimeError(solution.message)

    points = []

    for i in range(len(times)):
        psi = solution.y[:, i]
        psi = psi / np.linalg.norm(psi)

        evolved = Statevector(psi)
        points.append(bloch_vector(evolved))

    final_psi = solution.y[:, -1]
    final_psi = final_psi / np.linalg.norm(final_psi)
    final_state = Statevector(final_psi)

    return times, np.array(points), final_state, B_of_t


# ==================================================
# MANIM VISUALIZATION
# ==================================================

class BlochFieldEvolution(ThreeDScene):

    def construct(self):

        # ------------------------------------------
        # 1. Camera
        # ------------------------------------------

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=-45 * DEGREES,
        )

        # ------------------------------------------
        # 2. Bloch sphere
        # ------------------------------------------

        sphere = Sphere(
            radius=2,
            resolution=(24, 48),
        )

        sphere.set_fill(BLUE, opacity=0.10)
        sphere.set_stroke(BLUE, opacity=0.35)

        # ------------------------------------------
        # 3. Coordinate axes
        # ------------------------------------------

        axes = ThreeDAxes(
            x_range=[-1.2, 1.2, 1],
            y_range=[-1.2, 1.2, 1],
            z_range=[-1.2, 1.2, 1],
            x_length=4.8,
            y_length=4.8,
            z_length=4.8,
        )

        self.add(sphere, axes)

        # ------------------------------------------
        # 4. Initial qubit state |+x>
        # ------------------------------------------

        state = Statevector(
            np.array([1, 1], dtype=complex) / np.sqrt(2)
        )

        initial_bloch = 2 * bloch_vector(state)

        initial_arrow = Arrow3D(
            start=ORIGIN,
            end=initial_bloch,
            color=YELLOW,
        )

        self.add(initial_arrow)

        # ------------------------------------------
        # 5. Time-dependent magnetic field
        # ------------------------------------------

        B_perp = 0.8
        Bz = 0.35

        # One complete revolution in eight seconds.
        drive_omega = TAU / 8
        duration = 4 * ( TAU / drive_omega )

        # ------------------------------------------
        # 6. Calculate qubit evolution
        # ------------------------------------------

        times, points, final_state, B_of_t = (
            rotating_field_trajectory(
                state,
                B_perp,
                Bz,
                drive_omega,
                duration,
                samples=600,
            )
        )

        # Scale the unit Bloch vectors to the sphere.
        points = 2 * points
        # Complete qubit trajectory on the Bloch sphere.
        full_qubit_path = VMobject(color=YELLOW, stroke_width=3)

        full_qubit_path.set_points_as_corners(
            [np.array(point) for point in points]
        )

        parameters = np.linspace(0, 1, len(points))

        def point_at(u):
            u = np.clip(u, 0, 1)

            return np.array([
                np.interp(u, parameters, points[:, j])
                for j in range(3)
            ])

        # ------------------------------------------
        # 7. Magnetic-field trajectory
        # ------------------------------------------

        field_scale = 1.8

        field_path = ParametricFunction(
            lambda u: field_scale * np.array([
                B_perp * np.cos(TAU * u),
                B_perp * np.sin(TAU * u),
                Bz,
            ]),
            t_range=[0, 1],
            color=RED,
            use_smoothing=False,
        )

        self.add(field_path)

        # ------------------------------------------
        # 8. Animation progress
        # ------------------------------------------

        progress = ValueTracker(0)

        # ------------------------------------------
        # 9. Evolving qubit vector
        # ------------------------------------------

        moving_arrow = always_redraw(
            lambda: Arrow3D(
                start=ORIGIN,
                end=point_at(progress.get_value()),
                color=YELLOW,
            )
        )

        # ------------------------------------------
        # 10. Rotating magnetic-field vector
        # ------------------------------------------

        field_arrow = always_redraw(
            lambda: Arrow3D(
                start=ORIGIN,
                end=field_scale * B_of_t(
                    progress.get_value() * duration
                ),
                color=RED,
            )
        )

        # ------------------------------------------
        # 11. Fading trail behind the qubit
        # ------------------------------------------

        trail_length = 0.30

        def make_trail():

            u = progress.get_value()
            start_u = max(0, u - trail_length)

            trail_params = np.linspace(
                start_u,
                u,
                35,
            )

            trail_points = [
                point_at(v)
                for v in trail_params
            ]

            trail = VGroup()

            for i in range(len(trail_points) - 1):

                segment = Line(
                    trail_points[i],
                    trail_points[i + 1],
                )

                fraction = (
                    (i + 1) / (len(trail_points) - 1)
                )

                segment.set_stroke(
                    color=YELLOW,
                    width=6 * fraction,
                    opacity=fraction ** 1.5,
                )

                trail.add(segment)

            return trail

        moving_trail = always_redraw(make_trail)

        # ------------------------------------------
        # 12. Animate the complete evolution
        # ------------------------------------------

        self.remove(initial_arrow)

        self.add(
            field_arrow,
            moving_trail,
            moving_arrow,
        )

        self.play(
            progress.animate.set_value(1),
            run_time=12,
            rate_func=linear,
        )
        self.remove(field_arrow,field_path,moving_trail)
        # Keep the final Bloch sphere configuration visible.
        self.add(full_qubit_path)
        self.begin_ambient_camera_rotation(
            rate=0.50,
            about="theta",
        )
        # Rotate the camera while displaying the full path.
        self.wait(3)
        # Stop the camera rotation at the end.
        self.stop_ambient_camera_rotation()
        self.wait(1)