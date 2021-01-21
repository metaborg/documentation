```eval_rst
.. _vnext-migration-guide:
```

# Spoofax vNext Migration Guide

This is a stub for the migration guide of Spoofax vNext.


## Statix Injection Explication
There was an issue with Statix injection explication where the origin of the top-level term was lost and this caused SPT tests of Stratego strategies on analyzed ASTs to fail. Fix this by wrapping the bodies of the `pre-analyze` and `post-analyze` strategies in `analyze.str` with `origin-track-forced`, like this:

    pre-analyze  = origin-track-forced(explicate-injections-MyLang-Start)
    post-analyze = origin-track-forced(implicate-injections-MyLang-Start)

This is already fixed in new projects.