# Developing Spoofax

If you are developing a project that is included in Spoofax it is recommended to set up a development environment.
This section describes how to set up such a development environment.

## Requirements

1. A working **Spoofax build** is required before being able to develop. Follow the [Building Spoofax](build.md) guide for instructions on how to build Spoofax.

## Eclipse

Currently, an Eclipse development environment is the most supported environment.

### Generating an Eclipse instance

The `b` script in the <span class='file'>spoofax-releng</span> repository can generate an Eclipse installation for you.
Change directory into the <span class='file'>spoofax-releng</span> repository and run:

```bash
./b gen-dev-spoofax -d ~/eclipse/spoofax-dev
```

This will download and install Eclipse into <span class='file'>~/eclipse/spoofax-dev</span> with the right plugins and <span class='file'>eclipse.ini</span> for Spoofax development. The latest nightly version of the Spoofax plugin will be installed into that Eclipse. If you would like to install your locally built Spoofax plugin instead, pass the `-l` flag:

```bash
./b gen-dev-spoofax -l -d ~/eclipse/spoofax-dev
```

Generating an Eclipse installation can take several minutes. After it's done generating, open the Eclipse installation and confirm that it works by creating a Spoofax entity project.

### Fixing Eclipse settings

Some Eclipse settings unfortunately have sub-optimal defaults. Go to the Eclipse preferences and set these options:

* <span class='menuselection'>General</span>
	* Enable: <span class='guilabel'>Keep next/previous editor, view and perspectives dialog open</span>
* <span class='menuselection'>General ‣ Startup and Shutdown</span>
	* Enable: <span class='guilabel'>Refresh workspace on startup</span>
* <span class='menuselection'>General ‣ Workspace</span>
	* Enable: <span class='guilabel'>Refresh using native hooks or polling</span>
* <span class='menuselection'>Maven</span>
	* Enable: <span class='guilabel'>Do not automatically update dependencies from remote repositories</span>
	* Enable: <span class='guilabel'>Download Artifact Sources</span>
	* Enable: <span class='guilabel'>Download Artifact JavaDoc</span>
* <span class='menuselection'>Maven ‣ User Interface</span>
  * Enable: <span class='guilabel'>Open XML page in the POM editor by default</span>
* <span class='menuselection'>Run/Debug ‣ Launching</span>
	* Disable: <span class='guilabel'>Build (if required) before launching</span>

### Developing

Import the projects you'd like to develop.
To import Java and language projects, use <span class='menuselection'>Import ‣ Maven ‣ Existing Maven Projects</span>.
Eclipse plugins are still imported with <span class='menuselection'>Import ‣ General ‣ Existing Projects into Workspace</span>.

### Running

To test your changes in the Spoofax Eclipse plugin, import the `org.metaborg.spoofax.eclipse` project from the `spoofax-eclipse` repository, which provides launch configurations for starting new Eclipse instances. Press the little down arrow next to the bug icon (next to the play icon) and choose `Spoofax with core (all plug-ins)` to start a new Eclipse instance that contains your changes.

Some gotcha's:

* When starting a new Eclipse instance using `Spoofax with core (all plug-ins)`, Eclipse might report problems about `org.eclipse.jdt.annotation`, `org.metaborg.meta.lang.spt.testrunner.cmd`, and `org.metaborg.meta.lang.spt.testrunner.core`. These problems can be ignored.
* If you change a language and want to test it in a new Eclipse instance, import that language's corresponding Eclipse plugin project. For example, `org.metaborg.meta.lang.nabl` has Eclipse plugin project `org.metaborg.meta.lang.nabl.eclipse`. Then compile both those projects from the command-line (don't forget to turn off build automatically in Eclipse), and start a new Eclipse instance.

### Troubleshooting

If there are many errors in a project, try updating the Maven project.
Right click the project and choose <span class='menuselection'>Maven -> Update Project...</span>, uncheck <span class='guilabel'>Clean projects</span> in the new dialog and press OK.
This will update the project from the POM file, update any dependencies, and trigger a build.
If this does not solve the problems, try it again but this time with <span class='guilabel'>Clean projects</span> checked.
Note that if you clean a language project, it has to be rebuilt from the command-line. Restarting Eclipse and repeating these steps may also help.

Multiple projects can be updated by selecting multiple projects in the package/project explorer, or by checking projects in the update dialog.

### Advanced: developing from scratch

In some cases it can be beneficial to have full control over all projects, instead of relying on Maven artifacts and the installed Spoofax plugin.
Only follow this approach if you know what you are doing!
To develop from scratch, uninstall Spoofax from Eclipse, and import all projects from `spoofax-releng` into the workspace.

If you change a language project, build them on the command-line, because languages cannot be built inside Eclipse without the Spoofax plugin.

## IntelliJ

To run the built plugin inside a special sandbox-instance of IntelliJ IDEA, execute the following command:

```
./gradlew runIdea
```

Alternatively, in IntelliJ IDEA you can invoke the _IntelliJ Plugin_ run/debug configuration.
You can use this to run or debug the IntelliJ IDEA plugin code.
However, this cannot be used to debug the JPS Spoofax build process.

To debug the JPS Spoofax build process, you need to execute the following command:

```
./gradlew debugJps
```

or invoke the _IntelliJ Plugin (Debug JPS)_ run configuration (_not debug_) from IntelliJ.

Then from the sandbox IntelliJ IDEA instance you start a build. IntelliJ will wait for a debugger to be attached to port 5005.
Attach a debugger, and the build will continue.
From the Spoofax plugin's IntelliJ IDEA project, you can invoke the _JPS Plugin_ debug configuration to attach the
debugger.

### Logging
To get debug logging in IntelliJ, locate the `bin/log.xml` file in the IntelliJ folder and add the following snippet in the `<log4j:configuration>` element, just above the `<root>` element:

```
<category name="#org.metaborg" additivity="true">
  <priority value="DEBUG"/>
  <appender-ref ref="CONSOLE-DEBUG"/>
  <appender-ref ref="FILE"/>
</category>
```
