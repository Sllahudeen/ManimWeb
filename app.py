from flask import Flask, render_template

from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import HtmlFormatter

import os


app = Flask(__name__)


projects = [

    {
        "name": "Curved Spacetime",
        "slug": "Curved-Spacetime",
        "description": "A visualization of Gaussian curvature for Earth and Sun",
        "video": "solar.mp4",
        "code": "source_code/solarsys.py"
    },

    {
        "name": "3D Rotations",
        "slug": "3D-Rotations",
        "description": "A visualization of tetrahedron spinning around a moving axis",
        "video": "tetra.mp4",
        "code": "source_code/moext.py"
    },

    {
        "name": "Shortest Path Under Constant Acceleration",
        "slug": "shortest-path-under-constant-acceleration",
        "description": "This animation demonstrates shortest path of a boby moving under constant acceleration",
        "video": "bc.mp4",
        "code": "source_code/Brachistochrone.py"
    },

    {
        "name": "Spherical Harmonics",
        "slug": "spherical-harmonics",
        "description": "This animation describes shape of different spherical harmonics in application to hydrogen atom they describe the probability density of electron in hydrogen atom",
        "video": "RSH.mp4",
        "code": "source_code/H_orbitals.py"
    },

    {
        "name": "Evolution of Qubit",
        "slug": "evolution-of-qubit",
        "description": "This animation describes the evolution of qubit in the presence of time-dependent magnetic field",
        "video": "BlochFieldEvolution.mp4",
        "code": "source_code/quantumdyn.py"
    },

    {
        "name": "Double Pendulum",
        "slug": "double-pendulum",
        "description": "This animation demonstrates double pendulum",
        "video": "DoublePendulum.mp4",
        "code": "source_code/pendulum.py"
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