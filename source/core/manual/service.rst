========
Services
========

.. todo:: Not all services have been listed, and no descriptions have been added.


This manual describes all services in Spoofax Core.
A service is a class (and typically a singleton) that provides a single piece of functionality to the Spoofax Core system.
Services can be accessed through facades, or injected through dependency injection.

Both MetaBorg, Spoofax, non-meta, and meta services are described, with each service noting in which component it can be found.
Each service has a corresponding interface which is the Java API to that service.
Some services have specializations that specialize the interface in order to provide more specialized return types or additional method arguments.

-----
Basic
-----

Basic services provide low-level functionality.

.. describe:: Resource service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.resource.IResourceService`

.. describe:: Source text service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.source.ISourceTextService`


--------
Language
--------

Language services provide all language, language implementation, and language component related functionality.

.. describe:: Language service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.language.ILanguageService`

.. describe:: Language identifier service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.language.ILanguageIdentifierService`

.. describe:: Language discovery service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.language.ILanguageDiscoveryService`

.. describe:: Dialect service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.language.dialect.IDialectService`

.. describe:: Language paths service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.build.paths.ILanguagePathService`

.. describe:: Language dependency service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.build.dependency.IDependencyService`


-------------------
Language processing
-------------------

Language processing services provide services for the processing of files of a language.

.. describe:: Syntax service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.syntax.ISyntaxService`
   :specialization Spoofax-meta: :java:ref:`org.metaborg.spoofax.core.syntax.ISpoofaxSyntaxService`


-------
Context
-------

Context services provide a context for language processing tasks.


---------------
Editor services
---------------

Editor services provide functionality for source code editors.

-------------
Configuration
-------------

Configuration services provide read and write access to project, component, and language specification configuration.
See the :doc:`language development manual on configuration </source/langdev/manual/config>` for documentation about the Spoofax language specification configuration, which is a superset of the language specification, component, and project configuration.

^^^^^^^
Project
^^^^^^^

Configuration services for projects.

.. describe:: Project configuration service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.config.IProjectConfigService`

.. describe:: Project configuration builder

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.config.IProjectConfigBuilder`

.. describe:: Project configuration writer

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.config.IProjectConfigWriter`

^^^^^^^^^^^^^^^^^^
Language component
^^^^^^^^^^^^^^^^^^

Configuration services for language components.

.. describe:: Language component configuration service

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.config.ILanguageComponentConfigService`

.. describe:: Language component configuration builder

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.config.ILanguageComponentConfigBuilder`

.. describe:: Language component configuration writer

   :component: MetaBorg
   :interface: :java:ref:`org.metaborg.core.config.ILanguageComponentConfigWriter`

^^^^^^^^^^^^^^^^^^^^^^
Language specification
^^^^^^^^^^^^^^^^^^^^^^

Configuration services for language specifications.

.. describe:: Language specification configuration service

   :component: MetaBorg-meta
   :interface: :java:ref:`org.metaborg.meta.core.config.ILanguageSpecConfigService`
   :specialization Spoofax-meta: :java:ref:`org.metaborg.spoofax.meta.core.config.ISpoofaxLanguageSpecConfigService`

.. describe:: Language specification configuration builder

   :component: MetaBorg-meta
   :interface: :java:ref:`org.metaborg.meta.core.config.ILanguageSpecConfigBuilder`
   :specialization Spoofax-meta: :java:ref:`org.metaborg.spoofax.meta.core.config.ISpoofaxLanguageSpecConfigBuilder`

.. describe:: Language specification configuration writer

   :component: MetaBorg-meta
   :interface: :java:ref:`org.metaborg.meta.core.config.ILanguageSpecConfigWriter`
   :specialization Spoofax-meta: :java:ref:`org.metaborg.spoofax.meta.core.config.ISpoofaxLanguageSpecConfigWriter`
