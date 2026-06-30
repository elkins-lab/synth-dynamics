import os
import sys

sys.path.insert(0, os.path.abspath(".."))

project = "synth-dynamics"
copyright = "2026, George Elkins"
author = "George Elkins"
release = "0.1.3"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path: list[str] = []
html_extra_path = ["google7f0d84bcdb02d19b.html"]
