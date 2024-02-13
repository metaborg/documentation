.. highlight:: java

===============
Core Extensions
===============

Spoofax Core can be extended by providing additional `Guice Modules <https://github.com/google/guice/wiki/Bindings#creating-bindings>`_ with extensions at startup.
Additional modules can be hardcoded when creating a Spoofax facade object, or by specifying the module as a plugin.
Both Spoofax and meta-Spoofax can be extended with additional modules.

This manual describes the extension points in Spoofax Core, and how additional modules can be specified.

----------------
Extension points
----------------

Extension points in Spoofax Core are essentially the `Guice multibindings <https://github.com/google/guice/wiki/Multibindings>`_ that are being used in Spoofax Core.
There are 2 kinds of extension points; :java_ref:`~com.google.inject.multibindings.Multibinder` for a *Set* of implementations for a single interface, and :java_ref:`~com.google.inject.multibindings.MapBinder` for a *Map* of implementations for a single interface.
Guice merges all multibindings from all modules together.

.. note:: Extension points in Spoofax Core are not to be confused with Eclipse extension points, which are Eclipse-specific.

To add a singleton implementation to a Multibinding for an interface, use the following code inside the configure method of an :java_ref:`~com.google.inject.AbstractModule`::

  Multibinder
    .newSetBinder(binder(), interface-class)
    .addBinding()
    .to(implementation-class)
    .in(Singleton.class);

For map bindings, use::

  MapBinder
    .newMapBinder(binder(), key-class, interface-class)
    .addBinding(key)
    .to(implementation-class)
    .in(Singleton.class);

These examples use `linked bindings <https://github.com/google/guice/wiki/LinkedBindings>`_ with a singleton scope, but you can use any Guice binding logic after the ``addBinding`` part.

Some multibindings are annotated with an annotation, they are created by passing the annotation as a third parameter::

  Multibinder.newSetBinder(binder(), interface-class, annotation)

  MapBinder.newSetBinder(binder(), key-class, interface-class, annotation)

We describe the extension points for each component in this section.
These extension points can also be found in the Guice Modules of the Spoofax Core source code.

^^^^^^^^^^^^^^^^^^^^^^^^^
MetaBorg extension points
^^^^^^^^^^^^^^^^^^^^^^^^^

.. describe:: Resource cleanup

   Provides a means to clean up resources when the MetaBorg or Spoofax Core API is closed.

   :signature: ``Multibinder<AutoCloseable>``
   :interface: :java_ref:`~java.lang.AutoCloseable`

.. describe:: Language cache cleanup

   Provides a means to clean up cached language component or language implementation resources when a language component or language implementation is reloaded or removed.

   :signature: ``Multibinder<ILanguageCache>``
   :interface: :java_ref:`ILanguageCache`

.. describe:: Context factory

   Interface for creating :java_ref:`IContext` instances, linked to an identifier.
   A language specification uses a specific context factory by specifying the context type in ESV.

   :signature: ``MapBinder<String, IContextFactory>``
   :interface: :java_ref:`IContextFactory`

.. describe:: Context strategy

   Interface for :java_ref:`IContext` creation/retrieval strategies, linked to an identifier.
   A language specification uses a specific context strategy by specifying the context strategy in ESV.

   :signature: ``MapBinder<String, IContextStrategy>``
   :interface: :java_ref:`IContextStrategy`

.. describe:: Language path provider

   Provides source and include paths for languages.

   :signature: ``Multibinder<ILanguagePathProvider>``
   :interface: :java_ref:`ILanguagePathProvider`


^^^^^^^^^^^^^^^^^^^^^^^^
Spoofax extension points
^^^^^^^^^^^^^^^^^^^^^^^^

.. describe:: Parser

   Parser implementation, linked to an identifier.
   A language specification uses a specific parser by specifying the parser in ESV.
   An implementation **must** implement :java_ref:`ISpoofaxParser` and be bound to **both** signatures listed below for correct operation.

   :signature: ``MapBinder<String, IParser<ISpoofaxInputUnit, ISpoofaxParseUnit>>``
   :signature: ``MapBinder<String, ISpoofaxParser>``
   :interface: :java_ref:`IParser`
   :interface: :java_ref:`ISpoofaxParser`

.. describe:: Analyzer

   Analyzer implementation, linked to an identifier.
   A language specification uses a specific analyzer by specifying the analyzer in ESV.
   An implementation **must** implement :java_ref:`ISpoofaxAnalyzer` and be bound to **both** signatures listed below for correct operation.

   :signature: ``MapBinder<String, IAnalyzer<ISpoofaxParseUnit, ISpoofaxAnalyzeUnit, ISpoofaxAnalyzeUnitUpdate>>``
   :signature: ``MapBinder<String, ISpoofaxAnalyzer>``
   :interface: :java_ref:`IAnalyzer`
   :interface: :java_ref:`ISpoofaxAnalyzer`

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
MetaBorg-meta extension points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. describe:: Meta-resource cleanup

   Provides a means to clean up resources when the MetaBorg-meta or Spoofax-meta Core API is closed.
   Requires the ``Meta`` annotation class, for example::

     Multibinder.newSetBinder(binder(), AutoCloseable.class, Meta.class)

   :signature: ``Multibinder<AutoCloseable>``
   :annotation: ``Meta.class``
   :interface: :java_ref:`~java.lang.AutoCloseable`

^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
Spoofax-meta extension points
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. describe:: Build steps

   Build step implementation which can be executed during language specification builds.

   :signature: ``Multibinder<IBuildStep>``
   :interface: :java_ref:`IBuildStep`

