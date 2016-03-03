```eval_rst
.. highlight:: nabl
```

# NaBL

This is the NaBL reference manual.
In Spoofax, name binding is specified in NaBL.
NaBL stands for *Name Binding Language* and the acronym is pronounced 'enable'.
Name binding is specified in terms of:

* namespaces
* binding instances (name declarations)
* bound instances (name references)
* scopes
* imports

## Namespaces

A namespace is a collection of names and is not necessarily connected to a specific language concept. Different concepts can contribute names to a single namespace. For example, in Java, classes and interfaces contribute to the same namespace, as do variables and parameters. Namespaces are declared in the `namespaces` section of a language definition:

```
namespaces

  Module Entity Property Function Variable
```

```eval_rst
.. note:: Some languages such as C# provide namespaces as a language concept to scope the names of declarations such as classes. It is important to distinguish these namespaces as a language concept from NaBL namespaces as a language definition concept. The two are *not* related.
```

## Name Binding Rules

Name bindings are specified in name binding rules. Each rule consists of a term pattern (a term that may contain variables and wildcards `_`) and a list of name binding clauses about the language construct matched by the pattern. There are four different kinds of clauses for definition sites, use sites, scopes, and imports.

### Definition Sites

The following rules declare definition sites for module and entity names:

```
rules

  Module(m, _): defines non-unique Module m
  Entity(e, _): defines unique Entity e
```

The patterns in these rules match module and entity declarations, binding variables `m` and `e` to module and entity names, respectively. These variables are then used in the clauses on the right-hand sides. In the first rule, the clause specifies any term matched by `Module(m, _)` to define a name `m` in the `Module` namespace. Similarly, the second rule specifies any term matched by `Entity(e, _)` to define a name `e` in the `Entity` namespace.

Consider the following example module:

```entity
module shopping

entity Item {
    name : String
}
```

The parser turns this into an abstract syntax tree, represented as a term:

```aterm
Module(
  "shopping"
, [ Entity(
      "Item"
    , [ Property("name", EntityType("String")) ]
    )
  ]
)
```

The patterns in name binding rules match subterms of this term, indicating definition and use sites. The whole term is a definition site of the module name `shopping`. The first name binding rule specifies this binding. Its pattern matches the term and binds `m` to `"shopping"`. Similarly, the subterm `Entity("Item", ...)` is a definition site of the entity name `Item`.
The pattern of the second name binding rule matches this term and binds `e` to `"Item"`.

While entity declarations are `unique` definition sites, module declarations are `non-unique` definition sites. That is, multiple module declarations can share the same name. This allows language users to spread the content of a module over several files, similar to Java packages.
Definition sites are by default unique, so the `unique` keyword is only optional and can be omitted. For example, the following rules declare unique definition sites for property and variable names:

```
Property(p, _): defines Property p
Param(p, _)   : defines Variable p
Declare(v, _) : defines Variable v
```

```eval_rst
.. note:: Spoofax distinguishes the name of a namespace from the sort and the constructor of a program element: in the last rule above, the sort of the program element is ``Statement``, its constructor is ``Declare``, and it defines a name in the ``Variable`` namespace. By distinguishing these three things, it becomes easy to add or exclude program elements from a namespace. For example, return statements are also of syntactic sort ``Statement``, but they do not correspond to any namespace. On the other hand, function parameters also define names in the ``Variable`` namespace, even though (in contrast to variable declarations) they do not belong to the syntactic sort ``Statement``.
```

### Use Sites

Use sites refer to definition sites of names. They can be declared similarly to definition sites. The following rule declares use sites for entity names:

```
Type(t): refers to Entity t
```

Use sites might refer to different names from different namespaces. For example, a variable might refer either to a `Variable` or a `Property`. This can be specified by exclusive resolution options:

```
Var(x):
  refers to Variable x
  otherwise refers to Property x
```

The `otherwise` keyword signals ordered alternatives: only if the reference cannot be resolved to a variable, Spoofax will try to resolve it to a property. As a consequence, variable declarations shadow property definitions. If this is not intended, constraints can be defined to report corresponding errors.

