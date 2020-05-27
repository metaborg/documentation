```eval_rst
.. _vnext-migration-guide:
```

# Spoofax vNext Migration Guide

This is a stub for the migration guide of Spoofax vNext.


## SDF3
In a coming version of Spoofax 2 it will be required to properly declare sorts
in SDF3 syntax definitions. Sorts for which context-free rules are defined
should be declared in a `context-free sorts` block:

    context-free sorts
      Stmt Expr

> *Note*: For backward compatibility, sorts declared in a plain `sorts` block
> are treated as context-free sorts. So this is equivalent and also fine:
>
>     sorts
>       Stmt Expr
>

Sorts for which lexical rules are defined should be declared in a
`lexical sorts` block:

    lexical sorts
      ID INT STRING

## Typesmart
If your `metaborg.yaml` file still contains mention of Typesmart (e.g. `debug: typesmart: false`), you can remove it. See the release notes for why Typesmart support was removed.

## Stratego
Spoofax languages used to always generate `target/metaborg/stratego-javastrat.jar` which contains the compiled Java code from `src/main/stratego`. Conditional on your settings in the `metaborg.yaml` file, your Stratego code would be turned into `target/metaborg/stratego.ctree` or `target/metaborg/stratego.jar` depending on whether you chose compilation or interpretation. As of this release, there is no longer a separate `stratego-javastrat.jar`. Instead `stratego.jar` is always generated and always contains at least the compiled Java code from `src/main/stratego`. If you choose compilation for your Stratego code, the compiled Stratego code is added to the `stratego.jar` file as was already the case originally. 

**What you need to do:** Go to your `editor/main.esv` file and find the `provider: ...` lines (or search your other ESV files if it's not there). The line `provider: target/metaborg/stratego-javastrat.jar` should be replaced by `provider: target/metaborg/stratego.jar`. If you already have a `provider: target/metaborg/stratego.jar`, one is enough and you can remove the `stratego-javastrat.jar` provider directive entirely. 
