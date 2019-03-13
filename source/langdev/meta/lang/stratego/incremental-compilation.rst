Separate Compilation for Stratego
---------------------------------

.. warning :: This feature is still experimental, please `open issues <https://yellowgrass.org/project/Spoofax>`_ when your build fails or your program has different behaviour under this build setting.

The Stratego compiler is usually the slowest part in the build of a Spoofax project. To improve on the development experience, we have added an separate compilation option for Stratego. This can be opted into by editing the ``metaborg.yaml`` file:

.. code:: yaml

  dependencies:
    source:
    - org.metaborg:org.metaborg.meta.lang.stratego:${metaborgVersion}
  language:
    stratego:
      build: incremental
      format: jar

Your file most likely said nothing of the ``build``, meaning it was on the ``batch`` setting. The format was probably on ``ctree``. If that is the case you will also need to find the ``provider`` setting in your ESV files, likely in ``editor/Main.esv``. The provider settings should be as follows:

.. code:: esv

	provider: target/metaborg/stratego.jar
	provider: target/metaborg/stratego-javastrat.jar

Note that a clean build using this setting is necessary at first. It will likely take significantly longer than a clean build using the ``ctree`` format. All subsequent builds should be faster. 

Limitations
~~~~~~~~~~~

The separate compilation scheme does not do any static checking yet, so it will compile modules that refer to non-existing strategies. The result is broken Java code, which may still be compiled by the Eclipse Java Compiler. Keep an eye on the `src-gen/stratego-java` directory in your project explorer. If there are error markers on it, something went wrong.

Certain edge-cases with higher-order strategies are not supported. In particular, passing a higher-order strategy from the standard library to another strategy is not supported (e.g. ``foo(map)`` where ``foo(s) = s(bar)``). 

Due to a bug in release 2.5.2, the separate compiler will fail the build if concrete syntax is used in Stratego code. 
