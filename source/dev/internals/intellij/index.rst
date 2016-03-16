==============================
Intellij IDEA Plugin Internals
==============================
The Spoofax plugin for IntelliJ IDEA consists of two main parts: the IntelliJ
IDEA plugin and the JPS build plugin. They are separate plugins that are run
in separate processes and have separate Guice bindings, but since they share
a lot of code they live in the same project.

.. toctree::
   :maxdepth: 1

   idea-plugin
   jps-plugin
   bindings
   dependencies
   logging
   vfs
   configurations
   languages
   projects
   troubleshooting
