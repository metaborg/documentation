**************************
Spoofax Development Manual
**************************

This is the reference manual for building and developing Spoofax, as well as information about its internals.

Introduction
============

Spoofax is the integration of many different tools, compilers, (meta-)languages, (meta-)libraries, and runtime components. This integration is made concrete in the `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ Git repository on GitHub. This repository contains all components via `Git submodules <https://git-scm.com/book/en/v2/Git-Tools-Submodules>`_, which are updated by our `build farm <http://buildfarm.metaborg.org/view/Spoofax/job/metaborg/job/spoofax-releng/>`_ that builds Spoofax whenever one of its components in a submodule changes.

Spoofax currently contains the following subcomponents as submodules:

- `releng <https://github.com/metaborg/spoofax-deploy/>`_ - release engineering scripts for managing and building the ``spoofax-releng`` repostory.
- Java libraries and runtimes

  - `mb-rep <https://github.com/metaborg/mb-rep/>`_ - libraries for program representation such as abstract terms
  - `mb-exec <https://github.com/metaborg/mb-exec/>`_ - Stratego interpreter and utilities
  - `jsglr <https://github.com/metaborg/jsglr/>`_ - JSGLR parser
  - `spoofax <https://github.com/metaborg/spoofax/>`_ - Spoofax Core, a cross platform API to Spoofax languages
  - `spoofax-maven <https://github.com/metaborg/spoofax-maven/>`_ - Maven integration for Spoofax Core
  - `spoofax-sunshine <https://github.com/metaborg/spoofax-sunshine/>`_ - Command-line integration for Spoofax Core
  - `spoofax-eclipse <https://github.com/metaborg/spoofax-eclipse/>`_ - Eclipse plugin for Spoofax Core
  - `spoofax-intellij <https://github.com/metaborg/spoofax-intellij/>`_ - IntelliJ plugin for Spoofax Core

- Meta-languages and libraries

  - `esv <https://github.com/metaborg/esv/>`_ - Editor service language
  - `sdf <https://github.com/metaborg/sdf/>`_ - Syntax Definition Formalisms, containing the SDF2 and SDF 3 languages
  - `stratego <https://github.com/metaborg/stratego/>`_ and `strategoxt <https://github.com/metaborg/strategoxt/>`_ - Stratego compiler, runtime, and editor
  - `nabl <https://github.com/metaborg/nabl/>`_ - Name binding languages, containing the NaBL and NaBL2 languages, and support libraries for NaBL2
  - `ts <https://github.com/metaborg/ts/>`_ - Type system language
  - `dynsem <https://github.com/metaborg/dynsem/>`_ - Dynamic semantics language
  - `metaborg-coq <https://github.com/metaborg/metaborg-coq/>`_ - Coq signatures and syntax definition
  - `spt <https://github.com/metaborg/spt/>`_ - Spoofax testing language
  - `runtime-libraries <https://github.com/metaborg/runtime-libraries/>`_ - NaBL support libraries, incremental task engine for incremental name and type analysis

Furthermore, this repository contains a Bash script :command:`./b` that redirects into the Python release engineering scripts in the ``releng`` submodule. These scripts support managing this Git repository, version management, generation of Eclipse instances, building Spoofax, and releasing new versions of Spoofax.

The rest of this manual describes how to set up Maven and other required tools for building and developing Spoofax, how to build and develop Spoofax, how to write this documentation, and explains some of the internals of Spoofax components.


Supported Platforms
===================

macOS and Linux are directly supported. Windows is supported through the `Windows Subsystem for Linux (Bash on Windows) <https://msdn.microsoft.com/en-us/commandline/wsl/install_guide>`_.

Requirements
============

The following tools are required to build and develop Spoofax:


Git 1.8.2 or higher
  Required to check out the source code from our GitHub repositories. Instructions on how to install Git for your platform can be found here: http://git-scm.com/downloads.

  If you run macOs and have `Homebrew <http://brew.sh/>`_ installed, you can install Git by executing ``brew install git``. Confirm your Git installation by executing ``git version``.

