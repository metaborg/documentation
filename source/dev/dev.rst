==========
Developing
==========

If you are developing a project that is included in Spoofax it is recommended to set up a development environment.
This section describes how to set up such a development environment.

Requirements
------------

A working **Spoofax build** is required before being able to develop. You must be able to successfully build Spoofax by running `./b build all`. Do not continue if this does not work. Follow the :ref:`previous section <dev-build>` for instructions on how to build Spoofax.

Eclipse
-------

Currently, an Eclipse development environment is the most supported environment. An Eclipse development environment can be generated with our scripts.

Generating an Eclipse instance
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :command:`./b` script in the spoofax-releng repository can generate an Eclipse installation for you.
Change directory into the :file:`spoofax-releng` repository and run:

.. code:: bash

    ./b gen-spoofax -l -d ~/eclipse/spoofax-dev

This will download and install Eclipse into :file:`~/eclipse/spoofax-dev` with the right plugins and :file:`eclipse.ini` for Spoofax development. The locally built version of the Spoofax plugin will be installed into that Eclipse. Generating an Eclipse installation can take several minutes. After it's done generating, open the Eclipse installation and confirm that it works by creating a Spoofax project.

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

- :menuselection:`Maven --> Annotation Processing`

  - Enable: Automatically configure JDT APT

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

To test your changes in the Spoofax Eclipse plugin, import the ``org.metaborg.spoofax.eclipse`` project from the ``spoofax-eclipse`` repository, which provides launch configurations for starting new Eclipse instances (a "guest" Eclipse). Press the little down arrow next to the bug icon (next to the play icon) and choose ``Spoofax Eclipse Plugin`` to start a new Eclipse instance that contains your changes. If it is not in the list of recently used configurations, click ``Debug configurations...``, it should be under Eclipse Application configurations. 

Some tricks:

-  If you change a (meta-)language and want to test it in a new Eclipse instance, import that language's corresponding Eclipse plugin project. For example, ``org.metaborg.meta.lang.nabl`` has Eclipse plugin project ``org.metaborg.meta.lang.nabl.eclipse``. Then compile both those projects from the command-line (don't forget to turn off build automatically in Eclipse), and start a new Eclipse instance.
-  A different way to test the (meta-)language change is to import that language project into the workspace of the guest Eclipse. Because we use Maven snapshot versions, the built-in version will be overridden when you build the language in the guest eclipse. 

Troubleshooting
~~~~~~~~~~~~~~~

If there are many errors in a project, try updating the Maven project.
Right click the project and choose :menuselection:`Maven --> Update Project...`, uncheck :guilabel:`Clean projects` in the new dialog and press :guilabel:`OK`.
This will update the project from the POM file, update any dependencies, and trigger a build.
If this does not solve the problems, try it again but this time with :guilabel:`Clean projects` checked.
Note that if you clean a language project, it has to be rebuilt from the command-line. Restarting Eclipse and repeating these steps may also help.

Multiple projects can be updated by selecting multiple projects in the package/project explorer, or by checking projects in the update dialog.

If you have particular trouble with ``org.eclipse.*`` plugins in the MANIFEST.MF file that do not resolve, try the following. Go to :menuselection:`Preferences --> Plug-in Development --> Target Platform`, most likely there will not be an active Running Platform there. You can use :guilabel:`Add...` to add a new one if there isn't one already. Select the :guilabel:`Default` option, click :guilabel:`Next`, then click :guilabel:`Finish`. Check the box next to the platform to activate it. 

Advanced: developing from scratch
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

In some cases it can be beneficial to have full control over all projects, instead of relying on Maven artifacts and the installed Spoofax plugin. To develop completely from scratch, uninstall Spoofax from Eclipse, and import all projects by importing ``releng/eclipse/import/pom.xml``, which will import all relevant projects automatically.

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
