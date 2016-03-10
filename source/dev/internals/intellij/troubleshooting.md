# Troubleshooting

## `NoSuchMethodError` in IntelliJ IDEA or when running Spoofax build
There may be a JAR version conflict, as IntelliJ and JPS use their own versions
of certain common JARs (e.g. Apache's Commons IO) and those may get loading
priority.

To fix this, go to the dependencies project (in `deps/`) and edit the
`build.gradle` file. In the `shadowJar` section, add a new relation from
the original package to the new package (usually the same package name prefixed
with `intellij.`):

```
relocate 'org.apache.commons.io', 'intellij.org.apache.commons.io'
```

Now, whenever you want to use a class from that package you have to use the
new package name. The build script will take care of renaming usages of the
package in the dependencies.

```eval_rst
.. note:: Rebuild the dependencies project.

      ./gradlew clean publishToMavenLocal

```
