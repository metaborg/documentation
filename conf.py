#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import datetime
import sys
import os

import recommonmark
from recommonmark.parser import CommonMarkParser
from recommonmark.transform import AutoStructify

# -- General configuration

extensions = [
  'sphinx.ext.todo',
  'sphinx.ext.imgmath',
  'sphinx.ext.intersphinx',
  'sphinxcontrib.bibtex',
  'versionwarning.extension',
  'myst_parser'
]
imgmath_image_format = 'svg'
templates_path = ['_templates']
source_suffix = ['.rst', '.md']
master_doc = 'index'
project = 'Spoofax'
copyright = '2016-' + str(datetime.date.today().year) + ', MetaBorg'
author = 'MetaBorg'
version = '2.5.16'
release = version
language = 'en'
exclude_patterns = ['.venv', 'venv', '_build', 'notes', 'include', 'README.md']
pygments_style = 'sphinx'
todo_include_todos = True
bibtex_bibfiles = ['source/bib/spoofax.bib']

# Include include/_all.rst in all documents.
rst_prolog = """
.. include:: /include/_all.rst
"""


# -- Options for HTML output

# Only import and set the ReadTheDocs theme if we're building docs locally.
on_rtd = os.environ.get('READTHEDOCS', None) == 'True'
if not on_rtd:
  import sphinx_rtd_theme
  html_theme = 'sphinx_rtd_theme'
  html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

html_favicon = 'favicon.ico'
html_static_path = ['_static']
html_css_files = [
    'style.css',
    'https://dev-cats.github.io/code-snippets/JetBrainsMono.css',
    'https://use.fontawesome.com/releases/v5.12.1/css/all.css',
]
html_js_files = [
    'script.js',
]
htmlhelp_basename = 'Spoofaxdoc'

# -- Options for LaTeX output

latex_documents = [
  (master_doc, 'Spoofax.tex', 'Spoofax Documentation', 'MetaBorg', 'manual'),
]

# -- Options for manual page output

man_pages = [
  (master_doc, 'spoofax', 'Spoofax Documentation', [author], 1)
]

# -- Options for Texinfo output

texinfo_documents = [
  (master_doc, 'Spoofax', 'Spoofax Documentation', author, 'Spoofax', 'Spoofax documentation', 'Miscellaneous')
]

# -- Options for Epub output

epub_title = project
epub_author = author
epub_publisher = author
epub_copyright = copyright
epub_exclude_files = ['search.html']

# -- Options for intersphix extension

spoofax_api_loc = 'http://www.metaborg.org/projects/spoofax-api/en/latest/'

intersphinx_mapping = {'api': (spoofax_api_loc, None)}

# -- Options for versionwarning, used for deprecation banner

versionwarning_body_selector = 'div.document'
versionwarning_messages = {
  "latest": 'This documentation is deprecated and not maintained. For the most up-to-date documentation, please refer to <a href="https://www.spoofax.dev/">spoofax.dev</a>.'
}
versionwarning_project_slug = 'spoofax'
versionwarning_project_version = 'latest'

# -- Additional Sphinx configuration

def setup(app):
  app.add_config_value('recommonmark_config', {'auto_toc_tree_section': 'Contents'}, 'env')
  app.add_transform(AutoStructify)
