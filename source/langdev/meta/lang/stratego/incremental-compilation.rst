Incremental Compilation for Stratego
------------------------------------

.. note :: This feature is fairly new, please `open issues <https://yellowgrass.org/project/Spoofax>`_ when your build fails or your program has different behaviour under this build setting.

The Stratego compiler is usually the slowest part in the build of a Spoofax project. To improve on the development experience, we have added an incremental compilation option for Stratego. This can be opted into by editing the ``metaborg.yaml`` file:

.. code:: yaml

  dependencies:
    source:
    - org.metaborg:org.metaborg.meta.lang.stratego:${metaborgVersion}
  language:
    stratego:
      build: incremental
      format: jar

Your file most likely said nothing of the ``build``, meaning it was on the ``batch`` setting. The format was probably on ``ctree``. If that is the case you will also need to find the ``provider`` setting in your ESV files, likely in ``editor/Main.esv``. Find the ``ctree`` provider setting, it should now be:

.. code:: esv

	provider: target/metaborg/stratego.jar

Note that a clean build using this setting is necessary at first. It will likely take significantly longer than a clean build using the ``ctree`` format. All subsequent builds should be faster. 

As of Spoofax 2.5.7, there are no known limitations to the incremental compilation setting.
