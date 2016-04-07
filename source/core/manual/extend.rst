.. highlight:: java

===============
Core Extensions
===============

Spoofax Core can be extended by providing additional Guice Modules at startup.
Additional modules can be hardcoded when creating a Spoofax facade object, or by specifying the module as a plugin.
Both Spoofax and meta-Spoofax can be extended with additional modules.

This manual describes how additional modules can be specified, and what the extension points in Spoofax are.

-----------------------------
Hardcoding additional modules
-----------------------------

To extend Spoofax with additional hardcoded modules, add them when creating a :java:ref:`Spoofax <org.metaborg.spoofax.core.Spoofax>` facade object::

   final Spoofax spoofax = new Spoofax(new CustomModule(), new OtherCustomModule());

Similarly, to extend meta-Spoofax, add modules to the meta-facade :java:ref:`SpoofaxMeta <org.metaborg.spoofax.meta.core.SpoofaxMeta>`::

   final SpoofaxMeta spoofaxMeta = new SpoofaxMeta(spoofax, new CustomMetaModule(),
     new OtherCustomMetaModule());

--------------
Plugin modules
--------------

Modules can be loaded as plugins through Java service providers for regular Java applications, and through Eclipse extensions for Eclipse plugins.

^^^^^^^^^^^^^^^^^^^^^
Java service provider
^^^^^^^^^^^^^^^^^^^^^

Java service providers are the standard solution for creating extensible applications on the JVM.
Spoofax Core supports specifying additional modules as plugins through a service provider.
To register your module as a plugin, `register it as a service provider <https://docs.oracle.com/javase/tutorial/ext/basics/spi.html#register-service-providers>`_ for the :java:ref:`IServiceModulePlugin <org.metaborg.core.plugin.IServiceModulePlugin>` class.
For example, if you would like to register the ``org.example.CustomModule`` and ``org.example.OtherCustomModule`` module:

1. Create a class implementing :java:ref:`IServiceModulePlugin <org.metaborg.core.plugin.IServiceModulePlugin>`:
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

Similarly, for additional meta-modules, register a service provider for the :java:ref:`IServiceMetaModulePlugin <org.metaborg.meta.core.plugin.IServiceMetaModulePlugin>` class:

1. Create a class implementing :java:ref:`IServiceMetaModulePlugin <org.metaborg.core.plugin.IServiceMetaModulePlugin>`:
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


----------------
Extension points
----------------

.. todo:: This part of the documentation has not been written yet.

.. note:: Extension points in Spoofax Core are not to be confused with Eclipse extension points, which are Eclipse-specific.