Java JDK 8 or higher
  Required to build and run Java components. The latest JDK can be downloaded and installed from: http://www.oracle.com/technetwork/java/javase/downloads/index.html.

  On macOs, it can be a bit tricky to use the installed JDK, because Apple by default installs JRE 6. To check which version of Java you are running, execute the ``java -version`` command. If this tells you that the Java version is 1.8, everything is fine. If not, the Java version can be set with a command. After you have installed JDK, execute:

  .. code:: bash

      export JAVA_HOME=`/usr/libexec/java_home -v 1.8`

  .. note:: Such an export is not permanent. To make it permanent, add that line to :file:`~/.bashrc` or equivalent for your OS/shell (create the file if it does not exist), which will execute it whenever a new shell is opened.

  Confirm your JDK installation and version by executing ``java -version`` and ``javac -version``.

Python 3.4 or higher
  Python scripts are used to orchestrate the build. Instructions on how to install Python for your platform can be found here: https://www.python.org/downloads/.

  If you run macOs and have `Homebrew <http://brew.sh/>`__ installed, you can install Python by executing ``brew install python3``. Confirm your Python installation by executing ``python3 --version`` or ``python --version``, depending on how your package manager sets up Python.

Pip 7.0.3 or higher
  Pip is used to download some python dependencies. A version comes preinstalled with Python 3, but you need to make sure that you have version 7.0.3 or higher.

  To upgrade to the newest version use ``pip install --upgrade pip`` or ``pip3 install --upgrade pip``, depending on if your OS uses a different ``pip`` command for Python 3. Confirm using ``pip3 --version`` or ``pip --version``.

Maven 3.3.9 or higher
  Required to build most components of Spoofax. Our Maven artifact server must also be registered with Maven since the build depends on artifacts from previous builds for bootstrapping purposes. We explain how to install and set up Maven in the `next section <dev-maven_>`_.





.. _dev-maven:

Maven
=====

Maven is a project management and build tool for software projects. Most components in Spoofax are built with Maven.

Installing
----------

Maven can be downloaded and installed from http://maven.apache.org/download.cgi. We require Maven 3.3.9 or higher.
On macOs, Maven can be easily installed with Homebrew by executing ``brew install maven``.

Confirm the installation and version by running ``mvn --version``.

Memory allocation
-----------------

By default, Maven does not assign a lot of memory to the JVM that it runs in, which may lead to out of memory exceptions during builds.
To increase the allocated memory, execute before building:

.. code:: bash

    export MAVEN_OPTS="-Xms512m -Xmx1024m -Xss16m -XX:MaxPermSize=512m"

.. note:: Such an export is not permanent, see previous note about making this permanent.

.. note:: ``-XX:MaxPermSize=512m`` is not required for Java 8, and even gives a warning when added.

.. _using_metaborg_artifacts:

Spoofax Maven artifacts
-----------------------

Spoofax's Maven artifacts are hosted on our artifact server: http://artifacts.metaborg.org.
To use these artifacts, repositories have to be added to your Maven configuration.
This configuration is *required* when building and developing Spoofax.
Repositories can be added to your local Maven settings file (which is recommended), or to a project's POM file.

Local settings file
~~~~~~~~~~~~~~~~~~~

The recommended approach is to add repositories to your local Maven settings file, located at :file:`~/.m2/settings.xml`.
If you have not created this file yet, or want to completely replace it, simply create it with the following content:

.. code:: xml

    <?xml version="1.0" ?>
    <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
      <profiles>
        <profile>
          <id>add-metaborg-release-repos</id>
          <activation>
            <activeByDefault>true</activeByDefault>
          </activation>
          <repositories>
            <repository>
              <id>metaborg-release-repo</id>
              <url>http://artifacts.metaborg.org/content/repositories/releases/</url>
              <releases>
                <enabled>true</enabled>
              </releases>
              <snapshots>
                <enabled>false</enabled>
              </snapshots>
            </repository>
          </repositories>
          <pluginRepositories>
            <pluginRepository>
              <id>metaborg-release-repo</id>
              <url>http://artifacts.metaborg.org/content/repositories/releases/</url>
              <releases>
                <enabled>true</enabled>
              </releases>
              <snapshots>
                <enabled>false</enabled>
              </snapshots>
            </pluginRepository>
          </pluginRepositories>
        </profile>

        <profile>
          <id>add-metaborg-snapshot-repos</id>
          <activation>
            <activeByDefault>true</activeByDefault>
          </activation>
          <repositories>
            <repository>
              <id>metaborg-snapshot-repo</id>
              <url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
              <releases>
                <enabled>false</enabled>
              </releases>
              <snapshots>
                <enabled>true</enabled>
              </snapshots>
            </repository>
          </repositories>
          <pluginRepositories>
            <pluginRepository>
              <id>metaborg-snapshot-repo</id>
              <url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
              <releases>
                <enabled>false</enabled>
              </releases>
              <snapshots>
                <enabled>true</enabled>
              </snapshots>
            </pluginRepository>
          </pluginRepositories>
        </profile>
      </profiles>
    </settings>

If you've already created a settings file before and want to add the repositories, just add the ``profile`` element (and the ``profiles`` element if it does not exist yet) to the settings file.

Advanced: project POM file
~~~~~~~~~~~~~~~~~~~~~~~~~~

Repositories can also be added directly to a project's POM file, which only set the repositories for that particular project. This is not recommended, because it makes repositories harder to change by users, and duplicates the configuration. But it can be convenient, because it does not require an external settings file.

To do this, just add the the following content to the POM file:

.. code:: xml

    <repositories>
        <repository>
            <id>metaborg-release-repo</id>
            <url>http://artifacts.metaborg.org/content/repositories/releases/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </repository>
        <repository>
            <id>metaborg-snapshot-repo</id>
            <url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
            <releases>
                <enabled>false</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </repository>
    </repositories>

    <pluginRepositories>
        <pluginRepository>
            <id>metaborg-release-repo</id>
            <url>http://artifacts.metaborg.org/content/repositories/releases/</url>
            <releases>
                <enabled>true</enabled>
            </releases>
            <snapshots>
                <enabled>false</enabled>
            </snapshots>
        </pluginRepository>
        <pluginRepository>
            <id>metaborg-snapshot-repo</id>
            <url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
            <releases>
                <enabled>false</enabled>
            </releases>
            <snapshots>
                <enabled>true</enabled>
            </snapshots>
        </pluginRepository>
    </pluginRepositories>

Maven central repository mirror
-------------------------------

Artifacts of most open source projects are hosted on the `Central Repository <https://search.maven.org/>`_ server. If you are building any project using Maven, many artifacts will be downloaded from that server. While it is a fast server, it can still take a while to download all required artifacts for big projects.

If you are on the TUDelft network, you can use our local mirror of the Central Repository to speed things up. Using the mirroring requires a change in your local settings.xml file located at :file:`~/.m2/settings.xml`. If this file does not exist, create it with the following content:

.. code:: xml

    <?xml version="1.0" ?>
    <settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
      xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
      <mirrors>
        <mirror>
          <id>metaborg-central-mirror</id>
          <url>http://artifacts.metaborg.org/content/repositories/central/</url>
          <mirrorOf>central</mirrorOf>
        </mirror>
      </mirrors>
    </settings>

If you've already created a settings file before and want to add the mirror configuration, just add the ``mirror`` element (and the ``mirrors`` element if it does not exist yet) to the settings file.



.. _dev-build:

Building
========

This section describes how to build Spoofax from scratch, on the command-line.

Cloning the source code
-----------------------

