from manim import *
from PIL import Image
import numpy as np

# ============================================================
# TEXTURED 3D SPHERE
# ============================================================

class TexturedSphere(Surface):

    def __init__(self, radius, texture_file, **kwargs):

        self.radius = radius

        # Load the image
        self.texture = Image.open(texture_file).convert("RGB")

        # Mathematical sphere
        def sphere(u, v):

            x = radius * np.sin(v) * np.cos(u)
            y = radius * np.sin(v) * np.sin(u)
            z = radius * np.cos(v)

            return np.array([x, y, z])

        super().__init__(
            sphere,
            u_range=[0, TAU],
            v_range=[0, PI],
            resolution=(100, 50),
            checkerboard_colors=False,
            fill_color=WHITE,
            fill_opacity=1,
            stroke_width=0,
            **kwargs
        )

        # Put the image onto the sphere
        self.apply_texture()

    def apply_texture(self):

        width, height = self.texture.size

        for face in self.submobjects:

            x, y, z = face.get_center()

            # Longitude
            longitude = np.arctan2(y, x)

            # Latitude
            latitude = np.arcsin(
                np.clip(z / self.radius, -1, 1)
            )

            # Image coordinates
            u = (longitude + PI) / TAU
            v = 0.5 - latitude / PI

            px = int(
                np.clip(
                    u * (width - 1),
                    0,
                    width - 1
                )
            )

            py = int(
                np.clip(
                    v * (height - 1),
                    0,
                    height - 1
                )
            )

            # RGB
            r, g, b = self.texture.getpixel((px, py))

            color = rgb_to_color(
                np.array([r, g, b]) / 255
            )

            face.set_fill(
                color=color,
                opacity=1
            )


# ============================================================
# SCENE
# ============================================================
config.frame_rate = 60
class solar(ThreeDScene):

    def construct(self):

        # ----------------------------------------------------
        # CAMERA
        # ----------------------------------------------------

        self.set_camera_orientation(
            phi=70 * DEGREES,
            theta=0 * DEGREES,
            zoom=1.2
        )

        # ====================================================
        # SUN
        # ====================================================

        sun = TexturedSphere(
            radius=1.5,
            texture_file="sun.jpg"
        )

        sun.move_to(ORIGIN)

        self.add(sun)

        # ====================================================
        # SUN GLOW
        # ====================================================

        for i in range(49):

            glow = Sphere(
                radius=1.5 * (1.00 + 0.01 * i),
                resolution=(40, 24)
            )

            glow.set_fill(
                color=YELLOW,
                opacity=0.16 / (i + 1)
            )

            glow.set_stroke(
                width=0,
                opacity=0
            )

            glow.move_to(ORIGIN)

            self.add(glow)

        # ====================================================
        # EARTH
        # ====================================================

        earth = TexturedSphere(
            radius=0.6,
            texture_file="earth.jpg"
        )

        earth.move_to(6.5 * UP)

        self.add(earth)

        # ====================================================
        # ORBIT
        # ====================================================

        orbit = Circle(
            radius=6.5,
            color=WHITE,
            stroke_width=1,
            stroke_opacity=0.5
        )

        self.add(orbit)

        # ====================================================
        # ORBITAL ANGLE
        # ====================================================

        orbit_angle = ValueTracker(0)

        # ====================================================
        # EARTH POSITION
        # ====================================================

        def earth_position():

            angle = orbit_angle.get_value()

            return np.array([
                6.5 * np.sin(angle),
                6.5 * np.cos(angle),
                0
            ])

        # ====================================================
        # EARTH ORBIT
        # ====================================================

        earth.add_updater(
            lambda m, dt: m.move_to(
                earth_position()
            )
        )

        # ====================================================
        # EARTH SELF-SPIN
        # ====================================================

        earth.add_updater(
            lambda m, dt: m.rotate(
                2 * PI * dt,
                axis=OUT,
                about_point=m.get_center()
            )
        )

        # ====================================================
        # FUNCTION TO CREATE SHEET
        # ====================================================

        def create_sheet(angle):

            # ------------------------------------------------
            # EARTH POSITION
            # ------------------------------------------------

            xe = 6.5 * np.sin(angle)
            ye = 6.5 * np.cos(angle)

            # ------------------------------------------------
            # CURVATURE
            # ------------------------------------------------

            def curvature(u, v):

                # Sun's Gaussian well
                sun_well = 2.5 * np.exp(
                    -(u ** 2 + v ** 2)
                    / (2 * 5.0 ** 2)
                )

                # Earth's Gaussian well
                earth_well = 0.5 * np.exp(
                    -((u - xe) ** 2 + (v - ye) ** 2)
                    / (2 * 1.2 ** 2)
                )

                # Total curvature
                z = -(sun_well + earth_well)

                return np.array([
                    u,
                    v,
                    z
                ])

            # ------------------------------------------------
            # SURFACE
            # ------------------------------------------------

            return Surface(
                curvature,
                u_range=[-12, 12],
                v_range=[-12, 12],
                resolution=(30, 30),
                checkerboard_colors=False,
                fill_color=GREY_BROWN,
                fill_opacity=0.5,
                stroke_width=0.3
            )

        # ====================================================
        # INITIAL SHEET
        # ====================================================

        sheet = create_sheet(0)

        self.add(sheet)

        # ====================================================
        # SHEET UPDATE
        # ====================================================

        def update_sheet(mob, dt):

            angle = orbit_angle.get_value()

            new_sheet = create_sheet(angle)

            mob.become(new_sheet)

        sheet.add_updater(update_sheet)

        self.move_camera(
            theta=180 * DEGREES,
            zoom=0.7,
            added_anims=[
                orbit_angle.animate.set_value(5 * TAU)
            ],
            run_time=10,
            rate_func=linear
        )
        earth.clear_updaters()
        sheet.clear_updaters()