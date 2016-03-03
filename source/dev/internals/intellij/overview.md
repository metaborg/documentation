# Overview
The Spoofax plugin for IntelliJ IDEA consists of two main parts: the IntelliJ
IDEA plugin and the JPS build plugin. They are separate plugins that are run
in separate processes and have separate Guice bindings, but since they share
a lot of code they live in the same project.



## IntelliJ IDEA plugin
The IntelliJ IDEA plugin is responsible for integrating the Spoofax languages
in IntelliJ IDEA. It provides the GUI for the user to configure and use Spoofax
languages and source files.

The Guice bindings for the plugin can be found in the [`IdeaSpoofaxModule`][1]
and [`IdeaSpoofax`][2] classes. [Here's more information][5] on how to use Guice
bindings.



## JPS build plugin
The JPS build plugin is responsible for building a Spoofax language
specification or Spoofax-enabled project. It's loaded in a separate process
by IntelliJ IDEA when the user executes the _Make_ action.

The Guice bindings for the plugin can be found in the [`JpsSpoofaxModule`][1]
and [`JpsSpoofaxMetaModule`][2] classes. [Here's more information][5] on how to
use Guice bindings.


[1]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/IdeaSpoofaxModule.java
[2]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/IdeaSpoofaxMetaModule.java
[3]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/JpsSpoofaxModule.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/JpsSpoofaxMetaModule.java
[5]: bindings.md
