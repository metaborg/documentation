# Spoofax development versions

These notes provide the download links for the various artifacts of the latest development version.
The development version of Spoofax is not rigorously tested, use at your own risk!

## Eclipse plugin

### Premade Eclipse installations

With embedded JRE:

* [Windows 32-bits, embedded JRE](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-win32-x86-jre.zip)
* [Windows 64-bits, embedded JRE](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-win32-x64-jre.zip)
* [Linux 32-bits, embedded JRE](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-linux-x86-jre.tar.gz)
* [Linux 64-bits, embedded JRE](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-linux-x64-jre.tar.gz)
* [Mac OS X (Intel only), embedded JRE](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-macosx-x64-jre.tar.gz)

Without embedded JRE:

* [Windows 32-bits](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-win32-x86.zip)
* [Windows 64-bits](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-win32-x64.zip)
* [Linux 32-bits](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-linux-x86.tar.gz)
* [Linux 64-bits](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-linux-x64.tar.gz)
* [Mac OS X (Intel only)](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/spoofax-macosx-x64.tar.gz)

### Update site

* Eclipse update site: `http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/eclipse/site/`

## IntelliJ plugin

* IntelliJ update site: `http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/dist/spoofax/intellij/plugin.zip`

## JAR files

* [Sunshine JAR](http://artifacts.metaborg.org/service/local/artifact/maven/redirect?r=snapshots&g=org.metaborg&a=org.metaborg.sunshine2&v=LATEST)
* [SPT testrunner JAR](http://artifacts.metaborg.org/service/local/artifact/maven/redirect?r=snapshots&g=org.metaborg&a=org.metaborg.spt.cmd&v=LATEST)

## Stratego/XT

* [Distribution](http://artifacts.metaborg.org/service/local/artifact/maven/redirect?r=snapshots&g=org.metaborg&a=strategoxt-distrib&c=bin&p=tar&v=LATEST)
* [JAR](http://artifacts.metaborg.org/service/local/artifact/maven/redirect?r=snapshots&g=org.metaborg&a=strategoxt-jar&v=LATEST)

## Maven artifacts

Maven artifacts can be found on our [artifact server](http://artifacts.metaborg.org/content/repositories/snapshots/org/metaborg/).
The Maven version used for these snapshots is `2.1.0-SNAPSHOT`.
See the instructions on [using MetaBorg Maven artifacts](../../dev/maven.md) for more information.

## Build farm

Our build server builds Spoofax whenever a commit to master is made, in the [metaborg/spoofax-releng/master](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/) build job.
The latest successfully built artifacts are [stored here](http://buildfarm.metaborg.org/job/metaborg/job/spoofax-releng/job/master/lastSuccessfulBuild/artifact/).
