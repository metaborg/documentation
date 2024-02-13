```eval_rst
.. highlight:: str
```

# 3. Lists

This chapter will introduce you to the basic strategies for working with lists. The strategies provide functionality for composing and decomposing, sorting, filtering, mering as well as constructing new abstractions from basic lists, such as associative lists.

Every value in Stratego is a term. This is also the case for lists. You can write the list 1, 2, 3 as `Cons(1,Cons(2,Cons(3,Nil)))`, which is clearly a term. Fortunately, Stratego also provides some convenient syntactic sugar that makes lists more readable and easy to work with. We can write the same list as `[1,2,3]`, which will be desugared internally in the the term above.



## 3.1. Making heads and tails of it

The most fundamental operations on lists is the ability compose and decompose lists. In Stratego, list composition on "sugared" lists, that is, lists written in the sugared form, has some sugar of its own. Assume `xs` is the list `[1,2,3]`. The code `[0|xs]` will prepend a 0 to it, yielding [0,1,2,3]. List decomposition is done using the match operator. The code `![0,1,2,3] ; ?[y|ys]` will bind `y` to the head of the list, `0`, and `ys` to the tail of the list, `[1,2,3]`.

The module `collection/list` contains a lot of convenience functions for dealing with lists. (`collection/list` is contained in the `libstratego-lib` library.) For example, the strategy `elem` will check if a given value is in a list. If it is, the identity of the list will be returned.

```
stratego> import libstratego-lib
stratego> <elem> (1, [2,3,1,4])
[2,3,1,4]
```

Continuing on the above Stratego Shell session, we can exercise some of the other strategies:

```
stratego> <length> [1,2,3,4,5]
5
stratego> <last> [5,6,7,8,9]
9
stratego> <reverse> [1,2,3,4,5]
[5,4,3,2,1]
```

There are two strategies for concatenating lists. If the lists are given as a tuple, use `conc`. If you have a list of lists, use `concat`:

```
stratego> <conc> ([1,2,3],[4,5,6],[7,8,9])
[1,2,3,4,5,6,7,8,9]
stratego> <concat> [[1,2,3],[4,5,6],[7,8,9]]
[1,2,3,4,5,6,7,8,9]
```

The sublist of the first <span class="emphasis">_n_</span> elements can be picked out with the `take(|n)` strategy:

```
stratego> <take(|3)> [1,2,3,4,5]
[1,2,3]
```

Finally, the `fetch(s)` strategy can be used to find the first element for which `s` succeeds:

```
stratego> <fetch(?2)> [1,2,3]
2
```

The Stratego library contains many other convenient functions, which are documented in the API documentation.



## 3.2. Sorting

The list sorting function is called `qsort(s)`, and implements the Quicksort algorithm. The strategy parameter `s` is the comparator function.

```
stratego> <qsort(gt)> [2,3,5,1,9,7]
[9,7,5,3,2,1]
```


## 3.3. Associative Lists

Stratego also has library support for associative lists, sometimes known as assoc lists. There are essentially lists of `(key, value)` pairs, and work like a poor man's hash table. The primary strategy for working with these lists is `lookup`. This strategy looks up the first value associated with a particular key, and returns it.

```
stratego> <lookup> (2, [(1, "a"), (2, "b"), (3, "c")]) => "b"
```


## 3.4. Pairing Lists

The library also contains some useful strategies for combining multiple lists. The `cart(s)` strategy makes a Cartesian product of two lists. For each pair, the parameter strategy `s` will be called. In the second case below, each pair will be summed by `add`.

```
stratego> <cart(id)> ([1,2,3],[4,5,6])
[(1,4),(1,5),(1,6),(2,4),(2,5),(2,6),(3,4),(3,5),(3,6)]
stratego> <cart(add)> ([1,2,3],[4,5,6])
[5,6,7,6,7,8,7,8,9]
```

Two lists can be paired using `zip(s)`. It takes a tuple of two lists, and will successively pick out the head of the lists and pair them into a tuple, and apply `s` to the tuple. `zip` is equivalent to `zip(id)`.

```
stratego> <zip> ([1,2,3],[4,5,6])
[(1,4),(2,5),(3,6)]
stratego> <zip(add)> ([1,2,3],[4,5,6])
[5,6,7]
```

The inverse function of `zip` is `unzip`.

