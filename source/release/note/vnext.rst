=============
Spoofax vNext
=============

This is a stub for the release notes of Spoofax vNext.

See the corresponding :ref:`migration guide <vnext-migration-guide>` for migrating from Spoofax vPrev to Spoofax vNext.

Changes
-------
- | SDF3: Lexical and context-free sort declarations
  | In SDF3 you should now explicitly declare your sorts. Declare lexical sorts
    in a ``lexical sorts`` block, and context-free sorts in a
    ``context-free sorts`` block. Sorts declared in a kernel ``sorts`` block
    default to declaring context-free sorts until a suffix such as ``-LEX``
    is added.
- | Statix: New projects use the signature generator by default
    New project that use Statix automatically have the Statix signature generator
    enabled. For this to work properly, declare your lexical and context-free
    sorts in SDF3 explicitly. See the :ref:`Statix signature generator
    <statix-signature-generator>` documentation for more information.


Overall
~~~~~~~
