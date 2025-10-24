# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys
import datetime

sys.path.insert(0, os.path.abspath(".."))

project = 'PurrfectKit'
copyright = f'{str(datetime.datetime.now().year)}, SUWALUTIONS CO., LTD'
author = 'Kharapsy'

from purrfectmeow import __version__ as release

version = ".".join(release.split(".")[:2])

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo", 
    "sphinx.ext.viewcode", 
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
]

autosummary_generate = True

templates_path = ['_templates']
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

todo_include_todos = True

autoclass_content = "both"
autodoc_member_order = "bysource"
autodoc_typehints = "description"

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    "logo_only": True,
    "canonical_url": "https://suwalutions.com",
    "collapse_navigation": False,
    "navigation_depth": 3,
    "style_nav_header_background": "#42220E",
}

html_static_path = ['_static']

html_logo = "_static/logo.png"
html_favicon = "_static/favicon.png"

html_context = {
    "display_github": True,
    "github_user": "suwalutions",
    "github_repo": "PurrfectKit",
    "github_version": "meow",
    "conf_py_path": "/docs/",
}

# Mock heavy libraries to avoid installing them
autodoc_mock_imports = [
    "sentence_transformers",
    "transformers",
    "docling",
    "pymupdf4llm",
    "pdf2image",
    "pytesseract",
    "easyocr",
    "surya_ocr",
    "python_doctr",
    "pandas",
    "numpy"
]
