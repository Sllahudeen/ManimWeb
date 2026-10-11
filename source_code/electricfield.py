from manim import *
import numpy as np

class ElectricFieldParticle(ThreeDScene):

    def construct(self):

        # Physical parameters
        E0 = 4.0
        q = 1.0
        m = 1.0
        acceleration = q * E0 / m

        # Capacitor geometry
        x_left = -3.5
        x_right = 3.5
        plate_y = 2.5
        plate_z = 2.0

        # Initial particle position
        x0 = -3.2
        y0 = 0.0
        z0 = 0.0

        # Camera
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.8,
        )

        # Positive plate: flat sheet
        positive_plate = Surface(
            lambda u, v: np.array([x_left, u, v]),
            u_range=[-plate_y, plate_y],
            v_range=[-plate_z, plate_z],
            resolution=(1, 1),
            fill_color=BLUE,
            fill_opacity=0.8,
            stroke_width=0,
        )

        # Negative plate: flat sheet
        negative_plate = Surface(
            lambda u, v: np.array([x_right, u, v]),
            u_range=[-plate_y, plate_y],
            v_range=[-plate_z, plate_z],
            resolution=(1, 1),
            fill_color=RED,
            fill_opacity=0.8,
            stroke_width=0,
        )

        # Charge labels
        positive_label1 = MathTex(
            r"+\,+\,+\,+\,+", color=WHITE
        ).scale(1.0)

        positive_label1.rotate(PI / 2, axis=OUT)
        positive_label1.rotate(PI / 2, axis=UP)
        positive_label1.move_to([x_left - 0.02, 0 , 1.0])

        positive_label2 = MathTex(
            r"+\,+\,+\,+\,+", color=WHITE
        ).scale(1.0)

        positive_label2.rotate(PI / 2, axis=OUT)
        positive_label2.rotate(PI / 2, axis=UP)
        positive_label2.move_to([x_left - 0.02, 0, 0])

        positive_label3 = MathTex(
            r"+\,+\,+\,+\,+", color=WHITE
        ).scale(1.0)

        positive_label3.rotate(PI / 2, axis=OUT)
        positive_label3.rotate(PI / 2, axis=UP)
        positive_label3.move_to([x_left - 0.02, 0, -1.0])

        negative_label1 = MathTex(
            r"-\,-\,-\,-\,-", color=WHITE
        ).scale(1.0)

        negative_label1.rotate(PI / 2, axis=OUT)
        negative_label1.rotate(PI / 2, axis=UP)
        negative_label1.move_to([x_right + 0.02, 0, 1.0])

        negative_label2 = MathTex(
            r"-\,-\,-\,-\,-", color=WHITE
        ).scale(1.0)

        negative_label2.rotate(PI / 2, axis=OUT)
        negative_label2.rotate(PI / 2, axis=UP)
        negative_label2.move_to([x_right + 0.02, 0, 0])

        negative_label3 = MathTex(
            r"-\,-\,-\,-\,-", color=WHITE
        ).scale(1.0)

        negative_label3.rotate(PI / 2, axis=OUT)
        negative_label3.rotate(PI / 2, axis=UP)
        negative_label3.move_to([x_right + 0.02, 0, -1.0])

        # Static electric field arrows
        # All arrows point from the positive plate to the negative plate.
        field_arrows = VGroup()

        x_positions = np.linspace(-2.7, 2.7, 5)
        y_positions = np.linspace(-1.8, 1.8, 4)
        z_positions = [-1.0, 0.0, 1.0]

        for x in x_positions:
            for y in y_positions:
                for z in z_positions:

                    arrow = Arrow(
                        start=[x - 0.18, y, z],
                        end=[x + 0.18, y, z],
                        buff=0,
                        color=YELLOW,
                        stroke_width=2,
                        max_tip_length_to_length_ratio=0.3,
                    )

                    field_arrows.add(arrow)

        # Small, smooth-looking solid charged sphere
        particle = Sphere(
            center=[x0, y0, z0],
            radius=0.14,
            resolution=(10, 10),
            color=GREEN,
        )

        particle.set_fill(GREEN, opacity=1)

        charge_symbol = MathTex(
            "+", color=BLACK
        ).scale(0.60)

        charge_symbol.move_to(particle.get_center())

        # Velocity arrow: same style as electric-field arrows
        velocity_arrow = Arrow(
            start=[x0, y0, z0],
            end=[x0 + 0.2, y0, z0],
            buff=0,
            color=RED,
            stroke_width=3,
            max_tip_length_to_length_ratio=0.3,
        )

        # Title at the top of the screen
        title = Text(
            "Motion of a Positive Charge in an Electric Field",
            color=WHITE,
        ).scale(0.55).to_edge(UP)

        # Electric field label
        electric_field_label = MathTex(
            r"\vec{E}", color=YELLOW
        ).scale(0.8)
        electric_field_label.move_to([0, -1.0, 0])
        electric_field_label.rotate(PI / 2, axis=RIGHT)

        # Velocity vector label
        velocity_label = MathTex(
            r"\vec{v}", color=ORANGE
        ).scale(0.8)
        velocity_label.move_to(velocity_arrow.get_end() + UP * 0.25)
        velocity_label.rotate(PI / 2, axis=RIGHT)


        # Display the setup.
        # Field arrows are added directly: no individual arrow animations.
        self.add(
            positive_plate,
            negative_plate,
            positive_label1, positive_label2, positive_label3,
            negative_label1, negative_label2, negative_label3,
            field_arrows,
            electric_field_label,
            particle,
            charge_symbol,
            velocity_arrow,
            velocity_label,
        )

        # Keep the title fixed at the top of the screen
        self.add_fixed_in_frame_mobjects(title)

        # Animate the title into view
        self.play(Write(title), run_time=1.5)

        # Particle motion: x(t) = x0 + (1/2) a t^2
        motion_time = 1.8
        time_tracker = ValueTracker(0)

        def position_at_time(t):
            x = x0 + 0.5 * acceleration * t**2
            return np.array([x, y0, z0])

        particle.add_updater(
            lambda mob: mob.move_to(
                position_at_time(time_tracker.get_value())
            )
        )

        charge_symbol.add_updater(
            lambda mob: mob.move_to(particle.get_center())
        )

        def update_velocity_arrow(arrow):
            t = time_tracker.get_value()

            # Velocity magnitude: v = a*t
            velocity = acceleration * t
            length = 0.25 * velocity

            start = particle.get_center()
            end = start + RIGHT * max(length, 0.2)

            new_arrow = Arrow(
                start=start,
                end=end,
                buff=0,
                color=ORANGE,
                stroke_width=3,
                max_tip_length_to_length_ratio=0.3,
            )

            arrow.become(new_arrow)

        velocity_arrow.add_updater(update_velocity_arrow)
        # Keep the velocity label just above the arrow's tip
        velocity_label.add_updater(
            lambda mob: mob.move_to(
                velocity_arrow.get_end() + UP * 0.25
            )
        )
        # Start rotating the camera around the scene
        self.begin_ambient_camera_rotation(
            rate=-0.12,
            about="theta",
        )
        # Only the particle moves; the camera rotates simultaneously
        self.play(
            time_tracker.animate.set_value(motion_time),
            run_time=6,
            rate_func=linear,
        )
        # Stop the camera rotation
        self.stop_ambient_camera_rotation()

        particle.clear_updaters()
        charge_symbol.clear_updaters()

        ##############################
        ##############################
        #Motion in Magnetic field
        ##############################
        ##############################


        # =====================================================
        # PART 2: MOTION OF A CHARGED PARTICLE IN A MAGNETIC FIELD
        # =====================================================

        # Remove the entire electric-field scene abruptly
        self.clear()

        #set camera
        self.set_camera_orientation(
            phi=65 * DEGREES,
            theta=-45 * DEGREES,
            zoom=0.8,
        )

        # New title
        title = Text(
            "Motion of a Charged Particle in a Magnetic Field",
            color=WHITE,
        ).scale(0.52).to_edge(UP)

        # -----------------------------------------------------
        # Magnetic field and geometry
        # -----------------------------------------------------
        B0 = 1.2
        q_m = 1.0       # q/m
        v0 = 4.0        # Initial speed

        x_left = -2.5
        x_right = 2.5
        plate_y = 2.0
        plate_thickness = 0.18
        gap_half = 0.65

        # North pole: red upper plate
        north_plate = Cube(
            side_length=1,
            fill_color=RED,
            fill_opacity=1.0,
            stroke_color=RED,
        )
        north_plate.stretch_to_fit_width(x_right - x_left)
        north_plate.stretch_to_fit_height(2 * plate_y)
        north_plate.stretch_to_fit_depth(plate_thickness)
        north_plate.move_to([
            (x_left + x_right) / 2,
            0,
            gap_half + plate_thickness / 2 + 1.0,
        ])

        # South pole: blue lower plate
        south_plate = Cube(
            side_length=1,
            fill_color=BLUE,
            fill_opacity=1.0,
            stroke_color=BLUE,
        )
        south_plate.stretch_to_fit_width(x_right - x_left)
        south_plate.stretch_to_fit_height(2 * plate_y)
        south_plate.stretch_to_fit_depth(plate_thickness)
        south_plate.move_to([
            (x_left + x_right) / 2,
            0,
            -gap_half - plate_thickness / 2 - 1.0,
        ])

        # Pole labels on the visible front sides of the plates
        north_label = Text(
            "NORTH POLE",
            color=WHITE,
        ).scale(0.55)
        north_label.move_to([0, -plate_y - 0.03, gap_half + 1.0])

        south_label = Text(
            "SOUTH POLE",
            color=WHITE,
        ).scale(0.55)
        south_label.move_to([0, -plate_y - 0.03, -gap_half - 1.0])

        # -----------------------------------------------------
        # Magnetic field arrows: from North to South
        # -----------------------------------------------------
        magnetic_arrows = VGroup()

        z_positions=[-0.7,0,0.7]
        for x in np.linspace(-1.8, 1.8, 4):
            for y in np.linspace(-1.3, 1.3, 3):
                for z in z_positions:
                    magnetic_arrows.add(
                        Arrow(
                            start=[x, y, z + 0.18],
                            end=[x, y, z - 0.18],
                            buff=0,
                            color=YELLOW,
                            stroke_width=2,
                            max_tip_length_to_length_ratio=0.3,
                        )
                    )

        # -----------------------------------------------------
        # Numerical solution of the Lorentz-force equations
        #
        # dr/dt = v
        # dv/dt = (q/m) (v x B)
        #
        # The field is present only inside the plate region.
        # -----------------------------------------------------
        d = 4.5
        r0 = np.array([-d, -0.5, 0.0])
        velocity0 = np.array([v0, 0.0, 0.0])

        dt = 0.005
        total_time = 5.0
        number_steps = int(total_time / dt)

        def magnetic_field(r):
            inside_x = x_left <= r[0] <= x_right
            inside_y = abs(r[1]) <= plate_y

            if inside_x and inside_y:
                return np.array([0.0, 0.0, -B0])

            return np.zeros(3)

        def derivatives(state):
            r = state[:3]
            v = state[3:]

            dr_dt = v
            dv_dt = q_m * np.cross(v, magnetic_field(r))

            return np.concatenate([dr_dt, dv_dt])

        # Fourth-order Runge-Kutta integration
        state = np.concatenate([r0, velocity0])
        trajectory = [state[:3].copy()]

        for _ in range(number_steps):
            k1 = derivatives(state)
            k2 = derivatives(state + 0.5 * dt * k1)
            k3 = derivatives(state + 0.5 * dt * k2)
            k4 = derivatives(state + dt * k3)

            state = state + (dt / 6) * (
                k1 + 2 * k2 + 2 * k3 + k4
            )

            trajectory.append(state[:3].copy())

        trajectory = np.array(trajectory)

        # -----------------------------------------------------
        # Charged particle and its trajectory
        # -----------------------------------------------------
        particle = Sphere(
            radius=0.13,
            resolution=(12, 12),
            color=GREEN,
        )
        particle.set_fill(GREEN, opacity=1)
        particle.move_to(trajectory[0])

        charge_symbol = MathTex(
            "+", color=BLACK
        ).scale(0.55)
        charge_symbol.move_to(particle.get_center())

        # Display the complete path as it is traced
        path = TracedPath(
            particle.get_center,
            stroke_color=GREEN,
            stroke_width=3,
        )

        time_tracker = ValueTracker(0)

        def update_particle(mob):
            index = time_tracker.get_value() / dt
            index = np.clip(index, 0, len(trajectory) - 1)

            i = int(index)
            j = min(i + 1, len(trajectory) - 1)
            alpha = index - i

            position = (
                (1 - alpha) * trajectory[i]
                + alpha * trajectory[j]
            )
            mob.move_to(position)

        particle.add_updater(update_particle)

        charge_symbol.add_updater(
            lambda mob: mob.move_to(particle.get_center())
        )

        # -----------------------------------------------------
        # Show the new magnetic-field setup
        # -----------------------------------------------------

        # Group the magnetic-field setup
        magnetic_setup = VGroup(
            north_plate,
            south_plate,
            north_label,
            south_label,
            magnetic_arrows,
        )

        # Keep the particle path and particle together for viewing
        moving_objects = VGroup(
            magnetic_setup,
            path,
            particle,
            charge_symbol,
        )

        self.add(moving_objects)

        # Animate title
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.5)


        # -----------------------------------------------------
        # Smooth multi-axis camera rotation
        # -----------------------------------------------------

        camera_time = 0.0

        initial_phi = 65 * DEGREES
        initial_theta = -45 * DEGREES

        def rotate_camera(mob, dt):
            nonlocal camera_time
            camera_time += dt

            # Dynamically vary elevation and azimuth
            phi = initial_phi + 18 * DEGREES * np.sin(
                0.7 * camera_time
            )

            theta = initial_theta + 0.45 * camera_time

            self.camera.set_phi(phi)
            self.camera.set_theta(theta)

        camera_driver = VectorizedPoint(ORIGIN)
        camera_driver.add_updater(rotate_camera)
        self.add(camera_driver)

        # Particle motion and camera rotation run simultaneously
        self.play(
            time_tracker.animate.set_value(total_time),
            run_time=total_time,
            rate_func=linear,
        )

        camera_driver.clear_updaters()
        self.remove(camera_driver)

        particle.clear_updaters()
        charge_symbol.clear_updaters()

