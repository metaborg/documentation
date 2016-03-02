# Building Spoofax for IntelliJ IDEA
We did our best to make building the Spoofax plugin for IntelliJ IDEA as easy and painless as
possible.


## Building
To build the IntelliJ IDEA Spoofax plugin locally, you first need to get the
source [from GitHub][1]. Choose one of the branches:

* [`master` branch][2]: stable build of current release. ([ZIP][4])
* [`develop` branch][3]: unstable build for next release. ([ZIP][5])

Either clone the repository locally or download and extract the ZIP archive.

Next you need to invoke Gradle to build the project. Simply execute the following command
from the main project's root folder (that is `org.metaborg.intellij/`):

```
./gradlew clean build
```
(On Windows simply `gradlew clean build`.)

Alternatively, you can import the project in IntelliJ and build it from there.



## Running
To run the built plugin inside a special sandbox-instance of IntelliJ IDEA, execute the following
command:

```
./gradlew runIdea
```

Alternatively, in IntelliJ IDEA you can invoke the _IntelliJ Plugin_ run/debug configuration. You
can use this to run or debug the IntelliJ IDEA plugin code. However, this cannot be used to debug
the JPS Spoofax build process.



## Debugging JPS
To debug the JPS Spoofax build process, you need to execute the following command:

```
./gradlew debugJps
```

or invoke the _IntelliJ Plugin (Debug JPS)_ run configuration (_not debug_) from IntelliJ.

Then from the sandbox IntelliJ IDEA instance you start a build. IntelliJ will wait for a debugger
to be attached to port 5005. Attach a debugger, and the build will continue. From the Spoofax
plugin's IntelliJ IDEA project, you can invoke the _JPS Plugin_ debug configuration to attach the
debugger.








[1]: https://github.com/metaborg/spoofax-intellij
[2]: https://github.com/metaborg/spoofax-intellij/tree/master
[3]: https://github.com/metaborg/spoofax-intellij/tree/develop
[4]: https://github.com/metaborg/spoofax-intellij/archive/master.zip
[5]: https://github.com/metaborg/spoofax-intellij/archive/develop.zip
