# Logging
Metaborg Core uses its own logging implementation of [`ILogger`][1]. You can
[ask Guice][2] to inject it into your classes. Underneath it calls Slf4J to do
the logging. IntelliJ IDEA uses its own built-in [`Logger`][3] implementation
that is called by the [`IntelliJLoggerAdapter`][4] that's bound to the Metaborg
Core Slf4J logger.

In unit tests where Guice is not availabel, you can inject the
[`PrintStreamLogger`][5]. See [the Bindings documentation][2] for more
information.


## Throwing and logging an exception
Often when you want to throw an exception, you first have to format the
exception message and then log the message and finally throw the exception.
The [`LoggerUtils#exception()`][6] functions make this a whole lot easier.

```java
throw LoggerUtils.exception(this.logger, RuntimeException.class,
    "Error occurred in {}.", this.name);
```

This will format the message, construct the given exception class with the
current stack trace, and return it. You can then throw the exception.
The stack trace is cleaned up such that the `LoggerUtils` class doesn't appear
in the trace.






[1]: https://github.com/metaborg/mb-exec/blob/master/org.metaborg.util/src/main/java/org/metaborg/util/log/ILogger.java
[2]: bindings.md#injecting-the-logger
[3]: https://github.com/JetBrains/intellij-community/blob/3240cd7a32d7aa5e44872527c58eee3f0f3786ce/platform/util/src/com/intellij/openapi/diagnostic/Logger.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/slf4j/impl/IntelliJLoggerAdapter.java
[5]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/PrintStreamLogger.java
[6]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/LoggerUtils.java
