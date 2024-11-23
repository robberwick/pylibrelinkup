# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import os

from setuptools_scm import get_version

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "PyLibreLinkUp"
copyright = "2024, Rob Berwick"
author = "Rob Berwick"

release = get_version(root="..", relative_to=__file__)

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

autodoc_member_order = "groupwise"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.viewcode",
    "sphinx.ext.duration",
    "sphinx.ext.doctest",
    "sphinx.ext.autosummary",
    "sphinx.ext.intersphinx",
    "sphinx_autodoc_typehints",
    "sphinxcontrib.autodoc_pydantic",
    "enum_tools.autoenum",
]

intersphinx_mapping = {
    "python": ("https://docs.python.org/3/", None),
    "sphinx": ("https://www.sphinx-doc.org/en/master/", None),
}
intersphinx_disabled_domains = ["std"]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]


# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_baseurl = os.environ.get("READTHEDOCS_CANONICAL_URL", "/")
html_theme = "sphinx_rtd_theme"

# -- Options for EPUB output
epub_show_urls = "footnote"
