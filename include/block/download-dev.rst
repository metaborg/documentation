Eclipse plugin
~~~~~~~~~~~~~~

Premade Eclipse installations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

With embedded JRE:

.. include:: /include/block/download-dev-eclipse-jre.rst

Without embedded JRE:

.. include:: /include/block/download-dev-eclipse.rst

Update site
^^^^^^^^^^^

-  Eclipse update site: |dev-eclipse-update-site|

IntelliJ plugin
~~~~~~~~~~~~~~~

-  IntelliJ update site: |dev-intellij-update-site|
-  `IntelliJ update site archive <dev-intellij-update-site-archive_>`_

Command-line utilities
~~~~~~~~~~~~~~~~~~~~~~

-  `Sunshine JAR <dev-sunshine-jar_>`_
-  `SPT testrunner JAR <dev-spt-testrunner-jar_>`_

Core API
~~~~~~~~

-  `Spoofax Core uber JAR <dev-spoofax-core-uber-jar_>`_
-  Spoofax Core uber Maven artifact: |dev-spoofax-core-uber-maven-artifact|

StrategoXT
~~~~~~~~~~

-  `StrategoXT distribution <dev-strategoxt-distrib_>`_
-  `StrategoXT JAR <dev-strategoxt-jar_>`_

Maven artifacts
~~~~~~~~~~~~~~~

Maven artifacts can be found on our `artifact server <artifact-server-snapshots_>`_.
The Maven version used for this release is |dev-version|.
See the instructions on :ref:`using MetaBorg Maven artifacts <dev-maven>` for more information.

Build farm
~~~~~~~~~~

Our build server builds Spoofax whenever a commit to master is made, in the `metaborg/spoofax/master <buildfarm-server-spoofax-master_>`_ build job.
The latest successfully built artifacts from that job are stored `here <buildfarm-server-spoofax-master-artifacts_>`_.
