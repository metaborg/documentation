# Spoofax documentation

This repository contains the Spoofax documentation, made with [Sphinx](http://www.sphinx-doc.org/en/stable/) in the [Read The Docs](https://docs.readthedocs.org/en/latest/index.html) style of documentation.

This documentation is hosted at http://spoofax.readthedocs.org/.
When a commit to this repository is made, it will automatically [build and update](http://readthedocs.org/projects/spoofax/builds/) the documentation.

## Building

To build the documentation, use the Makefile:

```bash
make html
```

which will generate HTML documentation into `_build/html` with `_build/html/index.html` as the main page.

Sphinx does incremental building if possible. If your changes are not being built for some reason, use the `clean` target:

```bash
make clean html
```

### Other targets

* `latexpdf` for a PDF version (via latex) of the documentation. A working latex distribution is required.
* `epub` for an epub version, an e-book format with resizable text, for tablets and e-readers.
* `singlehtml` for single page HTML documentation.
* `text` for plain-text documentation.
* `help` for a list of all other targets.

### Generated API documentation

Java API documentation is generated from submodules in the `code` directory.
Make sure all submodules are checked out and up to date by running:

```bash
git submodule update --init --remote --recursive
```

By default, generated API docs are not built when building the documentation, because it can take several minutes to generate and render them.
To generate API docs, pass `APIDOC=1` to make:

```bash
make html APIDOC=1
```

## Requirements

Sphinx requires Python, at least version 2.6. To install the required Python packages, run:

```
pip install -r requirements.txt
```
