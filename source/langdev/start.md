# Language Development Getting Started

This guide will get you started with language development in Spoofax, within an Eclipse environment.

## Requirements

Spoofax runs on the major operating systems:

* Windows (32 and 64 bits)
* Linux (32 and 64 bits)
* Mac OSX (Intel only)

Spoofax requires a working internet connection to download several libraries when it is first started.
These libraries are cached afterwards, and only need to be re-downloaded when you update Spoofax.

## Installation

To get started with Spoofax, download an Eclipse Mars installation with Spoofax preinstalled for your platform:

* [Windows 32-bits, embedded JRE](hhttp://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-win32-x86-jre.zip)
* [Windows 64-bits, embedded JRE](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-win32-x86_64-jre.zip)
* [Linux 32-bits, embedded JRE](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-linux-x86-jre.tar.gz)
* [Linux 64-bits, embedded JRE](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-linux-x86_64-jre.tar.gz)
* [Mac OS X (Intel only), embedded JRE](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-macosx-x86_64-jre.tar.gz)

These are bundled with an embedded Java Runtime Environment (JRE) version 7, such that a JRE on your system is not required.
If your system has a JRE of version 7 or higher installed, and would rather use that, use the following download links instead:

* [Windows 32-bits](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-win32-x86.zip)
* [Windows 64-bits](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-win32-x86_64.zip)
* [Linux 32-bits](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-linux-x86.tar.gz)
* [Linux 64-bits](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-linux-x86_64.tar.gz)
* [Mac OS X (Intel only)](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/eclipse/spoofax-macosx-x86_64.tar.gz)

Unpack the downloaded archive to a location with write access, since Eclipse requires write access to the unpacked Eclipse installation.

```eval_rst
.. warning:: On Windows, do **not** unpack the Eclipse installation into :file:`Program Files`, because no write access is granted there, breaking both Eclipse and Spoofax.
```

Start up Eclipse, depending on your operating system:

* Windows: open <span class='file'>eclipse.exe</span>
* Linux: open <span class='file'>eclipse</span>
* Mac OSX: open <span class='file'>Eclipse.app</span>. If that doesn't work, right click <span class='file'>Eclipse.app</span> and choose <span class='guilabel'>Open</span> to grant permissions to open Eclipse.

## Hello World Language

```eval_rst
.. todo:: This part of the documentation has not been written yet.
```

create a new Spoofax project; fill in names

build the project to confirm things are working

add hello world syntax

build project again; project must be built manually to test changes

create test file and open

type test program

show AST to confirm things are working

make syntactic error, confirm error shows up

done!

## How to proceed?

```eval_rst
.. todo:: This part of the documentation has not been written yet.
```

guides (declare your language, updating Spoofax, IntelliJ getting started, etc.)

manual

meta-languages and libraries manual

examples
