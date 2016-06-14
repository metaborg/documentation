Language Reference
==================

.. todo:: This part of the documentation still needs to be written.

.. code-block:: sdf3

   Module = [module [ModuleId] [Section*]]
   
.. code-block:: sdf3

   Section = [
     imports [ModuleId*]
   ]

.. code-block:: sdf3

   Section = [
     type signatures [TypeSignature*]
   ]
           
   TypeSignature = ...
   
.. code-block:: sdf3

   Section = [
     resolution parameters
       labels [{Label ","}*]
       order [{Label[ < ]Label ","}*]
       well-formedness [LabelRegex]
   ]

   Label      = [a-zA-Z]
   
   LabelRegex = Label
   LabelRegex = [[LabelRegex]*]
   LabelRegex = [[LabelRegex] . [LabelRegex]]
   LabelRegex = [[LabelRegex] & [LabelRegex]]
   LabelRegex = [[LabelRegex] | [LabelRegex]]
   LabelRegex = [([LabelRegex])]

.. code-block:: sdf3

   Section = [
     constraint-generation rules
       [Rule*]
   ]

   Rule = [
     init \[\[ [Pattern] \]\] :=
       [Constraint] [New?].
   ]
   Rule = [
     [RuleId] \[\[ [Pattern] ^ ([{Scope ","}*]) : [Type] \]\] :=
       [Constraint] [New?].
   ]

   Constraint = [[RuleId] \[\[ [Var] ^ ([{Scope ","}*]) : [Type] \]\]]
   
   New = [, new [{Scope ","}*]]
   
   Pattern = ...
   Type = ...

.. code-block:: sdf3

   Constraint = [[Constraint], [Constraint]]
   Constraint = [([Constraint])]

   Constraint = [[X] == [X]]
   Constraint = [[X] != [X]]

   Constraint = [[X] <- [X]]
   Constraint = [[X] -> [X]]
   Constraint = [[X] -[Label|[-]]-> [X]]
   Constraint = [[X] =[Label|[=]]=> [X]]
   Constraint = [[X] <=[Label|[=]]= [X]]

   Constraint = [[X] <! [X]]
   Constraint = [[X] <? [X]]

