========
Services
========

This manual describes all services in Spoofax Core.
A service is a class (and typically a singleton) that provides a single piece of functionality to the Spoofax Core system.
Services can be accessed through facades, or injected through dependency injection.

Both MetaBorg, Spoofax, non-meta, and meta services are described.
Each service has a corresponding interface which is the Java API to that service.
Some services have specializations that specialize the interface in order to provide more specialized return types or additional method arguments.


-----------------
MetaBorg services
-----------------

^^^^^
Basic
^^^^^

Basic services provide low-level functionality.

.. describe:: Resource service

   :interface: :java:ref:`org.metaborg.core.resource.IResourceService`

.. describe:: Source text service

   :interface: :java:ref:`org.metaborg.core.source.ISourceTextService`

^^^^^^^^
Language
^^^^^^^^

Language services provide all language, language implementation, and language component related functionality.

.. describe:: Language service

   :interface: :java:ref:`org.metaborg.core.language.ILanguageService`

.. describe:: Language identifier service

   :interface: :java:ref:`org.metaborg.core.language.ILanguageIdentifierService`

.. describe:: Language discovery service

   :interface: :java:ref:`org.metaborg.core.language.ILanguageDiscoveryService`

.. describe:: Dialect service

   :interface: :java:ref:`org.metaborg.core.language.dialect.IDialectService`

.. describe:: Language paths service

   :interface: :java:ref:`org.metaborg.core.build.paths.ILanguagePathService`

.. describe:: Language dependency service

   :interface: :java:ref:`org.metaborg.core.build.dependency.IDependencyService`

^^^^^^^^^^^^^^^^^^^
Language processing
^^^^^^^^^^^^^^^^^^^

Language processing services provide services for the processing of files of a language.

.. describe:: Syntax service

   :interface: :java:ref:`org.metaborg.core.syntax.ISyntaxService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.syntax.ISpoofaxSyntaxService`

.. describe:: Analysis service

   :interface: :java:ref:`org.metaborg.core.analysis.IAnalysisService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.analysis.ISpoofaxAnalysisService`

.. describe:: Transformation service

   :interface: :java:ref:`org.metaborg.core.transform.ITransformService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.transform.ISpoofaxTransformService`

.. describe:: Unit service

   :interface: :java:ref:`org.metaborg.core.unit.IUnitService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.unit.ISpoofaxUnitService`

   .. describe:: Input unit service

      Sub-interface of the unit service that only provides methods for creating input units.
      Use this sub-interface when you only require creating input units for parsing.

      :interface: :java:ref:`org.metaborg.core.unit.IInputUnitService`
      :specialization: :java:ref:`org.metaborg.spoofax.core.unit.ISpoofaxInputUnitService`

.. describe:: Builder

   :interface: :java:ref:`org.metaborg.core.build.IBuilder`
   :specialization: :java:ref:`org.metaborg.spoofax.core.build.ISpoofaxBuilder`

.. describe:: Parse result processor

   :interface: :java:ref:`org.metaborg.core.processing.parse.IParseResultProcessor`
   :specialization: :java:ref:`org.metaborg.spoofax.core.processing.parse.ISpoofaxParseResultProcessor`

.. describe:: Analysis result processor

   :interface: :java:ref:`org.metaborg.core.processing.analyze.IAnalysisResultProcessor`
   :specialization: :java:ref:`org.metaborg.spoofax.core.processing.analyze.ISpoofaxAnalysisResultProcessor`

^^^^^^^
Context
^^^^^^^

Context services in MetaBorg provide a context for language processing tasks.

.. describe:: Project service

   :interface: :java:ref:`org.metaborg.core.project.IProjectService`
   :specialization: :java:ref:`org.metaborg.core.project.ISimpleProjectService`

.. describe:: Context service

   :interface: :java:ref:`org.metaborg.core.context.IContextService`

^^^^^^^^^^^^^^^
Editor services
^^^^^^^^^^^^^^^

Editor services provide functionality for source code editors.

.. describe:: Categorizer service

   :interface: :java:ref:`org.metaborg.core.style.ICategorizerService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.style.ISpoofaxCategorizerService`

.. describe:: Styler service

   :interface: :java:ref:`org.metaborg.core.style.IStylerService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.style.ISpoofaxStylerService`

