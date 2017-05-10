```eval_rst
.. highlight:: str
```


# 4 Strings


## 4.1. Basic String Operations

Strings, like all other primitive data types in Stratego, are terms. They are built with the build (`!`) operator and matched with the match (`?`) operator. Additional operations on and with strings are realized through strategies provided by the Stratego library. The most basic operations on strings provided by the library are concatenation, length computation and splitting. We will discuss operation each in turn.

The library provides two variants of the string concatenation operation. The first, `concat-strings`, takes a list of strings and returns the concatenated result. The second, `conc-strings` takes a two-element tuple of strings and returns the concatenated result:

```
stratego> <concat-strings> ["foo", "bar", "baz"]
"foobarbaz"
stratego> <conc-strings ("foo", "bar")
"foobar"
```

Once you have a string, you may want to know its length, i.e. the number of characters it contains. There are two equivalent strategies for determining the length of a string. If you come from a C background, you may favor the `strlen` strategy. If not, the `string-length` strategy may offer a clearer name.

The final basic operation on strings is splitting. There is a small family of closely related strategies for this, which all do simple string tokenization. The simplest of them is `string-tokenize(|sepchars)`. It takes a list of characters as its term argument, and must of course be applied to a string.

```
stratego> <string-tokenize(|[' '])> "foo bar baz"
["foo","bar","baz"]
```

Another strategy in the tokenizer family is `string-tokenize-keep-all(|sepchars)`. It works exactly like `string-tokenize(|sepchars)`, except that it also keeps the separators that were matched:

```
stratego> <string-tokenize-keep-all(|[' '])> "foo bar baz"
["foo"," ","bar"," ","baz"]
```


## 4.2. Sorting Strings


Even if you don't maintain a phone directory, sorting lists of strings may come in handy in many other enterprises. The strategies `string-sort` and `string-sort-desc` sort a list of strings in ascending and descending order, respectively.

```
stratego> !["worf", "picard", "data", "riker"]
["worf", "picard", "data", "riker"]
stratego> string-sort
["data","picard","riker","worf"]
stratego> string-sort-desc
["worf","riker","picard","data"]
```

If you only have two strings to sort, it may be more intuitive to use the string comparison strategies instead. Both `string-gt` and `string-lt` take a two-element tuple of strings, and return `1` if the first string is lexicographically bigger (resp. smaller) than the second, otherwise they fail.

```
stratego> <string-gt> ("picard","data")
1
stratego> <string-lt> ("worf","data")
command failed
```

Not directly a sorting operation, `string-starts-with(|pre)` is a strategy used to compare prefixes of strings. It takes a string as the term argument `pre` and must be applied to a string. It will succeed if `pre` is a prefix of the string it was applied to:

```
stratego> <strings-starts-with(|"wes")> "wesley"
"wesley"
```

## 4.3. Strings and Terms

We already said that strings are terms. As with terms, we can also deconstruct strings, but we cannot use normal term deconstruction for this. Taking apart a string with `explode-string` will decompose a string into a list of characters. We can then manipulate this character list using normal list operations and term matching on the elements. Once finished, we can construct a new string by calling `implode-string`. Consider the following code, which reverses a string:

```
stratego> !"evil olive"
"evil olive"
stratego> explode-string
[101,118,105,108,32,111,108,105,118,101]
stratego> reverse
[101,118,105,108,111,32,108,105,118,101]
stratego> implode-string
"evilo live"
```

This `explode-string`, strategy, `implode-string` idiom is useful enough to warrant its own library strategy, namely `string-as-chars(s)`. The code above may be written more succinctly:

```
stratego> <string-as-chars(reverse)> "evil olive"
"evilo live"
```

Sometimes, in the heat of battle, it is difficult to keep track of your primitive types. This is where `is-string` and `is-char` come in handy. As you might imagine, they will succeed when applied to a string and a character, respectively. A minor note about characters is in order. The Stratego runtime does not separate between characters and integers. The `is-char` must therefore be applied to an integer, and will verify that the value is within the printable range for ASCII characters, that is between 32 and 126, inclusive.

Finally, it may be useful to turn arbitrary terms into strings, and vice versa. This is done by `write-to-string` and `read-from-string`, which may be considered string I/O strategies.

```
stratego> <write-to-string> Foo(Bar())
"Foo(Bar)"
stratego> read-from-string
Foo(Bar)
```


## 4.4. Strings and Numbers

Another interplay between primitive types in Stratego is between numbers and strings. Converting numbers to strings and strings to numbers is frequently useful when dealing with program transformation, perhaps particularly partial evaluation and interpretation. Going from numbers to strings is done by `int-to-string` and `real-to-string`. Both will accept reals and integers, but will treat is input as indicated by the name.

```
stratego> <int-to-string> 42.9
"42"
stratego> <real-to-string> 42.9
"42.899999999999999"
```

The resulting number will be pretty-printed as best as possible. In the second example above, the imprecision of floating point numbers results in a somewhat non-intuitive result.

Going the other way, from strings to numbers, is a bit more convoluted, due to the multiple bases available in the string notation. The simplest strategies, `string-to-real` and `string-to-int`, assume the input string is in decimal.

```
stratego> <string-to-real> "123.123"
1.231230000000000e+02
stratego> <string-to-int> "123"
123
```

For integers, the strategies `hex-string-to-int`, `dec-string-to-int`, `oct-string-to-int` and `bin-string-to-int` can be used to parse strings with numbers in the most popular bases.
