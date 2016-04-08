# Spoofax nightly

These notes provide the download links for the various artifacts of the latest nightly version.

## Eclipse plugin

### Premade Eclipse installations

With embedded JRE:

* [Windows 32-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-win32-x86-jre.zip)
* [Windows 64-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-win32-x86_64-jre.zip)
* [Linux 32-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-linux-x86-jre.tar.gz)
* [Linux 64-bits, embedded JRE](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-linux-x86_64-jre.tar.gz)
* [Mac OS X (Intel only), embedded JRE](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-macosx-x86_64-jre.tar.gz)

Without embedded JRE:

* [Windows 32-bits](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-win32-x86.zip)
* [Windows 64-bits](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-win32-x86_64.zip)
* [Linux 32-bits](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-linux-x86.tar.gz)
* [Linux 64-bits](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-linux-x86_64.tar.gz)
* [Mac OS X (Intel only)](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-2.0.0-beta1-macosx-x86_64.tar.gz)

### Update site

* Eclipse update site: `http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/site`
* [Eclipse update site archive](http://download.spoofax.org/update/release/2.0.0-beta1/eclipse/spoofax-updatesite-2.0.0-beta1.zip)

## JAR files

* [Sunshine JAR](http://download.spoofax.org/update/release/2.0.0-beta1/spoofax-sunshine-2.0.0-beta1.jar)
* [SPT testrunner JAR](http://download.spoofax.org/update/release/2.0.0-beta1/spoofax-testrunner-2.0.0-beta1.jar)

## Maven artifacts

Maven artifacts can be found on our [artifact server](http://artifacts.metaborg.org/content/repositories/releases/org/metaborg/).
The Maven version used for this release is `2.0.0-SNAPSHOT`.
See the instructions on [using MetaBorg Maven artifacts](../../dev/maven.md) for more information.

## Build farm

Our build server builds Spoofax whenever a commit to master is made, in the [spoofax-master](http://buildfarm.metaborg.org/job/spoofax-master/) build job.
The latest successfully built artifacts are [stored here](http://buildfarm.metaborg.org/job/spoofax-master/lastSuccessfulBuild/artifact/dist/).
