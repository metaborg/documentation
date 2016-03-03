# Projects
A Metaborg project can contain source files written in Metaborg languages. Such
projects are represented by classes derived from the [`IProject`][1]
interface. In the IDEA plugin this is the [`IdeaProject`][2] class, but in the
JPS plugin this is the [`MetaborgJpsProject`][3] class.

A Metaborg language specification defines a new language. Such projects are
represented by [`IdeaLanguageSpec`][4] (IDEA) and [`JpsLanguageSpec`][5] (JPS),
both of which derive from the [`ISpoofaxLanguageSpec`][6] interface, which
indirectly derives from `IProject`.

Additionally, there is the [`ArtifactProject`][7] for language artifacts.


## Modules
IntelliJ IDEA uses the concept of _modules_, which are similar to projects in
Eclipse. To get the Metaborg project that corresponds to a module, use the
[`IIdeaProjectService`][8] methods (in IDEA), or the [`IJpsProjectService`][9]
(or JPS) methods.

An IntelliJ module lives in a _project_, which corresponds to a workspace in
Eclipse. And projects live in the application, which is application-wide.

A module has so-called content roots: folders that hold the content of the
module. A simple module just has the module's root folder as a content root, but
a more complex module might have several content roots from all over the place.
A single file may belong to multiple modules.


## Module Type
A language specification project is represented in IntelliJ IDEA as a module
with the [`MetaborgModuleType`][10]. Such a module is created and managed by
the [`MetaborgModuleBuilder`][11]. Its `setupRootModel()` method is responsible
for setting up the module and creating its files.



[1]: https://github.com/metaborg/spoofax/blob/master/org.metaborg.core/src/main/java/org/metaborg/core/project/IProject.java
[2]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/projects/IdeaProject.java
[3]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/projects/MetaborgJpsProject.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/projects/IdeaLanguageSpec.java
[5]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/projects/JpsLanguageSpec.java
[6]: https://github.com/metaborg/spoofax/blob/master/org.metaborg.spoofax.meta.core/src/main/java/org/metaborg/spoofax/meta/core/project/ISpoofaxLanguageSpec.java
[7]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/projects/ArtifactProject.java
[8]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/projects/IIdeaProjectService.java
[9]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/projects/IJpsProjectService.java
[10]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/projects/MetaborgModuleType.java
[11]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/projects/MetaborgModuleBuilder.java
