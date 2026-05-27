# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import pycroxe

project = "PyCroXe"
copyright = "2026, Luca Cinnirella"
author = "Luca Cinnirella"
release = pycroxe.__version__

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = ["sphinx.ext.autodoc", "sphinx.ext.autosummary"]

templates_path = ["_templates"]
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "pydata_sphinx_theme"
html_theme_options = {
    "icon_links": [
        {
            "name": "Codeberg",
            "url": "https://codeberg.org/Kruayd/PyCroXe",
            "icon": "https://design.codeberg.org/logo-kit/icon_inverted.svg",
            "type": "url",
        }
    ]
}
html_static_path = ["_static"]
