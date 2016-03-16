# Bindings
Both the IntelliJ IDEA plugin and the JPS plugin use Guice bindings for the
dependency injection.



## Injecting Dependencies
To inject dependencies in a class that is created by Guice, simply annotate
the constructor with `@Inject` and add the dependencies as parameters.

```java
public final class MyClass implements IMyInterface {

  private final MyDependency dependency;

  @Inject
  public MyClass(final MyDependency dependency) {
    this.dependency = dependency;
  }
}
```

[Register the binding][1] in the applicable Guice module.

```java
bind(IMyInterface.class).to(MyClass.class).in(Singleton.class);
```

---

In some cases the class is not created by Guice but by IntelliJ IDEA's
[extension system][6] or by the [Java service loader][7]. In that case you have
to inject your dependencies like this:

```java
public final class MyClass implements IMyInterface {

  private MyDependency dependency;

  /**
   * This instance is created by IntelliJ's plugin system.
   * Do not call this constructor manually.
   */
  public MetaborgReferenceContributor() {
      SpoofaxIdeaPlugin.injector().injectMembers(this);
  }

  @SuppressWarnings("unused")
  @Inject
  private void inject(final MyDependency dependency) {
      this.dependency = dependency;
  }
}
```

Note that `SpoofaxIdeaPlugin` in this example can also be `SpoofaxJpsPlugin`
if you're writing a JPS plugin class.

Since the class is not created by Guice, you don't need to register a binding
if you're not depending on it. However, if you _do_ depend on such a class,
register the appropriate kind of binding that depends on who created the
class and where it was registered.


For an IntelliJ component registered in `META-INF/plugin.xml` under the
`<application-components />` tag:

```java
install(new IntelliJComponentProviderFactory().provide(IdeaApplicationComponent.class));
```

```eval_rst
.. note:: Binding module-level or project-level components is not currently
   implemented.
```

For an IntelliJ service registered in `META-INF/plugin.xml` under the
`<applicationService />` extension:

```java
install(new IntelliJServiceProviderFactory().provide(IMetaborgModuleConfig.class));
```

```eval_rst
.. note:: Binding module-level or project-level services is not currently
   implemented.
```

For any other IntelliJ extension registered under the `<extensions>` tag
in `META-INF/plugin.xml` (e.g. the `MetaborgFacetType` class registered for the
`<facetType />` extension):

```java
install(new IntelliJExtensionProviderFactory().provide(
  MetaborgFacetType.class, "com.intellij.facetType"));
```

For a class registered using the Java service provider (mostly used in the JPS
plugin):

```java
install(new JavaServiceProviderFactory().provide(BuilderService.class));
```



## Injecting Arguments
Sometimes you have some arguments that you want to use in the constructor,
but the constructor is also used for dependency injection. In that case,
annotate those arguments with `@Assisted` and create a factory interface
for the class.

```java
public final class MyClass {

  private final String name;
  private final MyDependency dependency;

  @Inject
  public MyClass(@Assisted final String name,
                 final MyDependency dependency) {
    this.name = name;
    this.dependency = dependency;
  }
}

public interface MyClassFactory {
    MyClass create(String name);
}
```

And [register the factory][2] instead of the binding:

```java
install(new FactoryModuleBuilder()
        .implement(MyClass.class, MyClass.class)
        .build(MyClassFactory.class));
```

You can use it by depending on the factory instead of the class itself.



## Injecting the Logger
In most classes you need the logger. Guice will automatically inject it if
you add the following field:

```java
@InjectLogger
private ILogger logger;
```

This also works with classes that are not created by Guice and have to use
`injectMembers()`, as explained above. Injection is handled by the
[`MetaborgLoggerTypeListener`][3] and [`Slf4JLoggerTypeListener`][4] classes.

---

In unit tests where Guice is not available, you can inject a logger in a class
using the [`LoggerUtils#injectLogger()`][5] function.


## Singleton Classes
Mark any classes that must only be used as singletons with the `@Singleton`
attribute. This prevents issues where the registered binding is incomplete,
and makes the intent of the class clear to future maintainers.

```java
@Singleton
public final class MyClass implements IMyInterface {

}
```



[1]: https://github.com/google/guice/wiki/Bindings
[2]: https://github.com/google/guice/wiki/AssistedInject
[3]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/MetaborgLoggerTypeListener.java
[4]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/Slf4JLoggerTypeListener.java
[5]: https://github.com/metaborg/spoofax-intellij/blob/develop/org.metaborg.intellij/src/main/java/org/metaborg/intellij/logging/LoggerUtils.java
[6]: http://www.jetbrains.org/intellij/sdk/docs/basics/plugin_structure/plugin_extensions_and_extension_points.html
[7]: https://docs.oracle.com/javase/7/docs/api/java/util/ServiceLoader.html
