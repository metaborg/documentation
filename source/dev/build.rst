.. _dev-build:

========
Building
========

This section describes how to build Spoofax from scratch, on the command-line.

.. _dev-build-clone:

Cloning the source code
-----------------------

Clone the source code from the `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ repository with the following commands:

|macOS| macOS, |Linux| Linux, |Windows| Windows
  .. code:: bash

      git clone --recursive https://github.com/metaborg/spoofax-releng.git
      cd spoofax-releng

Cloning and updating submodules can take a while, since we have many submodules and some have a large history.
Additionally, only on Windows, you have to do the following:

|Windows| Windows
  .. code:: bat

      cd releng\releng
      py -m pip install -r .\requirements.txt


Start a build
-------------

To build Spoofax, simply execute:

|macOS| macOS, |Linux| Linux
  .. code:: bash

      ./b build all

|Windows| Windows
  .. code:: bat

      .\bd.bat build all

This downloads the latest Stratego/XT, and builds Spoofax. If you also want to build Stratego/XT from scratch, execute:

|macOS| macOS, |Linux| Linux
  .. code:: bash

      ./b build -st all

|Windows| Windows
  .. code:: bat

      .\bd.bat build -st all

The ``-s`` flag build Stratego/XT instead of downloading it, and ``-t`` skips the Stratego/XT tests since they are very lengthy.
The ``all`` part of the command indicates that we want to build all components. If you would only like to build the Java components of Spoofax, and skip the Eclipse plugins, execute:

In |Windows| Windows, type ``.\bd.bat`` instead of ``./b`` in the following commands.

|macOS| macOS, |Linux| Linux
  .. code:: bash

      ./b build java

Use ``./b build`` to get a list of components available for building, and ``./b build --help`` for help on all the command-line flags and switches.

.. note:: If you have opened a project in the repository in Eclipse, you **must turn off** :menuselection:`Project --> Build Automatically` in Eclipse, otherwise the Maven and Eclipse compilers will interfere and possibly fail the build. After the Maven build is finished, enable :guilabel:`Build Automatically` again.

Updating the source code
------------------------

If you want to update the repository and submodules, execute:

|macOS| macOS, |Linux| Linux
  .. code:: bash

      git pull --rebase
      ./b checkout
      ./b update

The ``git pull`` command will update any changes in the main repository. The ``./b checkout`` command will check out the correct branches in all submodules, because Git does not do this automatically. The ``./b update`` command will update all submodules.

Switching to a different branch
-------------------------------

Switching to a different branch, for example the ``spoofax-release`` branch, is done with the following commands:

|macOS| macOS, |Linux| Linux
  .. code:: bash

      git checkout spoofax-release
      git pull --rebase
      git submodule update --init --remote --recursive
      ./b checkout
      ./b update

Troubleshooting
---------------

Resetting and cleaning
~~~~~~~~~~~~~~~~~~~~~~

If updating or checking out a branch of submodule fails (because of unstaged or conflicting changes), you can try to resolve it yourself, or you can reset and clean everything. Reset and clean all submodules using:

|macOS| macOS, |Linux| Linux
  .. code:: bash

      ./b reset
      ./b clean

.. warning:: Resetting and cleaning DELETES UNCOMMITTED AND UNPUSHED CHANGES, which can cause PERMANENT DATA LOSS. Make sure all your changes are committed and pushed!

Weird compilation errors
~~~~~~~~~~~~~~~~~~~~~~~~

If you get any weird compilation errors during the build, make sure that Project ‣ Build Automatically is turned off in Eclipse.
