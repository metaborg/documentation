# Maven Builds

This page describes how to build Spoofax languages with Maven.

## Requirements

### JDK8 or higher

A recent version of JDK 8 or higher is required to build Spoofax languages with Maven.
Old versions may not accept the LetsEncrypt certificate of our artifact server.
We try to keep Spoofax compatible with newer JDKs (such as JDK13) as well, but if they do not work, please try JDK8.

### Maven

We require Maven version 3.5.4 or higher, except Maven version 3.6.1 or 3.6.2 (due to bugs in those Maven versions).
Maven can be downloaded and installed from https://maven.apache.org/download.cgi.
On macOs, Maven can be easily installed with Homebrew by executing ``brew install maven``.

Confirm the installation and version by running ``mvn --version``.

By default, Maven does not assign a lot of memory to the JVM that it runs in, which may lead to out of memory exceptions during builds.
To increase the allocated memory, set the `MAVEN_OPTS` environment variable:

```shell
export MAVEN_OPTS="-Xms512m -Xmx1024m -Xss16m"
```

To make this permanent, add this line to your `.bashrc`/`.profile` or equivalent for your operating system/shell.

## Maven Build

The local Maven build starts from the generate new project wizard (you need the generated files).
`New Project` > `New Spoofax language project` > select all generation options.
This generates 6 projects in total.
In this tutorial, our language name and ID is `entity`.

Move the six projects to a new parent directory, and create a `pom.xml` file in this directory with the following contents:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<project
  xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd"
  xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance">

  <modelVersion>4.0.0</modelVersion>
  <artifactId>entity.build</artifactId>
  <version>0.1.0-SNAPSHOT</version>
  <packaging>pom</packaging>

  <parent>
    <groupId>org.metaborg</groupId>
    <artifactId>parent</artifactId>
    <version>REPLACEME_SPOOFAX_VERSION</version>
    <relativePath />
  </parent>

  <modules>
    <module>entity</module>
    <module>entity.eclipse</module>
    <module>entity.eclipse.feature</module>
    <module>entity.eclipse.site</module>
    <module>entity.test</module>
  </modules>

  <repositories>
    <repository>
      <id>metaborg-release-repo</id>
      <url>https://artifacts.metaborg.org/content/repositories/releases/</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
    <repository>
      <id>metaborg-snapshot-repo</id>
      <url>https://artifacts.metaborg.org/content/repositories/snapshots/</url>
      <releases>
        <enabled>false</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </repository>
    <repository>
      <id>spoofax-eclipse-repo</id>
      <url>https://artifacts.metaborg.org/content/unzip/releases-unzipped/org/metaborg/org.metaborg.spoofax.eclipse.updatesite/|rel-version|/org.metaborg.spoofax.eclipse.updatesite-|rel-version|-assembly.zip-unzip/</url>
      <layout>p2</layout>
      <releases>
        <enabled>false</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </repository>
  </repositories>

  <pluginRepositories>
    <pluginRepository>
      <id>metaborg-release-repo</id>
      <url>https://artifacts.metaborg.org/content/repositories/releases/</url>
      <releases>
        <enabled>true</enabled>
      </releases>
      <snapshots>
        <enabled>false</enabled>
      </snapshots>
    </pluginRepository>
    <pluginRepository>
      <id>metaborg-snapshot-repo</id>
      <url>https://artifacts.metaborg.org/content/repositories/snapshots/</url>
      <releases>
        <enabled>false</enabled>
      </releases>
      <snapshots>
        <enabled>true</enabled>
      </snapshots>
    </pluginRepository>
  </pluginRepositories>

</project>
```

and replace `REPLACEME_SPOOFAX_VERSION` with the version of Spoofax you are using.

Copy the `.mvn` folder from your language folder to the parent folder. e.g. `root/entity/.mvn -> root/.mvn`.
(Error message otherwise: `[ERROR] Failed to execute goal org.metaborg:spoofax-maven-plugin:2.1.0-SNAPSHOT:clean (default-clean) on project entity: Building clean input failed unexpectedly: Language for dependency org.metaborg:org.metaborg.meta.lang.esv:2.1.0-SNAPSHOT does not exist -> [Help 1]`)

Fix the generated test yaml file (known issue) e.g. `root/entity.test/metaborg.yaml`.
(Error message otherwise: `[ERROR] Field 'id' must be set`)

```yaml
---
dependencies:
  compile:
  - org.example:entity:0.1.0-SNAPSHOT
  - org.metaborg:org.metaborg.meta.lang.spt:${metaborgVersion}
```
to
```yaml
---
id: org.example:entity.test:0.1.0-SNAPSHOT
name: entity
dependencies:
  compile:
  - org.example:entity:0.1.0-SNAPSHOT
  - org.metaborg:org.metaborg.meta.lang.spt:${metaborgVersion}
```

Now you can build the language with `mvn clean verify`, with the final output succeeding with something like:

```
[INFO] ------------------------------------------------------------------------
[INFO] Building entity.build 0.1.0-SNAPSHOT
[INFO] ------------------------------------------------------------------------
[INFO]
[INFO] --- maven-clean-plugin:3.0.0:clean (default-clean) @ entity.build ---
[INFO] ------------------------------------------------------------------------
[INFO] Reactor Summary:
[INFO]
[INFO] entity ............................................. SUCCESS [ 31.033 s]
[INFO] entity.eclipse ..................................... SUCCESS [  1.252 s]
[INFO] entity.eclipse.feature ............................. SUCCESS [  0.469 s]
[INFO] entity.eclipse.site ................................ SUCCESS [  3.776 s]
[INFO] entity.test ........................................ SUCCESS [  0.140 s]
[INFO] entity.build ....................................... SUCCESS [  0.013 s]
[INFO] ------------------------------------------------------------------------
[INFO] BUILD SUCCESS
[INFO] ------------------------------------------------------------------------
[INFO] Total time: 51.354 s
[INFO] Finished at: 2016-09-16T16:58:25+02:00
[INFO] Final Memory: 280M/963M
[INFO] ------------------------------------------------------------------------
```
