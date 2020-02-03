.. _installation-guide:

==================
Installing Spoofax
==================

Spoofax is distributed as an Eclipse plugin.
This guide shows how to download, install, and run Spoofax in Eclipse.

Requirements
------------

Spoofax runs on the major operating systems:

-  Windows (32 and 64 bits)
-  Linux (32 and 64 bits)
-  macOS (Intel only)

Spoofax requires a working internet connection to download several libraries when it is first started.
These libraries are cached afterwards, and only need to be re-downloaded when you update Spoofax.

Installing the Spoofax Eclipse Plugin
-------------------------------------

Download
~~~~~~~~

To get started with Spoofax, download an Eclipse Oxygen installation with Spoofax preinstalled for your platform:

.. include:: /include/block/download-rel-eclipse-jre.rst

These are bundled with an embedded Java Runtime Environment (JRE) version 8, such that a JRE on your system is not required.
If your system has a JRE of version 8 or higher installed, and would rather use that, use the following download links instead:

.. include:: /include/block/download-rel-eclipse.rst

Unpack
~~~~~~

Unpack the downloaded archive to a location with write access, since Eclipse requires write access to the unpacked Eclipse installation.

.. warning::

   On *Windows*, do **not** unpack the Eclipse installation into :file:`Program Files`, because no write access is granted there, breaking both Eclipse and Spoofax.

.. warning::

   On *macOS Sierra (10.12)* and above, you must move the unpacked :file:`spoofax.app` file to a different location (such as :file:`Applications`) after unpacking, to prevent `App Translocation <http://lapcatsoftware.com/articles/app-translocation.html>`_ from moving the app into a read-only filesystem, breaking Eclipse and Spoofax.

   Alternatively, you can prevent App Translocation by clearing attributes from the application. To do this, open the Terminal, navigate to the directory where the :file:`spoofax.app` is located, and execute:

   .. code-block:: bash

     xattr -rc spoofax.app

Running Eclipse
~~~~~~~~~~~~~~~

Start up Eclipse, depending on your operating system:

-  Windows: open :command:`spoofax/eclipse.exe`
-  Linux: open :command:`spoofax/eclipse`
-  Mac OSX: open :command:`spoofax.app`

.. warning::

   On *macOS*, if Eclipse cannot be opened because it is from an *unidentified developer*, right click :file:`spoofax.app` and choose :guilabel:`Open` to grant permission to open Eclipse.

   If Eclipse cannot be opened because it is *damaged*, open the Terminal, navigate to the directory where :file:`spoofax.app` is located, and execute:

   .. code-block:: bash

      xattr -rc spoofax.app

   This will clear the attributes that Eclipse has been downloaded from the internet, and grant permission to open Eclipse.

.. warning::

   On *Ubuntu 16.04*, Eclipse is known to have problems with GTK+ 3. To work around this issue, add the following to :file:`eclipse.ini`::

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

Further Instructions
~~~~~~~~~~~~~~~~~~~~

Follow the :ref:`Getting Started guide <langdev-getting-started>` to get started with Spoofax in Eclipse.
