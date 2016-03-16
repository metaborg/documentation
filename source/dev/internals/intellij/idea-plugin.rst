====================
IntelliJ IDEA Plugin
====================

The IntelliJ IDEA plugin is responsible for integrating the Spoofax languages
in IntelliJ IDEA. It provides the editor functionality (e.g. syntax
highlighting), dialogs and wizards (e.g. New Project dialog) using the IntelliJ
IDEA OpenAPI.

Initialization
==============
When the plugin is loaded, a singleton instance of the `IdeaPlugin`_ application
component is created by IntelliJ. This loads the Guice dependency injector.

Bindings
========
The Guice bindings for the plugin can be found in the `IdeaSpoofaxModule`_
and `IdeaSpoofaxMetaModule`_ classes. See :doc:`bindings` for more information
on how to use Guice bindings.

.. _`IdeaPlugin`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/idea/IdeaPlugin.java
.. _`IdeaSpoofaxModule`: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/IdeaSpoofaxModule.java
.. _`IdeaSpoofaxMetaModule`: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/IdeaSpoofaxMetaModule.java
