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
