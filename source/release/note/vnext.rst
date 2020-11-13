=============
Spoofax vNext
=============

These are the release notes for Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------

SDF3
~~~~

``prefer`` and ``avoid`` are now deprecated. Usages of the operators will be marked with a deprecation warning.

Parser
~~~~~~

The JSGLR2 parser variants now report warnings on ambiguously parsed substrings. This includes ambiguities in lexical and layout syntax that do not result into ``amb`` nodes in the AST.

SDF
~~~~~~
The ``run`` expectation now allows to call strategies with term arguments. It's now also possible to test if a strategy failed.
