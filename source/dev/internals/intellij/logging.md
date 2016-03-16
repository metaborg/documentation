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

## IntelliJ versus Spoofax
Both Spoofax Core (and related Metaborg libraries) and IntelliJ IDEA use _slf4j_
for logging. The Spoofax for IntelliJ plugin also uses _slf4j_ for logging, so
it depends on `org.slf4j:slf4j-api:1.7.10`.

Normally _slf4j_ looks for a `StaticLoggerBinder` implementation and bind to
that for logging. IntelliJ IDEA provides a `StaticLoggerBinder` by default
(from `org.slf4j:slf4j-log4j12:1.7.10`), so we'd like to bind to that. This is
_slf4j_'s default behavior, so we don't have to add any dependencies for this.
However, if we try that, we get an exception:

> java.lang.LinkageError: loader constraint violation: when resolving method "org.slf4j.impl.StaticLoggerBinder.getLoggerFactory()Lorg/slf4j/ILoggerFactory;" the class loader (instance of com/intellij/ide/plugins/cl/PluginClassLoader) of the current class, org/slf4j/LoggerFactory, and the class loader (instance of com/intellij/util/lang/UrlClassLoader) for the method's defining class, org/slf4j/impl/StaticLoggerBinder, have different Class objects for the type org/slf4j/ILoggerFactory used in the signature

Apparently there are two class loaders used to resolve the `StaticLoggerBinder`,
and they interfere.

We can use our own logger binder (depend on `org.slf4j:slf4j-simple:1.7.10`),
but this has some downsides: we have to configure the logger ourselves, and
can't choose the `StaticLoggerBinder` that _slf4j_ should bind to. This causes
it to warn us that there are now two `StaticLoggerBinder` classes and it doesn't
know which one to bind to. It will pick one at random:

    SLF4J: Class path contains multiple SLF4J bindings.
    SLF4J: Found binding in [jar:file:/home/daniel/.IdeaIC14/system/plugins-sandbox/plugins/spoofax-intellij/lib/slf4j-simple-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
    SLF4J: Found binding in [jar:file:/home/daniel/apps/1507-IntelliJ/lib/slf4j-log4j12-1.7.10.jar!/org/slf4j/impl/StaticLoggerBinder.class]
    SLF4J: See http://www.slf4j.org/codes.html#multiple_bindings for an explanation.
    SLF4J: Actual binding is of type [org.slf4j.impl.SimpleLoggerFactory]

We don't have a solution for this yet.

```eval_rst
:download:`Full stack trace of the error <logging_stacktrace.txt>`
```



[1]: https://github.com/metaborg/mb-exec/blob/master/org.metaborg.util/src/main/java/org/metaborg/util/log/ILogger.java
[2]: bindings.md
[3]: https://github.com/JetBrains/intellij-community/blob/3240cd7a32d7aa5e44872527c58eee3f0f3786ce/platform/util/src/com/intellij/openapi/diagnostic/Logger.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/slf4j/impl/IntelliJLoggerAdapter.java
[5]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/PrintStreamLogger.java
[6]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/LoggerUtils.java