Clone the source code from the `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ repository with the following commands:

.. code:: bash

    git clone https://github.com/metaborg/spoofax-releng.git
    cd spoofax-releng
    git submodule update --init --remote --recursive

Cloning and updating submodules can take a while, since we have many submodules and some have a large history.

Start a build
-------------

To build Spoofax, simply execute:

.. code:: bash

    ./b build all

This downloads the latest Stratego/XT, and builds Spoofax. If you also want to build Stratego/XT from scratch, execute:

.. code:: bash

    ./b build -st all

The ``-s`` flag build Stratego/XT instead of downloading it, and ``-t`` skips the Stratego/XT tests since they are very lengthy.
The ``all`` part of the command indicates that we want to build all components. If you would only like to build the Java components of Spoofax, and skip the Eclipse plugins, execute:

.. code:: bash

    ./b build java

Use ``./b build`` to get a list of components available for building, and ``./b build --help`` for help on all the command-line flags and switches.

.. note:: If you have opened a project in the repository in Eclipse, you **must turn off** :menuselection:`Project --> Build Automatically` in Eclipse, otherwise the Maven and Eclipse compilers will interfere and possibly fail the build. After the Maven build is finished, enable :guilabel:`Build Automatically` again.

Updating the source code
------------------------

If you want to update the repository and submodules, execute:

.. code:: bash

    git pull --rebase
    ./b checkout
    ./b update

The ``git pull`` command will update any changes in the main repository. The ``./b checkout`` command will check out the correct branches in all submodules, because Git does not do this automatically. The ``./b update`` command will update all submodules.

Switching to a different branch
-------------------------------

Switching to a different branch, for example the ``spoofax-release`` branch, is done with the following commands:

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

.. code:: bash

    ./b reset
    ./b clean

.. warning:: Resetting and cleaning DELETES UNCOMMITTED AND UNPUSHED CHANGES, which can cause PERMANENT DATA LOSS. Make sure all your changes are committed and pushed!

Weird compilation errors
~~~~~~~~~~~~~~~~~~~~~~~~

If you get any weird compilation errors during the build, make sure that Project ‣ Build Automatically is turned off in Eclipse.





Developing
==========

If you are developing a project that is included in Spoofax it is recommended to set up a development environment.
This section describes how to set up such a development environment.

Requirements
------------

A working **Spoofax build** is required before being able to develop. Follow the `previous section <dev-build_>`_ for instructions on how to build Spoofax.

Eclipse
-------

Currently, an Eclipse development environment is the most supported environment.
You can generate a dedicated Eclipse instance for Spoofax development, or you can install Spoofax in an existing Eclipse.

Generating an Eclipse instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :command:`./b` script in the spoofax-releng repository can generate an Eclipse installation for you.
Change directory into the spoofax-releng repository and run:

.. code:: bash

    ./b gen-spoofax -d ~/eclipse/spoofax-dev

This will download and install Eclipse into ~/eclipse/spoofax-dev with the right plugins and eclipse.ini for Spoofax development. The latest nightly version of the Spoofax plugin will be installed into that Eclipse. If you would like to install your locally built Spoofax plugin instead, pass the ``-l`` flag:

.. code:: bash

    ./b gen-spoofax -l -d ~/eclipse/spoofax-dev

Generating an Eclipse installation can take several minutes. After it's done generating, open the Eclipse installation and confirm that it works by creating a Spoofax project.

Using an existing Eclipse instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

To use an existing (or new) Eclipse instance, you will have to install the required plugins yourself.
The first plugin you need is Spoofax itself.
You can either install this from an update site as listed in :ref:`the downloads section <stable-release>`,
or you can use your own local update site as generated by the ``org.metaborg.spoofax.eclipse.updatesite`` project (follow the `build guide <dev-build_>`_ on how to set that up).

The next step would be to get Maven integration in Eclipse.
The `M2Eclipse <http://www.eclipse.org/m2e/>`_ plugin would be the go to way to get that.
Now you can start importing the Spoofax projects you want to change.
However, you will likely run into some trouble with m2e's 'new' approach to integrating with the maven lifecycle configuration.
The errors in your :file:`pom.xml` file might look something like

