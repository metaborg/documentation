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
   lexing-and-parsing
   projects
   troubleshooting

See also
========
- Bjorn Tipling — `How to make an IntelliJ IDEA plugin in less than 30 minutes <https://bjorn.tipling.com/how-to-make-an-intellij-idea-plugin-in-30-minutes>`_
- JetBrains — `Custom Language Support Tutorial <https://www.jetbrains.org/intellij/sdk/docs/tutorials/custom_language_support_tutorial.html>`_
- JetBrains — `Writing Tests For Plugins <https://www.jetbrains.org/intellij/sdk/docs/tutorials/writing_tests_for_plugins.html>`_
- Terence Parr — `IntelliJ Plugin Development Notes <https://github.com/antlr/jetbrains/blob/master/doc/plugin-dev-notes.md>`_
