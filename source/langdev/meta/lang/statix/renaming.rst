.. _renaming:

===================
Rename Refactoring
===================

.. role:: statix(code)
   :language: statix
   :class: highlight

.. role:: stratego(code)
   :language: stratego
   :class: highlight
   
Spoofax provides an automated Rename refactoring as an editor service for every language developed with it.
The renaming algorithm is implemented as a Stratego strategy and can be imported from the ``statixruntime`` library. When called, the strategy needs to be parameterized with the layout-preserving pretty-printing strategy ``construct-textual-change``, the ``editor-analyze`` strategy and an indicator strategy for multi-file mode.

When creating a new Spoofax language project, such a strategy is automatically generated and placed in the ``analysis`` module. But it can also easily be added to existing projects, for example with a module like this:

.. code-block:: stratego

  module renaming

  imports
    statixruntime
    statix/runtime/renaming
    
    pp
    analysis

  rules
    rename-menu-action = rename-action(construct-textual-change, 
                                       editor-analyze, id) 


The renaming is triggered from an entry in the Spoofax menu. For new projects this is automatically created. To add it to an existing project a menu like the following can be implemented in ESV:

.. code-block:: none

  module Refactoring

  menus
    menu: "Refactoring"
  
    action: "Rename" = rename-menu-action
    

For the renaming to work correctly in all cases, terms that represent a declaration of  a program entity, such as a function or a variable, need to set the ``decl`` property on the name of the entity. This is an example when declaring a type: 

.. code-block:: statix

  declareType(scope, name, T) :-
    scope -> Type{name} with typeOfDecl T,
    @name.decl := name,
    typeOfDecl of Type{name} in scope |-> [(_, (_, T))].
    
Renaming in NaBL2
-----------------------------    
There also exists a version of the Rename refactoring that works with languages using NaBL2.
It can be added with a Stratego module like this:

.. code-block:: stratego

  module renaming

  imports
    nabl2/runtime
    
    pp
    analysis

  rules
    rename-menu-action = nabl2-rename-action(construct-textual-change, 
                                             editor-analyze, id) 


