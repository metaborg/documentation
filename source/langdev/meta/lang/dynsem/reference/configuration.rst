.. _dynsem_reference_configfile:

------------------
Configuration file
------------------

The **dynsem.properties** file specifies configuration parameters for the DynSem interpreter and interpreter generator. Such a file is required for every  project from which a DynSem-based interpreter will be derived. The **dynsem.properties** file should be present at the root of the language project. If no properties file can be found a warning will be reported in every DynSem editor for that language.

.. describe:: dynsem.properties

    source.language = SIMPL
      Name of the language. May be any valid Java identifier

    source.version = 0.1
      Version of the language/semantics. Any valid version, e.g. 1.2.3 is permitted.

    source.mimetype = application/x-simpl
      (optional) mime type for files of this language

    source.table = target/metaborg/sdf.tbl
      (optional) path to parse table for programs in the language.

    source.startsymbol = Prog
      Start symbol for parsing programs of this language.

    source.initconstructor.name = Program
      Constructor name of the term where program reduction begins.

    source.initconstructor.arity = 1
      Arity of the reduction entry-point constructor.

    interpreter.fullbacktracking = false
      (optional) Enable full backtracking support in the interpreter. If full backtracking is disabled, once the interpreter descends into a reduction premise it is committed to successfully applying one of the rules for that reduction. If full backtracking is enable, the interpreter treats the inability to apply successfully apply a reduction as a regular failure of a pattern match and bails out of the currently evaluated rule to attempt others. In this case, currently evaluated rules are peeled off until a succeeding alternative is found, or the top-level rule is peeled off and the interpreter halts.

    interpreter.safecomponents = false
      (optional) Enables safe semantic components operations. If enabled, all semantic component operations that write or yield a `null` semantic component will cause the interpreter to halt immediately. The same is enforced for referencing a variable which has not been bound. Enabling safe components is a good way to catch bugs in rules with multiple branches.

    interpreter.termcaching = false
      (optional) Enables inline caching of terms and pattern matching results. This can be make a performance difference for programs which are longer running or contain loops. Caching is disabled by default. When enabled every term construction whose subterms are constant will be fetched from a cache instead of recomputed.

    interpreter.vmargs =
      (optional) Customize arguments passed to the JVM. For example setting this option to -ea will enable assertions in the running JVM. The arguments passed should not be surrounded by quotes.

    project.path = ../simpl.interpreter/
      Path to the interpreter project. The path must be eithe relative to the language project or absolute.

    project.groupid = org.metaborg
      Maven Group Identifier for the interpreter project.

    project.artifactid = simpl.interpreter
      Maven Artifact Identifier for the interpreter project.

    project.create = true
      (optional) Enable generation of an interpreter project and associated launch configuration. Defaults to false. When enabled, during generation of the interpreter a project will also be generated including all required directories. A pom.xml file will also be created. The project will not be automatically imported in the Eclipse workspace. The generator will also create a launch configuration which can be used in Eclipse.

    project.clean = true
      (optional) Enable cleaning of the target project before writing files. Defaults to false.

    project.javapackage = simpl.interpreter.generated
      (optional) Package to contain all generated Java classes. Defaults to GROUPID.ARTIFACTID.interpreter.generated.

    project.nativepackage = simpl.interpreter.natives
      Package name for manually implemented interpreter nodes

    project.preprocessor = org.metaborg.lang.sl.interpreter.natives.DesugarTransformer
      (optional) Fully qualified class name of a custom program pre-processor. The pre-processor will be invoked on the program AST prior to evaluation. Defaults to the identity transformation. See `IdentityTransformer`_ for an example.

    project.ruleregistry = org.metaborg.lang.sl.interpreter.natives.SLRuleRegistry
      (optional) Fully qualified class name of a manually implemented rule registry. Languages which do not provide hand-written rules in Java need not have a custom rule registry. See `SLRuleRegistry`_ from the *SL* language for an example.

    project.javapath = src/main/java
      (optional) Path relative to the interpreter project where Java code will reside.

    project.specpath = src/main/resources/specification.aterm
      (optional) Path in interpreter project for the DynSem specification file.

    project.tablepath     = src/main/resources/parsetable.tbl
      (optional) Path in interpreter project for parse table

.. _IdentityTransformer: https://github.com/metaborg/dynsem/blob/master/org.metaborg.meta.lang.dynsem.interpreter/src/main/java/org/metaborg/meta/lang/dynsem/interpreter/terms/ITermTransformer.java#L16

.. _SLRuleRegistry: https://github.com/MetaBorgCube/metaborg-sl/blob/master/org.metaborg.lang.sl.interp/src/main/java/org/metaborg/sl/interpreter/natives/SLRuleRegistry.java
