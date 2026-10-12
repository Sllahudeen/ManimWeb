
from manim import *
from manim.renderer.shader import FullScreenQuad
import numpy as np


FRAGMENT_SHADER = r"""
#version 330

uniform vec2 u_resolution;
uniform vec3 u_cam_pos;
uniform vec3 u_cam_target;
uniform float u_zoom;

out vec4 fragColor;


// ------------------------------------------------------------
// Approximate gravitational ray bending
// ------------------------------------------------------------

vec3 get_acceleration(vec3 pos, vec3 dir, float rs)
{
    float r_sq = max(dot(pos, pos), 0.0001);
    float r = sqrt(r_sq);

    vec3 L_vec = cross(pos, dir);
    float L_sq = dot(L_vec, L_vec);

    return -(1.5 * rs * L_sq / (r_sq * r_sq * r))
           * (pos / r);
}


// ------------------------------------------------------------
// Flamm paraboloid
// ------------------------------------------------------------

float grid_height(float rho, float rs)
{
    float rho_safe = max(rho, rs + 0.05);

    float flamm = 2.0 * sqrt(rs * (rho_safe - rs));
    float flamm_outer = 2.0 * sqrt(rs * (25.0 - rs));

    return min(0.0, flamm - flamm_outer);
}


float surface_function(vec3 pos, float rs)
{
    return pos.y - grid_height(length(pos.xz), rs);
}


// ------------------------------------------------------------
// Main ray tracer
// ------------------------------------------------------------

void main()
{
    const float rs = 2.5;

    vec3 background = vec3(0.005, 0.005, 0.015);
    vec3 color = background;

    // Screen coordinates; zoom < 1 narrows the field of view
    vec2 uv = (gl_FragCoord.xy - 0.5 * u_resolution)
              / u_resolution.y;

    uv *= u_zoom;

    // Camera basis, recalculated every frame
    vec3 forward = normalize(u_cam_target - u_cam_pos);
    vec3 right = normalize(cross(forward, vec3(0.0, 1.0, 0.0)));
    vec3 up = cross(right, forward);

    vec3 ray_dir = normalize(
        forward + uv.x * right + uv.y * up
    );

    vec3 ray_pos = u_cam_pos;

    // --------------------------------------------------------
    // Integrate the ray
    // --------------------------------------------------------

    for (int i = 0; i < 250; i++)
    {
        float r = length(ray_pos);

        // Black-hole horizon
        if (r <= rs)
        {
            color = vec3(0.0);
            break;
        }

        // Escaped ray
        if (r > 65.0)
        {
            break;
        }

        float dt = clamp(0.025 * r, 0.025, 0.65);

        vec3 previous_pos = ray_pos;
        vec3 previous_dir = ray_dir;

        // RK4 integration of the original approximate model

        vec3 k1p = previous_dir;
        vec3 k1d = get_acceleration(
            previous_pos, previous_dir, rs
        );

        vec3 d2 = normalize(previous_dir + 0.5 * dt * k1d);
        vec3 p2 = previous_pos + 0.5 * dt * k1p;

        vec3 k2p = d2;
        vec3 k2d = get_acceleration(p2, d2, rs);

        vec3 d3 = normalize(previous_dir + 0.5 * dt * k2d);
        vec3 p3 = previous_pos + 0.5 * dt * k2p;

        vec3 k3p = d3;
        vec3 k3d = get_acceleration(p3, d3, rs);

        vec3 d4 = normalize(previous_dir + dt * k3d);
        vec3 p4 = previous_pos + dt * k3p;

        vec3 k4p = d4;
        vec3 k4d = get_acceleration(p4, d4, rs);

        ray_pos = previous_pos + (dt / 6.0) *
            (k1p + 2.0 * k2p + 2.0 * k3p + k4p);

        ray_dir = normalize(previous_dir + (dt / 6.0) *
            (k1d + 2.0 * k2d + 2.0 * k3d + k4d));


        // ----------------------------------------------------
        // Accretion disk intersection: y = 0
        // ----------------------------------------------------

        if (previous_pos.y * ray_pos.y <= 0.0
            && abs(previous_pos.y - ray_pos.y) > 0.00001)
        {
            float t = previous_pos.y
                    / (previous_pos.y - ray_pos.y);

            vec3 intersect = mix(previous_pos, ray_pos, t);
            float disk_r = length(intersect.xz);

            if (disk_r >= 2.85 && disk_r <= 10.35)
            {
                vec3 disk_tangent = normalize(
                    vec3(-intersect.z, 0.0, intersect.x)
                );

                float doppler = 1.0
                    + dot(ray_dir, disk_tangent) * 0.35;

                float edge_factor = clamp(
                    (disk_r - 2.85) / 7.5, 0.0, 1.0
                );

                vec3 disk_color = mix(
                    vec3(1.0, 0.45, 0.1),
                    vec3(0.7, 0.05, 0.0),
                    pow(edge_factor, 1.5)
                );

                disk_color *= clamp(doppler, 0.5, 1.5);

                color = disk_color;
                break;
            }
        }


        // ----------------------------------------------------
        // Flamm paraboloid grid intersection
        // ----------------------------------------------------

        float f0 = surface_function(previous_pos, rs);
        float f1 = surface_function(ray_pos, rs);

        if (f0 * f1 <= 0.0)
        {
            float lo = 0.0;
            float hi = 1.0;

            for (int j = 0; j < 6; j++)
            {
                float mid = 0.5 * (lo + hi);
                vec3 test_pos = mix(previous_pos, ray_pos, mid);

                float fm = surface_function(test_pos, rs);

                if (f0 * fm <= 0.0)
                {
                    hi = mid;
                }
                else
                {
                    lo = mid;
                    f0 = fm;
                }
            }

            float t_hit = 0.5 * (lo + hi);
            vec3 grid_pos = mix(previous_pos, ray_pos, t_hit);

            float rho = length(grid_pos.xz);

            if (abs(grid_pos.x) < 25.0
                && abs(grid_pos.z) < 25.0
                && rho > rs + 0.2)
            {
                float dx = abs(grid_pos.x - round(grid_pos.x));
                float dz = abs(grid_pos.z - round(grid_pos.z));
                float line_dist = min(dx, dz);

                if (line_dist < 0.06)
                {
                    float redshift = 1.0 / sqrt(
                        max(1.0 - rs / rho, 0.001)
                    );

                    vec3 base_color = vec3(0.25, 0.3, 0.35);

                    vec3 redshifted_color = base_color *
                        vec3(
                            1.0,
                            0.7 + 0.3 / redshift,
                            0.5 + 0.5 / redshift
                        );

                    float brightness = clamp(
                        1.0 - 0.5 * rs / rho,
                        0.3,
                        1.0
                    );

                    color = redshifted_color * brightness;
                    break;
                }
            }
        }
    }

    fragColor = vec4(color, 1.0);
}
"""


