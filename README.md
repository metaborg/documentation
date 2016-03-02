# Spoofax Documentation

This repository contains the Spoofax documentation, made with [Sphinx](http://www.sphinx-doc.org/en/stable/) in the [Read The Docs](https://docs.readthedocs.org/en/latest/index.html) style of documentation.

This documentation is hosted at http://spoofax.readthedocs.org/.
When a commit to this repository is made, it will automatically [build and update](http://readthedocs.org/projects/spoofax/builds/) the documentation.

## Building

To build the documentation, use the Makefile:

```
make clean html
```

which will generate HTML documentation into `_build/html` with `_build/html/index.html` as the main page.
Use the `latexpdf` target to build a PDF version of the documentation, and `epub` for an e-book (book format with resizable text, for tablets and e-readers) build.

## Requirements

Sphinx requires Python, at least version 2.6. To install the required Python packages, run:

```
pip install -r requirements.txt
```
