```eval_rst
.. highlight:: str
```


# 5 Hashtables and Sets

## 5.1. Hashtables

The rewriting paradigm of Stratego is functional in nature, which is somewhat contradictory to the imperative nature of hashtables. Normally, this doesn't present any practical problems, but remember that changes to hashtables "stick", i.e. they are changed by side-effect.

The Stratego hashtable API is pretty straightforward. Hashtables are created by `new-hastable` and destroyed by `hashtable-destroy`.

```
stratego> import lib
stratego> new-hashtable => h
Hashtable(136604296)
```

The result `Hashtable(136604296)` here is a handle to the actual hashtable. Consider it a pointer, if you will. The content of the hashtable must be retrieved with the `hashtable-*` strategies, which we introduce here. The strategy `hashtable-copy` can be used to copy a hashtable.

Adding a key with value to the table is done with `hashtable-put(|k,v)`, where `k` is the key, `v` is the value. Retrieving the value again can be done by `hashtable-get(|k)`.

```
stratego> <hashtable-put(|"one", 1)> h
Hashtable(136604296)
stratego> <hashtable-get(|"one")
1
```

The contents of the hashtable can be inspected with `hashtable-values` and `hashtable-keys`.

Nesting is also supported by the Stratego hashtables. Using `hashtable-push(|k,v)`, a new "layer" can be added to an existing key (or an initial layer can be added to a non-existing key). Removing a layer for a key can be done with `hashtable-pop(|k)`.

```
stratego> <hashtable-push("one",2)> h
Hashtable(136604296)
stratego> <hashtable-get("one")> h
[2,1]
stratego> <hashtable-pop(|"one")> h
Hashtable(136604296)
stratego> <hashtable-get(|"one")> h
[1]
stratego> <hashtable-remove(|"one")> h
Hashtable(136604296)
stratego> <hashtable-values> h
[]
```


## 5.2. Indexed Sets

The library provides a rather feature complete implementation of indexed sets, based on hashtables. A lightweight implementation of sets, based on lists, is explained in the [chapter on lists](03-lists.md).

Similar to hashtables, indexed sets are created with the `new-iset` strategy, copied with `iset-copy` and destroyed with `iset-destroy`.

```
stratego> new-iset => i
IndexedSet(136662256)
```

The resulting term, `IndexedSet(136662256)`, is a handle to the actual indexed set, which can only be manipulated through the `iset-*` strategies.

Adding a single element to a set is done with `iset-add(|e)`, whereas an entire list can be added with the `iset-addlist(|es)`. Its elements can be returned as a list using `iset-elements`.

```
stratego> <iset-addlist(|[1,2,3,4,4])> i
IndexedSet(136662256)
stratego> iset-elements
[1,2,3,4]
```

Notice that the result is indeed a set: every value is only represented once.

Using `iset-get-index(|e)`, the index of a given element `e` can be found. Similarly, `iset-get-elem(|i)` is used to get the value for a particular index.

```
stratego> <iset-get-index(|3)> i
2
stratego> <iset-get-elem(|3)> i
4
```

Note that the indexes start at 0.

The set intersection between two sets can be computed with the `iset-isect(|set2)` strategy. The strategy `iset-union(|set2)` calculates the union of two sets, whereas `iset-subset(|set2)` checks if one set is a subset of another. Equality between two sets is checked by `iset-eq(|set2)`. These strategies are all used in a similar way:

```
stratego> <iset-eq(|set2)> set1
```

A single element can be removed from the set with `iset-remove(|e)`. `iset-clear` will remove all elements in a set, thus emptying it.