::

    Plugin execution not covered by lifecycle configuration: org.codehaus.mojo:build-helper-maven-plugin:1.10:add-source

If you want to read up on where these errors come from or why they won't be going away any time soon, take a look at https://www.eclipse.org/m2e/documentation/m2e-execution-not-covered.html.
To solve them, the cleanest solution is to use connectors, which are conveniently made available from inside Eclipse:
Go to :menuselection:`Eclipse --> Preferences --> Maven --> Discovery`, here you will find a button that says :guilabel:`Open Catalog`, click it.
Here you can search for so called connectors that make some maven plugins work with the 'new' m2e.
The ones you're most likely looking for are:

1. ``buildhelper`` for the integration with the ``build-helper-maven-plugin``
2. ``m2e-jdt-compiler`` for the integration with the ``maven-compile-plugin``
3. ``Tycho Configurators`` for the integration with the Tycho build plugins

After installing these connectors, you should be able to successfully build your first Spoofax project.
For Spoofax language projects, you can select the project and then go to the menu bar: :menuselection:`Project -> Build Project`.

If you import projects from Spoofax, Eclipse might give you the following type of error on some files in the projects:
``Access restriction: The type 'MetaborgException' is not API``.
This is caused by Eclipse being weird, as discussed on this `stackoverflow post <http://stackoverflow.com/questions/25222811/access-restriction-the-type-application-is-not-api-restriction-on-required-l>`_.
As there really is no reason why the project couldn't access the type, other than Eclipse being weird, just add an Access Rule to the project that has the error:
:menuselection:`Right click on Project --> properties --> Java Build Path --> Libraries tab --> Expand Plug-in Dependencies --> Access rules --> Edit --> Add --> Resolution: Accessible --> Rule Pattern: org/metborg/core/*`.
The actual rule pattern depends on which type Eclipse claimed was not accessible.

To be able to run a new Eclipse instance with the Spoofax projects in your workspace, you can get a launch configuration from the ``org.metaborg.spoofax.eclipse`` project.
When you first try to launch the Eclipse Plugin, you will most likely be notified of missing constraints in some of your projects.
This means you have to install these constraints into your Eclipse.
Most of these can be installed through the `Eclipse Orbit <http://www.eclipse.org/orbit/>`_ project.
Just add their update site and select the missing plugins.
Here is a list of plugins I had to install through Orbit:

-  Google Guice (No AOP)

These setup steps have been tested with `Eclipse Neon <http://www.eclipse.org/neon/>`_ and a nightly build of Spoofax ``2.1.0-SNAPSHOT``.

Fixing Eclipse settings
~~~~~~~~~~~~~~~~~~~~~~~

Some Eclipse settings unfortunately have sub-optimal defaults. Go to the Eclipse preferences and set these options:

- :menuselection:`General`

  -  Enable: Keep next/previous editor, view and perspectives dialog open

- :menuselection:`General --> Startup and Shutdown`

  -  Enable: Refresh workspace on startup

- :menuselection:`General --> Workspace`

  -  Enable: Refresh using native hooks or polling

- :menuselection:`Maven`

  -  Enable: Do not automatically update dependencies from remote repositories
  -  Enable: Download Artifact Sources
  -  Enable: Download Artifact JavaDoc

- :menuselection:`Maven --> User Interface`

  -  Enable: Open XML page in the POM editor by default

- :menuselection:`Run/Debug --> Launching`

  -  Disable: Build (if required) before launching

Developing
~~~~~~~~~~

Import the projects you'd like to develop.
To import Java and language projects, use :menuselection:`Import --> Maven --> Existing Maven Projects`.
Eclipse plugins are still imported with :menuselection:`Import --> General --> Existing Projects into Workspace`.

