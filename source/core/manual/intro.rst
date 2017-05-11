.. highlight:: java

============
Introduction
============

Spoofax Core, part of Spoofax 2.x, is a Java API for building languages and running languages made with the Spoofax Language Workbench, and a concrete implementation of that API.
Spoofax Core is intended to be used by:

- Language designers wishing to embed their language into their application, so that their end-users can use their language.
- Researchers wishing to experiment with (meta-)languages, for example by running their languages in experiments or benchmarks.
- The Spoofax developers themselves, to create plugins for JVM platforms such as Maven, Eclipse, and IntelliJ, which can be used to specify, build, and run Spoofax languages.

The two main use cases of Spoofax Core are running languages and building languages.
To give an overview of what is possible, here is a code fragment that uses the API to run a Spoofax language, by loading the language, parsing a file, and displaying an outline::

    public class Main {
      public static void main(String[] args) throws Throwable {
        try(Spoofax spoofax = new Spoofax()) {
          FileObject languageDir = spoofax.resourceService.resolve(args[0]);
          ILanguageImpl language = spoofax.languageDiscoveryService.languageFromDirectory(languageDir)

          FileObject fileToParse = spoofax.resourceService.resolve(args[1]);
          String text = spoofax.sourceTextService.text(fileToParse);
          ISpoofaxInputUnit input = spoofax.unitService.inputUnit(fileToParse, language, null);
          ISpoofaxParseUnit parseUnit = spoofax.syntaxService.parse(input);

          IOutline outline = spoofax.outlineService.outline(parseUnit);
          System.out.println(outline);
        }
      }
    }

And a code fragment to build a language that has been specified in the Spoofax Language Workbench::

    public class Main {
      public static void main(String[] args) throws Throwable {
        try(SpoofaxMeta spoofax = new SpoofaxMeta()) {
          FileObject languageSpecificationDir = spoofax.resourceService.resolve(args[0]);
          IProject project = spoofax.parent.projectService.get(languageSpecificationDir);
          ISpoofaxLanguageSpec languageSpecification = spoofax.languageSpecService.get(project);

          LanguageSpecBuildInput input = new LanguageSpecBuildInput(languageSpecification);
          spoofax.metaBuilder.initialize(input);
          spoofax.metaBuilder.generateSources(input, null);
          spoofax.metaBuilder.compile(input);
          spoofax.metaBuilder.pkg(input);
          spoofax.metaBuilder.archive(input);
        }
      }
    }

Spoofax Core has been designed and implemented with several goals in mind:

- Portability - the ability to build and run languages on multiple platforms

  - For external users, the Spoofax Core support running Spoofax languages on any platform on the JVM, allowing them to embed languages into their JVM application. For example, you could define a DSL in the Spoofax Lanuage Workbench, and then have your users use the DSL by embedding it in your application.
  - For the developers of the Spoofax Language Workbench, it supports building and running languages on any JVM platform. This has allowed us to make plugins for the Maven, Eclipse, and IntelliJ platforms that can build and run any Spoofax language, and will allow us to expand this support to other platforms in the future.

- Maintainability

  - The API to Spoofax Core is separated from the implementation of Spoofax Core. This allows us to update the implementation without changing the API.

- Extensibility

  - Spoofax Core supports extensibility in several places, without having to change the source code.

The source code of Spoofax Core can be found in the `metaborg/spoofax repository on GitHub <https://github.com/metaborg/spoofax>`__.

Next, we describe the architecture of Spoofax Core.
