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
        "description": "A visualization of Gaussian curvature using Manim.",
        "video": "solar.mp4",
        "code": "source_code/solarsys.py"
    },

    {
        "name": "BPS Black Holes",
        "slug": "bps-black-holes",
        "description": "A visualization related to BPS black holes in supergravity and string theory.",
        "video": "PortfolioTest.mp4",
        "code": "source_code/testfile.py"
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