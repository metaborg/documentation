========================
Using the API
========================

This guide will get you started with the Spoofax Core API, within an Eclipse environment.

------------
Requirements
------------

Spoofax is written in Java, and thus runs on the major operating systems:

- Windows (32 and 64 bits)
- Linux (32 and 64 bits)
- Mac OSX (Intel only)

The Spoofax Core API is written in Java 8, and can be compiled with a Java Development Kit (JDK) of version 8 up to version 11.
Higher JDK versions have not been tested, and may result in errors about unresolved Java base classes (e.g., ``java.lang.Object``).
You can download and install JDK 8 or JDK 11 from `AdoptOpenJDK <https://adoptopenjdk.net/>`_, or get a proprietary release from `Oracle <https://www.oracle.com/nl/java/technologies/javase-downloads.html>`_.

The Spoofax Core API is deployed as a set of Maven artifacts.
We do not (yet) publish these artifacts to Maven Central, but rather to repositories on our own artifact server.
To get access to our artifacts, read the :ref:`Using MetaBorg Maven artifacts <using_metaborg_artifacts>` section.
Adding our Maven repositories gives access to our artifacts.

In this guide, we will be using Eclipse to use the Core API, but any environment that works with Maven artifacts (e.g. IntelliJ, NetBeans, command-line Maven builds) will work.
Download and install the Eclipse IDE for Java Developers from the `Eclipse website <http://www.eclipse.org/downloads/packages/eclipse-ide-java-developers/mars2>`_.

-------------
Project Setup
-------------

.. highlight:: xml

In Eclipse, open the new project dialog by choosing :menuselection:`File -> New -> Project` from the main menu.
In the new project dialog, select :menuselection:`Maven -> Maven project` and press :guilabel:`Next` to open the wizard for creating a Maven project.
Enable :guilabel:`Create a simple project (skip archetype selection)` and press :guilabel:`Next`.

Fill in the artifact details to your liking (see `Maven Naming Conventions <https://maven.apache.org/guides/mini/guide-naming-conventions.html>`_) for some info on these names), and press :guilabel:`Finish` to create the project.
Once the project has been created, open and expand it in the package or project explorer view.

Open the :file:`pom.xml` file and click the :guilabel:`pom.xml` tab to edit the source code of the POM file.
Add the following snippet to the POM file::

  <dependencies>
    <dependency>
      <groupId>org.metaborg</groupId>
      <artifactId>org.metaborg.spoofax.core</artifactId>
      <version>2.0.0</version>
    </dependency>
    <dependency>
      <groupId>ch.qos.logback</groupId>
      <artifactId>logback-classic</artifactId>
      <version>1.1.2</version>
    </dependency>
  </dependencies>

  <build>
    <plugins>
      <plugin>
        <artifactId>maven-compiler-plugin</artifactId>
        <version>3.2</version>
        <configuration>
          <source>1.7</source>
          <target>1.7</target>
        </configuration>
      </plugin>
    </plugins>
  </build>

This declares a dependency on version ``2.0.0`` of Spoofax Core, and a dependency on a logging framework so we get logging output from Spoofax Core.
It also instructs Maven that this project requires a Java 7 compiler (instead of the default; Java 5).

Since the :file:`pom.xml` file has changed, we need to update our Eclipse project.
Right click the project in the package or project explorer view, select :menuselection:`Maven -> Update Project...`, and press :guilabel:`Ok`.

Now we can start using the Core API.

-------------
Using the API
-------------

.. highlight:: java

^^^^^
Setup
^^^^^

To get started, we will download a language component, load it into Spoofax Core, and parse a file of that language.

First, let's create a main class as an entry point to the application.
Right click :file:`src/main/java` in the project, and select :menuselection:`New -> Class`.
Call the class `Main` and press :guilabel:`Finish`.
Add a main method to the class::

  public static void main(String[] args) {

  }

Second, let's download a language component that we can load into Spoofax Core.
Download the `NaBL language <http://artifacts.metaborg.org/service/local/repositories/releases/content/org/metaborg/org.metaborg.meta.lang.nabl/2.0.0/org.metaborg.meta.lang.nabl-2.0.0.spoofax-language>`_ and store it in the :file:`src/main/resources` directory of the project.
Any resources stored in :file:`src/main/resources` are packaged into the JAR file of your application and are available at runtime.

To initialize Spoofax Core, create an instance of the :java_ref:`org.metaborg.spoofax.core.Spoofax` facade::

  try(final Spoofax spoofax = new Spoofax()) {
      // Use Spoofax here
  } catch(MetaborgException e) {
      e.printStackTrace();
  }

We use the `try-with-resources <https://docs.oracle.com/javase/tutorial/essential/exceptions/tryResourceClose.html>`_ statement to initialize the Spoofax facade, such that it can clean up any temporary resources when the application shuts down.
All code that uses Spoofax must go inside the statement, where the comment is.

