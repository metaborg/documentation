# Continuous Integration

This page describes how to build Spoofax languages on a Jenkins buildfarm or using an alternative platform such as GitHub Actions.

Full continuous integration includes:

* Building the language on the buildfarm
* Running SPT tests as part of the build
* Publishing an eclipse updatesite for the language
* Doing the above on every commit, and on every spoofax-master update

Setting up continuous integration is a two step process.
The first step is to setup a local maven build for building the language, running the tests and creating an update site.
The second step is configuring Jenkins to perform these maven builds and publish the artifacts.

## Local Maven Build

Follow the [guide for getting a local Maven build](maven.md) going first.

## Build on Jenkins
(Note: can be skipped in GitHub organizations MetaBorg and MetaBorgCube)

`New Item` > enter a name and choose `Multibranch Pipeline`

Add the git repo `Branch Sources` > `Add source` > `Git`. Fill in project repository such as `https://github.com/MetaBorgCube/metaborg-entity.git`, select credentials, and save.

You should now get a message saying that the repository has branch but does not meet the criteria, as the `Jenkinsfile` is not setup yet.

## Jenkins configuration

Create the file `Jenkinsfile` in the root of the repository containing (be sure to update the update site path, and to change the slack integration channel or comment out the slack integration):

```groovy
properties([
  pipelineTriggers([
    upstream(
      threshold: hudson.model.Result.SUCCESS,
      upstreamProjects: '/metaborg/spoofax-releng/master' // build this project after Spoofax-master is built
    )
  ]),
  buildDiscarder(logRotator(artifactNumToKeepStr: '3')),
  disableConcurrentBuilds() //disableds parallel builds
])

node{
  try{
    notifyBuild('Started')

    stage('Checkout') {
      checkout scm
      sh "git clean -fXd"
    }

    stage('Build and Test') {
      withMaven(
        //mavenLocalRepo: "${env.JENKINS_HOME}/m2repos/${env.EXECUTOR_NUMBER}", //https://yellowgrass.org/issue/SpoofaxWithCore/173
        mavenLocalRepo: ".repository",
        mavenOpts: '-Xmx1G -Xms1G -Xss16m'
      ){
        sh 'mvn -B -U clean verify -DforceContextQualifier=\$(date +%Y%m%d%H%M)'
      }
    }

    stage('Archive') {
      archiveArtifacts(
        artifacts: 'yourlanguagename.eclipse.site/target/site/',
        excludes: null,
        onlyIfSuccessful: true
      )
    }

    stage('Cleanup') {
      sh "git clean -fXd"
    }

    notifyBuild('Succeeded')

  } catch (e) {

    notifyBuild('Failed')
    throw e

  }
}

def notifyBuild(String buildStatus) {
  def message = """${buildStatus}: ${env.JOB_NAME} [${env.BUILD_NUMBER}] ${env.BUILD_URL}"""

  if (buildStatus == 'Succeeded') {
    color = 'good'
  } else if (buildStatus == 'Failed') {
    color = 'danger'
  } else {
    color = '#4183C4' // Slack blue
  }

  slackSend (color: color, message: message, channel: '#some-slack-channel')
}
```

Go to the Jenkins project > `Branch Indexing` > `Run now`. This should trigger the build of the master branch.

## Trigger Jenkins on commit
(Note: can be skipped in GitHub organizations MetaBorg and MetaBorgCube)

In order to trigger Jenkins to build on every commit we need to install a GitHub service.
In the GitHub repository go to `Settings` > `Integrations & services` > `Add service` > `Jenkins (Git plugin)` (not GitHub plugin) and provide the jenkins url (for example https://buildfarm.metaborg.org/ )

## Build badge on GitHub
For a GitHub build-badge add the following the the readme file:

```
[![Build status](https://buildfarm.metaborg.org/job/Entity/job/master/badge/icon)](https://buildfarm.metaborg.org/job/Entity/job/master/)
```

TODO: figure out how to use `Promoted Builds` to promote spoofax-master only if language build succeeds.

## CI using GitHub Actions

Using GitHub [Actions](https://github.com/features/actions) is an alternative to Jenkins for setting up CI using Maven.
Enable it by adding the file `.github/workflows/ci.yml` to your repository with the following contents:

```yaml
name: CI

on: [push]

jobs:
  build:

    runs-on: ubuntu-latest
    container: maven:3.5.4-jdk-8

    steps:
    - uses: actions/checkout@v2
    - name: Maven build
      run: mvn clean verify
```

This configures your repository with a `CI` workflow that runs the build on every push.
Publishing the language is not included in this configuration.

See the [Spoofax definition of MiniZinc](https://github.com/MetaBorgCube/metaborg-minizinc) for an example ([config](https://github.com/MetaBorgCube/metaborg-minizinc/blob/master/.github/workflows/ci.yml) and [actions](https://github.com/MetaBorgCube/metaborg-minizinc/actions)).

Similar to Jenkins, you can add a build status badge by adding the following to the readme file:

```
![Build status](https://github.com/namespace/project/workflows/CI/badge.svg)
```
