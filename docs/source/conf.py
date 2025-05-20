
# -- Project information -----------------------------------------------------

project = 'PurrfectKit'
copyright = '2025, SUWALUTIONS'
author = 'SUWALUTIONS'
version = '0.0.1'
release = '0.0.1'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
]

templates_path = ['_templates']
exclude_patterns = []
language = 'en'

# -- Intersphinx configuration -----------------------------------------------
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
}

# -- Autodoc configuration ---------------------------------------------------
autodoc_member_order = 'bysource'
autosummary_generate = True
autodoc_mock_imports = ['pytesseract', 'easyocr', 'surya', 'markitdown', 'docling', 'pymupdf']

# -- Options for HTML output -------------------------------------------------
html_theme = 'furo'
html_static_path = ['_static']
templates_path = ['_templates']

html_css_files = [
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/fontawesome.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/solid.min.css",
    "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/brands.min.css",
]
html_theme_options = {
    "footer_icons": [
        {
            "name": "GitHub",
            "url": "https://github.com/suwalutions/PurrfectKit/tree/meow",
            "html": "",
            "class": "fa-brands fa-solid fa-github fa-2x",
        },
    ],
}