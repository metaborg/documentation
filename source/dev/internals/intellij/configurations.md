# Configurations
This document is about the configuration data used within the Spoofax plugin.
Go to the [Spoofax Core documentation][1] for more information on the project
and language specification configurations.

There are currently four configurations:

* Application configuration.
* Project configurations.
* Module configurations.
* Facet configurations.

These configurations are persisted between IntelliJ IDEA sessions
(in XML-files), and are marshalled to the JPS build plugin when it's invoked.

Below I'm describing the application configuration, but the other configurations
are treated and implemented very similarly.


## Configuration State
The configuration state (the raw data) is represented by the
[`MetaborgApplicationConfigState`][2] class. The state class may only contain
simple types: numbers, booleans, strings, collections, maps and enums.

The default constructor of the state is used to initialize the state to its
default value.

```eval_rst
.. note:: IntelliJ only persists the configuration state when it has changed
   from the default state.
```

The state must implement the `equals()` method to allow it to be compared to
other states.


## Configuration Interface
The configuration state may be very crude, as it contains only simple types.
The [`IMetaborgApplicationConfig`][3] interface describes how the data can be
accessed in a nicer way. This interface is used by both the IntelliJ IDEA and
JPS plugins.


## IDEA configuration
Asking for the `IMetaborgApplicationConfig` interface in the IntelliJ IDEA
plugin will give you the [`IdeaMetaborgApplicationConfig`][5] class that
implements the [`PersistentStateComponent<T>`][4] interface. The class has a
`@State` attribute that indicates where the configuration is persisted. By
persisting it to default locations, the configuration can be read from within
the JPS plugin.


## JPS configuration
In the JPS plugin asking for the `IMetaborgApplicationConfig` interface will
give you the [`JpsMetaborgApplicationConfig`][6] class that reads the
configuration back. Reading is automatically done through the
[`MetaborgApplicationConfigDeserializer`][7] class.




[1]: /source/dev/internals/index.rst
[2]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/configuration/MetaborgApplicationConfigState.java
[3]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/configuration/IMetaborgApplicationConfig.java
[4]: https://github.com/JetBrains/intellij-community/blob/3240cd7a32d7aa5e44872527c58eee3f0f3786ce/platform/core-api/src/com/intellij/openapi/components/PersistentStateComponent.java
[5]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/idea/configuration/IdeaMetaborgApplicationConfig.java
[6]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/configuration/JpsMetaborgApplicationConfig.java
[7]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/jps/configuration/MetaborgApplicationConfigDeserializer.java
