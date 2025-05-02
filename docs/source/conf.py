# Configuration file for the Sphinx documentation builder.

project = 'REST API'
copyright = '2025, Victoria Stovba'
author = 'Victoria Stovba'
release = '0.1'

import os
import sys
sys.path.insert(0, os.path.abspath('../../'))



extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
]

templates_path = ['_templates']
exclude_patterns = []

html_theme = 'alabaster'
html_static_path = ['_static']
