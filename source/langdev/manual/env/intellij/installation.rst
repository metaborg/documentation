.. _intellij-installation:

============
Installation
============

Recently we created a Spoofax plugin for IntelliJ IDEA.

To install the plugin, either:

- clone this repository, then execute `make run` from the repository's root to start an instance of IntelliJ IDEA with the Spoofax plugin loaded; or
- ensure you have Git and a JDK installed, then execute this from the command line; or::

   curl https://raw.githubusercontent.com/metaborg/spoofax-intellij/master/repository/install.sh -sSLf | bash

- download `IntelliJ IDEA <https://www.jetbrains.com/idea/download/>`_ (the free Community Edition is sufficient) and install the Spoofax plugin from this plugin repository (see detailed instructions below)::

   http://download.spoofax.org/update/nightly/updatePlugins.xml

----------------------------------------------
Installing the Spoofax plugin in IntelliJ IDEA
----------------------------------------------

If you already have an IntelliJ IDEA installation or manually downloaded one, here are the detailed instructions for installing the Spoofax plugin:

1. Go to the *File* menu, *Settings*, and click the *Plugins* tab. Or if you're on the welcome screen, click the *Configure* button at the bottom, then click *Plugins*. Here you can manage the plugins.

   .. image:: img/install_plugin1.png

2. Click the *Browse repositories...* button, then in the new window click *Manage repositories...*. This window allows you to add and remove custom repositories.

   .. image:: img/install_plugin2.png

3. Add the above mentioned repository URL, and click *OK* to close the dialog.

4. In the *Browse repositories* window, find and select the *spoofax-intellij* plugin.

5. Click the green *Install* button, and restart IntelliJ after the plugin's installation.

   .. image:: img/install_plugin3.png
