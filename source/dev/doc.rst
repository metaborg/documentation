=============
Documentation
=============

This section describes the documentation tools and provides guidelines for writing documentation.

Tools
-----

This documentation is written with the `Sphinx documentation generator <http://www.sphinx-doc.org/en/stable/>`_.
Sphinx is the tool that transforms the documentation into a website and other output formats. Documentation can be found in their website:

- `Sphinx-specific Markup Constructs <http://www.sphinx-doc.org/en/stable/markup/index.html>`_
- `Domains <http://www.sphinx-doc.org/en/stable/domains.html>`_
- `All documentation <http://www.sphinx-doc.org/en/stable/contents.html>`_

Formats
~~~~~~~

ReStructuredText is the main documentation format used by Sphinx. Documentation can be found at:

- `Quick reference <http://docutils.sourceforge.net/docs/user/rst/quickref.html>`_
- `Primer <http://www.sphinx-doc.org/en/stable/rest.html>`_
- `Full reference documentation <http://docutils.sourceforge.net/docs/ref/rst/directives.html>`_

Markdown is also supported, but is less powerful for technical documentation purposes. It is supported through the `recommonmark <http://recommonmark.readthedocs.io/en/latest/index.html>`_ extension. To use markdown, just create ``.md`` files and link them in a ``toctree``.

Converting formats with Pandoc
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

`Pandoc <http://pandoc.org/>`_ is a documentation format converting tool. It can be used to convert between various documentation formats.
On macOS with Homebrew, it can be installed with ``brew install pandoc``.

Conversion is performed by passing the ``from`` and ``to`` flags. For example, to convert Markdown to ReStructuredText, run the following command:

.. code-block:: bash

   pandoc --from=markdown --to=rst file.md --wrap=preserve > file.rst

See their `manual <http://pandoc.org/MANUAL.html>`_ for more info.

Bibliographies
~~~~~~~~~~~~~~

BibTeX bibliographies and citations are supported through the `sphinxcontrib-bibtext <https://sphinxcontrib-bibtex.readthedocs.io/en/latest/quickstart.html#minimal-example>`__ extension.

To create a separate bibliography for a chapter use a label and key prefix as follows::

   Syntactic completions :cite:`s-AmorimEWV16` 

   .. bibliography:: ../../../../bib/spoofax.bib 
      :style: plain  
      :labelprefix: S
      :keyprefix: s-
   
   
Customizing HTML with CSS and JavaScript
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``_static`` directory contains a ``style.css`` and ``script.js`` file to customize the HTML output.

Writing guide
-------------

General guidelines
~~~~~~~~~~~~~~~~~~

Each chapter in the manual, i.e. a top-level entry in the table of contents should start with a paragraph that explains what the chapter is about, including a definition of the thing it documents. For example: "Stratego is a language for defining program transformations ..."

Meta-language documentation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Standard documentation ingredients for meta-language documentation:

- Introduction

  - main concepts and a small example
  - how does it fit in the bigger picture?

- Reference manual

  - a systematic description of all language features
  - include schematic descriptions
  - use examples for illustration

- Configuration

  - how to build it
  - configuration options (yaml, esv, stratego hooks)
  - how to call it / use it

- Examples

  - typical examples
  - examples for some specific features
  - pointers to real projects

- Bibliography

  - list with all or at least key publications
  - discussion of what each publication contributes

It probably makes sense to put each of these in a separate section.
