# Spoofax documentation

This repository contains the Spoofax documentation, made with [Sphinx](http://www.sphinx-doc.org/en/stable/) in the [Read The Docs](https://docs.readthedocs.io/en/latest/index.html) style of documentation.

This documentation is hosted at http://www.metaborg.org/en/latest/.
When a commit to this repository is made, it will automatically [build and update](http://readthedocs.org/projects/spoofax/builds/) the documentation.

## Requirements

Sphinx requires Python, at least version 2.6. To install the required Python packages, run:

```bash
pip install -r requirements.txt --upgrade
```

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

## Troubleshooting

### Could not import extension

While making the documentation, if you get an error similar to this:

```bash
Could not import extension foo (exception: No module named foo)
```

Then you need to update the installed Python packages from the `requirements.txt` file.

### Could not find function xmlCheckVersion in library libxml2

If you get this error while installing the required Python packages:

```bash
*********************************************************************************
Could not find function xmlCheckVersion in library libxml2. Is libxml2 installed?
*********************************************************************************
```

Then you need to install `lxml` through `easy_install` instead:

```bash
easy_install lxml
```

After that, installing the required Python packages through `pip` should succeed.

### Microsoft Visual C++ 9.0 is required (Unable to find vcvarsall.bat)

If you get this error while installing the required Python packages on Windows:

```
error: Microsoft Visual C++ 9.0 is required (Unable to find vcvarsall.bat).
```

Then you need to download and install _Microsoft Visual C++ Compiler
for Python 2.7_ from [http://aka.ms/vcpython27](http://aka.ms/vcpython27).
