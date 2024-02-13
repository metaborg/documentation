.. _publications:

============
Publications
============

The concepts and techniques underlying the design and implementation of Spoofax are described in scientific publications in conference proceedings and journals.
While those publications are typically (somewhat) behind when it comes to technical details,
this documentation cannot replace that body of work when it comes to exposition of concepts and ideas.
We recommend students of Spoofax to explore the literature.

The work on Spoofax has its origins in the ASF+SDF MetaEnvironment :cite:`r-BrandDHJJKKMOSVVV01` and work on the SDF2 syntax definition formalism :cite:`r-Vis97.thesis`. Experience with rewriting in ASF lead to the development of the Stratego transformation language :cite:`r-VisserBT98`.

The Spoofax language workbench was first developed as an IDE extension of Stratego/XT :cite:`r-BravenboerKVV08`, a tool set for program transformation based on SDF2 and Stratego.
The main publication about Spoofax is :cite:`r-KatsV10`, which was based on Spoofax 1.0 and develops the requirements and architecture for a language workbench supporting agile language development.

In :cite:`r-KatsVKV12` we develop a vision and first prototype to take Spoofax to the web; realizing that vision is still work in progress.
The vision for a *language designer's workbench* is outlined in :cite:`r-VisserOnward14`.
That vision drives the current (May 2017) ongoing development to enable higher-level definition of static and dynamic semantics in Spoofax.

We maintain a complete `bibliography <https://researchr.org/bibliography/metaborg-spoofax/publications>`_ of research results on `researchr <https://researchr.org>`_.
In the chapters on specific components, we discuss their history and related publications.

.. bibliography:: ../bib/spoofax.bib
   :style: plain
   :labelprefix: R
   :keyprefix: r-