class BlackHoleShader(ThreeDScene):

    def construct(self):

        # ----------------------------------------------------
        # Create full-screen shader quad
        # ----------------------------------------------------

        resolution = (
            float(config.pixel_width),
            float(config.pixel_height)
        )

        shader_quad = FullScreenQuad(
            self.renderer.context,
            fragment_shader_source=FRAGMENT_SHADER,
        )

        shader_quad.shader.set_uniform(
            "u_resolution", resolution
        )

        # ----------------------------------------------------
        # Camera trackers
        # ----------------------------------------------------

        angle = ValueTracker(0.0)   # Azimuthal orbit angle
        phi = ValueTracker(0.0)     # Additional elevation angle
        zoom = ValueTracker(1.0)    # 1.0 normal; 0.5 zoomed in

        camera_distance = 50.0
        base_elevation = np.radians(12.0)

        shader_quad.shader.set_uniform("u_zoom", 1.0)

        # ----------------------------------------------------
        # Update camera uniforms
        # ----------------------------------------------------

        def update_camera(mob):

            azimuth = angle.get_value()
            elevation = base_elevation + phi.get_value()

            cx = (
                camera_distance
                * np.sin(azimuth)
                * np.cos(elevation)
            )

            cy = camera_distance * np.sin(elevation)

            cz = (
                camera_distance
                * np.cos(azimuth)
                * np.cos(elevation)
            )

            mob.shader.set_uniform(
                "u_cam_pos",
                (float(cx), float(cy), float(cz))
            )

            mob.shader.set_uniform(
                "u_cam_target",
                (0.0, 0.0, 0.0)
            )

            mob.shader.set_uniform(
                "u_zoom",
                float(zoom.get_value())
            )

        update_camera(shader_quad)
        shader_quad.add_updater(update_camera)
        self.add(shader_quad)

        # ----------------------------------------------------
        # Camera animation: 20 seconds total
        # ----------------------------------------------------

        phi_30 = np.radians(30.0)

        # Phase 1: phi = 0 -> +30 degrees
        # Zoom: 1.0 -> 0.75
        self.play(
            angle.animate.set_value(PI / 2),
            phi.animate.set_value(phi_30),
            zoom.animate.set_value(0.75),
            run_time=5,
            rate_func=linear,
        )

        # Phase 2: phi = +30 -> -30 degrees
        # This is a -60-degree swing.
        # Zoom: 0.75 -> 0.5
        self.play(
            angle.animate.set_value(PI),
            phi.animate.set_value(-phi_30),
            zoom.animate.set_value(0.5),
            run_time=5,
            rate_func=linear,
        )

        # Phase 3: phi = -30 -> 0 degrees
        self.play(
            angle.animate.set_value(3 * PI / 2),
            phi.animate.set_value(0.0),
            run_time=5,
            rate_func=linear,
        )

        # Phase 4: complete azimuthal orbit
        # Hold phi = 0 and zoom = 0.5
        self.play(
            angle.animate.set_value(TAU),
            run_time=5,
            rate_func=linear,
        )

        shader_quad.remove_updater(update_camera)

        self.wait(1)
