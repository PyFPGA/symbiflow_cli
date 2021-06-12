# -*- coding: utf-8 -*-

import os
import sys
sys.path.insert(0, os.path.abspath('..'))

# -- Project information -----------------------------------------------------

project = 'SymbiFlow CLI'
copyright = '2021, Rodrigo A. Melo'
author = 'Rodrigo A. Melo'

# The short X.Y version
version = ''
# The full version, including alpha/beta/rc tags
release = ''

# -- General configuration ---------------------------------------------------

# needs_sphinx = '3.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.extlinks',
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'inherited-members': True,
}

templates_path = ['_templates']

source_suffix = '.rst'

master_doc = 'index'

language = None

exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

pygments_style = None

# -- Options for HTML output -------------------------------------------------

html_theme = 'classic'

# html_theme_options = {}

html_static_path = ['_static']

# html_sidebars = {}

# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = 'SymbiFlowCLIdoc'

# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',

    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',

    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',

    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (master_doc, 'SymbiFlowCLI.tex', 'SymbiFlow CLI Documentation',
     'Rodrigo A. Melo', 'manual'),
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [
    (master_doc, 'symbiflowcli', 'SymbiFlow CLI Documentation',
     [author], 1)
]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (master_doc, 'SymbiFlowCLI', 'SymbiFlow CLI Documentation',
     author, 'SymbiFlowCLI', 'One line description of project.',
     'Miscellaneous'),
]


# -- Options for Epub output -------------------------------------------------

# Bibliographic Dublin Core info.
epub_title = project

# The unique identifier of the text. This can be a ISBN number
# or the project homepage.
#
# epub_identifier = ''

# A unique identification for the text.
#
# epub_uid = ''

# A list of files that should not be packed into the epub file.
epub_exclude_files = ['search.html']

# -- Sphinx.Ext.ExtLinks --------------------------------------------------

extlinks = {
    'wikipedia': ('https://en.wikipedia.org/wiki/%s', None),
    'github':    ('https://github.com/%s', None),
}
