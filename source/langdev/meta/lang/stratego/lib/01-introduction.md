```eval_rst
.. highlight:: str
```

# 1. Introduction

The Stratego Library was designed with one goal in mind: it should contain be a good collection of strategies, rules and data types for manipulating programs. In the previous part of this tutorial, we have already introduced you some of the specific features in the library for doing program manipulation. However, the library also contains abstract data types which are found in almost any library, such as lists, strings, hashtables, sets, file and console I/O, directory manipulation and more. In this chapter, we aim to complete your basic Stratego education by introducing you to how these bread-and-butter data types have been implemented for Stratego.

> Beware that the online documentation will display strategies on the form `apply-and-fail(Strategy s, ATerm name, ATerm in-term, ATerm out)`, whereas we adopt the more conventional format in this manual: `apply-and-fail(s | name, in-term, out)`


## 1.1. Anatomy of the Stratego Library

The organization of the Stratego library is hierarchical. At the coarsest level of organization, it is divided into packages, whose named as on a path-like form, e.g. `collection/list`. Each package in turn consists of one or several modules. A module is a leaf in the hierarchy. It maps to one Stratego (`.str`) file, and contains definitions for strategies, rules, constructors and overlays. The available packages in the library is listed below.

* `collection/hash-table`
* `collection/list`
* `collection/set`
* `collection/tuple`
* `lang`
* `strategy`
* `strategy/general`
* `strategy/pack`
* `strategy/traversal`
* `system/io`
* `system/posix`
* `term`
* `util`
* `util/config`

As an example, the `collection/list` package consists of the modules `common`, `cons`, `filter`, `index`, `integer`, `lookup`, `set`, `sort`, `zip`. Inside the `sort` module, we find the `qsort` strategy, for sorting lists.

In the remainder of this part of the tutorial, we will present the most important parts of the library, and show their typical usage patterns and idioms. If anything seems unclear, you are encouraged to consult the [online documentation](http://releases.strategoxt.org/docs/api/libstratego-lib/libstratego-lib-docs-stable/docs/) for further details.
