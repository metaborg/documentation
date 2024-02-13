```eval_rst
.. highlight:: str
```

# 2. Arithmetic Operations

In this chapter we introduce strategies for working with numbers. The Stratego runtime provides two kinds of numbers: real numbers and integers. They are both terms, but cannot be used interchangeably. The library strategies described in this chapter also maintain the distinction between real numbers and integers, but many may also be applied to strings which contain numbers.


## 2.1. Basic Operations

Stratego does not have the normal mathematical syntax for arithmetic operators, such as `+`, `-`, `/` and `*`. These operators are used for other purposes. Instead, the library provides the operators as the strategies, namely `add`, `subt`, `div` and `mul`. Further, there is convenience strategy for integer increment, `inc` and decrement, `dec`.

While the Stratego language operates exclusively on terms, there are different kinds of primitive terms. The runtime maintains a distinction between real numbers and integer numbers. The library mirrors this distinction by providing a family of strategies for arithmetic operations. Arithmetic strategies which work on real numbers end in an `r`, e.g. `addr`, and strategies working on integers end in an `i`, e.g. `subti`. For each arithmetic operator, there is also a type-promoting variant, e.g. `mul`, which will type-promote from integer to real, when necessary. Finally, there are convenience strategies for working on strings containing numbers. For each arithmetic operation, there is a string variant, e.g `divS`.

The full set of arithmetic operations in Stratego:

```
add,  addr,  addi,  addS
div,  divr,  divi,  divS
mul,  mulr,  muli,  mulS
subt, subtr, subti, subtS
```

Using these strategies is straightforward.

```
stratego> <addr> (1.5, 1.5)
3.000000000000000e+00
stratego> <subti> (5, 2)
3
stratego> <mul> (1.5, 2)
3.000000000000000e+00
stratego> <inc> 2
3
```

As we can see, the `mul` operator can be applied to a pair which consists of different terms (real and integer). In this case, type promotion from integer to real happens automatically.

### Working on Strings
The string variants, e.g. `addS` and `divS` work on strings containing integers. The result in strings containing integers.

```
stratego> <addS> ("40", "2")
"42"
stratego> <divS> ("9", "3")
"3"
```


## 2.2. Number comparisons

The strategies found in the library for comparing two numbers correspond to the usual mathematical operators for less-than (`lt`), less-than-equal (`leq`), equal (`eq`), greater-than (`gt`), greater-than-or-equal (`geq`). As with the arithmetic strategies, each of these operators comes in an integer variant, suffixed with `i`, a real variant (suffixed by `r`), a string variant (suffixed by `S`) and a type promoting variant without suffix. The full matrix of comparison functions thus looks like:

```
lt,  ltr,  lti,  ltS
gt,  gtr,  gti,  gtS
leq, leqr, leqi, leqS
geq, geqr, geqi, geqS
```

A few examples:

```
stratego> <lt> (1.0, 2)
(1.000000000000000e+00,2)
stratego> <ltS> ("1", "2")
("1", "2")
stratego> <geqS> ("2", "2")
("2","2")
stratego> <gtr> (0.9, 1.0)
command failed
```

The maximum and minimum of a two-element tuple of numbers can be found with the `max` and `min` strategies, respectively. These do not distinguish between real and integers. However, they do distinguish between numbers and strings; `maxS` and `minS` are applicable to strings.

```
stratego> <max> (0.9, 1.0)
1.0
stratego> <min> (99, 22)
22
stratego> <minS> ("99", "22")
"22"
```

Some other properties of numbers, such as whether a number is even, negative or positive, can be be tested with the strategies `even`, `neg` and `pos`, respectively.


## 2.3. Other Operations

The modulus (remainder) of dividing an integer by another is provided by the `mod` strategy. `gcd` gives the greatest common divisor of two numbers. Both `mod` and `gcd` work on a two-element tuple of integers. The `log2` strategy can be used to find the binary logarithm of a number. It will only succeed if the provided number is an integer and that number has an integer binary logarithm.

```
stratego> <mod> (412,123)
43
stratego> <gcd> (412,123)
1
stratego> <log2> 16
4
```


## 2.4. Random Numbers

The library provides a strategy for generating random numbers, called `next-random`. The algorithm powering this random generator requires an initial "seed" to be provided. This seed is just a first random number. You can pick any integer you want, but it's advisable to pick a different seed on each program execution. A popular choice (though not actually random) is the number of seconds since epoch, provided by `time`. The seed is initialized by the `set-random-seed` strategy. The following code shows the normal idiom for getting a random number in Stratego:

```
stratego> time ; set-random-seed
[]
stratego> next-random     
1543988747
```

The random number generator needs only be initialized with a seed once for every program invocation.

## 2.5. Summary

In this chapter, we saw that Stratego is different from many other languages in that it does not provide the normal arithmetic operators. We saw that instead, strategies such as `add` and `mul` are used to add and multiply numbers. We also saw which strategies to use for comparing numbers and generating random numbers.

The module `term/integer` contains strategies for working with numbers. Refer to the [library reference documentation](https://releases.strategoxt.org/docs/api/libstratego-lib/libstratego-lib-docs-stable/docs/) for more information.