.. describe:: Tracing service

   :interface: :java:ref:`org.metaborg.core.tracing.ITracingService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.tracing.ISpoofaxTracingService`

.. describe:: Hover tooltip service

   :interface: :java:ref:`org.metaborg.core.tracing.IHoverService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.tracing.ISpoofaxHoverService`

.. describe:: Reference resolution service

   :interface: :java:ref:`org.metaborg.core.tracing.IResolverService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.tracing.ISpoofaxResolverService`

.. describe:: Outline service

   :interface: :java:ref:`org.metaborg.core.outline.IOutlineService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.outline.ISpoofaxOutlineService`

.. describe:: Completion service

   :interface: :java:ref:`org.metaborg.core.completion.ICompletionService`
   :specialization: :java:ref:`org.metaborg.spoofax.core.completion.ISpoofaxCompletionService`

.. describe:: Menu service

   :interface: :java:ref:`org.metaborg.core.menu.IMenuService`

^^^^^^^^^^^^^
Configuration
^^^^^^^^^^^^^

Configuration services provide read and write access to project and language component configuration at runtime.

See the :doc:`language development manual on configuration </source/langdev/manual/config>` for documentation about the Spoofax language specification configuration, which is a superset of the language specification, component, and project configuration.

.. describe:: Project configuration

   .. describe:: Service

      :interface: :java:ref:`org.metaborg.core.config.IProjectConfigService`

   .. describe:: Builder

      :interface: :java:ref:`org.metaborg.core.config.IProjectConfigBuilder`

   .. describe:: Writer

      :interface: :java:ref:`org.metaborg.core.config.IProjectConfigWriter`


.. describe:: Language component configuration

   .. describe:: Service

      :interface: :java:ref:`org.metaborg.core.config.ILanguageComponentConfigService`

   .. describe:: Builder

      :interface: :java:ref:`org.metaborg.core.config.ILanguageComponentConfigBuilder`

   .. describe:: Writer

      :interface: :java:ref:`org.metaborg.core.config.ILanguageComponentConfigWriter`


----------------
Spoofax services
----------------

.. describe:: Term factory service

   :interface: :java:ref:`org.metaborg.spoofax.core.terms.ITermFactoryService`

.. describe:: Stratego runtime service

   :interface: :java:ref:`org.metaborg.spoofax.core.stratego.IStrategoRuntimeService`

.. describe:: Common Stratego functionality

   :interface: :java:ref:`org.metaborg.spoofax.core.stratego.IStrategoCommon`


----------------------
MetaBorg-meta services
----------------------

^^^^^^^
Project
^^^^^^^

Project services in MetaBorg-meta provide a context for language specification builds.

.. describe:: Language specification project service

   :interface: :java:ref:`org.metaborg.meta.core.project.ILanguageSpecService`
   :specialization: :java:ref:`org.metaborg.spoofax.meta.core.project.ISpoofaxLanguageSpecService`


^^^^^^^^^^^^^
Configuration
^^^^^^^^^^^^^

Configuration services for language specifications.
See the :doc:`language development manual on configuration </source/langdev/manual/config>` for documentation about the Spoofax language specification configuration.

.. describe:: Language specification configuration

   .. describe:: Service

      :interface: :java:ref:`org.metaborg.meta.core.config.ILanguageSpecConfigService`
      :specialization: :java:ref:`org.metaborg.spoofax.meta.core.config.ISpoofaxLanguageSpecConfigService`

   .. describe:: Builder

      :interface: :java:ref:`org.metaborg.meta.core.config.ILanguageSpecConfigBuilder`
      :specialization: :java:ref:`org.metaborg.spoofax.meta.core.config.ISpoofaxLanguageSpecConfigBuilder`

   .. describe:: Writer

      :interface: :java:ref:`org.metaborg.meta.core.config.ILanguageSpecConfigWriter`
      :specialization: :java:ref:`org.metaborg.spoofax.meta.core.config.ISpoofaxLanguageSpecConfigWriter`


---------------------
Spoofax-meta services
---------------------

.. describe:: Language specification builder

   :interface: :java:ref:`org.metaborg.spoofax.meta.core.build.LanguageSpecBuilder`