.. note:: Use :menuselection:`Source -> Organize Imports` or :kbd:`Ctrl+Shift+O` (:kbd:`Cmd+Shift+O` on Mac OSX) to automatically add required imports when needed.

^^^^^^^^^^^^^^^^^^
Loading a language
^^^^^^^^^^^^^^^^^^

Now we can load the NaBL language into Spoofax Core.
Spoofax Core uses `Apache VFS <https://commons.apache.org/proper/commons-vfs/>`_ as a file system abstraction, to be able to interact with different file systems.
This means we must first get a :java_ref:`~org.apache.commons.vfs2.FileObject` (Apache VFS counterpart of :java_ref:`~java.io.File`) that points to the NaBL language file we downloaded earlier.
First get a URL to the NaBL language file which is on the classpath::

  URL nablUrl = Main.class.getClassLoader().getResource(
    "org.metaborg.meta.lang.nabl-2.0.0.spoofax-language");

Then we resolve that to a FileObject, which points to the contents of the NaBL language implementation archive (which is actually a regular Zip file)::

  FileObject nablLocation = spoofax.resourceService.resolve("zip:" + nablUrl + "!/");

The :java_ref:`org.metaborg.core.resource.IResourceService` class is a service in Spoofax Core that provides functionality to retrieve FileObjects.
In this case, we resolve to the contents inside the zip file.
The ``zip:`` part indicates that we're using the `zip file system <https://commons.apache.org/proper/commons-vfs/filesystems.html#Zip_Jar_and_Tar>`_, and the ``!/`` part indicates that we refer to the root path **inside** the zip file.

Spoofax Core has many services that provide small pieces of functionality.
The :java_ref:`org.metaborg.core.language.ILanguageDiscoveryService` class is a service that discovers and loads languages, which we will use now to load the NaBL language::

  Iterable<ILanguageDiscoveryRequest> requests =
    spoofax.languageDiscoveryService.request(nablLocation);
  Iterable<ILanguageComponent> components =
    spoofax.languageDiscoveryService.discover(requests);

Since multiple languages can be requested from a single location, and multiple language components can be discovered from a single file, both methods return multiple values.
However, we know that the NaBL language file only contains one language implementation, we can retrieve it with a couple of utility methods::

  Set<ILanguageImpl> implementations = LanguageUtils.toImpls(components);
  ILanguageImpl nabl = LanguageUtils.active(implementations);

  if(nabl == null) {
      System.out.println("No language implementation was found");
      return;
  }
  System.out.println("Loaded " + nabl);

Run the program by selecting :menuselection:`Run -> Debug As -> Java Application`.
If all went well, ``Loaded language impl. org.metaborg:org.metaborg.meta.lang.nabl:2.0.0`` should appear in the log output.

^^^^^^^^^^^^^^
Parsing a file
^^^^^^^^^^^^^^

Now that the NaBL language is loaded into Spoofax Core, we can parse NaBL programs.

Right click :file:`src/main/resources` and select :menuselection:`New -> File`, name the file :file:`test.nabl` and press :guilabel:`Finish`.
Open the file and fill it with the following content:

.. code-block:: nabl

   module test

   namespaces Test1 Test2

To parse a file, we must first create a :java_ref:`org.metaborg.spoofax.core.unit.ISpoofaxInputUnit` which contains all information required to parse a file::

  FileObject nablFile = spoofax.resourceService.resolve("res:test.nabl");
  String nablContents = spoofax.sourceTextService.text(nablFile);
  ISpoofaxInputUnit input = spoofax.unitService.inputUnit(nablFile, nablContents, nabl, null);

The `res file system <https://commons.apache.org/proper/commons-vfs/filesystems.html#res>`_ can be used to resolve files on the classpath.
The catch clause must also be extended with :java_ref:`~java.io.IOException` to handle the case where the text for the NaBL file cannot be retrieved::

  } catch(MetaborgException | IOException e) {
      e.printStackTrace();
  }

Then we pass the input to the :java_ref:`org.metaborg.core.syntax.ISyntaxService` for parsing::

  ISpoofaxParseUnit output = spoofax.syntaxService.parse(input);
  if(!output.valid()) {
      System.out.println("Could not parse " + nablFile);
      return;
  }
  System.out.println("Parsed: " + output.ast());

Run the program, ``Parsed: Module("test",[Namespaces([NamespaceDef("Test1"),NamespaceDef("Test2")])])`` should appear in the log output.
Now you can optionally experiment a bit by making an error in the program, and printing the error messages from the oput.

---------------
How to proceed?
---------------

.. todo:: We are currently in the process of writing documentation, this section will be updated once we have more material.

The following manuals describe parts of the Spoofax Core API:

- :doc:`manual/service` - full list of available services in the Spoofax Core API
- :doc:`manual/extend` - how to extend Spoofax Core
