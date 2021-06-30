=============
Spoofax vNext
=============

These are the release notes for Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------

Statix
^^^^^^

* Make `ArithTest` Serializable
* Integrate the Incremental Solver in Spoofax.
* Fix issue where edges were closed twice when having debug log enabled.
* Deprecate the `concurrent` property in favor of the `mode` (for language projects) or `modes` (for example projects) properties.
* Allow singleton properties to be set to the same value multiple times.
* Reduce number of cascading messages.
