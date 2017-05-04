# Building Spoofax

This section describes how to build Spoofax from scratch, on the command-line.

## Supported platforms

OSX, Linux, and Windows are supported.

## Requirements

1. **Java JDK 8** is required for build the projects. The `JAVA_HOME` environment variable must point to the JDK root directory.
2. **Git 1.8.2 or higher** is required to check out the source code from our GitHub repositories. Instructions on how to install Git for your platform can be found here: <http://git-scm.com/downloads>. If you run OSX and have [Homebrew](http://brew.sh/) installed, you can install Git by executing `brew install git`. Confirm your Git installation by executing `git version`.
3. **Maven 3.3.9 or higher** is required to build Spoofax and StrategoXT, refer to the [Setting up Maven](maven.md) section for instructions on how to install Maven.
4. **MetaBorg Maven artifacts** are required since the build depends on artifacts from previous builds for bootstrapping purposes. Follow [Using MetaBorg Maven artifacts](maven.md) to make these artifacts available to Maven.
5. **Python 3.4 or higher** is used to orchestrate the build. Instructions on how to install Python for your platform can be found here: <https://www.python.org/downloads/>. If you run OSX and have [Homebrew](http://brew.sh/) installed, you can install Python by executing `brew install python3`. Confirm your Python installation by executing `python3 --version`.
6. **Pip 7.0.3 or higher** is used to download some python dependencies. A version comes preinstalled with Python 3, but you need to make sure that you have version 7.0.3 or higher. To upgrade to the newest version use `pip install --upgrade pip` or `pip3 install --upgrade pip`, depending on if your OS uses a different pip for Python 3. Confirm using `pip --version` or `pip3 --version`.

## Cloning the source code

Clone the source code from the [spoofax-releng](https://github.com/metaborg/spoofax-releng) repository with the following commands:

```bash
git clone https://github.com/metaborg/spoofax-releng.git
cd spoofax-releng
git submodule update --init --remote --recursive
```

Cloning and updating submodules can take a while, since we have many submodules and some have a large history.

## Building

To build Spoofax, simply execute:

```bash
./b build all
```

This downloads the latest StrategoXT, and builds Spoofax. If you also want to build StrategoXT from scratch, execute:

```bash
./b build -st all
```

The `-s` flag build StrategoXT instead of downloading it, and `-t` skips the StrategoXT tests since they are very lengthy.
The `all` part of the command indicates that we want to build all components. If you would only like to build the Java components of Spoofax, and skip the Eclipse plugins, execute:

```bash
./b build java
```

Use `./b build` to get a list of components available for building, and `./b build --help` for help on all the command-line flags and switches.

```eval_rst
.. note:: If you have opened a project in the repository in Eclipse, you **must turn off** :menuselection:`Project --> Build Automatically` in Eclipse, otherwise the Maven and Eclipse compilers will interfere and possibly fail the build. After the Maven build is finished, enable :guilabel:`Build Automatically` again.
```

## Updating the source code

If you want to update the repository and submodules, execute:

```bash
git pull --rebase
./b checkout
./b update
```

The `git pull` command will update any changes in the main repository. The `./b checkout` command will check out the correct branches in all submodules, because Git does not do this automatically. The `./b update` command will update all submodules.

## Switching to a different branch

Switching to a different branch, for example the `spoofax-release` branch, is done with the following commands:

```bash
git checkout spoofax-release
git pull --rebase
git submodule update --init --remote --recursive
./b checkout
./b update
```

## Troubleshooting

### Resetting and cleaning

If updating or checking out a branch of submodule fails (because of unstaged or conflicting changes), you can try to resolve it yourself, or you can reset and clean everything. Reset and clean all submodules using:

```bash
./b reset
./b clean
```

```eval_rst
.. warning:: Resetting and cleaning DELETES UNCOMMITTED AND UNPUSHED CHANGES, which can cause PERMANENT DATA LOSS. Make sure all your changes are committed and pushed!
```

### Weird compilation errors

If you get any weird compilation errors during the build, make sure that <span class='menuselection'>Project ‣ Build Automatically</span> is turned off in Eclipse.
