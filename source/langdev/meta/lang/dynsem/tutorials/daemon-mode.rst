==================================
Run an interpreter as a **daemon**
==================================

Interpreters derived from DynSem specifications can be run as daemons. They run as a background process which accepts client requests for program evaluation. Running interpreters in the background significantly reduces the startup time of the interpreter.

~~~~~~~~~~~~~
Requirements
~~~~~~~~~~~~~

The daemon mode uses `Nailgun for Java <http://www.martiansoftware.com/nailgun/>`_ to launch background processes and make requests. On OS X you can install Nailgun using `Homebrew <https://brew.sh>`_:

.. code-block:: bash

  brew install nailgun

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Launching an interpreter daemon
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you have enabled generation of the interpreter project in *dynsem.properties*:

.. code-block:: jproperties

  project.create = true

upon generation of an interpreter three files will be generated in the root of the interpreter project. Assuming your language is named **simpl** these files will be:

- *simpl-server*
- *simpl-client*
- *simpl (Daemon).launch*

Launch an interpreter daemon by running the *simpl-server* shell script or by launching the *simpl (Daemon)* launch configuration from Eclipse. To quit the daemon simply quit the process or run the stop command from a shell:

.. code-block:: bash

  ng ng-stop

To evaluate a program you can either use the *simpl-client*:

.. code-block:: bash

  ./simpl-client yourprogram.smpl

or invoke the *ng* command:

.. code-block:: bash

  ng simpl yourprogram.smpl

.. warning:: Nailgun daemon are not secure. For more information see the `Nailgun website <http://www.martiansoftware.com/nailgun/>`_
