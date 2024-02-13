.. _installation-guide:

.. role:: bash(code)
  :language: bash

==================
Installing Spoofax
==================

Spoofax is distributed as an Eclipse plugin.
This guide shows how to download, install, and run Spoofax in Eclipse.

Requirements
------------

Spoofax runs on the major operating systems:

-  |Windows| Windows (32 and 64 bits)
-  |Linux| Linux (32 and 64 bits)
-  |macOS| macOS (Intel only)

Spoofax requires a working internet connection to download several libraries when it is first started.
These libraries are cached afterwards, and only need to be re-downloaded when you update Spoofax.

Installing the Spoofax Eclipse Plugin
-------------------------------------

Using Homebrew (|macOS| macOS)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

On *macOS* Spoofax can be installed easily using `Homebrew <https://brew.sh/>`_.
For other platforms, or manual installation, follow the `Download (all platforms)`_ instructions below.

Install the *latest release* of Spoofax Eclipse as follows:

.. code-block:: bash

  brew tap metaborg/metaborg
  brew cask install spoofax

The optional command-line tools are installed with:

.. code-block:: bash

  brew install strategoxt

Continue at `Running Eclipse`_.

.. warning::

  Upgrading the Spoofax cask using :bash:`brew cask upgrade --greedy` will lose all manually installed plugins. It is recommended to use Eclipse update sites to keep Spoofax up-to-date.

Download (all platforms)
~~~~~~~~~~~~~~~~~~~~~~~~

To get started with Spoofax, download an Eclipse Oxygen installation with Spoofax preinstalled for your platform:

.. include:: /include/block/download-rel-eclipse-jre.rst

These are bundled with an embedded Java Runtime Environment (JRE) version 8, such that a JRE on your system is not required.
If your system has a JRE of version 8 or higher installed, and would rather use that, use the following download links instead:

.. include:: /include/block/download-rel-eclipse.rst

Unpack
~~~~~~

Unpack the downloaded archive to a location with write access, since Eclipse requires write access to the unpacked Eclipse installation.

.. warning::

   On |Windows| *Windows*, do **not** unpack the Eclipse installation into :file:`Program Files`, because no write access is granted there, breaking both Eclipse and Spoofax.

.. warning::

   On |macOS| *macOS Sierra (10.12)* and above, you must move the unpacked :file:`spoofax.app` file to a different location (such as :file:`Applications`) after unpacking, to prevent `App Translocation <https://lapcatsoftware.com/articles/app-translocation.html>`_ from moving the app into a read-only filesystem, breaking Eclipse and Spoofax.

   Alternatively, you can prevent App Translocation by clearing attributes from the application. To do this, open the Terminal, navigate to the directory where the :file:`spoofax.app` is located, and execute:

   .. code-block:: bash

     xattr -rc spoofax.app


Running Eclipse
~~~~~~~~~~~~~~~

Start up Eclipse, depending on your operating system:

-  |Windows| Windows: open :command:`spoofax/eclipse.exe`
-  |Linux| Linux: open :command:`spoofax/eclipse`
-  |macOS| macOS: open :command:`spoofax.app`

.. warning::

   Do not update Eclipse with :menuselection:`Help --> Check For Updates`, as it will update Eclipse to newer major versions which are not always backwards compatible, and which require a JRE of version 11 or higher which we do not bundle (we bundle JRE8) with Eclipse.

.. note::

   On |macOS| *macOS*, if Eclipse cannot be opened because it is from an *unidentified developer*, right click :file:`spoofax.app` and choose :guilabel:`Open` to grant permission to open Eclipse.

   If Eclipse cannot be opened because it is *damaged*, open the Terminal, navigate to the directory where :file:`spoofax.app` is located, and execute:

   .. code-block:: bash

      xattr -rc spoofax.app

   This will clear the attributes that Eclipse has been downloaded from the internet, and grant permission to open Eclipse.

.. note::

   If you downloaded Spoofax Eclipse without an embedded JRE, it may not start or give an error *A Java Runtime Environment (JRE) or Java Development Kit (JDK) must be available in order to run Eclipse* or *To open "spoofax" you need to install the legacy Java SE 6 runtime*. To fix this, specify the path to a valid JDK using the ``-vm`` option at the start of ``eclipse.ini`` (``spoofax.app/Contents/Eclipse/eclipse.ini`` on |macOS| macOS).

   For example, to specify the current JDK installed by `Sdkman <https://sdkman.io/>`_, add this at the top of your ``eclipse.ini``:

   .. code-block:: ini

     -vm
     /Users/myusername/.sdkman/candidates/java/current/lib/jli/libjli.dylib

   See `this link <https://wiki.eclipse.org/Eclipse.ini#Specifying_the_JVM>`_ for more information.

.. note::

   On |Linux| *Ubuntu 16.04*, Eclipse is known to have problems with GTK+ 3. To work around this issue, add the following to :file:`eclipse.ini`::

      --launcher.GTK_version
      2

   before the line::

     --launcher.appendVmargs

After starting up, choose where your workspace will be stored.
The Eclipse workspace will contain all of your settings, and is the default location for new projects.

Some Eclipse settings unfortunately have sub-optimal defaults.
After you have chosen a workspace and Eclipse has completely started up, go to the Eclipse preferences and set these options:

-  :menuselection:`General --> Startup and Shutdown`

   -  Enable: :guilabel:`Refresh workspace on startup`

-  :menuselection:`General --> Workspace`

   -  Enable: :guilabel:`Refresh using native hooks or polling`

-  :menuselection:`Maven --> Annotation Processing`

   -  Enable: :guilabel:`Automatically configure JDT APT`


Changing Eclipse Memory Allocation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
By default a plain Eclipse has a maximum heap size of 1 GB. You may want to
increase this limit. The default for the Eclipse application produced by
Spoofax is 2 GB.

To run Eclipse once with a different memory limit, call it from the command-line
like this::

   eclipse [normal arguments] -vmargs -Xmx2G

If this works, you can permanently apply this limit in the ``eclipse.ini`` file
in the Eclipse installation directory (|macOS| macOS: ``Contents/Eclipse`` in
the Eclipse package) by changing the ``-Xmx`` argument. For example::

   -vmargs
   [...]
   -XstartOnFirstThread
   -Xss16M
   -Xms2G
   -Xmx2G
   -Dosgi.requiredJavaVersion=1.8
   -server

``-Xss``
  the size of the thread stack
``-Xms``
  the initial size of the heap
``-Xmx``
  the maximum size of the heap


Further Instructions
~~~~~~~~~~~~~~~~~~~~

Follow the :ref:`Getting Started guide <langdev-getting-started>` to get started
with Spoofax in Eclipse.
