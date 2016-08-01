.. highlight:: java

===================
Language Processing
===================

Spoofax, at its core, is a language processing framework.
That is, a framework for reading, parsing, analyzing, transforming, and writing programs (files) of a language.

Spoofax provides a completely automated configurable language processing pipeline that works for most language.
Spoofax also exposes API for manual language processing, in the case that the automated language processing pipeline does not do what you would like.
We describe both ways of language processing in this manual.

Getting a project handle
========================

All language processing happens inside an :java:ref:`~org.metaborg.core.project.IProject`, which is a handle for a project at a certain location, containing source files.

Projects are retrieved with the :java:ref:`~org.metaborg.core.project.IProjectService` service.
However, different applications provide different implementations of this service, because they have different means of representing projects.
For example, in Eclipse and IntelliJ, projects are top-level directories in the workspace.
In Maven, a project is denoted by a directory which has a :file:`pom.xml` file.
Therefore, Eclipse, IntelliJ, and Maven provide special implementations of the project service.
Creation and removal of projects in those environments is determined by the environment.
Projects can be retrieved with the following code::

  IProjectService projectService = ... // Get through dependency injection
  IProject project = projectService.get(location);
  if(project == null) {
    // Handle case where project does not exist.
  }

In a command-line application, projects are typically passed as a command-line argument that points to a directory.
Therefore, the simple project service implementation can be used, which allows the command-line application to manage creation and removal of projects.
The simple project service is the default implementation, and can be accessed through the :java:ref:`~org.metaborg.core.project.ISimpleProjectService` interface by dependency injection.
With the simple project service, projects can be created and removed in a command-line environment with the following code::

  public class Main {
    public static void main(String[] args) {
      String projectDir = args[1]; // First command-line argument is the project directory.

      // Resolve project directory into a FileObject for use in Spoofax.
      IResourceService resourceService = ... // Get through dependency injection
      FileObject projectLoc = resourceService.resolve(projectDir);

      ISimpleProjectService projectService = ... // Get through dependency injection
      try {
        // Add a project
        IProject project = projectService.create(projectLoc);
      } catch(MetaborgException e) {
        // Handle project creation exception.
      }
    }
  }

After a project is added, it can be retrieved again with the project service interface.
Any files inside the project location (i.e. ancestor of project path) belong to the added project; retrieving the project for those files will return the added project.

Automatic language processing
=============================

Automated language processing is performed with the :java:ref:`~org.metaborg.spoofax.core.build.ISpoofaxBuilder` service.
It provides a ``build`` method for running the language processing pipeline, and a ``clean`` method for cleaning up generated files produced by the pipeline.

The ``build`` method takes a progress reporter for reporting the progress of a build, a cancellation token to cancel a build, and importantly, a :java:ref:`~org.metaborg.core.build.BuildInput` object that specifies what to build and how to build it.
A build input object is constructed with the :java:ref:`~org.metaborg.core.build.BuildInputBuilder`, class which is a `fluent interface <https://en.wikipedia.org/wiki/Fluent_interface>`_ for creating build inputs.

For example, to create a build input which parses, analyzes, and compiles all sources in a project, use the following code::

  BuildInput input = new BuildInputBuilder(project)
    .withDefaultIncludePaths(true)
    .withSourcesFromDefaultSourceLocations(true)
    .withSelector(new SpoofaxIgnoresSelector())
    .addTransformGoal(new CompileGoal())
    .build(dependencyService, languagePathService)
    ;

There are several methods in the build input builder which allow customisation of the build input object, to customise the processing pipeline.

To run the language processing pipeline, pass the build input along with a progress reporter and cancellation token to the builder service::

  ISpoofaxBuilder builder = ... // Get through dependency injection
  CancellationToken cancellationToken = new CancellationToken()
  ISpoofaxBuildOutput output = builder.build(input, new NullProgressReporter(),
    cancellationToken)

The result of building is a :java:ref:`~org.metaborg.spoofax.core.build.SpoofaxBuildOutput` object which denotes if the build was successful, and contains resource changes, parse, analysis, and transformation results, and any messages produced during building.
It also includes the state of the build, which can be passed to the next build input to perform incremental processing.

Manual language processing
==========================

While automatic language processing provides an easy way for processing programs of a language, sometimes more control is needed.
Therefore, we expose the parsing, analysis, and transformation API, to allow custom language processing pipelines.

Units
-----

The processing pipeline works with the concept of units.
A unit is a collection of information, about a certain processing aspect, for a single resource, of a certain language.
For example, a parse unit contains the parsed AST for a resource, or a collection of error messages if parsing that resource, and is specific to the language that it is parsed with.

.. Units can be attached to actual files, or detached from files to support in-memory processing, without requiring physical files to exist.