-----------------------------
Hardcoding additional modules
-----------------------------

Additional modules can be hardcoded when you control the application that you'd like to extend.

To extend Spoofax with additional hardcoded modules, add them when creating a :java_ref:`Spoofax <org.metaborg.spoofax.core.Spoofax>` facade object::

   final Spoofax spoofax = new Spoofax(new CustomModule(), new OtherCustomModule());

Similarly, to extend meta-Spoofax, add modules to the meta-facade :java_ref:`SpoofaxMeta <org.metaborg.spoofax.meta.core.SpoofaxMeta>`::

   final SpoofaxMeta spoofaxMeta = new SpoofaxMeta(spoofax, new CustomMetaModule(),
     new OtherCustomMetaModule());

--------------
Plugin modules
--------------

When you do not control the application you'd like to extend, or if you'd like to extend **all** applications that use Spoofax Core, modules will need to be specified as plugins.
Modules can be loaded as plugins through Java service providers for regular Java applications, and through Eclipse extensions for Eclipse plugins.

^^^^^^^^^^^^^^^^^^^^^
Java service provider
^^^^^^^^^^^^^^^^^^^^^

Java service providers are the standard solution for creating extensible applications on the JVM.
Spoofax Core supports specifying additional modules as plugins through a service provider.
To register your module as a plugin, `register it as a service provider <https://docs.oracle.com/javase/tutorial/ext/basics/spi.html#register-service-providers>`_ for the :java_ref:`IServiceModulePlugin <org.metaborg.core.plugin.IServiceModulePlugin>` class.
For example, if you would like to register the ``org.example.CustomModule`` and ``org.example.OtherCustomModule`` module:

1. Create a class implementing :java_ref:`IServiceModulePlugin <org.metaborg.core.plugin.IServiceModulePlugin>`:

  ::

    public class org.example.ExtensionModulePlugin implements IServiceModulePlugin {
      @Override public Iterable<Module> modules() {
        return Iterables2.<Module>from(new org.example.CustomModule(),
          new org.example.OtherCustomModule());
      }
    }

2. Create the :file:`src/main/resources/META-INF/services/org.metaborg.core.plugin.IServiceModulePlugin` file.
3. Add org.example.ExtensionModulePlugin to that file.

Whenever your JAR file is on the classpath together with Spoofax Core, Spoofax Core will pick up the module plugins and load them whenever the Spoofax facade is instantiated.

Similarly, for additional meta-modules, register a service provider for the :java_ref:`IServiceMetaModulePlugin <org.metaborg.meta.core.plugin.IServiceMetaModulePlugin>` class:

1. Create a class implementing :java_ref:`IServiceMetaModulePlugin <org.metaborg.meta.core.plugin.IServiceMetaModulePlugin>`:

  ::

    public class org.example.ExtensionMetaModulePlugin implements IServiceMetaModulePlugin {
      @Override public Iterable<Module> modules() {
        return Iterables2.<Module>from(new org.example.CustomMetaModule(),
          new org.example.OtherCustomMetaModule());
      }
    }

2. Create the :file:`src/main/resources/META-INF/services/org.metaborg.core.plugin.IServiceMetaModulePlugin` file.
3. Add org.example.ExtensionMetaModulePlugin to that file.

^^^^^^^^^^^^^^^^^
Eclipse extension
^^^^^^^^^^^^^^^^^

.. highlight:: xml

Eclipse does not support Java service providers.
To get your module plugins working in Eclipse, they need to be specified as an extension in the :file:`plugin.xml` file.

Add the module classes with the ``org.metaborg.spoofax.eclipse.module`` extension point. For example::

   <extension point="org.metaborg.spoofax.eclipse.module">
     <module class="org.example.CustomModule" />
     <module class="org.example.OtherCustomModule" />
   </extension>

For meta-modules, use the ``org.metaborg.spoofax.eclipse.meta.module`` extension point. For example::

   <extension point="org.metaborg.spoofax.eclipse.meta.module">
     <module class="org.example.CustomMetaModule" />
     <module class="org.example.OtherCustomMetaModule" />
   </extension>

The ``CustomModule`` and ``CustomMetaModule`` classes in these examples must implement the :java_ref:`~com.google.inject.Module` class.


^^^^^^^^^^^^^^^^^^^^^^^
IntelliJ IDEA extension
^^^^^^^^^^^^^^^^^^^^^^^

.. highlight:: xml

Java service providers are only supported when building a project using the JPS plugin. For the IDE, you need to depend on the IntelliJ plugin and provide an implementation for the ``org.metaborg.intellij.spoofaxPlugin`` extension point. For example::

   <extensions defaultExtensionNs="org.metaborg.intellij">
     <spoofaxPlugin implementation="org.example.CustomPlugin" />
     <spoofaxPlugin implementation="org.example.OtherCustomPlugin" />
   </extensions>

For meta-modules, use the ``org.metaborg.intellij.spoofaxMetaPlugin`` extension point. For example::

   <extensions defaultExtensionNs="org.metaborg.intellij">
     <spoofaxMetaPlugin implementation="org.example.CustomMetaPlugin" />
     <spoofaxMetaPlugin implementation="org.example.OtherCustomMetaPlugin" />
   </extensions>

The ``CustomPlugin`` and ``CustomMetaPlugin`` classes in these examples must implement the :java_ref:`IServiceModulePlugin <org.metaborg.core.plugin.IServiceModulePlugin>` and :java_ref:`IServiceMetaModulePlugin <org.metaborg.meta.core.plugin.IServiceMetaModulePlugin>` interfaces respectively.
