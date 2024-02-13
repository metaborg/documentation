# Languages

## Language management
All language operations (loading, unloading, activating, deactivating, and
discovery) should go through the [`ILanguageManager`][3] or
[`IIdeaLanguageManager`][4] interface. The implementations take care in
registering, unregistering, activating and deactivating the languages such that
the IDE can use them.

Discovering a language doesn't load it. Loading a language makes Metaborg Core
aware of it. Activating a language makes it usable in the IDE. For JPS plugins
language activation is not available, as it doesn't have an IDE.



## Language sources
A Metaborg language might be found in a Maven repository, or installed locally.
The [`ILanguageSource`][1] interface was introduced to abstract this. Given a
language identifier, it will return the location of a language component for
that language identifier.

Currently it only looks in the plugin's resources, but future implementations
may search Maven Central or [artifacts.metaborg.org][2].


## Languages in IntelliJ
IntelliJ expects a unique implementation of the abstract `Language` class for
each language. It considers two `Language` to be the same if they are instances
of the same class. Therefore, to represent multiple Spoofax languages, we need
to create our own `Language` class implementations dynamically.

The built-in `java.lang.reflect.Proxy` class is not sufficient. First of all
I'm not sure whether different proxies are different classes, but most
importantly, the `Proxy` class only supports implementing interfaces. We need
to implement the abstract class `Language`, so this won't work.

There are several third-party libraries that allow you to create classes at
runtime. A very promising one is _Javassist_, which I've used before when
trying to build a profiler for Stratego. [Here is some information][5].




[1]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/discovery/ILanguageSource.java
[2]: https://artifacts.metaborg.org/
[3]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/languages/ILanguageManager.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/languages/IIdeaLanguageManager.java
[5]: https://stackoverflow.com/a/3292208/146622