In most cases, it is not required to manually construct processing units, since the parse, analyze, and transform services create these units for you.
The only unit that must always be created, is the :java:ref:`~org.metaborg.spoofax.core.unit.ISpoofaxInputUnit`, which contains all information to parse a resource.
Such a unit can be constructed with the :java:ref:`~org.metaborg.spoofax.core.unit.ISpoofaxInputUnitService` service, for example::

  FileObject source = ...      // Source file to parse
  ILanguageImpl language = ... // Language of the source file
  // Get contents of the source file
  ISourceTextService sourceTextService = ... // Get through dependency injection
  String contents = sourceTextService.text(source);
  // Create an input unit for the source file
  ISpoofaxInputUnitService unitService = ... // Get through dependency injection
  ISpoofaxInputUnit inputUnit = unitService.inputUnit(source, contents, language, null);

If construction of other units is required, the :java:ref:`~org.metaborg.spoofax.core.unit.ISpoofaxUnitService` service must be used.
For example, the following code creates an :java:ref:`~org.metaborg.spoofax.core.unit.ISpoofaxParseUnit` from a custom AST::

  IStrategoTerm customAST = ... // Custom AST made by the developer
  // Create a parse unit using the custom AST
  ISpoofaxUnitService unitService = ... // Get through dependency injection
  ISpoofaxParseUnit parseUnit = unitService.parseUnit(inputUnit, new ParseContrib(true, true,
    customAST, Iterables2.<IMessage>empty(), -1));

Parsing
-------

The :java:ref:`~org.metaborg.spoofax.core.syntax.ISpoofaxSyntaxService` service parse input units into parse units.
Parsing can be configured by customizing the input unit.
The resulting parse unit contains the parsed AST, any messages produced during parsing, and the duration of parsing.

Analysis
--------

The :java:ref:`~org.metaborg.spoofax.core.analysis.ISpoofaxAnalysisService` service parses parse units into analysis results.
An analysis result contains an analyze unit, which contains the actual unit produced by analysis, and updates, which contain updates for existing analyze units.
Updates are only produced in subsequent calles to the analysis service, to support incremental updates to units.

To be able to analyze something, a :java:ref:`~org.metaborg.core.context.IContext` object is required.
A context stores project and language specific information about analysis.
A context is retrieved using the :java:ref:`~org.metaborg.core.context.IContextService` service, by calling the ``get`` method with the resource that you'd like to analyze, its project, and the language of that resource.

For example, to analyze a parsed resource::

  IProject project = ...            // Project of the source file
  ISpoofaxParseUnit parseUnit = ... // Parsed source file
  // Get a context for the parsed source file
  IContextService contextService = ... // Get through dependency injection
  IContext context = contextService.get(parseUnit.source(), project,
    parseUnit.input().langImpl());
  // Analyze the parsed source file
  ISpoofaxAnalysisService analysisService = ... // Get through dependency injection
  ISpoofaxAnalyzeResult result = analysisService.analyze(parseUnit, context);
  ISpoofaxAnalyzeUnit analyzeUnit = result.result();

Transformation
--------------

The :java:ref:`~org.metaborg.spoofax.core.transform.ISpoofaxTransformService` service transforms parse or analyze units into transform units.

Since there are multiple transformations to choose from, a :java:ref:`~org.metaborg.core.action.ITransformGoal` object is required to choose which transformation to run.
There are three transform goals:

- :java:ref:`~org.metaborg.core.action.CompileGoal` which selects the compiler (on-save handler) transformation.
- :java:ref:`~org.metaborg.core.action.NamedGoal` which selects a named builder. A list of names is required to find an action in nested menus.
- :java:ref:`~org.metaborg.core.action.EndNamedGoal` which selects a named builder based on the name of the builder only, ignoring any menus.

No service is needed to instantiate a transform goal, just instantiate one of the goals manually.

To transform a parse or analyze unit, call one of the ``transform`` methods.
A context object is required for transforming. See the section on analysis on how to retrieve a context object.
Since a language implementation can contain multiple transformations for the same goal, executing a transformation can return multiple transform units.

The following example transforms an analyzed resource::

  IAnalyzeUnit analyzeUnit = ...
  ISpoofaxTransformService transformService = ... // Get through dependency injection
  Collection<ISpoofaxTransformUnit<ISpoofaxAnalyzeUnit>> transformUnits =
    transformService.transform(analyzeUnit, analyzeUnit.context(),
    new EndNamedGoal("Compile to Java"));

Stratego Transformation
-----------------------

The transform service abstracts over the fact that Stratego is perform transformations, by executing transformations through goals.
However, sometimes it may still be neccessary to call Stratego strategies directly.
Therefore, we expose the :java:ref:`~org.metaborg.spoofax.core.stratego.IStrategoCommon` class.

The ``invoke`` methods execute a strategy on a term, and return the transformed term.
A context object is required for transformation. See the section on analysis on how to retrieve a context object.
For example, to invoke a strategy on a parsed AST::

  ISpoofaxParseUnit parseUnit = ...
  IContext context = ...
  IStrategoCommon strategoCommon = ... // Get through dependency injection
  IStrategoTerm transformed = strategoCommon.invoke(parseUnit.input().langImpl(),
    context, parseUnit.ast(), "compile-to-java");

The ``toString`` and ``prettyPrint`` methods can be used to turn terms into string representations.

Internally, the :java:ref:`~org.metaborg.spoofax.core.stratego.IStrategoRuntimeService` service is used, but this has a lower-level interface.
