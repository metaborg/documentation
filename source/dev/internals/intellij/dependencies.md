# Dependencies
Dependencies of the Spoofax plugin for IntelliJ IDEA are not actually
managed in the plugin project itself, but in a separate project: the `deps/`
project.

Add dependencies to or remove them from the `deps/build.gradle` file.

If a dependency causes a JAR version conflict with a JAR that's distributed
with IntelliJ IDEA or JPS, see [the troubleshooting page][1] for a solution.

Rebuild the dependencies project to use them in the plugin:

```
./gradlew clean publishToMavenLocal
```


[1]: troubleshooting.md
