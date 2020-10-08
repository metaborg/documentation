=============
Spoofax vNext
=============

These are the release notes for Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------

Stratego
~~~~~~~~

Stratego has two new reserved words: ``cast`` and ``is``. Local variables can be reserved words if they start with ``'``, so you can use ``'cast`` and ``'is``.

Under the Stratego language options in your ``metaborg.yaml`` file you can turn on the gradual type system, if you use the incremental compiler. This option is ``gradual: static``, and only tests the types statically. The default is ``gradual: none`` right now, meaning the gradual type system is not on by default. There is an experimental third option ``gradual: dynamic`` which not only checks the types statically but also inserts casts to check types dynamically where necessary.

NaBL2
~~~~~

NaBL2 supports a new resolution algorithm based on fexid-point environment computation instead of graph search, which can be enabled by adding ``strategy environments`` to the ``name-resolution`` signature section.
It has much better performance characteristics, especially when dealing with mutually importing scopes and transitive imports.
Compared the the search-based, the environment-based algorithm can get stuck on scope graphs with cycles involving scopes importing references that can be resolved via that same scope.
Note that the environment-based algorithm may increase memory usage.
The default remains the search-based algorithm.

Statix
~~~~~~

Analysis times of large, multi-file Statix specifications has improved significantly.

SDF3
~~~~

``prefer`` and ``avoid`` are now deprecated. Usages of the operators will be marked with a deprecation warning.

Eclipse
~~~~~~~

* Premade Eclipse installations have been updated from Eclipse Photon to Eclipse 2020-6.
* Premade Eclipse installations for 32-bit Linux are no longer created.
* Embedded JRE in premade Eclipse installations has been updated from 8u162 (Oracle JRE) to 8u265-b01 (AdoptOpenJDK).
