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




[1]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/discovery/ILanguageSource.java
[2]: http://artifacts.metaborg.org/
[3]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/languages/ILanguageManager.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/languages/IIdeaLanguageManager.java
