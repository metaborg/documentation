.. _concurrent-migration:

==================================
Migrating to the Concurrent Solver
==================================

.. role:: statix(code)
   :language: statix
   :class: highlight

Enabling the concurrent solver
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In order to enable the concurrent solver, either one of the following approaches
can be taken.

For a Language
--------------

To enable the concurrent solver for a language, set the ``language.statix.concurrent``
property in the ``metaborg.yaml`` file to ``true``. This ensures that the
concurrent solver is used for all sources in the language.

*Example*

.. code-block:: yaml

   id: org.example:mylang:0.1.0-SNAPSHOT
   name: mylang
   language:
     statix:
       concurrent: true

For an example Project
----------------------

To enable the concurrent solver for a particular project only, set the
``runtime.statix.concurrent`` property in the ``metaborg.yaml`` file to a list
that contains all names of the languages for which you want to use the
concurrent solver. The name of the language should correspond to the ``name``
property in the ``metaborg.yaml`` of the language definition project.

*Example*

.. code-block:: yaml

   id: org.example:mylang.example:0.1.0-SNAPSHOT
   runtime:
     statix:
       concurrent:
       - mylang

.. warning::

   Please be aware that changes in the ``metaborg.yaml`` file may require a
   restart of Eclipse.

.. note::

   The concurrent solver can only be used in ``multifile`` mode.


Using new solver features
^^^^^^^^^^^^^^^^^^^^^^^^^

The concurrent solver also comes with some new features that were not present in
the traditional solver. This sections explains these features, and shows how to
use them.

Grouping
--------

.. warning::

	 Not yet written

Libraries
---------

.. warning::

	 Not yet written
