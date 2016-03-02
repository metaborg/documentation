# Maven

Maven is a project management and build tool for software projects. Spoofax is built with Maven.

## Setting up Maven

### Requirements

Maven requires a Java compiler, so a JDK needs to be installed on your computer, since the JRE does not ship with a Java compiler.
The latest JDK can be downloaded and installed from: <http://www.oracle.com/technetwork/java/javase/downloads/index.html>.
We require at least JDK7.

On OSX, it can be a bit tricky to use the installed JDK, because Apple by default installs JRE 6. To check which version of Java you are running, execute the `java -version` command. If this tells you that the Java version is 1.7, everything is fine. If not, the Java version can be set with a command. After you have installed JDK, execute:

```bash
export JAVA_HOME=`/usr/libexec/java_home -v version`
```

where `version` is `1.7` or `1.8` depending on which version of the JDK you have installed.

```eval_rst
.. note:: Such an export is not permanent. To make it permanent, add that line to :file:`~/.bashrc` or equivalent for your OS/shell (create the file if it does not exist), which will execute it whenever a new shell is opened.
```

Confirm your JDK installation and version by executing `java -version` and `javac -version`.

### Installing

Maven can be downloaded and installed from <http://maven.apache.org/download.cgi>. We require Maven 3.3.9 or higher. On OSX, Maven can be easily installed with Homebrew by executing `brew install maven`.

Confirm the installation and version by running `mvn --version`.

### Memory allocation

By default, Maven does not assign a lot of memory to the JVM that it runs in, which may lead to out of memory exceptions during builds.
To increase the allocated memory, execute before building:

```bash
export MAVEN_OPTS="-Xms512m -Xmx1024m -Xss16m -XX:MaxPermSize=512m"
```

```eval_rst
.. note:: Such an export is not permanent, see previous note about making this permanent.
```

```eval_rst
.. note:: ``-XX:MaxPermSize=512m`` is not required for Java 8, and even gives a warning when added.
```

## Using MetaBorg Maven artifacts

MetaBorg's Maven artifacts are hosted on our artifact server: <http://artifacts.metaborg.org>. To use these artifacts, repositories have to be added to your Maven configuration. Repositories can be added to your local Maven settings file (which is recommended), or to a project's POM file.

### Local settings file

The recommended approach is to add repositories to your local Maven settings file, located at <span class='file'>~/.m2/settings.xml</span>. If you have not created this file yet, or want to completely replace it, simply create it with the following content:

```xml
<?xml version="1.0" ?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">  
  <profiles>
    <profile>
      <id>add-metaborg-release-repos</id>
      <activation>
        <activeByDefault>true</activeByDefault>
      </activation>
      <repositories>
        <repository>
          <id>metaborg-release-repo</id>
          <url>http://artifacts.metaborg.org/content/repositories/releases/</url>
          <releases>
            <enabled>true</enabled>
          </releases>
          <snapshots>
            <enabled>false</enabled>
          </snapshots>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>metaborg-release-repo</id>
          <url>http://artifacts.metaborg.org/content/repositories/releases/</url>
          <releases>
            <enabled>true</enabled>
          </releases>
          <snapshots>
            <enabled>false</enabled>
          </snapshots>
        </pluginRepository>
      </pluginRepositories>
    </profile>

    <profile>
      <id>add-metaborg-snapshot-repos</id>
      <activation>
        <activeByDefault>true</activeByDefault>
      </activation>
      <repositories>
        <repository>
          <id>metaborg-snapshot-repo</id>
          <url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
          <releases>
            <enabled>false</enabled>
          </releases>
          <snapshots>
            <enabled>true</enabled>
          </snapshots>
        </repository>
      </repositories>
      <pluginRepositories>
        <pluginRepository>
          <id>metaborg-snapshot-repo</id>
          <url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
          <releases>
            <enabled>false</enabled>
          </releases>
          <snapshots>
            <enabled>true</enabled>
          </snapshots>
        </pluginRepository>
      </pluginRepositories>
    </profile>

    <profile>
      <id>add-spoofax-eclipse-repos</id>
      <activation>
        <activeByDefault>true</activeByDefault>
      </activation>
      <repositories>
        <repository>
          <id>spoofax-eclipse-repo</id>
          <url>http://download.spoofax.org/update/nightly/</url>
          <layout>p2</layout>
          <releases>
            <enabled>false</enabled>
          </releases>
          <snapshots>
            <enabled>false</enabled>
          </snapshots>
        </repository>
      </repositories>
    </profile>
  </profiles>
</settings>
```

If you've already created a settings file before and want to add the repositories, just add the `profile` element (and the `profiles` element if it does not exist yet) to the settings file.

### Advanced: project POM file

Repositories can also be added directly to a project's POM file, which only set the repositories for that particular project. This is not recommended, because it makes repositories harder to change by users, and duplicates the configuration. But it can be convenient, because it does not require an external settings file.

To do this, just add the the following content to the POM file:

```xml
<repositories>
	<repository>
		<id>metaborg-release-repo</id>
		<url>http://artifacts.metaborg.org/content/repositories/releases/</url>
		<releases>
			<enabled>true</enabled>
		</releases>
		<snapshots>
			<enabled>false</enabled>
		</snapshots>
	</repository>
	<repository>
		<id>metaborg-snapshot-repo</id>
		<url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
		<releases>
			<enabled>false</enabled>
		</releases>
		<snapshots>
			<enabled>true</enabled>
		</snapshots>
	</repository>
	<repository>
		<id>spoofax-eclipse-repo</id>
		<url>http://download.spoofax.org/update/nightly/</url>
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
		<url>http://artifacts.metaborg.org/content/repositories/releases/</url>
		<releases>
			<enabled>true</enabled>
		</releases>
		<snapshots>
			<enabled>false</enabled>
		</snapshots>
	</pluginRepository>
	<pluginRepository>
		<id>metaborg-snapshot-repo</id>
		<url>http://artifacts.metaborg.org/content/repositories/snapshots/</url>
		<releases>
			<enabled>false</enabled>
		</releases>
		<snapshots>
			<enabled>true</enabled>
		</snapshots>
	</pluginRepository>
</pluginRepositories>
```

## Maven central repository mirror

Artifacts of most open source projects are hosted on the [Central Repository](https://search.maven.org/) server. If you are building any project using Maven, many artifacts will be downloaded from that server. While it is a fast server, it can still take a while to download all required artifacts for big projects.

If you are on the TUDelft network, you can use our local mirror of the Central Repository to speed things up. Using the mirroring requires a change in your local settings.xml file located at <span class='file'>~/.m2/settings.xml</span>. If this file does not exist, create it with the following content:

```xml
<?xml version="1.0" ?>
<settings xmlns="http://maven.apache.org/SETTINGS/1.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
  xsi:schemaLocation="http://maven.apache.org/SETTINGS/1.0.0 http://maven.apache.org/xsd/settings-1.0.0.xsd">
  <mirrors>
    <mirror>
      <id>metaborg-nexus-central-mirror</id>
      <url>http://artifacts.metaborg.org/content/repositories/central/</url>
      <mirrorOf>central</mirrorOf>
    </mirror>
  </mirrors>
</settings>
```

If you've already created a settings file before and want to add the mirror configuration, just add the `mirror` element (and the `mirrors` element if it does not exist yet) to the settings file.
