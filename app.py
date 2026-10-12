from flask import Flask, render_template

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import os


app = Flask(__name__)


projects = [

    {


    "name": "Black Holes",
    "slug": "black-holes",
    "description": r"""
    <div class="physics-description">

        <p class="description-intro">
            This project visualizes gravitational light bending around
            a non-rotating black hole using Schwarzschild geometry as
            the theoretical framework. The implementation combines
            approximate numerical ray propagation, fourth-order
            Runge-Kutta integration, GLSL fragment shading, procedural
            rendering, surface-intersection detection, and animated
            camera control.
        </p>

        <h3>Part I — Physics and Mathematical Formulation</h3>

        <h4>1. Schwarzschild Spacetime</h4>

        <p>
            The Schwarzschild solution describes the exterior spacetime
            of a static, spherically symmetric, uncharged black hole.
            In geometrized units, G = c = 1, its metric is
        </p>

        <div class="equation">
            \[
            ds^2=-\left(1-\frac{2M}{r}\right)dt^2
            +\left(1-\frac{2M}{r}\right)^{-1}dr^2
            +r^2d\Omega^2.
            \]
        </div>

        <p>
            Restoring physical units, the Schwarzschild radius is
        </p>

        <div class="equation">
            \[
            r_s=\frac{2GM}{c^2}.
            \]
        </div>

        <p>
            The event horizon is located at r = r_s. The geometry
            determines how freely propagating light moves through
            curved spacetime.
        </p>

        <h4>2. Null Geodesics and the Orbit of Light</h4>

        <p>
            Photons follow null geodesics, for which ds² = 0. By
            exploiting spherical symmetry and the conserved energy E
            and angular momentum L, the radial equation can be written
            as
        </p>

        <div class="equation">
            \[
            \left(\frac{dr}{d\lambda}\right)^2
            =\frac{E^2}{c^2}
            -\left(1-\frac{r_s}{r}\right)\frac{L^2}{r^2}.
            \]
        </div>

        <p>
            Introducing the inverse radial coordinate u = 1/r and
            the impact parameter b = Lc/E gives the Schwarzschild
            null-orbit equation
        </p>

        <div class="equation">
            \[
            \boxed{
            \frac{d^2u}{d\phi^2}+u
            =\frac32 r_su^2
            }.
            \]
        </div>

        <p>
            The nonlinear term is responsible for the relativistic
            correction to the flat-space orbital equation. It allows
            light to undergo gravitational deflection and, for suitable
            initial conditions, strong lensing near the black hole.
        </p>

        <h4>3. Photon Sphere and Critical Impact Parameter</h4>

        <p>
            Schwarzschild spacetime has an unstable circular photon
            orbit at the photon sphere:
        </p>

        <div class="equation">
            \[
            r_{\mathrm{ph}}=\frac{3GM}{c^2}
            =\frac32 r_s.
            \]
        </div>

        <p>
            The critical impact parameter for an incoming photon is
        </p>

        <div class="equation">
            \[
            b_{\mathrm{crit}}=3\sqrt{3}\frac{GM}{c^2}.
            \]
        </div>

        <p>
            Incoming rays with impact parameters above the critical
            value can scatter back outward, while rays below it are
            captured in the idealized Schwarzschild problem. The
            unstable photon orbit is closely related to strong
            gravitational lensing near a black hole.
        </p>

        <h4>4. Why an Accretion Disk Forms</h4>

        <p>
            Matter approaching a black hole generally carries angular
            momentum. Instead of falling directly inward, gas tends
            to orbit the central object. Collisions, turbulence, and
            angular-momentum transport allow some material to spiral
            inward while transferring angular momentum outward.
            Dissipation heats the gas, which can radiate energy.
            Damping of motion perpendicular to the orbital plane helps
            produce a flattened accretion disk.
        </p>

        <p>
            For a Schwarzschild black hole, the innermost stable
            circular orbit of massive test particles is
        </p>

        <div class="equation">
            \[
            r_{\mathrm{ISCO}}=\frac{6GM}{c^2}=3r_s.
            \]
        </div>

        <p>
            The ISCO is distinct from the photon sphere. This animation
            renders a procedural disk for visualization; it does not
            solve the hydrodynamics, magnetic turbulence, or radiative
            transfer of a real accretion flow.
        </p>

        <h3>Part II — Numerical and Graphical Implementation</h3>

        <h4>5. Approximate Ray-Bending Model</h4>

        <p>
            The GLSL shader propagates a ray through three-dimensional
            space. Let x be its position, n its unit direction, and
            r = |x|. The code constructs an angular-momentum-like
            vector
        </p>

        <div class="equation">
            \[
            \boldsymbol{\ell}=\mathbf{x}\times\mathbf{n},
            \qquad
            \ell^2=\boldsymbol{\ell}\cdot\boldsymbol{\ell}.
            \]
        </div>

        <p>
            The approximate acceleration used by the shader has the
            form
        </p>

        <div class="equation">
            \[
            \mathbf{a}
            =-\frac{3r_s\ell^2}{2r^5}\hat{\mathbf r},
            \qquad
            \hat{\mathbf r}=\frac{\mathbf{x}}{r}.
            \]
        </div>

        <p>
            The ray is advanced according to the approximate system
        </p>

        <div class="equation">
            \[
            \frac{d\mathbf{x}}{ds}=\mathbf{n},
            \qquad
            \frac{d\mathbf{n}}{ds}=\mathbf{a}.
            \]
        </div>

        <p>
            This is the spatial ray-bending model used for rendering.
            It should not be confused with an exact integration of
            the Schwarzschild null-geodesic equations presented in
            Part I.
        </p>

        <h4>6. Fourth-Order Runge-Kutta Integration</h4>

        <p>
            A numerical integrator is needed to advance the ray through
            the spatially varying acceleration field. The classical
            fourth-order Runge-Kutta method evaluates the differential
            equation at four intermediate stages:
        </p>

        <div class="equation">
            \[
            \begin{aligned}
            k_1&=f(y_n),\\
            k_2&=f(y_n+\tfrac h2k_1),\\
            k_3&=f(y_n+\tfrac h2k_2),\\
            k_4&=f(y_n+hk_3),\\
            y_{n+1}&=y_n+
            \frac h6(k_1+2k_2+2k_3+k_4).
            \end{aligned}
            \]
        </div>

        <p>
            Here y represents the coupled ray variables and h is the
            numerical step size. The shader adapts its step according
            to the current radius:
        </p>

        <div class="equation">
            \[
            h=\operatorname{clamp}(0.025r,\;0.025,\;0.65).
            \]
        </div>

        <p>
            The direction vector is normalized during the integration
            to maintain a unit propagation direction. The ray loop
            terminates when the ray reaches the horizon, escapes the
            chosen rendering region, or reaches the iteration limit.
            RK4 provides a numerical approximation, whose accuracy
            depends on step size and the chosen model.
        </p>

        <h4>7. Procedural Accretion Disk</h4>

        <p>
            The shader represents the disk as a plane at y = 0.
            When a ray crosses this plane, the code estimates the
            intersection point and computes the cylindrical radius
        </p>

        <div class="equation">
            \[
            r_{\mathrm{disk}}=\sqrt{x^2+z^2}.
            \]
        </div>

        <p>
            The visible disk occupies the radial interval
        </p>

        <div class="equation">
            \[
            2.85\leq r_{\mathrm{disk}}\leq10.35.
            \]
        </div>

        <p>
            Radial color variation produces the glowing appearance.
            A directional brightness factor based on the local
            tangential direction imitates the brighter approaching
            side of a rotating disk. This is a visual approximation,
            not a complete relativistic Doppler and radiative-transfer
            calculation.
        </p>

        <h4>8. Flamm-Paraboloid Embedding</h4>

        <p>
            The curved spatial grid is based on the Flamm-paraboloid
            embedding function
        </p>

        <div class="equation">
            \[
            z_{\mathrm F}(r)=2\sqrt{r_s(r-r_s)}.
            \]
        </div>

        <p>
            This surface illustrates the intrinsic spatial geometry
            of a constant-time Schwarzschild slice through an
            embedding diagram. The shader checks ray-surface
            intersections and refines the intersection by bisection.
            Procedurally defined grid lines are then rendered on the
            surface. The embedding is a geometric visualization,
            not a literal membrane in spacetime.
        </p>

        <h4>9. GLSL Fragment Shader</h4>

        <p>
            Manim supplies a FullScreenQuad on which the GLSL
            fragment shader renders the scene. For each pixel, the
            shader generates a ray from the camera through the image
            plane and advances it through the approximate ray-bending
            model. It determines whether the ray intersects the
            black-hole horizon, accretion disk, or curved grid and
            assigns the corresponding color.
        </p>

        <p>
            Performing this work per pixel exploits GPU parallelism
            and avoids creating thousands of individual Manim objects.
            The disk texture, brightness gradients, and grid appearance
            are generated procedurally. A ring-like appearance in a
            rendered image is not, by itself, evidence that an exact
            photon-ring calculation has been performed.
        </p>

        <h4>10. Camera Animation</h4>

        <p>
            Manim ValueTracker objects control the azimuth, elevation
            offset, and zoom. The camera position is reconstructed
            from spherical coordinates:
        </p>

        <div class="equation">
            \[
            \begin{aligned}
            x_c&=R\sin\alpha\cos\beta,\\
            y_c&=R\sin\beta,\\
            z_c&=R\cos\alpha\cos\beta.
            \end{aligned}
            \]
        </div>

        <p>
            Here R is the camera distance, alpha is the azimuth, and
            beta is the total elevation. An updater transfers the
            current camera parameters to the shader every frame.
            The camera moves through staged rotations and zoom changes
            to reveal the disk and curved spatial grid from different
            viewpoints. These camera movements change the view, not
            the underlying ray equations.
        </p>

        <h3>Techniques Demonstrated</h3>

        <ul>
            <li>Schwarzschild geometry and null-geodesic theory.</li>
            <li>Approximate three-dimensional ray propagation.</li>
            <li>Fourth-order Runge-Kutta numerical integration.</li>
            <li>Adaptive step sizing and direction normalization.</li>
            <li>GLSL fragment shading and GPU-based ray marching.</li>
            <li>Ray-plane and ray-surface intersection detection.</li>
            <li>Bisection refinement and procedural grid rendering.</li>
            <li>Manim ValueTrackers, camera motion, and zoom animation.</li>
        </ul>

        </div>
        """,
        "video": "BlackHoleShader.mp4",
        "code": "source_code/shader.py"


    },

    {

        "name": "Curved Spacetime",
        "slug": "Curved-Spacetime",
        "description": """
        <h3>Part I — Physics and Mathematical Structure</h3>

        <p>
        This animation explores the geometric intuition behind curved space:
        a massive object can be represented schematically by a depression in a
        spatial surface, while a smaller body moves through the surrounding
        geometry. The scene contains a textured Sun at the origin, a textured
        Earth moving along a circular orbit, and a continuously reconstructed
    surface whose shape depends on the instantaneous position of the Earth.
    </p>

    <h4>1. Parametric representation of a sphere</h4>

    <p>
    Both the Sun and the Earth are constructed as parametric surfaces.
    A sphere of radius <i>R</i> is described by two angular coordinates,
    longitude-like parameter <i>u</i> and polar angle <i>v</i>:
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    \\begin{aligned}
    x(u,v)&=R\\sin v\\cos u,\\\\
    y(u,v)&=R\\sin v\\sin u,\\\\
    z(u,v)&=R\\cos v,
    \\end{aligned}
    \\]
    \\[
    0\\leq u\\leq 2\\pi,\\qquad
    0\\leq v\\leq \\pi.
    \\]
    </p>

    <p>
    These equations generate the spherical geometry before any texture is
    applied. The Sun uses radius \\(R_\\odot=1.5\\), while the Earth uses
    radius \\(R_\\oplus=0.6\\) in the animation's visual coordinate system.
    These radii are chosen for presentation and are not to scale with the
    actual astronomical radii.
    </p>

    <h4>2. Circular orbital motion</h4>

    <p>
    The Earth's position is controlled by an orbital angle
    \\(\\theta(t)\\). Its trajectory is a circle of radius \\(a=6.5\\)
    in the \\(xy\\)-plane:
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    \\begin{aligned}
    x_E(t)&=a\\sin\\theta(t),\\\\
    y_E(t)&=a\\cos\\theta(t),\\\\
    z_E(t)&=0.
    \\end{aligned}
    \\]
    </p>

    <p>
    The orbit is therefore prescribed geometrically rather than calculated
    from Newton's gravitational equations. During the ten-second camera
    animation, the angle increases from zero to \\(10\\pi\\), corresponding
    to five complete revolutions at constant angular speed:
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    \\theta(t)=\\omega t,\\qquad
    \\omega=\\frac{5(2\\pi)}{10}=\\pi\\ \\text{rad s}^{-1}.
    \\]
    </p>

    <p>
    This gives a controlled, uniform orbit that makes the relationship
    between the Earth's position and the changing surface easy to observe.
    It is a visualization of prescribed orbital motion, not a simulation
    that derives the orbit from the gravitational field.
    </p>

    <h4>3. Constructing the curvature-like surface</h4>

    <p>
    The central mathematical object is a surface defined as the graph of
    a height function \\(z(u,v)\\). The code superposes two negative
    Gaussian profiles: one centered at the Sun and another centered at
    the Earth's current orbital position.
    </p>

    <p>
    The Sun's contribution is
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    W_\\odot(u,v)=
    2.5\\exp\\!\\left[
    -\\frac{u^2+v^2}{2(5.0)^2}
    \\right].
    \\]
    </p>

    <p>
    The Earth's contribution is
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    W_\\oplus(u,v;t)=
    0.5\\exp\\!\\left[
    -\\frac{
    (u-x_E(t))^2+(v-y_E(t))^2
    }{2(1.2)^2}
    \\right].
    \\]
    </p>

    <p>
    The resulting height is the negative sum of the two profiles:
    </p>

    <p style="text-align:center; font-size:1.1em;">
    \\[
    \\boxed{
    z(u,v;t)=-\\left[
    W_\\odot(u,v)+W_\\oplus(u,v;t)
    \\right]
    }
    \\]
    </p>

    <p>
    Consequently, the complete surface is parameterized by
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    \\mathbf{X}(u,v;t)=
    \\bigl(u,\\ v,\\ z(u,v;t)\\bigr),
    \\qquad -12\\leq u,v\\leq12.
    \\]
    </p>

    <p>
    The amplitude of each Gaussian determines the depth of its depression,
    while its width determines how broadly the depression extends across
    the surface. The Sun's profile is deeper and broader; the Earth's
    profile is shallower and more localized. As the Earth moves, the
    center of its Gaussian depression moves with it, so the landscape
    changes throughout the animation.
    </p>

    <p>
    <strong>Physical interpretation and limitation:</strong>
    the depressions provide a visual analogy for gravitational geometry.
    However, the height function is a deliberately chosen sum of Gaussian
    functions. It is not derived from the Schwarzschild metric, the
    Einstein field equations, or the actual Gaussian curvature
    \\(K\\) of a specified spacetime metric. In particular, the plotted
    height \\(z(u,v;t)\\) should not itself be identified with the
    Gaussian curvature. A genuine curvature calculation would require
    specifying a metric and calculating its curvature from that metric.
    </p>

    <h3>Part II — How the Animation Is Implemented in Python and Manim</h3>

    <h4>1. Custom textured spheres</h4>

    <p>
    The code defines a class called <code>TexturedSphere</code> by
    subclassing Manim's <code>Surface</code>. Its spherical parameterization
    generates the mesh, with resolution \\((100,50)\\), and the class then
    maps a loaded image onto its faces.
    </p>

    <p>
    For each mesh face, the code obtains its center
    \\((x,y,z)\\), estimates the corresponding longitude and latitude,
    and converts them into image coordinates:
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    \\lambda=\\operatorname{atan2}(y,x),\\qquad
    \\varphi=\\arcsin\\!\\left(
    \\operatorname{clip}\\!\\left(\\frac{z}{R},-1,1\\right)
    \\right),
    \\]
    \\[
    U=\\frac{\\lambda+\\pi}{2\\pi},\\qquad
    V=\\frac12-\\frac{\\varphi}{\\pi}.
    \\]
    </p>

    <p>
    The normalized coordinates \\((U,V)\\) are converted into pixel
    indices, and the corresponding RGB color is assigned to the face.
    This produces recognizable solar and terrestrial textures using
    <code>PIL</code> for image loading and Manim's
    <code>rgb_to_color</code> for color conversion.
    </p>

    <h4>2. Layered glow around the Sun</h4>

    <p>
    The Sun's glow is produced by adding 49 translucent spheres around
    the main solar sphere. The radius of layer \\(i\\) is
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    R_i=1.5\\left(1+0.01i\\right),
    \\qquad i=0,1,\\ldots,48,
    \\]
    </p>

    <p>
    and its opacity is
    </p>

    <p style="text-align:center; font-size:1.05em;">
    \\[
    \\alpha_i=\\frac{0.16}{i+1}.
    \\]
    </p>

    <p>
    The layers become progressively larger and more transparent. Their
    overlapping yellow fills create a soft, approximate glow without
    requiring a separate lighting or volumetric-rendering simulation.
    The spheres are static decorative layers centered at the origin.
    </p>

    <h4>3. Updaters and the orbital angle tracker</h4>

    <p>
    Manim's <code>ValueTracker</code> stores the orbital angle. An updater
    moves the Earth to the position calculated by
    <code>earth_position()</code> on each frame. A second updater rotates
    the Earth about its own center, using the fixed axis
    <code>OUT</code> and the increment \\(2\\pi\\,dt\\), where
    \\(dt\\) is the elapsed time for the frame. This corresponds to
    one full self-rotation per second at the configured animation rate.
    The spin is an illustrative choice, not an astronomical timescale.
    </p>

    <p>
    The circular orbit itself is drawn as a white
    <code>Circle</code> of radius 6.5 with reduced stroke opacity.
    The Earth's movement and spin are therefore handled separately:
    one changes its orbital position, while the other changes its
    orientation about its center.
    </p>

    <h4>4. Rebuilding the surface as the Earth moves</h4>

    <p>
    The function <code>create_sheet(angle)</code> evaluates the two
    Gaussian profiles at the supplied orbital angle and constructs a
    new Manim <code>Surface</code>. The sheet is initially created with
    angle zero. Its updater then reads the current tracker value, creates
    a replacement surface, and applies it to the existing object using
    <code>mob.become(new_sheet)</code>.
    </p>

    <p>
    This technique keeps the surface synchronized with the Earth's
    motion, making the smaller depression follow the Earth. The sheet
    uses a mesh resolution of \\((30,30)\\), a semi-transparent
    grey-brown fill, and visible mesh strokes. Reconstructing a surface
    repeatedly is computationally more expensive than updating only
    its vertices, but it is straightforward and makes the dependence
    on the orbital angle explicit.
    </p>

    <h4>5. Three-dimensional camera motion</h4>

    <p>
    The scene uses <code>ThreeDScene</code> and starts with camera
    parameters \\(\\phi=70^\\circ\\), \\(\\theta=0^\\circ\\), and
    zoom 1.2. During the ten-second animation, <code>move_camera</code>
    changes the camera azimuth to \\(180^\\circ\\) and the zoom to 0.7,
    while the orbital tracker advances to \\(10\\pi\\). The
    <code>linear</code> rate function makes the tracked orbital angle
    increase uniformly over that interval.
    </p>

    <p>
    The changing viewpoint reveals the surface and the orbital motion
    from a different perspective. At the end, the Earth and sheet
    updaters are cleared, preventing further updates after the main
    animation has finished.
    </p>

    <h4>Summary of techniques</h4>

    <ul>
      <li><strong>Parametric geometry:</strong> custom spherical meshes and a height-field surface.</li>
      <li><strong>Image mapping:</strong> longitude/latitude-based texture sampling with PIL and NumPy.</li>
      <li><strong>Procedural visual effects:</strong> layered transparent spheres for the solar glow.</li>
      <li><strong>Time-dependent animation:</strong> a ValueTracker, frame updaters, and a linear camera animation.</li>
      <li><strong>Dynamic geometry:</strong> repeated surface construction using <code>create_sheet()</code> and <code>mob.become()</code>.</li>
      <li><strong>Three-dimensional presentation:</strong> controlled camera orientation, zoom, and a circular orbital path.</li>
    </ul>

    <p>
    Together, these methods combine mathematical parameterization,
    procedural graphics, and time-dependent geometry to present an
    intuitive visual analogy for curved space while keeping the distinction
    between the illustrative model and a physical gravitational solution
    explicit.
    </p>
    """,
        "video": "solar.mp4",
        "code": "source_code/solarsys.py"
    },

    {

    "name": "3D Rotations",
    "slug": "3D-Rotations",
    "description": r"""
    <h3>Part I — Mathematical Structure of Three-Dimensional Rotations</h3>

    <p>
    This animation explores three-dimensional rotational geometry using a regular tetrahedron. It first rotates the tetrahedron about an axis whose direction changes continuously with time. It then demonstrates rotations about three axes directed from the center of the tetrahedron toward selected vertices. These stages illustrate the difference between rotation about a moving axis and rotation about a fixed axis.
    </p>

    <h4>1. Constructing the tetrahedron</h4>

    <p>The four vertices are defined by the vectors</p>

    <p style="text-align:center;">
    \[
    \begin{aligned}
    \mathbf v_1&=(1,1,1),\\
    \mathbf v_2&=(1,-1,-1),\\
    \mathbf v_3&=(-1,1,-1),\\
    \mathbf v_4&=(-1,-1,1).
    \end{aligned}
    \]
</p>

<p>
All four vertices lie at the same distance from the origin:
</p>

<p style="text-align:center;">
\[
\|\mathbf v_i\|=\sqrt{3}.
\]
</p>

<p>
The distance between any two distinct vertices is \(2\sqrt{2}\), so these vertices define a regular tetrahedron. The origin is its center. The symmetry of this geometry makes axes passing through the center and a vertex particularly useful for studying rotations.
</p>

<h4>2. Rotation in three dimensions</h4>

<p>
A rotation is specified by an angle \(\alpha\), a unit axis vector \(\hat{\mathbf n}\), and a rotation center. For a point \(\mathbf r\) measured relative to that center, Rodrigues' rotation formula is
</p>

<p style="text-align:center;">
\[
\begin{aligned}
\mathbf r'={}&\mathbf r\cos\alpha
+(\hat{\mathbf n}\times\mathbf r)\sin\alpha\\
&+\hat{\mathbf n}(\hat{\mathbf n}\cdot\mathbf r)(1-\cos\alpha).
\end{aligned}
\]
</p>

<p>
This formula separates the rotation angle from the axis direction. Manim handles the geometric transformation through its rotation methods; the code does not explicitly implement Rodrigues' formula.
</p>

<h4>3. The moving rotation axis</h4>

<p>
During the first stage, the endpoint of the green arrow moves along a circle at height \(z=1\). Its position is
</p>

<p style="text-align:center;">
\[
\mathbf h(t)=
\begin{pmatrix}
\cos t\\
\sin t\\
1
\end{pmatrix}.
\]
</p>

<p>
The red curve shows this trajectory for \(0\leq t\leq2\pi\). The green arrow extends from the origin to the current point on that curve. The instantaneous rotation axis is the line through the origin and \(\mathbf h(t)\), so its unit direction is
</p>

<p style="text-align:center;">
\[
\boxed{
\hat{\mathbf n}(t)=
\frac{\mathbf h(t)}{\|\mathbf h(t)\|}
=
\frac{1}{\sqrt{2}}
\begin{pmatrix}
\cos t\\
\sin t\\
1
\end{pmatrix}
}
\]
</p>

<p>
Normalization ensures that the direction vector has unit length. As the arrow moves, the rotation axis changes direction continuously, sweeping around the vertical axis.
</p>

<h4>4. Angular increments and changing orientation</h4>

<p>
The animation advances its internal time variable by the frame duration \(dt\):
</p>

<p style="text-align:center;">
\[
t\leftarrow t+dt.
\]
</p>

<p>
The angular speed parameter is \(\omega=3\), and the applied angular increment per frame is
</p>

<p style="text-align:center;">
\[
\boxed{d\alpha=\omega\,dt=3\,dt.}
\]
</p>

<p>
At each frame, the tetrahedron is rotated about the newly calculated axis direction. It therefore undergoes a succession of small rotations about changing axes, rather than a single rotation about one permanently fixed axis.
</p>

<p>
Rotations about different axes generally do not commute. For two general rotation matrices \(R_1\) and \(R_2\),
</p>

<p style="text-align:center;">
\[
R_1R_2\neq R_2R_1.
\]
</p>

<p>
Thus, the order in which rotations are applied can affect the final orientation. The animation illustrates this feature of three-dimensional rotational geometry, although it does not explicitly calculate rotation matrices or commutators.
</p>

<p>
<strong>Physical interpretation:</strong> this is prescribed kinematic motion. The code does not derive the axis evolution from a torque, angular-momentum conservation, or Euler's equations for a freely rotating rigid body. The parameter \(\omega=3\) controls the applied angular increment; it is not a solution of a rigid-body dynamics problem.
</p>

<h4>5. Rotations about vertex axes</h4>

<p>
After the moving-axis stage, the code obtains the tetrahedron's current vertex positions and constructs three colored arrows. Each arrow starts at the origin and points toward a selected vertex. The corresponding axis direction is
</p>

<p style="text-align:center;">
\[
\hat{\mathbf a}_i=
\frac{\mathbf v_i}{\|\mathbf v_i\|}.
\]
</p>

<p>
The tetrahedron is then rotated through a full revolution about each selected axis:
</p>

<p style="text-align:center;">
\[
\alpha=2\pi.
\]
</p>

<p>
Each axis passes through the center and a vertex. For a regular tetrahedron, this is a threefold symmetry axis: a rotation of \(120^\circ\) maps the tetrahedron onto itself. A full \(360^\circ\) rotation also returns every point to its initial position relative to that fixed axis.
</p>

<p>
These demonstrations emphasize that different axes generate different intermediate trajectories, even when a complete revolution returns the object to its starting orientation.
</p>

<h3>Part II — How the Animation Is Implemented in Python and Manim</h3>

<h4>1. Three-dimensional scene and camera</h4>

<p>
The scene subclasses <code>ThreeDScene</code> and initializes the camera with
</p>

<p style="text-align:center;">
\[
\phi=65^\circ,\qquad
\theta=-45^\circ,\qquad
\text{zoom}=0.7.
\]
</p>

<p>
The oblique camera view makes the tetrahedron's faces, vertices, and changing axis easier to distinguish. Three <code>Arrow3D</code> objects represent the Cartesian axes, extending from \(-5\) to \(+5\) along each coordinate direction.
</p>

<h4>2. Constructing the triangular faces</h4>

<p>
Each face is a Manim <code>Polygon</code> defined by three of the four vertex vectors. The four polygons are collected into a single <code>VGroup</code> named <code>tetrahedron</code>. Grouping the faces ensures that transformations are applied to the entire geometric object rather than to isolated faces.
</p>

<p>
The faces use partially transparent fills and visible outlines. This makes the edges and overlapping geometry easier to interpret in the three-dimensional view.
</p>

<h4>3. Drawing the axis trajectory and arrow</h4>

<p>
A <code>ParametricFunction</code> draws the red circular trajectory. The initial green arrow extends from the origin to \((1,0,1)\). On each frame, <code>put_start_and_end_on()</code> updates the arrow's endpoint to \(\mathbf h(t)\), while its starting point remains at the origin.
</p>

<p>
The red circle indicates the path traced by the arrowhead, whereas the green arrow displays the instantaneous rotation-axis direction.
</p>

<h4>4. Frame-by-frame updater</h4>

<p>
The function <code>update_system(m, dt)</code> is attached to the tetrahedron using <code>add_updater()</code>. Each frame performs three operations:
</p>

<ul>
<li>Increment the internal time variable by the frame duration.</li>
<li>Calculate the arrowhead position and normalize it to obtain the current rotation axis.</li>
<li>Rotate the tetrahedron by \(3\,dt\) about that axis and update the arrow's endpoint.</li>
</ul>

<p>
The scene waits six seconds while the updater runs. The tetrahedron receives many small transformations, with the axis direction recalculated on every frame. Because the angular increment is proportional to \(dt\), the motion is designed to depend on elapsed time rather than simply on the number of rendered frames.
</p>

<p>
After this stage, <code>clear_updaters()</code> stops the continuous motion. The scene briefly pauses and removes the green arrow and red trajectory before beginning the fixed-axis demonstrations.
</p>

<h4>5. Extracting the current vertex directions</h4>

<p>
Because the tetrahedron has already rotated, the code obtains vertex positions from the transformed polygons rather than relying exclusively on the original coordinates. It constructs three arrows from the origin along selected vertex directions, normalizing each direction and scaling the arrows to length 2 for display.
</p>

<p>
Green, red, and yellow distinguish the three axes. Each arrow is displayed during its corresponding rotation and removed afterward.
</p>

<h4>6. Full rotations using Manim's Rotate animation</h4>

<p>
The fixed-axis stage uses Manim's <code>Rotate</code> animation with angle \(2\pi\), the selected vertex vector as the rotation axis, and <code>ORIGIN</code> as the rotation center. Each rotation lasts three seconds.
</p>

<p>
Unlike the earlier frame updater, which recalculates the axis continuously, each <code>Rotate</code> call uses one fixed axis for its entire turn. The contrast between these two animation techniques is a central feature of the project.
</p>

<h4>Summary of computational techniques</h4>

<ul>
<li><strong>Vector geometry:</strong> Cartesian coordinates define the tetrahedron and its rotation axes.</li>
<li><strong>Parametric curves:</strong> sine and cosine describe the circular trajectory.</li>
<li><strong>Axis normalization:</strong> the instantaneous direction is converted to a unit vector before rotation.</li>
<li><strong>Frame-based animation:</strong> a Manim updater uses \(dt\) to apply small rotations continuously.</li>
<li><strong>Grouped geometry:</strong> a <code>VGroup</code> keeps all four faces together during transformations.</li>
<li><strong>Sequential transformations:</strong> <code>Rotate</code> demonstrates full revolutions about three selected axes.</li>
<li><strong>Three-dimensional rendering:</strong> <code>ThreeDScene</code>, <code>Arrow3D</code>, and camera orientation provide spatial context.</li>
</ul>

<p>
Overall, this project combines vector mathematics and real-time geometric transformations to illustrate how an object's orientation changes under rotations about moving and fixed axes. It is a visualization of rotational geometry rather than a simulation of torque-driven rigid-body dynamics.
</p>
""",
        "video": "tetra.mp4",
        "code": "source_code/moext.py"
    },

    {

    "name": "Shortest Path Under Constant Acceleration",
    "slug": "shortest-path-under-constant-acceleration",
    "description": r"""
<h3>Part I — Physics and Mathematical Foundations</h3>

<p>
This animation compares three different trajectories connecting two points:
a straight line, a sinusoidal curve, and a cycloidal curve associated with
the classical brachistochrone problem. The central idea is that the path
with the shortest geometric length need not be the path that takes the
least time to traverse.
</p>

<h4>1. Distance versus travel time</h4>

<p>
Imagine releasing a small bead from rest and allowing it to slide under
gravity along a frictionless track. A straight track may have the shortest
length between two endpoints, but the bead's acceleration depends on the
slope of the track. A curved track can allow the bead to descend steeply
at first, gaining speed quickly, before approaching the final point.
Consequently, a longer trajectory can sometimes be traversed in less time.
</p>

<p>
The travel time along a path is
</p>

<p style="text-align:center;">
\[
T=\int_{\text{path}}\frac{ds}{v},
\]
</p>

<p>
where \(ds\) is an infinitesimal arc length and \(v\) is the bead's speed
at that point. Minimizing the total distance \(\int ds\) is therefore a
different problem from minimizing the time integral above.
</p>

<h4>2. Speed acquired under gravity</h4>

<p>
For a frictionless bead released from rest, conservation of mechanical
energy gives
</p>

<p style="text-align:center;">
\[
\frac12 mv^2+mgy=mgy_0,
\]
</p>

<p>
where \(y\) is the vertical coordinate measured upward, \(y_0\) is the
release height, and \(g\) is gravitational acceleration. Solving for
the speed gives
</p>

<p style="text-align:center;">
\[
\boxed{v(y)=\sqrt{2g(y_0-y)}}.
\]
</p>

<p>
The speed depends on the vertical drop, not simply on the distance
traveled along the track. Substituting this result into the travel-time
integral gives
</p>

<p style="text-align:center;">
\[
T=\int
\frac{\sqrt{1+(dy/dx)^2}}
{\sqrt{2g(y_0-y)}}\,dx.
\]
</p>

<p>
The brachistochrone problem asks which curve minimizes this functional
between specified endpoints. Its classical solution is a cycloid, under
the assumptions of a bead released from rest, uniform gravity, and
frictionless motion.
</p>

<h4>3. The cycloid</h4>

<p>
A cycloid is the curve traced by a point on the circumference of a
circle as the circle rolls along a straight line without slipping.
With a suitable choice of origin and scale, it can be parameterized as
</p>

<p style="text-align:center;">
\[
\boxed{
\begin{aligned}
x(\theta)&=a(\theta-\sin\theta),\\
y(\theta)&=a(1-\cos\theta).
\end{aligned}
}
\]
</p>

<p>
Here, \(a\) sets the length scale and \(\theta\) is a dimensionless
parameter. The parameterization combines linear progress with periodic
sine and cosine terms. Its derivatives are
</p>

<p style="text-align:center;">
\[
\frac{dx}{d\theta}=a(1-\cos\theta),
\qquad
\frac{dy}{d\theta}=a\sin\theta.
\]
</p>

<p>
The arc-length element follows from
\(ds=\sqrt{dx^2+dy^2}\):
</p>

<p style="text-align:center;">
\[
\begin{aligned}
ds
&=a\sqrt{(1-\cos\theta)^2+\sin^2\theta}\,d\theta\\
&=2a\left|\sin\frac{\theta}{2}\right|d\theta.
\end{aligned}
\]
</p>

<p>
Together with energy conservation, this structure leads to a particularly
simple travel-time integral for the appropriate descending cycloidal
branch. The cycloid is the exact minimum-time solution for the ideal
classical brachistochrone problem.
</p>

<p>
<strong>Important qualification:</strong> the animation uses the
cycloidal parameterization to draw a comparison curve, but its selected
parameter interval and endpoint construction are not a derivation of
the minimum-time solution for the displayed endpoints. The animation
should therefore be understood as an illustration of the brachistochrone
idea, rather than a numerical verification of the classical result.
</p>

<h4>4. The three trajectories in this animation</h4>

<p>
The endpoints are initially defined as
</p>

<p style="text-align:center;">
\[
\mathbf r_{\mathrm{start}}=(\pi,2,0),
\qquad
\mathbf r_{\mathrm{end}}=
\left(\frac{3\pi}{2}+1,1,0\right).
\]
</p>

<p>
The animation constructs three colored curves:
</p>

<ul>
<li><strong>Blue — Straight line:</strong> the direct segment connecting the endpoints.</li>
<li><strong>Green — Sinusoidal path:</strong> a curve constructed from a sine function plus a linear term.</li>
<li><strong>Red — Cycloidal path:</strong> a segment of the parameterized curve \(x(\theta)=\theta-\sin\theta\), \(y(\theta)=1-\cos\theta\).</li>
</ul>

<p>
The sinusoidal path is defined in the code by
</p>

<p style="text-align:center;">
\[
\boxed{
f(x)=-0.2\sin(4x)
-\frac{2(0.2\sin 8+1)}{\pi+2}(x-\pi)+2.
}
\]
</p>

<p>
The linear term controls the overall trend, while the sine term introduces
an oscillation. The curve is a prescribed comparison path; it is not
derived by minimizing the travel-time functional.
</p>

<p>
The endpoints and the displayed curves are transformed together for
presentation. The paths are therefore primarily a visual comparison
of different geometric choices, not a calibrated experimental setup
with physical units.
</p>

<h3>Part II — Python and Manim Implementation</h3>

<h4>1. Defining points and curves</h4>

<p>
The scene is implemented as a Manim <code>Scene</code>. NumPy arrays
represent the endpoints as three-dimensional vectors, with the
\(z\)-coordinate set to zero so that the paths lie in a plane.
</p>

<p>
The straight trajectory is created with <code>Line(start, end)</code>.
The sinusoidal trajectory uses <code>ParametricFunction</code> with
position vector
</p>

<p style="text-align:center;">
\[
\mathbf r_{\mathrm{sin}}(x)=
\begin{pmatrix}
x\\
f(x)\\
0
\end{pmatrix}.
\]
</p>

<p>
The cycloidal trajectory is also constructed with
<code>ParametricFunction</code>:
</p>

<p style="text-align:center;">
\[
\mathbf r_{\mathrm{cyc}}(\theta)=
\begin{pmatrix}
\theta-\sin\theta\\
1-\cos\theta\\
0
\end{pmatrix},
\qquad
\pi\leq\theta\leq\frac{3\pi}{2}.
\]
</p>

<p>
The code uses \(a=1\) implicitly in this parameterization. The curve
is drawn in red to distinguish it from the straight and sinusoidal
alternatives.
</p>

<h4>2. Adding guide lines</h4>

<p>
Two white vertical lines descend from the endpoints to the horizontal
level \(y=-1\). A third white line connects their lower endpoints.
These lines create a rectangular-like frame around the lower part
of the scene and provide a visual reference for the endpoints and
their relative heights.
</p>

<p>
The paths and guide lines are grouped in a <code>VGroup</code> named
<code>scene_elements</code>. The entire group is shifted left by 2
units, scaled by a factor of 1.5, and shifted downward by 2 units.
Grouping the geometry makes it possible to apply these presentation
transformations consistently.
</p>

<h4>3. Moving dots and frame updaters</h4>

<p>
Three white dots are used to represent motion along the three paths.
Each dot has an updater that stores a progress variable
\(\alpha\in[0,1]\). At every frame, the updater advances this variable
by a chosen amount proportional to the frame duration \(dt\):
</p>

<p style="text-align:center;">
\[
\begin{aligned}
\alpha_{\mathrm{line}}&\leftarrow
\min\left(1,\alpha_{\mathrm{line}}+\frac{dt}{3}\right),\\
\alpha_{\mathrm{sin}}&\leftarrow
\min\left(1,\alpha_{\mathrm{sin}}+\frac{dt}{2}\right),\\
\alpha_{\mathrm{cyc}}&\leftarrow
\min\left(1,\alpha_{\mathrm{cyc}}+dt\right).
\end{aligned}
\]
</p>

<p>
The dots are then positioned using
<code>point_from_proportion(alpha)</code> on their respective curves.
This method returns a point according to the curve's normalized
parameterization. It does not calculate the position from Newton's
equations of motion or determine the speed from the local slope.
</p>

<p>
The chosen progress rates make the dots reach the ends of their paths
after approximately three seconds, two seconds, and one second,
respectively, assuming a consistent animation time step. This creates
a visible comparison of three different prescribed motion schedules.
</p>

<h4>4. Title and mathematical equations</h4>

<p>
The animation displays the title
<em>Brachistochrone: The least time path</em> and presents the
cycloid parameterization in two equations:
</p>

<p style="text-align:center;">
\[
x(t)=a(t-\sin t),
\qquad
y(t)=a(1-\cos t).
\]
</p>

<p>
Manim's <code>Text</code> class creates the title, while
<code>MathTex</code> renders the equations using LaTeX. The equations
are arranged vertically with <code>VGroup</code> and
<code>arrange()</code>, and positioned below the title with
<code>next_to()</code>. A <code>SurroundingRectangle</code> creates
the orange frame around the equations.
</p>

<p>
The title and equations are introduced using <code>Write</code>;
the surrounding box is drawn using <code>Create</code>. Explicit
run times control the pace of these visual introductions.
</p>

<h4>5. What would be needed for a physical simulation?</h4>

<p>
To turn this visual comparison into a genuine dynamical study, one
would need to use a consistent coordinate convention, ensure that
all paths connect the same endpoints, and derive the bead's motion
along each path under gravity. For a frictionless track with arc
length coordinate \(s\) and height \(y(s)\), the tangential equation
of motion is
</p>

<p style="text-align:center;">
\[
\frac{d^2s}{dt^2}=-g\frac{dy}{ds},
\]
</p>

<p>
when \(s\) increases in the direction of travel and \(y\) is measured
upward. The initial condition for a bead released from rest is
\(\dot{s}(0)=0\). Integrating this equation, or using energy
conservation together with the path geometry, would produce the
motion and arrival time for each curve.
</p>

<p>
The arrival times could then be compared directly, with the cycloid
optimized for the specified endpoints. That would distinguish a
physically computed result from a visualization that assigns motion
rates for presentation.
</p>

<h4>Summary of computational techniques</h4>

<ul>
<li><strong>Parametric geometry:</strong> <code>Line</code> and <code>ParametricFunction</code> construct the competing paths.</li>
<li><strong>NumPy coordinates:</strong> arrays specify endpoints and points in the scene.</li>
<li><strong>Grouped transformations:</strong> <code>VGroup</code>, <code>shift()</code>, and <code>scale()</code> position the geometry together.</li>
<li><strong>Frame-based animation:</strong> updaters and <code>dt</code> control the three moving dots.</li>
<li><strong>Normalized curve progress:</strong> <code>point_from_proportion()</code> places each dot along its chosen path.</li>
<li><strong>Mathematical typesetting:</strong> <code>MathTex</code> displays the cycloid equations.</li>
<li><strong>Scene composition:</strong> <code>Text</code>, <code>Write</code>, <code>Create</code>, and <code>SurroundingRectangle</code> introduce the title and equations.</li>
</ul>

<p>
The animation introduces the geometric intuition behind the brachistochrone
problem and demonstrates how Python and Manim can construct curves,
coordinate moving objects, and present mathematical equations. Its
current motion is illustrative rather than a numerical solution of
the minimum-time problem under gravity.
</p>
""",
        "video": "bc.mp4",
        "code": "source_code/Brachistochrone.py"
    },

    {
         "name": "Spherical Harmonics",
         "slug": "spherical-harmonics",
         "video": "RSH.mp4",
         "code": "source_code/H_orbitals.py",
         "description": r"""
    <h2>Part I: Physics and Mathematical Background</h2>

    <h3>1. What are spherical harmonics?</h3>

    <p>
    Spherical harmonics are special functions defined on the surface of a
    sphere. They arise naturally when solving differential equations in
    spherical coordinates, particularly problems with rotational symmetry.
    They are important in quantum mechanics, atomic physics, gravitational
    physics, electromagnetic theory, and many other areas of mathematical
    physics.
    </p>

    <p>
    In quantum mechanics, spherical harmonics describe the angular
    dependence of wavefunctions for systems with spherical symmetry.
    For the hydrogen atom, the wavefunction separates into a radial part
    and an angular part:
    </p>

    <p style="text-align:center;">
    \[
    \psi_{nlm}(r,\theta,\phi)
    =R_{nl}(r)Y_l^m(\theta,\phi).
    \]
    </p>

    <p>
    Here, \(R_{nl}(r)\) describes the radial dependence, while
    \(Y_l^m(\theta,\phi)\) describes the angular dependence. The quantum
    numbers \(l\) and \(m\) determine important features of the angular
    structure. In particular, \(l\) is the orbital angular-momentum
    quantum number, and \(m\) labels its projection along a chosen axis.
    </p>

    <h3>2. Spherical coordinates</h3>

    <p>
    The animation uses spherical coordinates, where \(\theta\) is the
    polar angle measured from the positive \(z\)-axis and \(\phi\) is the
    azimuthal angle in the \(xy\)-plane. A point at radial distance \(r\)
    has Cartesian coordinates
    </p>

    <p style="text-align:center;">
    \[
    x=r\sin\theta\cos\phi,\qquad
    y=r\sin\theta\sin\phi,\qquad
    z=r\cos\theta.
    \]
    </p>

    <p>
    To visualize an angular function as a three-dimensional surface,
    its value can be used to define a radius that varies with direction.
    This converts an abstract function of two angles into a geometric
    shape.
    </p>

    <h3>3. From an angular function to a surface</h3>

    <p>
    In this project, each selected real angular function is denoted by
    \(f(\theta,\phi)\). The code defines the displayed radial distance as
    </p>

    <p style="text-align:center;">
    \[
    r_{\mathrm{display}}=2|f(\theta,\phi)|.
    \]
    </p>

    <p>
    Substituting this radius into the spherical-coordinate equations
    produces the surface. Directions in which the function has a large
    absolute value extend farther from the origin, while directions
    where it vanishes approach the origin. The resulting lobes and
    nodal structures provide a geometric way to explore angular
    dependence.
    </p>

    <p>
    The absolute value is significant: it removes the sign of the
    function. Consequently, the visualization does not distinguish
    positive and negative phases by opposite radial directions or
    by a sign-dependent color scheme.
    </p>

    <h3>4. The angular functions explored</h3>

    <p>
    The program cycles through 15 manually defined real functions
    associated with angular patterns for degrees \(l=0,1,2,3\).
    Examples include the constant function
    </p>

    <p style="text-align:center;">
    \[
    f(\theta,\phi)=1,
    \]
    </p>

    <p>
    the degree-one functions
    </p>

    <p style="text-align:center;">
    \[
    f(\theta,\phi)=\cos\theta,
    \qquad
    f(\theta,\phi)=\sin\theta\cos\phi,
    \]
    </p>

    <p>
    and the degree-two angular patterns
    </p>

    <p style="text-align:center;">
    \[
    f(\theta,\phi)=\frac{1}{2}
    (3\cos^2\theta-1),
    \]
    </p>

    <p style="text-align:center;">
    \[
    f(\theta,\phi)=\sin^2\theta\cos(2\phi).
    \]
    </p>

    <p>
    Higher-degree functions introduce more intricate angular variation.
    Their dependence on trigonometric factors creates additional
    directions in which the function vanishes, producing more elaborate
    shapes.
    </p>

    <p>
    <strong>Physical interpretation:</strong> spherical harmonics are
    angular factors in atomic wavefunctions, but the surfaces shown here
    are geometric representations of manually specified functions.
    They are not complete hydrogen-atom orbitals: the radial wavefunction
    \(R_{nl}(r)\) is not calculated, and the displayed radius is based
    on the absolute value of the angular function rather than on the
    probability density \(|\psi|^2\). The functions are also not
    consistently normalized using the conventional spherical-harmonic
    normalization.
    </p>

    <h2>Part II: Python and Manim Implementation</h2>

    <h3>1. Three-dimensional scene and camera</h3>

    <p>
    The class <code>RSH</code> inherits from Manim's
    <code>ThreeDScene</code>, which provides a three-dimensional scene
    and camera. The initial camera orientation is set using
    <code>phi=70 * DEGREES</code> and
    <code>theta=45 * DEGREES</code>. Ambient camera rotation is started
    at a rate of <code>0.5</code>, allowing each surface to be viewed
    from changing angles.
    </p>

    <h3>2. Storing the angular functions</h3>

    <p>
    The list named <code>harmonics</code> contains dictionaries.
    Each dictionary has two entries: <code>label</code>, which stores
    the mathematical expression displayed on screen, and
    <code>func</code>, a Python lambda function that evaluates the
    corresponding angular expression.
    </p>

    <p>
    For example, the degree-one function
    <code>np.cos(theta)</code> is evaluated numerically using NumPy.
    The list-based design makes it possible to reuse the same surface
    construction procedure for every function.
    </p>

    <h3>3. Parametric construction of each surface</h3>

    <p>
    The loop over <code>harmonics</code> retrieves the current function
    and its label. The nested function <code>parametric_surface(u, v)</code>
    interprets its two inputs as the polar and azimuthal angles:
    </p>

    <ul>
      <li><code>theta = u</code> varies from \(0\) to \(\pi\).</li>
      <li><code>phi = v</code> varies from \(0\) to \(2\pi\).</li>
      <li><code>r_val = 2 * r_func(theta, phi)</code> evaluates the scaled angular function.</li>
      <li><code>r = np.abs(r_val)</code> makes the displayed radius nonnegative.</li>
    </ul>

    <p>
    The Cartesian coordinates are then calculated using
    <code>x = r * np.sin(theta) * np.cos(phi)</code>,
    <code>y = r * np.sin(theta) * np.sin(phi)</code>, and
    <code>z = r * np.cos(theta)</code>. The function returns these
    coordinates as a NumPy array, defining a point on the surface.
    </p>

    <h3>4. Rendering the surface</h3>

    <p>
    Manim's <code>Surface</code> class evaluates the parametric function
    over the angular domain. The resolution is set to
    <code>(75, 150)</code>, giving a relatively dense sampling of the
    two parameter directions. The surface uses a fill opacity of
    <code>0.85</code>, red and yellow checkerboard colors, and
    <code>stroke_width=0</code> to suppress the surface's drawn
    mesh outlines.
    </p>

    <p>
    The checkerboard colors help reveal the geometry of the surface.
    They are visual styling rather than a representation of the
    positive and negative signs of the angular function.
    </p>

    <h3>5. Mathematical labels and animation sequence</h3>

    <p>
    For each function, the code constructs a <code>MathTex</code>
    object from the stored label and scales it by a factor of
    <code>1.5</code>. The label is added using
    <code>add_fixed_in_frame_mobjects</code>, which keeps it fixed
    relative to the camera frame while the three-dimensional view
    rotates.
    </p>

    <p>
    The surface and its label are added to the scene, followed by
    <code>self.wait(1)</code>. The code then removes both objects
    before proceeding to the next function. This produces a sequence
    in which each angular pattern appears briefly with its mathematical
    expression.
    </p>

    <p>
    Finally, <code>stop_ambient_camera_rotation()</code> stops the
    camera's continuous rotation when the sequence has finished.
    </p>

    <h3>6. What the implementation demonstrates</h3>

    <p>
    The project illustrates a useful computational-physics workflow:
    define a mathematical function, evaluate it over a parameter space,
    map the numerical values into Cartesian coordinates, and render the
    resulting geometry. It connects analytical expressions with
    three-dimensional visualization and shows how changes in angular
    dependence lead to different spatial patterns.
    </p>

    <p>
    The construction is intended as a visual exploration of
    spherical-harmonic-like angular patterns. A more physically complete
    hydrogen-orbital visualization would use properly normalized
    spherical harmonics, retain their phase or sign information, include
    the appropriate radial wavefunction, and visualize a quantity such
    as \(|\psi_{nlm}(r,\theta,\phi)|^2\).
    </p>
    """,
    },

    {

    "name": "Evolution of Qubit",
    "slug": "evolution-of-qubit",
    "video": "BlochFieldEvolution.mp4",
    "code": "source_code/quantumdyn.py",
    "description": r"""
    <h2>Part I: Physics and Mathematical Background</h2>

    <h3>1. A qubit in a magnetic field</h3>

    <p>
    A qubit is the quantum-mechanical analogue of a two-level system.
    Unlike a classical bit, which takes one of two definite values,
    a qubit can occupy a coherent superposition of two basis states.
    A general pure qubit state can be written as
    </p>

    <p style="text-align:center;">
    \[
    |\psi(t)\rangle
    =\alpha(t)|0\rangle+\beta(t)|1\rangle,
    \qquad
    |\alpha(t)|^2+|\beta(t)|^2=1.
    \]
    </p>

    <p>
    The complex amplitudes \(\alpha(t)\) and \(\beta(t)\) determine
    the state and its measurement probabilities. In this project,
    the qubit evolves under a time-dependent magnetic field. The
    changing field modifies the Hamiltonian and therefore determines
    how the quantum state changes with time.
    </p>

    <h3>2. The time-dependent Hamiltonian</h3>

    <p>
    Using the convention \(\hbar=1\), the code defines the Hamiltonian
    as
    </p>

    <p style="text-align:center;">
    \[
    H(t)=-\frac{1}{2}\mathbf B(t)\cdot\boldsymbol{\sigma},
    \]
    </p>

    <p>
    where \(\boldsymbol{\sigma}=(\sigma_x,\sigma_y,\sigma_z)\)
    is the vector of Pauli matrices and
    \(\mathbf B(t)=(B_x(t),B_y(t),B_z(t))\) is the effective field.
    Explicitly,
    </p>

    <p style="text-align:center;">
    \[
    H(t)=-\frac12
    \begin{pmatrix}
    B_z(t) & B_x(t)-iB_y(t)\\
    B_x(t)+iB_y(t) & -B_z(t)
    \end{pmatrix}.
    \]
    </p>

    <p>
    The overall sign and the factor of one-half follow the convention
    selected in the source code. The field components are expressed in
    units consistent with \(\hbar=1\); a physical magnetic field would
    ordinarily enter together with the relevant gyromagnetic factor.
    </p>

    <h3>3. A rotating magnetic field</h3>

    <p>
    The field is prescribed to rotate in the \(xy\)-plane while retaining
    a constant component along the \(z\)-axis:
    </p>

    <p style="text-align:center;">
    \[
    \mathbf B(t)=
    \begin{pmatrix}
    B_\perp\cos(\Omega t)\\
    B_\perp\sin(\Omega t)\\
    B_z
    \end{pmatrix}.
    \]
    </p>

    <p>
    The transverse component has fixed magnitude \(B_\perp\), and its
    azimuthal angle increases with angular frequency \(\Omega\). The
    constant component \(B_z\) tilts the field away from the \(xy\)-plane.
    In the simulation, the parameters are
    </p>

    <p style="text-align:center;">
    \[
    B_\perp=0.8,\qquad B_z=0.35,
    \qquad \Omega=\frac{2\pi}{8}.
    \]
    </p>

    <p>
    The field completes one revolution every eight time units. The
    evolution duration is four such periods, or \(32\) time units.
    The field therefore completes four revolutions during the simulated
    quantum evolution.
    </p>

    <h3>4. Schrödinger time evolution</h3>

    <p>
    The state obeys the time-dependent Schrödinger equation
    </p>

    <p style="text-align:center;">
    \[
    i\frac{d}{dt}|\psi(t)\rangle=H(t)|\psi(t)\rangle.
    \]
    </p>

    <p>
    Equivalently,
    </p>

    <p style="text-align:center;">
    \[
    \frac{d}{dt}|\psi(t)\rangle=-iH(t)|\psi(t)\rangle.
    \]
    </p>

    <p>
    Because the Hamiltonian depends explicitly on time, the evolution
    cannot generally be obtained by applying a single constant
    Hamiltonian exponential. The source numerically integrates the
    differential equation, allowing the state to respond continuously
    to the rotating field.
    </p>

    <h3>5. The Bloch sphere representation</h3>

    <p>
    A pure qubit state can be represented by a point on the Bloch sphere.
    Its Bloch vector is defined by the expectation values of the Pauli
    matrices:
    </p>

    <p style="text-align:center;">
    \[
    \mathbf s(t)=
    \begin{pmatrix}
    \langle\sigma_x\rangle\\
    \langle\sigma_y\rangle\\
    \langle\sigma_z\rangle
    \end{pmatrix}
    =
    \begin{pmatrix}
    \langle\psi|\sigma_x|\psi\rangle\\
    \langle\psi|\sigma_y|\psi\rangle\\
    \langle\psi|\sigma_z|\psi\rangle
    \end{pmatrix}.
    \]
    </p>

    <p>
    For a normalized pure state, this vector has unit length. Its
    direction encodes the qubit state, with the north and south poles
    corresponding to the computational basis states \(|0\rangle\)
    and \(|1\rangle\).
    </p>

    <p>
    The animation uses a sphere of radius \(2\), so it multiplies the
    unit Bloch vectors by two before drawing the trajectory. This is
    a display scaling: it does not change the physical state.
    </p>

    <h3>6. The initial state and its evolution</h3>

    <p>
    The simulation begins with the state
    </p>

    <p style="text-align:center;">
    \[
    |\psi(0)\rangle=|+x\rangle
    =\frac{|0\rangle+|1\rangle}{\sqrt2}.
    \]
    </p>

    <p>
    Its Bloch vector points along the positive \(x\)-axis. As the
    magnetic field rotates, the state follows a trajectory determined
    by the full time-dependent Schrödinger equation. The path need not
    coincide with the instantaneous direction of the magnetic field:
    the state responds dynamically to the Hamiltonian rather than simply
    pointing along the field at every instant.
    </p>

    <p>
    The yellow arrow represents the instantaneous Bloch vector. A
    yellow fading trail marks its recent motion, while the red arrow
    represents the instantaneous field direction. The complete
    simulated qubit trajectory is revealed at the end so that its
    three-dimensional geometry can be examined.
    </p>

    <h2>Part II: Python, Qiskit, SciPy and Manim Implementation</h2>

    <h3>1. Defining the Pauli matrices</h3>

    <p>
    The source begins by defining the three Pauli matrices as complex
    NumPy arrays:
    <code>SIGMA_X</code>, <code>SIGMA_Y</code> and
    <code>SIGMA_Z</code>. The imaginary entries in
    \(\sigma_y\) require complex-valued arithmetic.
    </p>

    <p>
    The code also creates Qiskit's <code>Pauli</code> objects and
    stores them in the list <code>PAULI</code>. These are used to
    calculate the expectation values needed for the Bloch vector.
    </p>

    <h3>2. Constructing the Hamiltonian</h3>

    <p>
    The function <code>hamiltonian(B)</code> receives the three
    components of the field, unpacks them into <code>Bx</code>,
    <code>By</code> and <code>Bz</code>, and returns
    <code>-0.5 * (Bx * SIGMA_X + By * SIGMA_Y + Bz * SIGMA_Z)</code>.
    This directly implements the matrix expression for the chosen
    Hamiltonian.
    </p>

    <h3>3. Computing the Bloch vector with Qiskit</h3>

    <p>
    The function <code>bloch_vector(state)</code> converts the input
    into a Qiskit <code>Statevector</code> and evaluates its
    expectation value for each Pauli operator. The real parts of the
    three expectation values are collected into a NumPy array.
    This converts the quantum state into the three real coordinates
    used for the visualization.
    </p>

    <h3>4. Numerically integrating the Schrödinger equation</h3>

    <p>
    The function <code>rotating_field_trajectory</code> performs the
    numerical evolution. Its nested function <code>B_of_t(t)</code>
    calculates the field at any requested time using the prescribed
    rotating-field formula.
    </p>

    <p>
    The nested function <code>schrodinger_rhs(t, psi)</code> returns
    <code>-1j * hamiltonian(B_of_t(t)) @ psi</code>, which is the
    right-hand side of the Schrödinger equation. SciPy's
    <code>solve_ivp</code> integrates this differential equation from
    zero to the selected duration.
    </p>

    <p>
    The integration requests 600 equally spaced sample times through
    <code>t_eval</code> and uses relative and absolute tolerances
    of \(10^{-9}\) and \(10^{-11}\), respectively. These tolerances
    control the numerical solver's local error estimates; they do not
    mean that every result is guaranteed to have that exact accuracy.
    If the solver reports failure, the code raises a
    <code>RuntimeError</code>.
    </p>

    <p>
    At every sample, the state is normalized before its Bloch vector
    is computed. The final state is also normalized and returned
    together with the time samples, trajectory points and field
    function.
    </p>

    <h3>5. Creating the three-dimensional Bloch sphere</h3>

    <p>
    The Manim scene class <code>BlochFieldEvolution</code> inherits
    from <code>ThreeDScene</code>. The camera is initialized at
    \(\phi=70^\circ\) and \(\theta=-45^\circ\).
    A sphere of radius \(2\) is rendered with a translucent blue fill
    and a partially transparent blue outline. Three-dimensional axes
    are added to establish the coordinate directions.
    </p>

    <p>
    The initial Qiskit state is constructed from
    <code>np.array([1, 1], dtype=complex) / np.sqrt(2)</code>.
    Its Bloch vector is calculated and multiplied by two to match
    the radius of the displayed sphere. A yellow
    <code>Arrow3D</code> initially points from the origin toward
    this scaled vector.
    </p>

    <h3>6. Precomputing the full qubit path</h3>

    <p>
    The function <code>rotating_field_trajectory</code> is called
    with the field parameters, total duration and 600 samples. The
    returned Bloch vectors are multiplied by two and passed to
    <code>set_points_as_corners</code> to construct a yellow
    <code>VMobject</code> containing the complete trajectory.
    </p>

    <p>
    The helper function <code>point_at(u)</code> maps a normalized
    progress parameter \(u\in[0,1]\) to a position along the sampled
    path. It uses <code>np.interp</code> independently on each
    Cartesian coordinate. This allows the moving arrow and trail
    to follow the precomputed numerical solution.
    </p>

    <h3>7. Visualizing the magnetic-field direction</h3>

    <p>
    A red <code>ParametricFunction</code> represents a circular path
    traced by the rotating field at constant height. The field's
    displayed arrow is generated with <code>always_redraw</code>;
    its endpoint is calculated by evaluating <code>B_of_t</code>
    at the time associated with the current animation progress.
    A scale factor of \(1.8\) makes the field vector visible in
    the scene.
    </p>

    <p>
    There is an implementation detail worth distinguishing: the
    red reference curve is parameterized using
    \(\cos(2\pi u)\) and \(\sin(2\pi u)\), so it draws one
    revolution. The red arrow, however, uses the actual time
    \(t=32u\) in the field function and therefore makes four
    revolutions during the animation. The curve is a reference
    circle, not the full time-history of the arrow.
    </p>

    <h3>8. Animating the qubit and its fading trail</h3>

    <p>
    A <code>ValueTracker</code> named <code>progress</code>
    controls the animation parameter. The yellow
    <code>moving_arrow</code> is recreated using
    <code>always_redraw</code>, with its endpoint determined by
    <code>point_at(progress.get_value())</code>.
    </p>

    <p>
    The function <code>make_trail()</code> selects a short interval
    immediately behind the moving qubit, with a length of
    <code>0.30</code> in normalized path progress. It samples this
    interval at 35 points and constructs line segments between
    neighboring points.
    </p>

    <p>
    Each segment receives a width proportional to its position
    within the trail and an opacity proportional to the segment
    fraction raised to the power \(1.5\). This produces a trail
    that becomes thicker and more visible near the moving arrow.
    The trail is refreshed through <code>always_redraw</code>
    as the progress tracker changes.
    </p>

    <h3>9. The animation timeline and final camera view</h3>

    <p>
    The initial arrow is removed once the dynamic arrows and trail
    are ready. The tracker is then animated linearly from zero to
    one over 12 seconds. This means the 32 units of simulated
    physical time are displayed over 12 seconds of video; the
    video duration is not the physical evolution duration.
    </p>

    <p>
    After the evolution, the red field arrow, red reference curve
    and fading trail are removed. The complete yellow qubit path
    is added to the sphere. Ambient camera rotation is then started
    about the azimuthal direction, allowing the viewer to inspect
    the trajectory from different angles before the scene ends.
    </p>

    <h3>10. What this project demonstrates</h3>

    <p>
    This project combines a time-dependent quantum Hamiltonian,
    numerical differential-equation solving, Qiskit's state-vector
    and expectation-value tools, and Manim's three-dimensional
    animation system. It illustrates how a quantum state can be
    evolved numerically and translated into a geometric trajectory
    on the Bloch sphere.
    </p>

    <p>
    The resulting path is a numerical solution for the specified
    Hamiltonian and initial state, not an arbitrary curve drawn
    independently of the dynamics. The animation therefore connects
    the underlying quantum evolution with a geometric picture of
    the changing qubit state.
    </p>
    """,
    },

    {

    "name": "Double Pendulum",
    "slug": "double-pendulum",
    "video": "DoublePendulum.mp4",
    "code": "source_code/pendulum.py",
    "description": r"""
    <h2>Part I: Physics and Mathematical Background</h2>

    <h3>1. Introduction: When two simple pendulums become a complex dynamical system</h3>

    <p>
    A simple pendulum consists of a mass suspended from a fixed pivot
    by a rod or string. Under ideal conditions, its motion is periodic
    and can be described by a relatively simple differential equation.
    A double pendulum consists of two pendulums connected in series:
    the first mass is attached to a fixed support, while the second
    mass is attached to the first. Although each rod has a fixed length,
    the motion of one mass influences the motion of the other.
    </p>

    <p>
    This seemingly small modification produces a much richer dynamical
    system. The two masses exchange energy through their coupled motion,
    the effective torques depend on both angular coordinates, and the
    resulting equations are nonlinear. For suitable initial conditions,
    a double pendulum can display irregular motion and strong sensitivity
    to its initial state, making it a classic example used to study
    deterministic chaos.
    </p>

    <p>
    The animation is based on the equations of motion rather than on
    manually prescribed rotations. The initial angles and angular
    velocities determine the initial state. The equations then determine
    the angular accelerations at every instant, and numerical integration
    calculates how the entire system evolves.
    </p>

    <h3>2. Mechanical model and assumptions</h3>

    <p>
    The model contains two point masses, \(m_1\) and \(m_2\), connected
    by two rigid, massless rods of lengths \(L_1\) and \(L_2\). The
    upper rod is attached to a fixed pivot, and the lower rod connects
    the two masses. Gravitational acceleration is denoted by \(g\).
    </p>

    <p>
    The simulation uses the following parameter values:
    </p>

    <ul>
      <li>First mass: \(m_1=1.0\,\mathrm{kg}\).</li>
      <li>Second mass: \(m_2=1.0\,\mathrm{kg}\).</li>
      <li>First rod length: \(L_1=2.0\,\mathrm{m}\).</li>
      <li>Second rod length: \(L_2=2.0\,\mathrm{m}\).</li>
      <li>Gravitational acceleration: \(g=9.81\,\mathrm{m/s^2}\).</li>
    </ul>

    <p>
    The rods are treated as rigid constraints, the masses are treated
    as point particles, and gravity is the only external force doing
    work. The model does not include air resistance, friction at the
    pivot, rod mass, or any external driving force.
    </p>

    <p>
    Under these assumptions, the system has two generalized coordinates:
    the angles of the two rods. Because each rod has fixed length, the
    positions of both masses can be expressed completely in terms of
    these two angles.
    </p>

    <h3>3. Generalized coordinates and angular conventions</h3>

    <p>
    The code uses the generalized coordinates
    \(\theta_1\) and \(\theta_2\). Both angles are measured from the
    downward vertical, with positive angles corresponding to displacement
    toward the positive horizontal direction in the coordinate convention
    used by the simulation.
    </p>

    <p>
    The corresponding angular velocities are
    </p>

    <p style="text-align:center;">
    \[
    \omega_1=\dot{\theta}_1,\qquad
    \omega_2=\dot{\theta}_2.
    \]
    </p>

    <p>
    Here, a dot denotes differentiation with respect to physical time.
    The angular accelerations are
    </p>

    <p style="text-align:center;">
    \[
    \alpha_1=\ddot{\theta}_1,\qquad
    \alpha_2=\ddot{\theta}_2.
    \]
    </p>

    <p>
    An important detail is that \(\theta_2\) is an absolute angle
    measured from the downward vertical. It is not the angle of the
    second rod relative to the first rod. Therefore, the relative
    angular separation between the rods is
    \(\theta_1-\theta_2\).
    </p>

    <p>
    The code begins with
    \(\theta_1(0)=-30^\circ\) and
    \(\theta_2(0)=90^\circ\), with both initial angular velocities
    set to zero. The first rod initially leans to one side, while
    the second rod initially extends horizontally according to this
    angle convention.
    </p>

    <h3>4. Cartesian coordinates of the two masses</h3>

    <p>
    Let the fixed pivot have Cartesian coordinates
    \((x_0,y_0)\). Because the first rod has length \(L_1\), the
    position of the first mass is
    </p>

    <p style="text-align:center;">
    \[
    x_1=x_0+L_1\sin\theta_1,
    \qquad
    y_1=y_0-L_1\cos\theta_1.
    \]
    </p>

    <p>
    The second rod is connected to the first mass. Its horizontal
    displacement relative to the first mass is
    \(L_2\sin\theta_2\), while its vertical displacement is
    \(-L_2\cos\theta_2\). Consequently,
    </p>

    <p style="text-align:center;">
    \[
    x_2=x_1+L_2\sin\theta_2,
    \]
    </p>

    <p style="text-align:center;">
    \[
    y_2=y_1-L_2\cos\theta_2.
    \]
    </p>

    <p>
    These equations enforce the fixed-length constraints automatically.
    In particular,
    </p>

    <p style="text-align:center;">
    \[
    (x_1-x_0)^2+(y_1-y_0)^2=L_1^2,
    \]
    </p>

    <p style="text-align:center;">
    \[
    (x_2-x_1)^2+(y_2-y_1)^2=L_2^2.
    \]
    </p>

    <p>
    The simulation does not integrate the Cartesian coordinates of the
    masses independently. Instead, it integrates the angles and
    reconstructs the Cartesian positions from these formulas. This
    is an effective way to preserve the rod constraints in the rendered
    motion.
    </p>

    <h3>5. Why the two pendulums are dynamically coupled</h3>

    <p>
    For a single pendulum of mass \(m\), length \(L\), and angle
    \(\theta\) measured from the downward vertical, the gravitational
    equation of motion is
    </p>

    <p style="text-align:center;">
    \[
    \ddot{\theta}+\frac{g}{L}\sin\theta=0.
    \]
    </p>

    <p>
    This equation is already nonlinear because of the sine function.
    For small angles, one may approximate
    \(\sin\theta\approx\theta\), obtaining the familiar linear
    harmonic-oscillator equation. That approximation is useful for
    small oscillations but is not generally valid for large excursions.
    </p>

    <p>
    In a double pendulum, the situation is more complicated. The
    acceleration of the upper mass depends on the motion of the lower
    mass, and the acceleration of the lower mass depends on the motion
    of the upper mass. The coupling appears through terms involving
    both angles, their difference, and the squares of the angular
    velocities.
    </p>

    <p>
    The angular difference
    \[
    \Delta=\theta_1-\theta_2
    \]
    is especially important. Terms such as
    \(\sin\Delta\) and \(\cos\Delta\) describe how the relative
    orientation of the rods affects their motion. The centrifugal
    contributions involving \(\omega_1^2\) and \(\omega_2^2\)
    also influence the angular accelerations.
    </p>

    <h3>6. Deriving the equations using Lagrangian mechanics</h3>

    <p>
    The coupled equations can be derived systematically using the
    Lagrangian formulation. Define the Lagrangian as the kinetic energy
    minus the gravitational potential energy:
    </p>

    <p style="text-align:center;">
    \[
    \mathcal{L}=T-V.
    \]
    </p>

    <p>
    For point masses and massless rods, the kinetic energy is
    </p>

    <p style="text-align:center;">
    \[
    T=\frac12m_1v_1^2+\frac12m_2v_2^2.
    \]
    </p>

    <p>
    Differentiating the Cartesian coordinates with respect to time
    gives the velocity components. For the first mass,
    </p>

    <p style="text-align:center;">
    \[
    \dot{x}_1=L_1\cos\theta_1\,\omega_1,
    \qquad
    \dot{y}_1=L_1\sin\theta_1\,\omega_1.
    \]
    </p>

    <p>
    Squaring and adding yields
    </p>

    <p style="text-align:center;">
    \[
    v_1^2=L_1^2\omega_1^2.
    \]
    </p>

    <p>
    The second mass receives velocity contributions from both rods.
    Its squared speed is
    </p>

    <p style="text-align:center;">
    \[
    v_2^2=L_1^2\omega_1^2+L_2^2\omega_2^2
    +2L_1L_2\omega_1\omega_2\cos(\theta_1-\theta_2).
    \]
    </p>

    <p>
    Therefore, the total kinetic energy becomes
    </p>

    <p style="text-align:center;">
    \[
    \begin{aligned}
    T={}&\frac12(m_1+m_2)L_1^2\omega_1^2
    +\frac12m_2L_2^2\omega_2^2\\
    &+m_2L_1L_2\omega_1\omega_2
    \cos(\theta_1-\theta_2).
    \end{aligned}
    \]
    </p>

    <p>
    Choosing the zero of potential energy at the pivot height, the
    gravitational potential energy is
    </p>

    <p style="text-align:center;">
    \[
    V=-(m_1+m_2)gL_1\cos\theta_1
    -m_2gL_2\cos\theta_2.
    \]
    </p>

    <p>
    The Lagrangian is obtained by substituting these expressions into
    \(\mathcal{L}=T-V\). The equations of motion then follow from
    the Euler-Lagrange equations:
    </p>

    <p style="text-align:center;">
    \[
    \frac{d}{dt}
    \left(\frac{\partial\mathcal{L}}
    {\partial\dot{\theta}_i}\right)
    -
    \frac{\partial\mathcal{L}}{\partial\theta_i}=0,
    \qquad i=1,2.
    \]
    </p>

    <p>
    These equations contain the full inertial and gravitational
    coupling of the two pendulums. After collecting the terms
    proportional to the angular accelerations, one obtains a pair
    of coupled nonlinear second-order differential equations.
    </p>

    <h3>7. The coupled equations implemented in the code</h3>

    <p>
    The source defines
    \(\Delta=\theta_1-\theta_2\) and introduces the common
    denominator
    </p>

    <p style="text-align:center;">
    \[
    D=2m_1+m_2-m_2\cos(2\Delta).
    \]
    </p>

    <p>
    The first angular acceleration is implemented as
    </p>

    <p style="text-align:center;">
    \[
    \begin{aligned}
    \alpha_1={1\over L_1D}\Big[&
    -g(2m_1+m_2)\sin\theta_1\\
    &-m_2g\sin(\theta_1-2\theta_2)\\
    &-2m_2\sin\Delta
    \left(L_2\omega_2^2+
    L_1\omega_1^2\cos\Delta\right)
    \Big].
    \end{aligned}
    \]
    </p>

    <p>
    This expression combines gravitational contributions with
    velocity-dependent coupling terms. The terms containing
    \(\omega_1^2\) and \(\omega_2^2\) show that the angular
    acceleration depends not only on the instantaneous angles
    but also on how quickly both rods are moving.
    </p>

    <p>
    The second angular acceleration is
    </p>

    <p style="text-align:center;">
    \[
    \begin{aligned}
    \alpha_2={2\sin\Delta\over L_2D}\Big[&
    L_1\omega_1^2(m_1+m_2)\\
    &+g(m_1+m_2)\cos\theta_1\\
    &+m_2L_2\omega_2^2\cos\Delta
    \Big].
    \end{aligned}
    \]
    </p>

    <p>
    The denominator \(D\) is part of the coupled inertial response.
    With positive masses, it can be written as
    \(D=2m_1+2m_2\sin^2\Delta\), so it is positive for this model.
    It therefore does not introduce a singularity for ordinary
    positive masses.
    </p>

    <p>
    The two acceleration expressions are evaluated simultaneously
    from the current state. They are not solved as two independent
    simple-pendulum equations. This coupling is essential: replacing
    them with independent sinusoidal motions would remove the
    dynamics that make the double pendulum interesting.
    </p>

    <h3>8. Converting the equations into a first-order system</h3>

    <p>
    Numerical integrators such as SciPy's
    <code>solve_ivp</code> operate on first-order differential
    equations. To use one, the code defines the state vector
    </p>

    <p style="text-align:center;">
    \[
    \mathbf q=
    \begin{pmatrix}
    \theta_1\\
    \omega_1\\
    \theta_2\\
    \omega_2
    \end{pmatrix}.
    \]
    </p>

    <p>
    Its time derivative is
    </p>

    <p style="text-align:center;">
    \[
    \frac{d\mathbf q}{dt}
    =
    \begin{pmatrix}
    \omega_1\\
    \alpha_1\\
    \omega_2\\
    \alpha_2
    \end{pmatrix}.
    \]
    </p>

    <p>
    The function <code>equations_of_motion(t, state)</code>
    unpacks the four state variables, calculates the angular
    difference and denominator, evaluates the two accelerations,
    and returns the derivative vector in precisely this order.
    The time argument is included to conform to the interface
    expected by the numerical integrator, even though the equations
    themselves have no explicit time dependence.
    </p>

    <h3>9. Deterministic chaos and sensitivity to initial conditions</h3>

    <p>
    The double pendulum is a useful model for understanding the
    distinction between deterministic and predictable motion. Its
    equations are deterministic: if the initial state and parameters
    are specified exactly, the equations determine the subsequent
    trajectory. Yet in chaotic regimes, two states that begin
    extremely close together can separate rapidly as time evolves.
    </p>

    <p>
    This sensitivity can be represented schematically by
    </p>

    <p style="text-align:center;">
    \[
    \delta(t)\sim\delta(0)e^{\lambda t},
    \]
    </p>

    <p>
    where \(\delta(t)\) measures a suitably defined separation
    between nearby trajectories and \(\lambda\) is a Lyapunov
    exponent. A positive largest Lyapunov exponent is a common
    diagnostic of chaos in an appropriate dynamical regime.
    </p>

    <p>
    The important point is that the irregular motion is not produced
    by a random force. It arises from the nonlinear equations and
    the coupling between the two degrees of freedom. Small differences
    in initial angles or angular velocities may eventually produce
    noticeably different trajectories.
    </p>

    <p>
    The present animation uses one initial condition,
    \(\theta_1(0)=-30^\circ\), \(\theta_2(0)=90^\circ\),
    \(\omega_1(0)=\omega_2(0)=0\). Its evolving path illustrates
    nonlinear coupled motion, but a single animation does not by
    itself prove that the selected trajectory is chaotic. A stronger
    demonstration would compare nearby initial conditions or calculate
    a Lyapunov exponent.
    </p>

    <h3>10. Energy conservation as a physical consistency check</h3>

    <p>
    Because the model has no friction or external driving, its
    mechanical energy should remain constant in the exact equations
    of motion. The conserved energy is
    </p>

    <p style="text-align:center;">
    \[
    E=T+V,
    \]
    </p>

    <p>
    with kinetic and potential energies defined above. During motion,
    energy can be transferred between kinetic and gravitational
    potential forms and between the motion of the two masses, but
    the total energy should remain constant.
    </p>

    <p>
    In a numerical simulation, the calculated energy may show small
    errors because of finite integration tolerances and interpolation.
    Monitoring \(E(t)-E(0)\) is therefore a useful diagnostic for
    checking the accuracy of a computed trajectory. The current
    program does not plot the energy error; it focuses on rendering
    the motion itself.
    </p>

    <h2>Part II: Numerical Simulation and Manim Implementation</h2>

    <h3>1. Separating physics from visualization</h3>

    <p>
    The program is organized into two main layers. The first layer
    defines the physical parameters, implements the equations of
    motion, and numerically solves for the angular evolution. The
    second layer uses Manim to draw the pivot, rods and masses,
    update their positions, and display the evolving trajectory.
    </p>

    <p>
    This separation is important. The physics solver does not need
    to know how the pendulum is drawn, and the rendering code does
    not need to solve the equations again at every frame. Instead,
    the animation reads the previously calculated solution.
    </p>

    <h3>2. Defining physical parameters and initial conditions</h3>

    <p>
    The variables <code>m1</code>, <code>m2</code>,
    <code>L1</code>, <code>L2</code> and <code>g</code>
    specify the physical model. The initial angles are entered
    in degrees for convenience, whereas the differential equations
    use radians.
    </p>

    <p>
    The conversion is performed using
    <code>np.deg2rad(theta1_0)</code> and
    <code>np.deg2rad(theta2_0)</code>. The initial state is assembled
    in the order
    <code>[theta1, omega1, theta2, omega2]</code>. The two initial
    angular velocities are zero, so the system is released from rest.
    </p>

    <p>
    The simulation duration is set to 20 seconds. The parameter
    <code>SLOW_MOTION</code> controls how long the animation takes
    relative to physical time. With its current value of \(1.0\),
    the 20 seconds of simulated motion are played over 20 seconds
    of animation time.
    </p>

    <h3>3. Choosing the numerical time grid</h3>

    <p>
    The code defines a numerical sampling interval
    </p>

    <p style="text-align:center;">
    \[
    \Delta t=\frac{1}{240}\ \mathrm{s}.
    \]
    </p>

    <p>
    This gives 240 sampling intervals per second. The array
    <code>time_points</code> is generated from zero to the simulation
    endpoint using <code>np.arange</code>, with a small half-step
    adjustment to help include the final time.
    </p>

    <p>
    The sampling interval is distinct from the video frame duration.
    The numerical solution is sampled at 240 intervals per second,
    while <code>FPS = 60</code> documents a desired animation frame
    rate. Manim's renderer controls the actual video frame rate;
    defining the <code>FPS</code> variable alone does not change
    the renderer's configuration.
    </p>

    <h3>4. Integrating with SciPy's DOP853 method</h3>

    <p>
    The function <code>solve_ivp</code> integrates
    <code>equations_of_motion</code> from zero to
    <code>SIMULATION_TIME</code>. The initial state supplies the
    starting point, and <code>t_eval=time_points</code> requests
    the solution at the selected sample times.
    </p>

    <p>
    The integration method is <code>DOP853</code>, an explicit
    Runge-Kutta method of order eight with an embedded error
    estimator. It is designed for accurate integration of
    non-stiff ordinary differential equations, making it suitable
    for this smooth mechanical model.
    </p>

    <p>
    The solver uses a relative tolerance of \(10^{-10}\) and an
    absolute tolerance of \(10^{-12}\), with
    <code>max_step=DT</code>. The small maximum step limits the
    distance in time between internal solver steps, while the
    tolerances control the solver's local error estimates.
    These settings request a highly accurate numerical solution,
    although they do not guarantee that every observable has an
    error equal to the specified tolerance.
    </p>

    <p>
    The code checks <code>solution.success</code> after integration.
    If the solver fails, a <code>RuntimeError</code> is raised
    rather than allowing the animation to proceed with an invalid
    trajectory. The returned arrays contain the sampled times and
    the calculated values of both angles.
    </p>

    <h3>5. Interpolating the precomputed solution</h3>

    <p>
    The function <code>get_angles(t)</code> retrieves the angular
    coordinates at an arbitrary animation time. First,
    <code>np.clip</code> restricts the requested time to the
    numerical integration interval. Then <code>np.interp</code>
    independently interpolates the two angular arrays.
    </p>

    <p>
    This is necessary because Manim requests updates at video frame
    times, which generally do not coincide exactly with the numerical
    sample times. Interpolation supplies an angle for each requested
    frame without rerunning the differential-equation solver.
    </p>

    <p>
    The interpolation is linear between neighboring numerical samples.
    Because the solution was sampled densely, it provides a practical
    way to drive the animation. It remains an approximation to the
    continuous numerical solution, and it is distinct from a new
    high-order integration step at each video frame.
    </p>

    <h3>6. Building the visual scene</h3>

    <p>
    The Manim class <code>DoublePendulum</code> inherits from
    <code>Scene</code>, since the displayed motion is planar.
    The fixed pivot is placed at
    <code>np.array([0.0, 2.0, 0.0])</code>, above the center of
    the scene. A short grey line represents the support, and a
    white dot marks the pivot.
    </p>

    <p>
    The first bob is blue and the second bob is red. Both are
    represented by Manim <code>Dot</code> objects with radius
    <code>0.14</code>. The two rods are grey lines with a
    stroke width of four. These colors make the two masses easy
    to distinguish throughout their coupled motion.
    </p>

    <p>
    The rods are initially created as vertical lines. Their final
    endpoints are then controlled by updaters, so their visible
    geometry is determined by the physical state rather than by
    a separate animation path.
    </p>

    <h3>7. Mapping physical positions into scene coordinates</h3>

    <p>
    The function <code>positions(t)</code> first calls
    <code>get_angles(t)</code> to obtain the two angles. It then
    calculates the relative Cartesian coordinates:
    </p>

    <p style="text-align:center;">
    \[
    x_1=L_1\sin\theta_1,\qquad
    y_1=-L_1\cos\theta_1,
    \]
    </p>

    <p style="text-align:center;">
    \[
    x_2=x_1+L_2\sin\theta_2,\qquad
    y_2=y_1-L_2\cos\theta_2.
    \]
    </p>

    <p>
    The pivot position and the scene scale are then added to obtain
    the final Manim coordinates. The function returns the positions
    of both masses as three-component vectors, with zero \(z\)-coordinate.
    The motion therefore remains in the \(xy\)-plane.
    </p>

    <p>
    The variable <code>scale</code> is set to \(1.0\), so one unit
    of rod length maps to one Manim coordinate unit. This scale
    could be adjusted to fit a different rod length or scene layout
    without changing the physical equations.
    </p>

    <h3>8. Updaters synchronize rods and masses</h3>

    <p>
    The function <code>update_rod1</code> obtains the current
    position of the first mass and uses
    <code>put_start_and_end_on</code> to connect it to the fixed
    pivot. The function <code>update_rod2</code> obtains both mass
    positions and places the second rod between them.
    </p>

    <p>
    Similarly, <code>update_bob1</code> and <code>update_bob2</code>
    move the two dots to their calculated positions. Each rod and
    bob receives its corresponding updater through
    <code>add_updater</code>.
    </p>

    <p>
    This design means the rods and masses remain geometrically
    synchronized with the same pair of angles. The rods do not rotate
    independently of the bobs; all four objects are derived from the
    same underlying numerical solution.
    </p>

    <h3>9. The time tracker connects the numerical and visual systems</h3>

    <p>
    A <code>ValueTracker</code> named <code>clock</code> stores
    the current physical time. The updater functions use
    <code>clock.get_value()</code> to request the appropriate angles
    and positions.
    </p>

    <p>
    The main animation is
    <code>clock.animate.set_value(SIMULATION_TIME)</code>, with
    the animation duration set to
    <code>SIMULATION_TIME / SLOW_MOTION</code> and
    <code>rate_func=linear</code>. A linear rate function ensures
    that the tracker's physical time advances uniformly over the
    animation, rather than accelerating or decelerating because of
    an easing function.
    </p>

    <p>
    Consequently, the apparent motion of the rods is controlled by
    the computed angular dynamics, while the rate at which the
    precomputed solution is traversed is controlled by the clock.
    Changing <code>SLOW_MOTION</code> changes playback speed without
    requiring a different physical initial-value problem.
    </p>

    <h3>10. Tracing the second mass</h3>

    <p>
    The code creates a <code>TracedPath</code> object using
    <code>bob2.get_center</code> as its point function. Its color is
    red, matching the second bob, and its stroke width is \(2.5\).
    As the second mass moves, the traced path records its changing
    position and displays the history of its motion.
    </p>

    <p>
    This trajectory makes the geometric complexity of the motion
    easier to see. Rather than observing only the current position,
    the viewer can compare the current bob position with the region
    of the plane it has already explored.
    </p>

    <p>
    Although the source section is titled "Trails of Both Masses",
    the current implementation creates a traced path only for the
    second bob. The first bob's path is not separately drawn.
    </p>

    <h3>11. Displaying the physical time</h3>

    <p>
    The variable <code>time_label</code> is created with
    <code>always_redraw</code>. At each update, a new text object
    displays the clock value formatted to two decimal places,
    followed by the unit seconds.
    </p>

    <p>
    The label is positioned near the upper-left corner of the scene.
    It connects the displayed motion to the numerical time parameter
    and helps the viewer distinguish physical time from the number
    of video frames that have elapsed.
    </p>

    <h3>12. Initialization and animation cleanup</h3>

    <p>
    Before the animation begins, the code calls
    <code>positions(0)</code> to calculate the initial locations of
    both masses. The bobs are placed at these positions before being
    added to the scene, preventing the animation from starting with
    both masses at arbitrary default locations.
    </p>

    <p>
    The rods, traced path, bobs and time label are then added to the
    scene. Manim animates the clock from zero to the full simulation
    duration, and the updater functions reconstruct the system at
    every rendered frame.
    </p>

    <p>
    At the end, the code clears the updaters from both rods and both
    bobs. This stops their dynamic updates cleanly after the numerical
    motion has finished.
    </p>

    <h3>13. What this simulation establishes—and what could be added</h3>

    <p>
    The animation demonstrates a genuine numerical solution of the
    coupled double-pendulum equations. The positions are calculated
    from the evolving angles, and the angles are obtained by integrating
    the nonlinear equations of motion. The motion is therefore not
    generated by manually selecting a sequence of positions.
    </p>

    <p>
    Several additional diagnostics could turn this visual project into
    a more comprehensive computational study of chaos:
    </p>

    <ul>
      <li>
        <strong>Energy conservation:</strong> calculate and plot
        \(E(t)\) to check the numerical integration and quantify
        energy drift.
      </li>
      <li>
        <strong>Angular time series:</strong> plot
        \(\theta_1(t)\) and \(\theta_2(t)\) to investigate the
        irregularity and characteristic time scales of the motion.
      </li>
      <li>
        <strong>Phase-space portraits:</strong> plot
        \((\theta_1,\omega_1)\) or
        \((\theta_2,\omega_2)\) to study the relationship between
        angles and angular velocities.
      </li>
      <li>
        <strong>Nearby initial conditions:</strong> repeat the
        simulation with a tiny perturbation to one initial angle
        and compare the resulting trajectories.
      </li>
      <li>
        <strong>Lyapunov analysis:</strong> quantify the growth of
        the separation between nearby trajectories to test for
        sensitive dependence on initial conditions.
      </li>
      <li>
        <strong>Return maps or Poincaré sections:</strong> sample
        the system at selected crossings or phases to investigate
        its phase-space structure.
      </li>
    </ul>

    <p>
    These diagnostics are not currently calculated by this source
    file. They are natural extensions that would help distinguish
    regular oscillations from chaotic regimes more rigorously.
    </p>

    <p>
    Overall, the project connects analytical mechanics, nonlinear
    ordinary differential equations, numerical integration, and
    scientific visualization. It demonstrates how a compact
    mechanical system governed by deterministic laws can produce
    motion whose long-term behavior is visually intricate and,
    in chaotic regimes, highly sensitive to its initial conditions.
    </p>
    """,
    },

    {

    "name": "3D Lissajous Curves",
    "slug": "3d-lissajous-curves",
    "video": "Lissajous3D.mp4",
    "code": "source_code/lissajous.py",
    "description": r"""
    <h2>Part I: Physics and Mathematical Background</h2>

    <h3>1. Introduction: How independent oscillations create a complex trajectory</h3>

    <p>
    Lissajous curves arise when two or more periodic oscillations act
    simultaneously along different coordinate directions. Although each
    individual coordinate follows a simple sinusoidal law, their
    superposition can produce intricate geometric patterns. These curves
    appear in classical mechanics, wave physics, electrical engineering,
    signal analysis, and the study of harmonic motion.
    </p>

    <p>
    A two-dimensional Lissajous curve is commonly generated by combining
    sinusoidal oscillations along the horizontal and vertical directions.
    A three-dimensional Lissajous curve extends this idea by introducing
    an independent oscillation along a third coordinate axis. The resulting
    trajectory can weave through space, form loops, and intersect itself
    when viewed from particular directions.
    </p>

    <p>
    This project constructs such a trajectory by assigning a sinusoidal
    function to each Cartesian coordinate. A moving particle travels along
    the resulting path while Manim gradually draws its history. Once the
    trajectory is complete, the animation rotates the curve itself to
    reveal its three-dimensional structure from changing orientations.
    </p>

    <h3>2. Mathematical definition of a three-dimensional Lissajous curve</h3>

    <p>
    The position of the particle is defined by three time-dependent
    coordinates:
    </p>

    <p style="text-align:center;">
    \[
    x(t)=A_x\sin(\omega_x t+\phi_x),
    \]
    </p>

    <p style="text-align:center;">
    \[
    y(t)=A_y\sin(\omega_y t+\phi_y),
    \]
    </p>

    <p style="text-align:center;">
    \[
    z(t)=A_z\sin(\omega_z t+\phi_z).
    \]
    </p>

    <p>
    These equations define a parametric curve
    \(\mathbf r(t)\) in three-dimensional space:
    </p>

    <p style="text-align:center;">
    \[
    \mathbf r(t)=
    \begin{pmatrix}
    A_x\sin(\omega_x t+\phi_x)\\
    A_y\sin(\omega_y t+\phi_y)\\
    A_z\sin(\omega_z t+\phi_z)
    \end{pmatrix}.
    \]
    </p>

    <p>
    The parameter \(t\) determines the position along the trajectory.
    It plays the role of time in the prescribed oscillatory motion,
    although the code constructs the path directly rather than deriving
    it from a force law.
    </p>

    <p>
    Each coordinate oscillates independently according to its own
    amplitude, angular frequency, and phase. Their simultaneous values
    determine the position of the particle at every instant.
    </p>

    <h3>3. The role of amplitudes</h3>

    <p>
    The amplitudes \(A_x\), \(A_y\), and \(A_z\) set the maximum
    displacement from the origin along each coordinate direction.
    Since the sine function takes values between \(-1\) and \(1\),
    the coordinates satisfy
    </p>

    <p style="text-align:center;">
    \[
    -A_x\leq x(t)\leq A_x,
    \qquad
    -A_y\leq y(t)\leq A_y,
    \qquad
    -A_z\leq z(t)\leq A_z.
    \]
    </p>

    <p>
    In this simulation, the amplitudes are
    </p>

    <p style="text-align:center;">
    \[
    A_x=3,\qquad A_y=2.5,\qquad A_z=2.5.
    \]
    </p>

    <p>
    Consequently, the trajectory extends farther along the \(x\)-axis
    than along either of the other coordinate axes. Its complete
    bounding region lies within the rectangular box
    \([-3,3]\times[-2.5,2.5]\times[-2.5,2.5]\).
    </p>

    <p>
    The amplitudes influence the shape and spatial extent of the curve
    but do not determine how quickly the particle traverses it. That
    behavior is controlled by the angular frequencies.
    </p>

    <h3>4. Angular frequencies and frequency ratios</h3>

    <p>
    Angular frequency describes how quickly the phase of an oscillation
    changes. For an oscillation with angular frequency \(\omega\), the
    ordinary frequency \(f\) and period \(P\) are
    </p>

    <p style="text-align:center;">
    \[
    f=\frac{\omega}{2\pi},
    \qquad
    P=\frac{2\pi}{\omega}.
    \]
    </p>

    <p>
    The code chooses
    </p>

    <p style="text-align:center;">
    \[
    \omega_x=3,\qquad
    \omega_y=4,\qquad
    \omega_z=5.
    \]
    </p>

    <p>
    The frequency ratio is therefore
    </p>

    <p style="text-align:center;">
    \[
    \omega_x:\omega_y:\omega_z=3:4:5.
    \]
    </p>

    <p>
    During a time interval of \(2\pi\), the \(x\)-coordinate completes
    three cycles, the \(y\)-coordinate completes four cycles, and the
    \(z\)-coordinate completes five cycles. The different oscillation
    rates are what cause the particle to move through a changing
    combination of coordinate values instead of retracing a single
    one-dimensional oscillation.
    </p>

    <p>
    A useful way to understand this is to imagine three oscillators
    operating simultaneously. At some instant, the \(x\)-oscillator
    might be near its maximum, the \(y\)-oscillator might be crossing
    zero, and the \(z\)-oscillator might be moving toward its minimum.
    A short time later, all three phases have changed by different
    amounts. The particle's position therefore changes in a coordinated
    but nontrivial way.
    </p>

    <h3>5. Phase differences and the initial geometry</h3>

    <p>
    The phase constants determine where each oscillation begins in its
    cycle. The source uses
    </p>

    <p style="text-align:center;">
    \[
    \phi_x=0,\qquad
    \phi_y=\frac{\pi}{3},\qquad
    \phi_z=\frac{\pi}{2}.
    \]
    </p>

    <p>
    At \(t=0\), the initial position is
    </p>

    <p style="text-align:center;">
    \[
    \mathbf r(0)=
    \begin{pmatrix}
    A_x\sin\phi_x\\
    A_y\sin\phi_y\\
    A_z\sin\phi_z
    \end{pmatrix}.
    \]
    </p>

    <p>
    Substituting the selected parameters gives
    </p>

    <p style="text-align:center;">
    \[
    \mathbf r(0)=
    \begin{pmatrix}
    0\\
    2.5\sin(\pi/3)\\
    2.5\sin(\pi/2)
    \end{pmatrix}
    =
    \begin{pmatrix}
    0\\
    1.25\sqrt{3}\\
    2.5
    \end{pmatrix}.
    \]
    </p>

    <p>
    Thus, the particle starts at approximately
    \((0,2.165,2.5)\). It does not start at the origin because the
    \(y\)- and \(z\)-oscillations begin at nonzero phases.
    </p>

    <p>
    Phase differences are crucial in determining the geometry of a
    Lissajous curve. Even if the amplitudes and frequencies are unchanged,
    changing a phase can alter the locations of loops, crossings, and
    extrema along the trajectory.
    </p>

    <h3>6. Why the trajectory closes</h3>

    <p>
    The animation uses the parameter interval
    </p>

    <p style="text-align:center;">
    \[
    0\leq t\leq T,\qquad T=2\pi.
    \]
    </p>

    <p>
    At the endpoint, the phase of each coordinate has advanced by
    an integer multiple of \(2\pi\):
    </p>

    <p style="text-align:center;">
    \[
    \omega_xT=3(2\pi)=6\pi,
    \]
    </p>

    <p style="text-align:center;">
    \[
    \omega_yT=4(2\pi)=8\pi,
    \]
    </p>

    <p style="text-align:center;">
    \[
    \omega_zT=5(2\pi)=10\pi.
    \]
    </p>

    <p>
    Since sine is periodic with period \(2\pi\), all three coordinates
    return to their initial values:
    </p>

    <p style="text-align:center;">
    \[
    \mathbf r(T)=\mathbf r(0).
    \]
    </p>

    <p>
    The curve is therefore closed. More generally, a Lissajous trajectory
    closes when the ratios of its angular frequencies are rational,
    provided the oscillations are considered over a common period.
    If the ratios are irrational, the trajectory generally does not
    close after any finite common period and can densely explore a
    region of its accessible coordinate space under suitable conditions.
    </p>

    <h3>7. Velocity and acceleration of the particle</h3>

    <p>
    Differentiating the position vector gives the velocity:
    </p>

    <p style="text-align:center;">
    \[
    \dot{x}(t)=A_x\omega_x
    \cos(\omega_x t+\phi_x),
    \]
    </p>

    <p style="text-align:center;">
    \[
    \dot{y}(t)=A_y\omega_y
    \cos(\omega_y t+\phi_y),
    \]
    </p>

    <p style="text-align:center;">
    \[
    \dot{z}(t)=A_z\omega_z
    \cos(\omega_z t+\phi_z).
    \]
    </p>

    <p>
    The instantaneous speed is the magnitude of the velocity vector:
    </p>

    <p style="text-align:center;">
    \[
    v(t)=\sqrt{\dot{x}^{\,2}+\dot{y}^{\,2}+\dot{z}^{\,2}}.
    \]
    </p>

    <p>
    Differentiating again yields the acceleration:
    </p>

    <p style="text-align:center;">
    \[
    \ddot{x}=-A_x\omega_x^2
    \sin(\omega_x t+\phi_x)=-\omega_x^2x,
    \]
    </p>

    <p style="text-align:center;">
    \[
    \ddot{y}=-\omega_y^2y,\qquad
    \ddot{z}=-\omega_z^2z.
    \]
    </p>

    <p>
    Each coordinate individually obeys the equation of a simple
    harmonic oscillator. However, the three-dimensional trajectory
    combines three oscillators with different frequencies and phases.
    The overall motion is not generally a circular orbit or a simple
    ellipse, and its speed need not remain constant.
    </p>

    <p>
    These equations also clarify the physical interpretation of the
    animation. The program prescribes three harmonic coordinate
    functions and computes their combined path. It does not derive
    these oscillations from a particular three-dimensional force field
    or simulate a particle subject to an independently specified
    mechanical potential.
    </p>

    <h3>8. Connection to coupled oscillators and harmonic analysis</h3>

    <p>
    Lissajous curves are useful for visualizing the relative phase and
    frequency of periodic signals. In an oscilloscope, for example,
    one signal can control the horizontal deflection while another
    controls the vertical deflection. The resulting figure can reveal
    information about their frequency ratio and phase difference.
    </p>

    <p>
    The three-dimensional construction generalizes that idea. Each
    coordinate is analogous to a separate periodic signal, and the
    particle's path records their combined evolution. This gives a
    direct geometric representation of the relationships among the
    phases.
    </p>

    <p>
    The term "independent oscillations" is important here. Although
    their coordinates are combined into one position vector, the
    code assigns each coordinate its own sinusoidal law. It does not
    solve a system of coupled differential equations in which the
    motion along one axis dynamically changes the frequency or
    amplitude of another.
    </p>

    <h3>9. Symmetry and the role of the coordinate system</h3>

    <p>
    The shape of a three-dimensional curve can be difficult to judge
    from a single projection. A trajectory that appears to intersect
    itself in a two-dimensional image may actually pass through
    different depths in space. Conversely, distinct portions of a
    three-dimensional curve may overlap in a particular camera view.
    </p>

    <p>
    Rotating the viewing direction helps reveal these spatial
    relationships. It can show which loops lie in front of or behind
    others and make the full three-dimensional structure easier
    to understand.
    </p>

    <p>
    The animation uses two different operations that should not be
    confused. First, the camera rotates while the particle traces
    the trajectory. Later, the completed curve itself is rotated
    about the origin. Camera rotation changes the viewpoint without
    changing the coordinates of the curve; rotating the curve changes
    its displayed orientation relative to the coordinate frame.
    </p>

    <h2>Part II: Python, NumPy and Manim Implementation</h2>

    <h3>1. Scene structure</h3>

    <p>
    The program imports all standard Manim objects using
    <code>from manim import *</code> and imports NumPy as
    <code>np</code> for numerical calculations. The animation is
    defined in the class <code>Lissajous3D</code>, which inherits
    from <code>ThreeDScene</code>.
    </p>

    <p>
    A three-dimensional scene is appropriate because the particle
    has three independent coordinates. Manim supplies the camera,
    three-dimensional sphere object, parametric-curve machinery,
    animation system, and updater framework needed to visualize
    the motion.
    </p>

    <h3>2. Defining the parameters</h3>

    <p>
    The amplitude variables are assigned using
    <code>Ax, Ay, Az = 3, 2.5, 2.5</code>. The angular frequencies
    are assigned as <code>wx = 3</code>,
    <code>wy = 4</code>, and <code>wz = 5</code>. The phase
    constants are stored as <code>phix = 0</code>,
    <code>phiy = PI / 3</code>, and <code>phiz = PI / 2</code>.
    </p>

    <p>
    The total parameter interval is defined by
    <code>T = 2 * PI</code>. Keeping these values together at the
    beginning of the method makes the mathematical specification
    easy to modify. For example, changing one frequency or phase
    changes the shape of the trajectory without requiring a
    different surface or animation class.
    </p>

    <h3>3. The position function</h3>

    <p>
    The nested function <code>position(t)</code> is the central
    mathematical component of the program. It evaluates the three
    sinusoidal expressions at the supplied parameter value and
    returns the result as a NumPy array:
    </p>

    <p style="text-align:center;">
    \[
    \texttt{position}(t)=
    [x(t),y(t),z(t)].
    \]
    </p>

    <p>
    Because the function returns a three-component vector, it can
    be reused wherever a three-dimensional point is required. The
    same function defines the complete curve, initializes the
    particle, updates its position during the animation, and
    generates the points used to draw the trail.
    </p>

    <p>
    This reuse is an important feature of the implementation:
    every displayed position comes from the same mathematical
    definition, reducing the risk of the particle and its trail
    following inconsistent paths.
    </p>

    <h3>4. Setting the camera orientation</h3>

    <p>
    The camera is initialized with
    <code>phi=70 * DEGREES</code>,
    <code>theta=0 * DEGREES</code>, and
    <code>zoom=0.70</code>. These settings determine the initial
    viewing direction and scale of the three-dimensional scene.
    </p>

    <p>
    The title is created as a white <code>Text</code> object with
    font size 36 and positioned near the top edge. The call
    <code>add_fixed_in_frame_mobjects(title)</code> keeps it fixed
    relative to the camera frame rather than letting it rotate
    as a three-dimensional object. The title is then animated
    onto the screen using <code>Write</code>.
    </p>

    <h3>5. Constructing the complete parametric curve</h3>

    <p>
    The source creates a <code>ParametricFunction</code> named
    <code>curve</code>, using <code>position</code> as its
    coordinate function and the parameter range from zero to
    <code>T</code>. The curve is blue and has a stroke width of
    three.
    </p>

    <p>
    A parametric function is a natural representation because the
    curve cannot generally be expressed conveniently as a single
    Cartesian function such as \(y=f(x)\). Instead, all three
    coordinates are functions of the same parameter.
    </p>

    <p>
    The code constructs this full curve object, but the animated
    trace is the object actually added and progressively drawn
    during the first stage. The variable <code>curve</code> is
    not subsequently added to the scene in the current source.
    The completed visible trajectory is therefore provided by
    <code>trace</code>, not by the unused <code>curve</code>
    object.
    </p>

    <h3>6. Creating the moving particle</h3>

    <p>
    The moving particle is represented by a yellow Manim
    <code>Sphere</code> with radius <code>0.09</code> and
    resolution <code>(12, 24)</code>. Its initial position is
    set using <code>particle.move_to(position(0))</code>.
    </p>

    <p>
    This places the particle at the same initial point defined
    by the mathematical trajectory. The sphere provides a
    clearly visible marker that helps the viewer identify the
    current location along the curve as it is being traced.
    </p>

    <h3>7. Initializing the trace</h3>

    <p>
    The trajectory history is stored in a
    <code>VMobject</code> called <code>trace</code>. It is
    assigned the color blue and a stroke width of three.
    Initially, its points are set to the single point
    <code>position(0)</code>.
    </p>

    <p>
    A <code>ValueTracker</code> named <code>tracker</code>
    is initialized to zero. It stores the current value of the
    trajectory parameter and acts as the common control variable
    for both the particle and the growing trace.
    </p>

    <h3>8. Updating the particle and trail</h3>

    <p>
    The function <code>update_particle(mob)</code> reads the
    tracker's current value and moves the particle to
    <code>position(t)</code>. It does not independently calculate
    a new trajectory; it simply evaluates the existing position
    function at the current parameter.
    </p>

    <p>
    The function <code>update_trace(mob)</code> uses the same
    tracker value. It generates 500 evenly spaced parameter
    samples between zero and the current value:
    </p>

    <p style="text-align:center;">
    \[
    t_i\in[0,t],\qquad i=0,\ldots,499.
    \]
    </p>

    <p>
    Each sample is passed to <code>position</code>, and the
    resulting points are collected in a NumPy array. The call
    <code>set_points_as_corners(points)</code> updates the
    blue <code>VMobject</code> so that it follows these points
    as a sequence of connected line segments.
    </p>

    <p>
    The particle updater and trace updater are attached with
    <code>add_updater</code>. As the tracker advances, the particle
    moves along the path while the visible trace expands behind it.
    Because the trace is reconstructed from the start of the motion
    at every update, the full history remains visible rather than
    only a short fading tail.
    </p>

    <h3>9. Stage one: Tracing the trajectory while the camera rotates</h3>

    <p>
    The first animation stage begins with
    <code>begin_ambient_camera_rotation(rate=0.50)</code>.
    The camera begins rotating while the tracker is animated
    linearly from zero to <code>T</code>.
    </p>

    <p>
    The tracker animation lasts 3.5 seconds and uses
    <code>rate_func=linear</code>. Consequently, the trajectory
    parameter advances uniformly from zero to \(2\pi\) over
    the 3.5-second tracing interval.
    </p>

    <p>
    During this stage, three things happen together:
    </p>

    <ul>
      <li>The tracker advances through the prescribed parameter range.</li>
      <li>The yellow particle follows the mathematical position function.</li>
      <li>The blue trace progressively draws the particle's trajectory.</li>
    </ul>

    <p>
    At the same time, ambient camera rotation changes the viewpoint.
    This helps reveal the three-dimensional structure while the curve
    is being constructed, rather than showing it only from one fixed
    projection.
    </p>

    <p>
    When the tracker reaches its endpoint, the code stops the ambient
    camera rotation and clears the updaters from the particle and
    trace. The particle is then removed, leaving the completed curve
    as the main visual object.
    </p>

    <h3>10. Stage two: Rotating the completed curve itself</h3>

    <p>
    In the second stage, the animation no longer advances the
    oscillator parameter. Instead, the completed trace receives
    a new updater named <code>rotate_curve</code>.
    This updater takes Manim's elapsed frame time, <code>dt</code>,
    and applies three incremental rotations to the curve.
    </p>

    <p>
    The first rotation is about the <code>RIGHT</code> axis:
    </p>

    <p style="text-align:center;">
    \[
    \Delta\alpha_x=1.5\,dt.
    \]
    </p>

    <p>
    The second rotation is about the <code>UP</code> axis:
    </p>

    <p style="text-align:center;">
    \[
    \Delta\alpha_y=1.0\,dt.
    \]
    </p>

    <p>
    The third rotation is about the <code>OUT</code> axis:
    </p>

    <p style="text-align:center;">
    \[
    \Delta\alpha_z=2.0\,dt.
    \]
    </p>

    <p>
    Each rotation is applied about <code>ORIGIN</code>. Since the
    increments are proportional to the frame time, their rates
    remain approximately consistent when the frame duration changes.
    </p>

    <p>
    The code applies these rotations sequentially on each update.
    Rotations about different axes generally do not commute, so their
    order matters: rotating first about \(x\), then \(y\), and then
    \(z\) need not produce the same orientation as applying them in
    another order.
    </p>

    <p>
    The curve is allowed to tumble for 6.5 seconds. This final
    presentation is a rigid geometric transformation of the completed
    path. It does not change the frequencies, phases, or underlying
    particle dynamics used to construct the original trajectory.
    </p>

    <h3>11. Parameter time versus animation time</h3>

    <p>
    It is useful to distinguish three separate notions of time in
    this implementation. The parameter \(t\) specifies a point on
    the mathematical curve. Manim's animation time determines how
    quickly the tracker moves through the parameter range. Finally,
    the frame-time increment <code>dt</code> controls how far the
    completed curve rotates during each rendered update.
    </p>

    <p>
    During the first stage, the tracker moves from zero to \(2\pi\)
    over 3.5 seconds of video. The oscillation frequencies determine
    the shape of the path as a function of the parameter, while the
    tracker determines the speed of traversal in the animation.
    </p>

    <p>
    During the second stage, the tracker remains at its final value.
    The particle has been removed, and only the geometric curve
    rotates. Thus, the final rotation is a visualization technique,
    not a continuation of the original oscillatory motion.
    </p>

    <h3>12. Numerical sampling and visual accuracy</h3>

    <p>
    The trace updater evaluates the trajectory at 500 evenly spaced
    points between zero and the current parameter value. These points
    are connected by straight segments. This is a piecewise-linear
    approximation to the continuous Lissajous curve.
    </p>

    <p>
    A larger number of samples generally improves the visual
    approximation, particularly where the curve bends sharply.
    However, increasing the number of samples also increases the
    work performed by the trace updater, since the current history
    is regenerated at each update. For more computationally demanding
    scenes, one could instead accumulate newly sampled points or
    construct the trajectory once and reveal it progressively.
    </p>

    <p>
    The present approach prioritizes a clear, continuously growing
    trace and is straightforward to understand. It also ensures that
    the trail and the moving particle are based on the same function,
    which is important for a consistent scientific visualization.
    </p>

    <h3>13. What this project demonstrates</h3>

    <p>
    This project combines elementary harmonic functions into a
    three-dimensional geometric trajectory. It demonstrates how
    amplitude, frequency ratios, and phase differences determine
    the shape of a periodic path, and how parametric equations can
    be turned into a moving particle and a continuously drawn curve.
    </p>

    <p>
    It also illustrates an important visualization distinction:
    rotating a camera changes the observer's viewpoint, while
    rotating a completed geometric object changes its orientation
    in the scene. Using both operations makes the spatial structure
    easier to inspect.
    </p>

    <p>
    The resulting animation is a computational visualization of
    prescribed harmonic motion. Although the coordinate functions
    individually have the form of simple harmonic oscillators, the
    project does not model a specific coupled mechanical system,
    calculate a force field, or infer chaos from the trajectory.
    Its principal purpose is to connect sinusoidal mathematics
    with three-dimensional geometry and scientific animation.
    </p>
    """,
    },

    {

    "name": "Motion of Charged Particles",
    "slug": "motion-of-charged-particles",
    "video": "ElectricFieldParticle.mp4",
    "code": "source_code/electricfield.py",
    "description": r"""
    <h2>Part I: Physical Principles — Charged-Particle Dynamics in Electric and Magnetic Fields</h2>

    <p>
    Charged-particle motion is one of the fundamental problems in classical
    electrodynamics. Electric and magnetic fields exert forces on charged
    matter, changing its momentum and, depending on the type of field, either
    changing its kinetic energy or redirecting its trajectory. The same
    principles underlie particle accelerators, mass spectrometers, plasma
    confinement, electron optics, radiation processes, and many experiments
    in atomic, nuclear, and high-energy physics.
    </p>

    <p>
    This project presents two complementary situations. The first illustrates
    how a positive charge accelerates between oppositely charged parallel
    plates under an idealized uniform electric field. The second investigates
    the trajectory of a moving charge in a magnetic field. Although the two
    fields are introduced separately to make their effects visually distinct,
    they are unified by the Lorentz force law.
    </p>

    <h3>1. The Lorentz Force: The Equation Governing Charged Motion</h3>

    <p>
    A particle with electric charge \(q\), mass \(m\), position
    \(\mathbf r(t)\), and velocity \(\mathbf v(t)\) experiences the
    electromagnetic force
    </p>

    <p style="text-align:center;">
    \[
        \boxed{
        \mathbf F=q\left(\mathbf E+\mathbf v\times\mathbf B\right)
        }
    \]
    </p>

    <p>
    Here, \(\mathbf E\) is the electric field and \(\mathbf B\) is the
    magnetic field. Applying Newton's second law gives
    </p>

    <p style="text-align:center;">
    \[
        m\frac{d\mathbf v}{dt}
        =q\left(\mathbf E+\mathbf v\times\mathbf B\right).
    \]
    </p>

    <p>
    Together with the kinematic relation
    </p>

    <p style="text-align:center;">
    \[
        \frac{d\mathbf r}{dt}=\mathbf v,
    \]
    </p>

    <p>
    this becomes a coupled system of differential equations for the
    particle's position and velocity. Given initial conditions, a field
    configuration, and the particle's charge-to-mass ratio, these equations
    determine the subsequent trajectory.
    </p>

    <p>
    The electric and magnetic contributions have importantly different
    properties. The electric force \(q\mathbf E\) can do work on the particle
    and change its kinetic energy. The magnetic force
    \(q\mathbf v\times\mathbf B\), by contrast, is perpendicular to the
    instantaneous velocity whenever it is nonzero. An ideal magnetic field
    therefore changes the direction of motion without directly changing the
    particle's speed.
    </p>

    <h3>2. Part A — Acceleration in a Uniform Electric Field</h3>

    <p>
    The first scene models a capacitor-like arrangement consisting of two
    parallel plates. The left plate is assigned positive charge and the
    right plate negative charge. In the idealized region between the plates,
    the electric field points from the positive plate towards the negative
    plate.
    </p>

    <p style="text-align:center;">
    \[
        \mathbf E=E_0\hat{\mathbf x}
    \]
    </p>

    <p>
    where \(E_0\) is the constant field magnitude and
    \(\hat{\mathbf x}\) is the unit vector along the positive \(x\)-direction.
    In the simulation, \(E_0=4.0\), \(q=1.0\), and \(m=1.0\), so the
    acceleration parameter is
    </p>

    <p style="text-align:center;">
    \[
        \mathbf a=\frac{q\mathbf E}{m},
        \qquad
        a_x=\frac{qE_0}{m}=4.0.
    \]
    </p>

    <p>
    These values are simulation parameters rather than a specification of a
    real capacitor in SI units. The scene uses a convenient dimensionless
    numerical scale to make the acceleration visible within a short animation.
    </p>

    <h3>3. Deriving the Electric-Field Trajectory</h3>

    <p>
    Newton's second law for a charge in a constant electric field is
    </p>

    <p style="text-align:center;">
    \[
        m\frac{d^2\mathbf r}{dt^2}=q\mathbf E.
    \]
    </p>

    <p>
    If the field points along \(x\) and the particle begins with zero
    transverse velocity, the \(y\) and \(z\) coordinates remain constant.
    The only nontrivial equation is
    </p>

    <p style="text-align:center;">
    \[
        \frac{d^2x}{dt^2}=\frac{qE_0}{m}=a.
    \]
    </p>

    <p>
    Integrating once gives the velocity:
    </p>

    <p style="text-align:center;">
    \[
        v_x(t)=v_{x,0}+at.
    \]
    </p>

    <p>
    Integrating a second time gives the position:
    </p>

    <p style="text-align:center;">
    \[
        \boxed{
        x(t)=x_0+v_{x,0}t+\frac12 at^2
        }
    \]
    </p>

    <p>
    The code assumes \(v_{x,0}=0\), reducing the expression to
    \(x(t)=x_0+\tfrac12 at^2\). The initial position is \(x_0=-3.2\),
    while \(y_0=z_0=0\). Consequently, the particle follows a straight
    path parallel to the field direction, with its displacement growing
    quadratically in time.
    </p>

    <p>
    The particle's speed grows linearly:
    </p>

    <p style="text-align:center;">
    \[
        v_x(t)=at,
        \qquad
        K(t)=\frac12 mv_x^2(t)=\frac12 ma^2t^2,
    \]
    </p>

    <p>
    where \(K\) is the kinetic energy. This illustrates the work-energy
    principle: the electric field performs work on the charge, transferring
    energy to its motion.
    </p>

    <h3>4. Reading the Electric-Field Visualization</h3>

    <p>
    The blue and red sheets represent the positive and negative plates,
    respectively. White plus and minus symbols identify their polarities.
    A collection of yellow arrows indicates the direction of the electric
    field. The green sphere represents the moving positive particle, while
    the plus sign placed on its surface makes its charge explicit.
    </p>

    <p>
    The orange arrow attached to the particle represents its velocity.
    As the particle accelerates, the arrow becomes longer, giving a visual
    representation of the increasing speed. The arrow's direction remains
    aligned with the positive \(x\)-axis because the electric force has no
    transverse component in this model.
    </p>

    <p>
    The animation also rotates the camera while the particle moves. This
    changes the observer's viewing direction, not the particle's physical
    coordinates. It helps reveal the three-dimensional arrangement of the
    plates and field arrows without changing the underlying one-dimensional
    dynamics.
    </p>

    <p>
    The electric-field arrows are a schematic representation of an idealized
    uniform field, not a numerical solution for the field around finite
    capacitor plates. Edge effects, the detailed surface-charge distribution,
    and the self-field of the moving particle are not calculated.
    </p>

    <h3>5. Part B — Motion in a Magnetic Field</h3>

    <p>
    The second scene changes the physical setup. A charged particle enters a
    region containing a magnetic field and follows a trajectory obtained by
    numerically integrating the Lorentz-force equations. Unlike the electric
    example, the magnetic force is perpendicular to the velocity, so the
    central effect is a change in direction rather than a direct increase
    in speed.
    </p>

    <p>
    For a magnetic field alone, the equation of motion is
    </p>

    <p style="text-align:center;">
    \[
        \boxed{
        m\frac{d\mathbf v}{dt}
        =q\,\mathbf v\times\mathbf B
        }
    \]
    </p>

    <p>
    or, in terms of the charge-to-mass ratio,
    </p>

    <p style="text-align:center;">
    \[
        \frac{d\mathbf v}{dt}
        =\frac qm\left(\mathbf v\times\mathbf B\right).
    \]
    </p>

    <p>
    The cross product is crucial: the magnetic acceleration is perpendicular
    to both the velocity and the magnetic field. Its direction depends on
    the sign of the charge and on the orientation of the two vectors.
    Reversing the sign of the charge reverses the magnetic force for the
    same instantaneous velocity and field.
    </p>

    <h3>6. Why a Magnetic Field Curves a Particle's Path</h3>

    <p>
    Consider a constant magnetic field pointing along the negative
    \(z\)-direction:
    </p>

    <p style="text-align:center;">
    \[
        \mathbf B=-B_0\hat{\mathbf z}.
    \]
    </p>

    <p>
    If the particle initially travels along the positive \(x\)-direction,
    its initial velocity is \(\mathbf v=v_x\hat{\mathbf x}\). The magnetic
    force points along positive \(y\) for a positive charge because
    </p>

    <p style="text-align:center;">
    \[
        \hat{\mathbf x}\times(-\hat{\mathbf z})
        =+\hat{\mathbf y}.
    \]
    </p>

    <p>
    The particle therefore starts bending towards positive \(y\). As its
    velocity develops a \(y\)-component, the force changes direction as well.
    This continuously changing perpendicular force produces a curved
    trajectory rather than straight-line motion.
    </p>

    <p>
    In a spatially uniform magnetic field, a particle with velocity
    perpendicular to the field undergoes circular motion in the plane
    perpendicular to \(\mathbf B\). Its cyclotron angular frequency and
    gyroradius are
    </p>

    <p style="text-align:center;">
    \[
        \boxed{\omega_c=\frac{|q|B_0}{m}},
        \qquad
        \boxed{r_L=\frac{m v_\perp}{|q|B_0}}.
    \]
    </p>

    <p>
    Here \(v_\perp\) is the component of velocity perpendicular to the field.
    If the particle also has a component parallel to the field, that component
    is unaffected by the magnetic force and the resulting trajectory is
    helical. The scene uses a field along the \(z\)-axis and an initial
    velocity along \(x\), so the initial velocity is perpendicular to the
    field.
    </p>

    <h3>7. Conservation of Kinetic Energy in a Magnetic Field</h3>

    <p>
    The magnetic force is always perpendicular to the instantaneous velocity.
    Its instantaneous power is therefore
    </p>

    <p style="text-align:center;">
    \[
        P=\mathbf F\cdot\mathbf v
        =q(\mathbf v\times\mathbf B)\cdot\mathbf v=0.
    \]
    </p>

    <p>
    Hence, in the magnetic-only model,
    </p>

    <p style="text-align:center;">
    \[
        \frac{dK}{dt}=0,
        \qquad
        |\mathbf v(t)|=|\mathbf v(0)|.
    \]
    </p>

    <p>
    The magnetic field changes the direction of the momentum vector without
    doing work on the particle. This distinction between electric and
    magnetic forces is one of the most important conceptual lessons of the
    animation: an electric field can change the magnitude of the velocity,
    whereas an ideal magnetic field redirects it.
    </p>

    <p>
    The code implements a finite magnetic-field region rather than a magnetic
    field that extends uniformly throughout all space. The particle initially
    travels through a region with zero field, enters the active region, bends
    while the field is present, and returns to field-free motion after leaving
    it. The resulting path need not be a complete circle because the magnetic
    force is applied only within the prescribed region.
    </p>

    <h2>Part II: Computational Implementation — Python, NumPy and Manim</h2>

    <h3>8. Three-Dimensional Scene Architecture</h3>

    <p>
    The animation is implemented as a Manim <code>ThreeDScene</code>. This
    class supports three-dimensional objects and camera orientation, allowing
    the plates, field vectors, and particle trajectories to be viewed from
    different angles. NumPy supplies arrays and vector operations, while
    Manim handles the geometry, labels, updaters, and rendered animation.
    </p>

    <p>
    The scene begins by defining the physical parameters:
    <code>E0 = 4.0</code>, <code>q = 1.0</code>, and <code>m = 1.0</code>.
    The acceleration is computed directly as
    <code>acceleration = q * E0 / m</code>. Keeping the acceleration tied
    to the charge, field strength, and mass makes the relation between the
    physical model and its implementation explicit.
    </p>

    <p>
    The initial camera is set using
    <code>phi = 65 degrees</code>, <code>theta = -45 degrees</code>,
    and <code>zoom = 0.8</code>. These parameters control the observer's
    view of the three-dimensional scene; they do not enter the force law.
    </p>

    <h3>9. Constructing the Electric Plates</h3>

    <p>
    Each electric plate is created using Manim's <code>Surface</code>
    object. Its position is defined by a parametric map. For the positive
    plate, the coordinates have the form
    </p>

    <p style="text-align:center;">
    \[
        \mathbf R(u,v)=(x_{\rm left},u,v),
    \]
    </p>

    <p>
    while the negative plate is constructed in the same way at
    \(x=x_{\rm right}\). Because the \(x\)-coordinate is fixed and the
    parameters \(u,v\) span the other two coordinates, each object is a
    flat rectangular sheet in the \(yz\)-plane.
    </p>

    <p>
    The left and right positions are \(-3.5\) and \(+3.5\), respectively.
    The sheets extend over the chosen ranges of \(y\) and \(z\), with
    blue and red fill colours and high opacity. A low surface resolution
    is sufficient because these objects are flat rather than curved.
    </p>

    <p>
    The polarity labels are created with <code>MathTex</code>. Rotations
    place the mathematical symbols on the visible sides of the sheets.
    Multiple rows of plus and minus symbols reinforce the interpretation
    of the plates as oppositely charged surfaces.
    </p>

    <h3>10. Building the Electric-Field Arrows</h3>

    <p>
    The electric-field visualization is generated with nested loops over
    regularly spaced \(x\), \(y\), and \(z\) coordinates. For each selected
    point, the code creates an arrow whose start and end points differ only
    in the \(x\)-coordinate:
    </p>

    <p style="text-align:center;">
    \[
        \mathbf r_{\rm start}=(x-0.18,y,z),
        \qquad
        \mathbf r_{\rm end}=(x+0.18,y,z).
    \]
    </p>

    <p>
    Every arrow therefore points in the positive \(x\)-direction. The
    nested loops generate a regular grid of 60 arrows, grouped into one
    <code>VGroup</code>. Grouping the arrows makes the scene easier to
    manage than adding each object separately.
    </p>

    <p>
    These arrows visualize the assumed field direction. Their equal lengths
    indicate a uniform field qualitatively, but their lengths and spacing
    are chosen for legibility rather than calculated from a field solver.
    </p>

    <h3>11. Representing the Particle and Its Velocity</h3>

    <p>
    The electric-field particle is represented by a green Manim
    <code>Sphere</code>. A black plus sign is placed at its centre to
    identify it as a positive charge. The sphere is a visual marker, not
    a model of the particle's physical size or internal structure.
    </p>

    <p>
    The position is controlled by a <code>ValueTracker</code>, which stores
    the animation time. A function called <code>position_at_time(t)</code>
    evaluates the analytic solution
    </p>

    <p style="text-align:center;">
    \[
        \mathbf r(t)=
        \begin{pmatrix}
        x_0+\frac12 at^2\\
        y_0\\
        z_0
        \end{pmatrix}.
    \]
    </p>

    <p>
    An updater moves the sphere to this position on every animation frame.
    A second updater moves the charge symbol to the sphere's current centre.
    This keeps the symbol attached to the particle even as the particle
    moves through the scene.
    </p>

    <p>
    The velocity arrow is recalculated during each frame. The code uses
    \(v=at\) and scales the displayed arrow length by a factor of \(0.25\).
    A minimum arrow length of \(0.2\) scene units keeps the vector visible
    at the beginning, when the ideal initial velocity is zero. The displayed
    length is therefore a visual scale, not a direct measurement in SI units.
    </p>

    <p>
    The arrow is replaced with a newly constructed arrow using
    <code>become()</code>, so its tail follows the particle and its tip moves
    farther away as the speed increases. The velocity label has its own
    updater and remains just above the arrow tip.
    </p>

    <h3>12. Animating the Electric-Field Motion</h3>

    <p>
    The electric-field scene is assembled by adding the two plates, polarity
    labels, field arrows, particle, velocity arrow, and their labels.
    The title is added as a fixed-in-frame object so it remains in the
    screen's upper region while the camera rotates.
    </p>

    <p>
    The time tracker is animated from zero to \(1.8\) over six seconds
    of rendered animation. The animation uses a linear rate function:
    the tracker's value advances uniformly in animation time. The particle's
    physical displacement, however, is quadratic in the tracker value.
    This distinction allows the rendered motion to communicate constant
    acceleration even though the animation clock advances uniformly.
    </p>

    <p>
    During this motion, Manim also rotates the camera slowly about its
    azimuthal angle. The camera rotation is stopped after the tracker reaches
    its final value. The particle and attached charge symbol then have their
    updaters cleared before the electric-field scene is removed.
    </p>

    <h3>13. Constructing the Magnetic-Field Geometry</h3>

    <p>
    The second part starts by clearing the first scene and resetting the
    camera. It introduces a new parameter set:
    <code>B0 = 1.2</code>, <code>q_m = 1.0</code>, and
    <code>v0 = 4.0</code>. The variable <code>q_m</code> represents the
    charge-to-mass ratio \(q/m\) in the equations of motion, rather than
    the charge alone.
    </p>

    <p>
    The north and south poles are represented by red and blue rectangular
    solids. Each solid begins as a unit cube and is stretched to the
    required width, height, and thickness. The red plate is positioned
    above the gap and the blue plate below it, with text labels identifying
    the two poles.
    </p>

    <p>
    Yellow magnetic-field arrows are placed in a regular grid. Each arrow
    begins at a point with \(z+0.18\) and ends at the corresponding point
    with \(z-0.18\). The arrows therefore point in the negative
    \(z\)-direction, matching the field vector used by the numerical
    model inside the active region.
    </p>

    <p>
    The pole geometry is an illustrative representation of a magnetic-field
    region, not a magnetostatic calculation of the field produced by a
    particular magnet. The code prescribes the field directly instead of
    solving Maxwell's equations for the magnetic materials and their
    boundaries.
    </p>

    <h3>14. The Magnetic-Field Model</h3>

    <p>
    The code defines the magnetic field as a piecewise function of the
    particle's position. Within the specified bounds in \(x\) and \(y\),
    the field is
    </p>

    <p style="text-align:center;">
    \[
        \mathbf B=(0,0,-B_0).
    \]
    </p>

    <p>
    Outside those bounds, the function returns the zero vector. In this
    implementation, the field-region test checks \(x\) and \(y\) but does
    not restrict \(z\). Thus, the numerical field occupies a rectangular
    region in the \(xy\)-coordinates and extends through all \(z\) values;
    the displayed pole geometry is a visual guide to the region rather
    than an exact finite-volume magnetic-field model.
    </p>

    <p>
    The particle starts at
    \(\mathbf r_0=(-4.5,-0.5,0)\) with initial velocity
    \(\mathbf v_0=(4,0,0)\). Initially it moves along positive \(x\).
    When it enters the region where the field is nonzero, the cross product
    in the Lorentz force produces acceleration in the positive \(y\)
    direction for the chosen positive charge-to-mass ratio.
    </p>

    <h3>15. Converting the Equations into a First-Order System</h3>

    <p>
    Numerical integrators operate naturally on first-order differential
    equations. The code therefore combines the three position components
    and three velocity components into a six-dimensional state vector:
    </p>

    <p style="text-align:center;">
    \[
        \mathbf Y=
        \begin{pmatrix}
        \mathbf r\\
        \mathbf v
        \end{pmatrix}
        =
        \begin{pmatrix}
        x\\y\\z\\v_x\\v_y\\v_z
        \end{pmatrix}.
    \]
    </p>

    <p>
    Its derivative is
    </p>

    <p style="text-align:center;">
    \[
        \frac{d\mathbf Y}{dt}
        =
        \begin{pmatrix}
        \mathbf v\\
        (q/m)(\mathbf v\times\mathbf B)
        \end{pmatrix}.
    \]
    </p>

    <p>
    In Python, <code>state[:3]</code> extracts the position and
    <code>state[3:]</code> extracts the velocity. The derivative function
    computes the position derivative as the velocity and the velocity
    derivative with <code>np.cross(v, magnetic_field(r))</code>.
    Finally, <code>np.concatenate</code> combines both three-component
    vectors into a six-component derivative.
    </p>

    <p>
    This separation between the state representation and the derivative
    function is useful computationally. The physical model is encoded in
    one function, while the numerical integration algorithm can remain
    independent of the particular field configuration.
    </p>

    <h3>16. Fourth-Order Runge–Kutta Integration</h3>

    <p>
    The magnetic trajectory is calculated before the particle animation
    begins. The integration time step is \(dt=0.005\), and the total
    simulated duration is \(T=5.0\). The resulting trajectory contains
    the initial position and the position calculated after each integration
    step.
    </p>

    <p>
    The code uses the classical fourth-order Runge–Kutta method, often
    abbreviated RK4. For an equation
    \(d\mathbf Y/dt=\mathbf f(t,\mathbf Y)\), its four intermediate
    slopes are
    </p>

    <p style="text-align:center;">
    \[
        \begin{aligned}
        \mathbf k_1&=\mathbf f(t,\mathbf Y),\\
        \mathbf k_2&=\mathbf f\left(t+\frac{dt}{2},
        \mathbf Y+\frac{dt}{2}\mathbf k_1\right),\\
        \mathbf k_3&=\mathbf f\left(t+\frac{dt}{2},
        \mathbf Y+\frac{dt}{2}\mathbf k_2\right),\\
        \mathbf k_4&=\mathbf f(t+dt,\mathbf Y+dt\,\mathbf k_3).
        \end{aligned}
    \]
    </p>

    <p>
    The state is advanced using the weighted average
    </p>

    <p style="text-align:center;">
    \[
        \boxed{
        \mathbf Y_{n+1}=\mathbf Y_n+
        \frac{dt}{6}
        \left(\mathbf k_1+2\mathbf k_2+2\mathbf k_3+\mathbf k_4\right)
        }
    \]
    </p>

    <p>
    The intermediate slopes improve the approximation over a simple
    forward-Euler step. For sufficiently smooth differential equations,
    RK4 has fourth-order global accuracy as the step size is reduced.
    Here, however, the field changes abruptly at the boundary of the
    prescribed magnetic region. The derivative is consequently
    discontinuous there, so the usual smooth-problem accuracy argument
    does not apply uniformly at the crossing. Reducing the time step or
    explicitly detecting boundary crossings can improve the reliability
    of the numerical trajectory.
    </p>

    <h3>17. Turning the Numerical Solution into an Animation</h3>

    <p>
    Once the integration is complete, the stored positions are converted
    into a NumPy array. A green sphere represents the particle, and a
    plus sign is attached to its centre. A <code>TracedPath</code> object
    records the positions visited by the moving sphere, progressively
    revealing its trajectory.
    </p>

    <p>
    A new <code>ValueTracker</code> controls the playback time. The particle
    updater converts the tracker's value into a trajectory index by dividing
    by the numerical step size. Since the tracker usually lies between
    discrete integration times, the code uses the neighbouring points
    indexed by \(i\) and \(i+1\) and linearly interpolates between them:
    </p>

    <p style="text-align:center;">
    \[
        \mathbf r(t)\approx
        (1-\alpha)\mathbf r_i+\alpha\mathbf r_{i+1},
        \qquad 0\leq\alpha\leq1.
    \]
    </p>

    <p>
    This interpolation allows the rendered particle to move smoothly
    between the precomputed numerical samples. The interpolation is a
    visualization step: the underlying physical trajectory remains the
    array of positions generated by RK4.
    </p>

    <p>
    The trace is generated during playback, rather than being displayed
    completely at the start. This makes the relation between the moving
    particle and its past path visible. The sphere, charge symbol, and
    trajectory can therefore be interpreted together as the instantaneous
    state and the history of the numerical solution.
    </p>

    <h3>18. A Moving Camera for Three-Dimensional Interpretation</h3>

    <p>
    During the magnetic motion, a <code>VectorizedPoint</code> acts as a
    camera driver. Its updater accumulates elapsed animation time and
    calculates new camera angles. The elevation varies sinusoidally,
    while the azimuth increases steadily:
    </p>

    <p style="text-align:center;">
    \[
        \phi(t)=65^\circ+18^\circ\sin(0.7t),
        \qquad
        \theta(t)=-45^\circ+0.45t.
    \]
    </p>

    <p>
    The camera angles are updated using <code>set_phi()</code> and
    <code>set_theta()</code>. Because the camera driver updates while the
    time tracker advances, the particle motion and camera motion occur
    simultaneously. After the animation, the camera driver's updater is
    cleared and the driver is removed.
    </p>

    <p>
    Changing the viewpoint is especially useful for distinguishing the
    direction of the magnetic field from the direction of the particle's
    velocity. It also makes clear that the trajectory is a spatial curve
    whose appearance on the screen depends on the observer's perspective.
    A camera rotation does not itself exert a force on the particle or
    alter the numerical solution.
    </p>

    <h3>19. Physical Assumptions and Numerical Limitations</h3>

    <p>
    The simulation is designed to communicate the structure of the equations
    and the difference between electric and magnetic forces. Several
    simplifications should be kept in mind when interpreting it:
    </p>

    <ul>
        <li>
        <strong>Classical dynamics:</strong> The particle is described by
        Newtonian equations of motion. Relativistic effects are not included.
        </li>
        <li>
        <strong>Prescribed fields:</strong> The electric and magnetic fields
        are defined by simple formulas and regions rather than calculated
        self-consistently from Maxwell's equations.
        </li>
        <li>
        <strong>No radiation reaction:</strong> Electromagnetic radiation
        emitted by an accelerating charge is not included in the equation
        of motion.
        </li>
        <li>
        <strong>No back-reaction:</strong> The particle does not alter the
        fields that act on it.
        </li>
        <li>
        <strong>Finite numerical resolution:</strong> The magnetic motion
        is computed at a finite time step and then interpolated for display.
        Numerical error can accumulate, particularly near the abrupt field
        boundary.
        </li>
        <li>
        <strong>Schematic geometry:</strong> The displayed plates and
        field arrows illustrate the prescribed fields; they do not constitute
        a complete electromagnetic model of a real capacitor or magnet.
        </li>
    </ul>

    <p>
    In the magnetic-only portion, an important numerical check is whether
    the speed remains approximately constant while the particle is inside
    the field. Since the ideal magnetic force does no work, large systematic
    changes in speed would indicate a numerical issue or an unintended
    change in the implemented equations. One could also compare the
    numerical path with the analytical circular orbit for a uniform field
    extending throughout space, while remembering that the present
    simulation switches the field off outside its prescribed region.
    </p>

    <h3>20. Further Investigations</h3>

    <p>
    The project provides a starting point for several extensions that turn
    the visualization into a more quantitative computational-physics study.
    One could vary the charge-to-mass ratio and investigate how the
    cyclotron frequency and gyroradius scale with \(q/m\). Reversing the
    sign of the charge would reverse the direction of curvature, while
    increasing the field magnitude would increase the curvature of the
    orbit for the same initial speed.
    </p>

    <p>
    A second extension would add simultaneous electric and magnetic fields
    and solve the full Lorentz equation
    \(m\,d\mathbf v/dt=q(\mathbf E+\mathbf v\times\mathbf B)\).
    This would allow the study of crossed-field motion, drift phenomena,
    and the conditions under which electric and magnetic forces balance.
    Another extension would replace the abrupt field boundary with a
    smooth spatial profile, allowing more controlled numerical comparisons.
    </p>

    <p>
    Finally, the numerical trajectory could be accompanied by plots of
    \(x(t)\), \(y(t)\), \(z(t)\), the velocity components, kinetic energy,
    and the magnitude of the velocity. Such plots would connect the
    geometric animation to quantitative diagnostics and make it possible
    to assess numerical accuracy rather than relying only on visual
    appearance.
    </p>

    <h3>Conclusion</h3>

    <p>
    This project combines analytical kinematics, vector algebra, numerical
    integration, and three-dimensional scientific visualization. The
    electric-field scene demonstrates constant acceleration and the
    quadratic dependence of displacement on time. The magnetic-field
    scene uses the Lorentz force and fourth-order Runge–Kutta integration
    to construct a trajectory in a prescribed spatial field.
    </p>

    <p>
    The central physical insight is that the direction and magnitude of a
    charged particle's velocity respond differently to electric and
    magnetic forces. By placing the two cases in one animation, the project
    links Newtonian dynamics to electromagnetic theory and demonstrates
    how a differential-equation model can be translated into a numerical
    solution and then into a visual representation.
    </p>
    """,

    }

]


@app.route("/")
def home():

    return render_template(
        "index.html",
        projects=projects
    )


@app.route("/project/<slug>")
def project(slug):

    selected_project = None

    for project in projects:

        if project["slug"] == slug:
            selected_project = project
            break

    if selected_project is None:
        return "Project not found", 404


    # Build the path to the source code

    code_path = os.path.join(
        app.root_path,
        selected_project["code"]
    )


    # Read the Python source code

    with open(code_path, "r", encoding="utf-8") as file:

        source_code = file.read()


    # Syntax highlighting

    highlighted_code = highlight(
        source_code,
        PythonLexer(),
        HtmlFormatter(
            cssclass="highlight"
        )
    )


    return render_template(
        "project.html",
        project=selected_project,
        highlighted_code=highlighted_code
    )


if __name__ == "__main__":
    app.run(debug=True)