### Scopes

Scopes restrict the visibility of definition sites. For example, an entity declaration scopes property declarations that are not visible from outside the entity.

```entity
entity Customer {
    name : String // Customer.name
}

entity Product {
    name : String // Product.name
}
```

In this example, the two `name` properties both reside in the `Property` namespace, but can still be distinguished: if `name` is referred in a function inside `Customer`, it refers the one in `Customer`, not the one in `Product`.

#### Simple Scopes

Scopes can be specified in scope clauses. They can be nested and name resolution typically looks for definition sites from inner to outer scopes. In the running example, modules scope entities, entities scope properties and functions, and functions scope local variables.

```
Module(m, _):
  defines Module m
  scopes Entity
Entity(e, _):
  defines Entity e
  scopes Property, Function
Function(f, _):
  defines Function f
  scopes Variable
```

As these examples illustrate, scopes are often also definition sites. However, this is not a requirement. For example, a block statement has no name, but scopes variables:

```
Block(_): scopes Variable
```

#### Definition Sites with Limited Scope

Many definitions are visible in their enclosing scope: entities are visible in the enclosing module, properties and functions are visible in the enclosing entity, and parameters are visible in the enclosing function. However, this does not hold for variables declared inside a function. Their visibility is limited to statements after the declaration. The following rule restricts the visibility to the subsequent scope:

```
Declare(v, _):
  defines Variable v in subsequent scope
```

Similarly, the iterator variable in a for loop is only visible in its condition, the update, and the loop’s body, but not in the initializing expression. This can be declared as follows:

```
For(v, t, init, cond, update, body):
  defines Variable v in cond, update, body
```

#### Scoped References

Typically, use sites refer to names which are declared in its surrounding scopes. But a use site might also refer to definition sites which reside outside its own scope. For example, a property name in an expression might refer to a property in another entity:

```entity
entity Customer {
    name : String
}

entity Order {
    customer : Customer

    function getCustomerName(): String {
        return customer.name;
    }
}
```

Here, `name` in `customer.name` refers to the property in entity `Customer`. The following name binding rule is a first attempt to specify this:

```
PropAccess(exp, p):
  refers to Property p in Entity e
```

But this rule does not specify which entity `e` is the right one. Interaction with the type system is required in this case:

```
PropAccess(exp, p):
  refers to Property p in Entity e
    where exp has type EntityType(e)
```

This rule extracts `e` from the type of the expression `exp`. We will later discuss interactions with the type system in more detail.

### Imports

Many languages offer import facilities to include definitions from another scope into the current scope. For example, a module can import other modules, making entities from the imported modules available in the importing module:

```entity
module order

import banking

entity Customer {
    name   : String
    account: BankAccount
}
```

Here, `BankAccount` is not declared in the scope of module `order`. However, module `banking` declares an entity `BankAccount` which is imported into module `order`. The type of property `account` should refer to this entity. This can be specified by the following name binding rule:

```
Import(m):
  imports Entity from Module m
```

This rule has two effects. First, `Import(m)` declares use sites for module names. Second, entities declared in these modules become visible in the current scope.

## Interaction with Type System

We can associate names with type information. This type information is specified at definition sites, and accessed at use sites. The following name binding rules involve type information at definition sites:

```
Property(p, t):
  defines Property p of type t
Param(p, t):
  defines Variable p of type t
```

These rules match property and parameter declarations, binding their name to `p` and their type to `t`. Spoofax remembers `t` as type information about the property or parameter name `p`.
In this example, the type is explicitly declared in property and parameter declarations. But the type of a definition site is not always explicitly declared but needs to be inferred by the type system. For example, variable declarations might come with an initial expression, but without an explicit type.

```entity
var x = 42;
```

The type of `x` is the type of its initial expression `42`. To make the type of `x` explicit, the type of the initial expression needs to be inferred by the type system. The following name binding rule makes this connection between name binding and type system:

```
Declare(v, e):
  defines Variable v
    of type t
    in subsequent scope
    where e has type t
```
