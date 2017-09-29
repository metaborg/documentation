=================
Releasing Spoofax
=================

This section describes how to release Spoofax.

Requirements
------------

To release Spoofax, you must first be able to build Spoofax. Follow the :ref:`Maven <dev-build>` and :ref:`Building <dev-maven>` guides first.

To publish releases, you will need write access to the `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ repository, to all submodule repositories in that repository, and to this documentation repository. An account with deploy access to our `artifact server <http://artifacts.metaborg.org/>`_ is required. Ask an administrator of the Programming Languages group to get access to the repositories and artifact server.

Instructions
------------

.. highlight:: xml

1. Prepare Maven deploy settings.

   a. Open your :file:`~/.m2/settings.xml` file.
   b. Add a ``<servers></servers>`` section if it does not exist.
   c. Add a server to the ``servers`` section with id ``metaborg-nexus`` that contains your username and password to our artifact server::

        <server>
          <id>metaborg-nexus</id>
          <username>myusername</username>
          <password>mypassword</password>
        </server>

   d. Optionally encrypt your password by following the `Password Encryption guide <https://maven.apache.org/guides/mini/guide-encryption.html>`_.

2. Prepare the repository containing the build scripts.

   a. Clone or re-use an existing clone of `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ on the ``master`` branch. See :ref:`Cloning the source code <dev-build-clone>`.
   b. Update it to the latest master with ``git pull --rebase && ./b checkout -y && ./b update``.

3. Prepare the source code repository.

   a. Make a separate clone (or re-use an existing one if you have released Spoofax before) of the ``spoofax-release`` branch of `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_. This must be a separate clone in a different directory from the first one. See :ref:`Cloning the source code <dev-build-clone>`.

     .. note:: The reason for two separate clones of `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ is that the release script will modify the files in the repository, which could include files of the release script itself. Therefore, we make a separate clone which the release script acts upon, so that it does not interfere with itself.

.. highlight:: bash

4. Perform the release.

   a. Change directory into the repository cloned in step 2. For example::

        cd /Users/gohla/spoofax/master/spoofax-releng

   b. Get an absolute path to the repository cloned in step 3. For example: ``/Users/gohla/spoofax/release/spoofax-releng``
   c. Figure out what the current development version of Spoofax is, what the next release version should be, and what the next development version should be. The release script will change the current development version into the next release version, deploy that, and then change the current development version to the next development version, and commit that.
   d. Execute the release script with the parameters you gathered::

        ./bd --repo <release-repository> release \
          spoofax-release <release-version> \
          master <current-development-version> \
          --next-develop-version <next-development-version> \
          --non-interactive \
          --maven-deploy --maven-deploy-identifier metaborg-nexus --maven-deploy-url http://artifacts.metaborg.org/content/repositories/releases/ \
          --nexus-deploy --nexus-username <artifact-server-username> --nexus-password <artifact-server-password> --nexus-repo releases

      For example, if we currently are at development version ``2.3.0-SNAPSHOT``, and would like to release ``2.3.0``, and update the development version to ``2.4.0-SNAPSHOT``, we would execute the following command::

        cd /Users/gohla/spoofax/master/spoofax-releng
        ./bd --repo /Users/gohla/spoofax/release/spoofax-releng release \
          spoofax-release 2.3.0 \
          master 2.3.0-SNAPSHOT \
          --next-develop-version 2.4.0-SNAPSHOT \
          --non-interactive \
          --maven-deploy --maven-deploy-identifier metaborg-nexus --maven-deploy-url http://artifacts.metaborg.org/content/repositories/releases/ \
          --nexus-deploy --nexus-username myusername --nexus-password mypassword --nexus-repo releases

      Unfortunately, it is currently not possible to encrypt the artifact server password passed to the build script.
