# Continuous Integration

This page describes how build Spoofax langauges on a Jenkins buildfarm.

Full continous integration includes:

* Building the language on the buildfarm
* Running SPT tests as part of the build
* Publishing an eclipse updatesite for the language
* Doing the above on every commit, and on every spoofax-master update

Setting up continues integration is a two step process.
The first step is to setup a local maven build for building the language, running the tests and creating an update site.
The second step is configuring Jenkins to perform these maven builds and publish the artifacts.

## Local Maven Build

<!-- TODO -->

## Build on Jenkins

<!-- TODO -->
