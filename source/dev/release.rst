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
   b. **Update it to the latest commit with** ``git pull --rebase && ./b checkout -y && ./b update``.
   c. Run ``./b set-remote -s`` to set submodule remotes to SSH URLs, enabling git pushing without having to supply a username and password via git over HTTPS.

3. Prepare the source code repository.

   a. Make a separate clone (or re-use an existing one if you have released Spoofax before) of the ``spoofax-release`` branch of `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_. This must be a separate clone in a different directory from the first one. See :ref:`Cloning the source code <dev-build-clone>`.

     .. note:: The reason for two separate clones of `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ is that the release script will modify the files in the repository, which could include files of the release script itself. Therefore, we make a separate clone which the release script acts upon, so that it does not interfere with itself.

   b. **If reusing an existing clone, ensure that it is checked out to** ``spoofax-release``, **and update it to the latest commit with** ``git pull --rebase && ./b checkout -y && ./b update``.
   c. **If there are new submodules repositories, follow the steps for preparing new submodules below**.
   d. Run ``./b set-remote -s`` to set submodule remotes to SSH URLs, enabling git pushing without having to supply a username and password via git over HTTPS.

.. highlight:: bash

4. Perform the release.

   a. Change directory into the repository cloned in step 2. For example::

        cd /Users/gohla/spoofax/master/spoofax-releng

   b. Get an absolute path to the repository cloned in step 3. For example: ``/Users/gohla/spoofax/release/spoofax-releng``
   c. Determine whether the release will be *patch* or *minor*/*major*. For a patch release, we do not bump the development version. For a minor or major release, we do.
   d. Figure out what the *current development version* of Spoofax is, what the *next release version* should be, and if doing a non-patch release, what the *next development version* should be. The release script will change the current development version into the next release version, deploy that, and then change the current development version to the next development version, and commit that. Setting the next development version is optional.
   e. Execute the release script with the parameters you gathered::

        ./b --repo <release-repository> release \
          spoofax-release <release-version> \
          master <current-development-version> \
          --non-interactive \
          --maven-deploy \
          --maven-deploy-identifier metaborg-nexus \
          --maven-deploy-url http://artifacts.metaborg.org/content/repositories/releases/ \
          --nexus-deploy \
          --nexus-username <artifact-server-username> \
          --nexus-password <artifact-server-password> \
          --nexus-repo releases

     or for a major version, with ``--next-develop-version``::

        ./b --repo <release-repository> release \
          spoofax-release <release-version> \
          master <current-development-version> \
          --next-develop-version <next-development-version> \
          --non-interactive \
          --maven-deploy \
          --maven-deploy-identifier metaborg-nexus \
          --maven-deploy-url http://artifacts.metaborg.org/content/repositories/releases/ \
          --nexus-deploy \
          --nexus-username <artifact-server-username> \
          --nexus-password <artifact-server-password> \
          --nexus-repo releases

     For example, if we currently are at development version ``2.3.0-SNAPSHOT``, and would like to release minor version ``2.3.0``, and update the development version to ``2.4.0-SNAPSHOT``, we would execute the following command::

        cd /Users/gohla/spoofax/master/spoofax-releng
        ./b --repo /Users/gohla/spoofax/release/spoofax-releng release \
          spoofax-release 2.3.0 \
          master 2.3.0-SNAPSHOT \
          --next-develop-version 2.4.0-SNAPSHOT \
          --non-interactive \
          --maven-deploy \
          --maven-deploy-identifier metaborg-nexus \
          --maven-deploy-url http://artifacts.metaborg.org/content/repositories/releases/ \
          --nexus-deploy \
          --nexus-username myusername \
          --nexus-password mypassword \
          --nexus-repo releases

     Unfortunately, it is currently not possible to encrypt the artifact server password passed to the build script.

New spoofax-releng submodules
-----------------------------

When adding a new submodule to the `spoofax-releng <https://github.com/metaborg/spoofax-releng>`_ repository, the following steps must be performed before starting the automated release process:

* Add a ``spoofax-release`` branch to the submodule (pointing to the current ``master`` branch), and push that branch.
* Add the submodule to the :file:`.gitmodule` file in the ``spoofax-release`` branch of the ``spoofax-releng`` repository. Make sure that the branch of the submodule is set to ``spoofax-release``, and that the remote is using a ``https`` URL. Commit and push this change.

Updating the release archive
----------------------------

To update the release archive of this documentation site, perform the following steps after a release:

* Update include files:

  * Copy :file:`include/hyperlink/download-<current-release-version>.rst` to new file :file:`include/hyperlink/download-<release-version>.rst`, replace all instances of ``<current-release-version>`` in that new file with ``<release-version>``, and update the date to the current date.
  * In :file:`include/hyperlink/download-rel.rst`, replace all instances of ``<current-release-version>`` with ``<release-version>``.
  * In :file:`include/hyperlink/download-dev.rst`, update the development version to ``<next-development-version>``.
  * In :file:`include/_all.rst`, add a new line to include the newly copied file: ``.. include:: /include/hyperlink/download-<release-version>.rst``.

* Update :file:`source/release/migrate/<release-version>.rst` (only if migrations are necessary):

  * Remove stub notice.

* Update :file:`source/release/note/<release-version>.rst`:

  * Remove stub notice.
  * Add small summary of the release as an introduction.
  * Include download links, which can be copied and have their versions replaced from a previous release.

* Create new stub files for the next release:

  * Create a new migration guide stub file.
  * Create a new release notes stub file.

* Update :file:`source/release/note/index.rst`:

  * Move stub for this release to the top of the notes.
  * Add new stub file at the bottom of the notes.

* Update :file:`source/release/migrate/index.rst`:

  * Move stub for this release to the top of the migration guides.
  * Add new stub file at the bottom of the migration guides.

* Update :file:`conf.py`:

  * Update ``version`` variable.
  * Update ``copyright`` variable with new year, if needed.