Running
~~~~~~~

To test your changes in the Spoofax Eclipse plugin, import the ``org.metaborg.spoofax.eclipse`` project from the ``spoofax-eclipse`` repository, which provides launch configurations for starting new Eclipse instances. Press the little down arrow next to the bug icon (next to the play icon) and choose ``Spoofax with core (all plug-ins)`` to start a new Eclipse instance that contains your changes.

Some gotcha's:

-  When starting a new Eclipse instance using ``Spoofax with core (all plug-ins)``, Eclipse might report problems about ``org.eclipse.jdt.annotation``, ``org.metaborg.meta.lang.spt.testrunner.cmd``, and ``org.metaborg.meta.lang.spt.testrunner.core``. These problems can be ignored.
-  If you change a language and want to test it in a new Eclipse instance, import that language's corresponding Eclipse plugin project. For example, ``org.metaborg.meta.lang.nabl`` has Eclipse plugin project ``org.metaborg.meta.lang.nabl.eclipse``. Then compile both those projects from the command-line (don't forget to turn off build automatically in Eclipse), and start a new Eclipse instance.

Troubleshooting
~~~~~~~~~~~~~~~

If there are many errors in a project, try updating the Maven project.
Right click the project and choose :menuselection:`Maven --> Update Project...`, uncheck :guilabel:`Clean projects` in the new dialog and press :guilabel:`OK`.
This will update the project from the POM file, update any dependencies, and trigger a build.
If this does not solve the problems, try it again but this time with :guilabel:`Clean projects` checked.
Note that if you clean a language project, it has to be rebuilt from the command-line. Restarting Eclipse and repeating these steps may also help.

Multiple projects can be updated by selecting multiple projects in the package/project explorer, or by checking projects in the update dialog.

Advanced: developing from scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases it can be beneficial to have full control over all projects, instead of relying on Maven artifacts and the installed Spoofax plugin.
Only follow this approach if you know what you are doing!
To develop from scratch, uninstall Spoofax from Eclipse, and import projects from ``spoofax-releng`` into the workspace.

If you change a language project, build them on the command-line, because languages cannot be built inside Eclipse without the Spoofax plugin.

IntelliJ
--------

Easiest is to :ref:`install the latest release of the Spoofax plugin <intellij-installation>` in an installation of IntelliJ IDEA.

Otherwise, you may want to build it from source, and to run the built plugin inside a special sandbox-instance of IntelliJ IDEA, execute the following command:

.. code:: bash

    ./gradlew runIdea

Alternatively, in IntelliJ IDEA you can invoke the *IntelliJ Plugin* run/debug configuration.
You can use this to run or debug the IntelliJ IDEA plugin code.
However, this cannot be used to debug the JPS Spoofax build process.

To debug the JPS Spoofax build process, you need to execute the following command:

.. code:: bash

    ./gradlew debugJps

or invoke the *IntelliJ Plugin (Debug JPS)* run configuration (*not debug*) from IntelliJ. Then in the sandbox IntelliJ IDEA instance you enable the "Debug Build Process" action (Ctrl+Shift+A). Then you start a build. IntelliJ will wait for a debugger to be attached to port 5005.
Attach a debugger, and the build will continue. From the Spoofax plugin's IntelliJ IDEA project, you can invoke the *JPS Plugin* remote debug configuration to attach the debugger.

Logging
~~~~~~~

To get debug logging in IntelliJ, locate the :file:`bin/log.xml` file in the IntelliJ folder and add the following snippet in the ``<log4j:configuration>`` element, just above the ``<root>`` element:

.. code:: xml

    <category name="#org.metaborg" additivity="true">
      <priority value="DEBUG"/>
      <appender-ref ref="CONSOLE-DEBUG"/>
      <appender-ref ref="FILE"/>
    </category>





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





Internals
=========

This section contains information about the internals of Spoofax.

.. toctree::
   :maxdepth: 1

   internals/intellij/index
