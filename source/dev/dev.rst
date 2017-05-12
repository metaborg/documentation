==========
Developing
==========

If you are developing a project that is included in Spoofax it is recommended to set up a development environment.
This section describes how to set up such a development environment.

Requirements
------------

A working **Spoofax build** is required before being able to develop. Follow the :ref:`previous section <dev-build>` for instructions on how to build Spoofax.

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
or you can use your own local update site as generated by the ``org.metaborg.spoofax.eclipse.updatesite`` project (follow the :ref:`build guide <dev-build>` on how to set that up).

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