```
stratego> <unzip> [(1,4),(2,5),(3,6)]
([1,2,3],[4,5,6])
```

There is also `unzip(s)` which like `unzip` takes a list of two-element tuples , and applies `s` to each tuple before unzipping them into two lists.


## 3.5. Lightweight Sets

In Stratego, lightweight sets are implemented as lists. A set differs from a list in that a given element (value) can only occur once. The strategy `nub` (also known as `make-set`) can be use to make a list into a set. It will remove duplicate elements. The normal functions on sets are provided, among them union, intersection, difference and equality:

```
stratego> <nub> [1,1,2,2,3,4,5,6,6]
[1,2,3,4,5,6]
stratego> <union> ([1,2,3],[3,4,5])
[1,2,3,4,5]
stratego> <diff> ([1,2,3],[3,4,5])
[1,2]
stratego> <isect> ([1,2,3],[3,4,5])
[3]
stratego> <set-eq> ([1,2,3],[1,2,3])
([1,2,3],[1,2,3])
```


## 3.6. Transforming Lists

Element-wise transformation of a list is normally done with the `map(s)` strategy. It must be applied to a list. When used, it will apply the strategy `s` to each element in the list, as shown here. It will return a list of equal length to the input. If the application of `s` fails on one of the elements `map(s)` fails.

```
stratego> <map(inc)> [1,2,3,4]
[2,3,4,5]
```

`mapconcat(s)` is another variant of the element-wise strategy application, equivalent to `map(s) ; concat`. It takes a strategy `s` which will be applied to each element. The strategy `s` must always result in a list, thus giving a list of lists, which will be concatenated. A slightly more convoluted version of the above mapping.

If we want to remove elements from the list, we can use `filter(s)`. The `filter` strategy will apply `s` to each element of a list, and keep whichever elements it succeeds on:

```
stratego> <filter(?2 ; !6)> [1,2,3,2]
[6,6]
```

```
stratego> <mapconcat(\ x -> [ <inc> x ] \)> [1,2,3,4]
```


## 3.7. Folding from the Left and Right

List folding is a somewhat flexible technique primarily intended for reducing a list of elements to a single value. Think of it as applying an operator between any two elements in the list, e.g. going from `[1,2,3,4]` to the result of `1 + 2 + 3 + 4`. If the operator is not commutative, that is `x <op> y` is not the same as `y <op> x`, folding from the left will not be the same as folding from the right, hence the need for both `foldl` and `foldr`.

The `foldr(init, oper)` strategy takes a list of elements and starts folding them from the right. It starts after the rightmost element of the list. This means that if we use the `+` operator with `foldr` on the list `[1,2,3,4]`, we get the expression `1 + 2 + 3 + 4 +` , which obviously has a dangling `+`. The strategy argument `init` is used to supply the missing argument on the right hand side of the last plus. If the `init` supplied is `id`, `[]` will be supplied by default. We can see this from the this trial run:

```
stratego> <foldr>(id, debug)
(4,[])
(3,(4,[]))
(2,(3,(4,[])))
(1,(2,(3,(4,[]))))
(1,(2,(3,(4,[]))))
```

With this in mind, it should be obvious how we can sum a list of numbers using `foldr`:

```
stratego> <foldr(!0, add)> [1,2,3,4]
10
```

The related strategy `foldl(s)` works similarly to `foldr`. It takes a two-element tuple with a list and a single element, i.e. `([x | xs], elem)`. The folding will start in the left end of the list. The first application is `s` on `(elem, x)`, as we can see from the following trial run:

```
stratego> <foldl(debug)> ([1,2,3,4], 0)
(1,0)
(2,(1,0))
(3,(2,(1,0)))
(4,(3,(2,(1,0))))
(4,(3,(2,(1,0))))
```

Again, summing the elements of the list is be pretty easy:

```
stratego> <foldl(add)> ([1,2,3,4], 0)
10
```


## 3.8. Summary

In this chapter we got a glimpse of the most important strategies for manipulating lists. We saw how to construct and deconstruct lists, using build and match. We also saw how we can sort, merge, split and otherwise transform lists. The strategies for associative lists and sets gave an impression of how we can construct new abstractions from basic lists.

More information about list strategies available can be found in the `collections/list` module, in the [library reference documentation](https://releases.strategoxt.org/docs/api/libstratego-lib/libstratego-lib-docs-stable/docs/).
