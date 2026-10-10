from manim import *
import numpy as np

class RSH(ThreeDScene):
    def construct(self):
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.5)  # Start rotation
        # Define manually added real spherical harmonics (r(θ, φ) values)
        harmonics = [
            {
                "label": r"Y_0^0 = 1",
                "func": lambda theta, phi: 1
            },
            {
                "label": r"Y_1^{-1} = \sin\phi \sin\theta",
                "func": lambda theta, phi: np.sin(phi) * np.sin(theta)
            },
            {
                "label": r"Y_1^0 = \cos\theta",
                "func": lambda theta, phi: np.cos(theta)
            },
            {
                "label": r"Y_1^1 = \cos\phi \sin\theta",
                "func": lambda theta, phi: np.cos(phi) * np.sin(theta)
            },

            {
                "label": r"Y_2^{-2} = \sin^2(\theta) \sin(2\phi)",
                "func": lambda theta, phi:  (np.sin(theta) ** 2) * np.sin(2 * phi)
            },
            {
                "label": r"Y_2^{-1} =  \sin(\theta) \cos(\theta) \sin(\phi)",
                "func": lambda theta, phi: 2 * np.sin(theta) * np.cos(theta) * np.sin(phi)
            },
            {
                "label": r"Y_2^{0} = \frac{1}{2} (3\cos^2(\theta) - 1)",
                "func": lambda theta, phi: (1 / 2) * (3 * np.cos(theta) ** 2 - 1)
            },
            {
                "label": r"Y_2^{1} =  \sin(\theta) \cos(\theta) \cos(\phi)",
                "func": lambda theta, phi: 2 * np.sin(theta) * np.cos(theta) * np.cos(phi)
            },
            {
                "label": r"Y_2^{2} =  \sin^2(\theta) \cos(2\phi)",
                "func": lambda theta, phi:  (np.sin(theta) ** 2) * np.cos(2 * phi)
            },
            {
                "label": r"Y_3^{-3} = \sin^3(\theta)\sin(3\phi)",
                "func": lambda theta, phi: (np.sin(theta) ** 3) * np.sin(3 * phi)
            },
            {
                "label": r"Y_3^{-2} = \sin^2(\theta)\cos(\theta)\sin(2\phi)",
                "func": lambda theta, phi: 2 * ((np.sin(theta) ** 2) * np.cos(theta) * np.sin(2 * phi))
            },
            {
                "label": r"Y_3^{-1} = \sin(\theta)(5\cos^2(\theta) - 1)\sin(\phi)",
                "func": lambda theta, phi: (1 / 2) * (np.sin(theta) * (5 * np.cos(theta) ** 2 - 1) * np.sin(phi))
            },
            {
                "label": r"Y_3^{0} = 5\cos^3(\theta) - 3\cos(\theta)",
                "func": lambda theta, phi: (1 / 2) * (5 * np.cos(theta) ** 3 - 3 * np.cos(theta))
            },
            {
                "label": r"Y_3^{1} = \sin(\theta)(5\cos^2(\theta) - 1)\cos(\phi)",
                "func": lambda theta, phi: (1 / 2) * (np.sin(theta) * (5 * np.cos(theta) ** 2 - 1) * np.cos(phi))
            },
            {
                "label": r"Y_3^{2} = \sin^2(\theta)\cos(\theta)\cos(2\phi)",
                "func": lambda theta, phi: 2 * ( (np.sin(theta) ** 2) * np.cos(theta) * np.cos(2 * phi) )
            },
            {
                "label": r"Y_3^{3} = \sin^3(\theta)\cos(3\phi)",
                "func": lambda theta, phi: (np.sin(theta) ** 3) * np.cos(3 * phi)
            }
        ]

        # Loop over harmonics
        for harmonic in harmonics:
            r_func = harmonic["func"]
            label_text = harmonic["label"]

            def parametric_surface(u, v):
                theta = u  # [0, π]
                phi = v    # [0, 2π]
                r_val = 2 * r_func(theta, phi)
                r = np.abs(r_val)
                x = r * np.sin(theta) * np.cos(phi)
                y = r * np.sin(theta) * np.sin(phi)
                z = r * np.cos(theta)
                return np.array([x, y, z])

            surface = Surface(
                lambda u, v: parametric_surface(u, v),
                u_range=[0, PI],
                v_range=[0, TAU],
                resolution=(75, 150),
                fill_opacity=0.85,
                checkerboard_colors=[RED, YELLOW],
                stroke_width=0
            )

            label = MathTex(label_text).scale(1.5).to_corner(UL)
            self.add_fixed_in_frame_mobjects(label)
            self.add(surface, label)
            self.wait(1)
            self.remove(surface, label)

        self.stop_ambient_camera_rotation()  # End rotation

