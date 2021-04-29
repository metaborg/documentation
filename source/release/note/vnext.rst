=============
Spoofax vNext
=============

These are the release notes for Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------
* On macOS, Spoofax temporarily requires `Docker <https://docs.docker.com/docker-for-mac/install/>`_
  and ``coreutils`` when building Spoofax on macOS Catalina, Big Sur, or newer.

SDF3
~~~~~~

* Fixed tree indexes in layout constraints/declarations to make them 0-based.

Statix
~~~~~~

* Fixed origin tracking in Statix injection explication for new projects
  that caused the top-level term of an AST to be missing
  when a Stratego strategy is applied to an analyzed AST in an SPT test.
* Add a menu action to view the scope graph resulting from Statix analysis.
* Deprecate namespaces, occurrences and query sugar.
