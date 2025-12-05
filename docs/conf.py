"""Sphinx configuration file for BRAID-DSPy documentation."""

import os
import sys
from datetime import datetime

# Add the parent directory to the path so we can import braid
sys.path.insert(0, os.path.abspath('..'))

# Project information
project = 'BRAID-DSPy'
copyright = f'{datetime.now().year}, Braid-DSPy Contributors'
author = 'Braid-DSPy Contributors'

# Get version from package
try:
    from braid import __version__
    release = __version__
    version = '.'.join(__version__.split('.')[:2])  # Major.minor
except ImportError:
    release = '0.1.0'
    version = '0.1'

# General configuration
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'myst_parser',
    'sphinx_copybutton',
]

# MyST parser configuration
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'html_admonition',
    'html_image',
    'replacements',
    'smartquotes',
    'substitution',
    'tasklist',
]

myst_heading_anchors = 3

# Napoleon settings for NumPy/Google style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = False
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_preprocess_types = False
napoleon_type_aliases = None
napoleon_attr_annotations = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': False,
    'exclude-members': '__weakref__',
}

autodoc_mock_imports = []

# Autosummary settings
autosummary_generate = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'dspy': ('https://dspy.ai/', None),
}

# Templates path
templates_path = ['_templates']

# The suffix(es) of source filenames
source_suffix = {
    '.rst': 'restructuredtext',
    '.txt': 'markdown',
    '.md': 'markdown',
}

# The master toctree document
master_doc = 'index'

# Language
language = 'en'

# List of patterns to ignore
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The name of the Pygments (syntax highlighting) style to use
pygments_style = 'sphinx'

# HTML theme options
html_theme = 'sphinx_rtd_theme'
html_theme_options = {
    'analytics_id': '',
    'logo_only': False,
    'display_version': True,
    'prev_next_buttons_location': 'bottom',
    'style_external_links': False,
    'vcs_pageview_mode': '',
    'style_nav_header_background': '#2980B9',
    # Toc options
    'collapse_navigation': True,
    'sticky_navigation': True,
    'navigation_depth': 4,
    'includehidden': True,
    'titles_only': False,
}

# HTML static files
html_static_path = ['_static']

# Custom CSS
html_css_files = [
    'custom.css',
]

# Logo
html_logo = None
html_favicon = None

# Output file base name for HTML help builder
htmlhelp_basename = 'braid-dspy-doc'

# -- Options for LaTeX output ------------------------------------------------
latex_elements = {}

latex_documents = [
    (master_doc, 'braid-dspy.tex', 'BRAID-DSPy Documentation',
     'Braid-DSPy Contributors', 'manual'),
]

# -- Options for manual page output ------------------------------------------
man_pages = [
    (master_doc, 'braid-dspy', 'BRAID-DSPy Documentation',
     [author], 1)
]

# -- Options for Texinfo output ----------------------------------------------
texinfo_documents = [
    (master_doc, 'braid-dspy', 'BRAID-DSPy Documentation',
     author, 'braid-dspy', 'BRAID integration for DSPy framework',
     'Miscellaneous'),
]

# -- Options for Epub output -------------------------------------------------
epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright

epub_exclude_files = ['search.html']

