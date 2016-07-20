=================
Shell environment
=================

The **Spoofax Shell** provides an interactive environment for
evaluating expressions in your language, much like the shells provided
by for example Haskell and Python. An interactive shell (sometimes
also called a `REPL`_) is useful for quickly experimenting with code
snippets, by allowing the code snippets to be evaluated in the context
of previous evaluations.

This part of the documentation explains how to install and configure
the shell to work for your language.

.. note:: The shell for Spoofax is still in development. As such, it
   currently only supports languages that use DynSem for their dynamic
   semantics specification.

.. toctree::
   :maxdepth: 1

   installation
   configuration
   contributing

.. _REPL: https://en.wikipedia.org/wiki/Read%E2%80%93eval%E2%80%93print_loop
