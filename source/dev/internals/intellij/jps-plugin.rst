==========
JPS Plugin
==========

The JPS build plugin is responsible for building a Spoofax language
specification or Spoofax-enabled project. It's loaded in a separate process
by IntelliJ IDEA when the user executes the *Make* action.


Initialization
==============
When the plugin is loaded, the static members of the `JpsPlugin`_ class are
initialized. This loads the Guice dependency injector.


Bindings
========
The Guice bindings for the plugin can be found in the `JpsSpoofaxModule`_
and `JpsSpoofaxMetaModule`_ classes. See :doc:`bindings` for more information
on how to use Guice bindings.


Deserialization
===============
The JPS plugin has an internal representation of the project, its modules,
files, settings, facets, SDK, and so on, in the `JpsModel`_ class.

When the JPS plugin is run, IntelliJ creates a JPS model that reflects the
IntelliJ project structure. However, IntelliJ has no knowledge of any special
extensions and settings that we have applied to the IntelliJ project. We need
to update the JPS model with our own information where needed. This is done
through the deserializers returned from the
`JpsSpoofaxModelSerializerExtension`_ class.


Gathering build targets
=======================
A *build target* is a single compilation unit. JPS now gathers all build targets
that can apply to the model, and orders them according to their dependencies.

The `BuilderService`_ advertises which build target *types* we have implemented.
Each `BuildTargetType<T>`_ implementation then decides which build targets we
have. Usually every module that we can compile gets its own `BuildTarget<T>`_.


Building
========
Our `BuilderService`_ also advertised which *target builders* we have. Every
`TargetBuilder<T, U>`_ has a ``build()`` method that's executed for every
appropriate build target.




.. _`JpsPlugin`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/jps/JpsPlugin.java
.. _`JpsSpoofaxModule`: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/JpsSpoofaxModule.java
.. _`JpsSpoofaxMetaModule`: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/JpsSpoofaxMetaModule.java
.. _`JpsModel`: https://github.com/JetBrains/intellij-community/blob/a5cd6ac6102731ea9b557dcc1c684340f7d8432a/jps/model-api/src/org/jetbrains/jps/model/JpsModel.java
.. _`JpsSpoofaxModelSerializerExtension`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/jps/JpsSpoofaxModelSerializerExtension.java>) class. They deserialize the information serialized by the IntelliJ plugin classes that implement [`PersistentStateComponent<T>`](<https://github.com/JetBrains/intellij-community/blob/a5cd6ac6102731ea9b557dcc1c684340f7d8432a/platform/core-api/src/com/intellij/openapi/components/PersistentStateComponent.java
.. _`BuilderService`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/jps/SpoofaxBuilderService.java
.. _`BuildTargetType<T>`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/SpoofaxTargetType.java
.. _`BuildTarget<T>`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/SpoofaxTarget.java
.. _`TargetBuilder<T, U>`: https://github.com/metaborg/spoofax-intellij/blob/develop/src/main/java/org/metaborg/spoofax/intellij/jps/SpoofaxBuilder.java
