# Troubleshooting

## `NoClassDefFoundError` when running Spoofax build
As the JPS plugin is loaded in a separate process, IntelliJ needs to know about
any and all dependencies of the plugin, so it can add them to the class path.
The dependencies are listed under the `<extensions>` tag in
`META-INF/plugin.xml`, at the `<compileServer.plugin />` tag. If you get
a `NoClassDefFoundError`, the list of dependencies in the `classpath` attribute
may not be correct.

Replace the list of dependencies in the `classpath` attribute by the list
returned by the following Gradle task executed in the project root folder
(`org.metaborg.intellij/`):

```
./gradlew printJpsDependencies
```
