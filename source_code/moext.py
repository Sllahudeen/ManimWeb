from manim import *
import numpy as np


class tetra(ThreeDScene):
    def construct(self):

        # -----------------------------
        # Camera
        # -----------------------------
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.7
        )

        # -----------------------------
        # 3D Axes
        # -----------------------------
        # Simple 3D axes with arrows

        x_axis = Arrow3D(
            start=np.array([-5, 0, 0]),
            end=np.array([5, 0, 0]),
            thickness=0.02,
            height=0.15,
            base_radius=0.1
        )

        y_axis = Arrow3D(
            start=np.array([0, -5, 0]),
            end=np.array([0, 5, 0]),
            thickness=0.02,
            height=0.15,
            base_radius=0.1
        )

        z_axis = Arrow3D(
            start=np.array([0, 0, -5]),
            end=np.array([0, 0, 5]),
            thickness=0.02,
            height=0.15,
            base_radius=0.1
        )

        axes = VGroup(x_axis, y_axis, z_axis)

        self.add(axes)

        # -----------------------------
        # Tetrahedron vertices
        # -----------------------------
        v1 = np.array([1, 1, 1])
        v2 = np.array([1, -1, -1])
        v3 = np.array([-1, 1, -1])
        v4 = np.array([-1, -1, 1])

        # -----------------------------
        # Four triangular faces
        # -----------------------------
        face1 = Polygon(
            v1, v2, v3,
            fill_opacity=0.15,
            stroke_width=2
        )

        face2 = Polygon(
            v1, v2, v4,
            fill_opacity=0.15,
            stroke_width=2
        )

        face3 = Polygon(
            v1, v3, v4,
            fill_opacity=0.15,
            stroke_width=2
        )

        face4 = Polygon(
            v2, v3, v4,
            fill_opacity=0.15,
            stroke_width=2
        )

        # -----------------------------
        # Group the faces
        # -----------------------------
        tetrahedron = VGroup(
            face1,
            face2,
            face3,
            face4
        )

        # -----------------------------
        # Add tetrahedron
        # -----------------------------

        self.add(tetrahedron)


        self.wait(1)

        # --------------------------------
        # Time variable
        # --------------------------------
        t = 0

        # --------------------------------
        # Fixed trajectory: unit circle at z = 1
        # --------------------------------
        trajectory = ParametricFunction(
            lambda u: np.array([
                np.cos(u),
                np.sin(u),
                1
            ]),
            t_range=[0, 2 * PI],
            color=PURE_RED
        )

        self.add(trajectory)

        # --------------------------------
        # Initial rotation axis
        # --------------------------------
        axis_vector = Arrow3D(
            start=[0, 0, 0],
            end=[1, 0, 1],
            thickness=0.03,
            height=0.2,
            base_radius=0.06,
            color=PURE_GREEN
        )

        self.add(axis_vector)

        # --------------------------------
        # Update tetrahedron AND vector
        # --------------------------------
        def update_system(m, dt):
            nonlocal t
            t += dt

            # Current position of vector head
            head = np.array([
                np.cos(t),
                np.sin(t),
                1
            ])

            # Current axis direction
            axis = normalize(head)

            # Angular velocity
            omega = 3

            # Rotate tetrahedron about current axis
            tetrahedron.rotate(
                omega * dt,
                axis=axis,
                about_point=ORIGIN
            )

            # Update the arrow
            axis_vector.put_start_and_end_on(
                ORIGIN,
                head
            )

        # --------------------------------
        # Add updater
        # --------------------------------

        tetrahedron.add_updater(update_system)

        self.wait(6)

        # --------------------------------
        # Stop
        # --------------------------------

        tetrahedron.clear_updaters()
        self.wait(1)
        self.remove(axis_vector, trajectory)

        # ----------------------------------
        # Get the current vertex positions
        # ----------------------------------

        new_v1 = face1.get_vertices()[0]
        new_v2 = face1.get_vertices()[1]
        new_v3 = face1.get_vertices()[2]
        new_v4 = face2.get_vertices()[2]

        symmetry_axis1 = new_v1
        symmetry_axis2 = new_v2
        symmetry_axis3 = new_v3
        symmetry_axis4 = new_v4


        symmetry_vector1 = Arrow3D(
            start=[0, 0, 0],
            end=2 * normalize(symmetry_axis1),
            thickness=0.03,
            height=0.2,
            base_radius=0.06,
            color=PURE_GREEN
        )

        symmetry_vector2 = Arrow3D(
            start=[0, 0, 0],
            end=2 * normalize(symmetry_axis2),
            thickness=0.03,
            height=0.2,
            base_radius=0.06,
            color=PURE_RED
        )

        symmetry_vector3 = Arrow3D(
            start=[0, 0, 0],
            end=2 * normalize(symmetry_axis3),
            thickness=0.03,
            height=0.2,
            base_radius=0.06,
            color=PURE_YELLOW
        )

        #-------------------------
        # rotation about v1
        #-------------------------

        self.add(symmetry_vector1)

        self.play(
            Rotate(
                tetrahedron,
                angle=2 * PI,
                axis=symmetry_axis1,
                about_point=ORIGIN
            ),
            run_time=3
        )
        self.remove(symmetry_vector1)

        #----------------------------
        # rotation about v2
        #----------------------------

        self.add(symmetry_vector2)

        self.play(
            Rotate(
                tetrahedron,
                angle=2 * PI,
                axis=symmetry_axis2,
                about_point=ORIGIN
            ),
            run_time=3
        )

        self.remove(symmetry_vector2)

        #----------------------------
        # rotation about v3
        # ---------------------------

        self.add(symmetry_vector3)

        self.play(
            Rotate(
                tetrahedron,
                angle=2 * PI,
                axis=symmetry_axis3,
                about_point=ORIGIN
            ),
            run_time=3
        )

        self.remove(symmetry_vector3)

        self.wait(1)
