.. _dynsembuiltins:

===================
Built-in data types
===================

DynSem has built-in support for the following types:

- :ref:`dynsem_number`
- :ref:`dynsem_bool`
- :ref:`dynsem_string`
- :ref:`dynsem_list`
- :ref:`dynsem_map`
- :ref:`dynsem_tuple`

.. _dynsem_number:

~~~~~~~
Numbers
~~~~~~~

.. describe:: Premises on numbers

  a == b
    Equality check. Fails if the two numbers are not equal. ``a`` and ``b`` may be bound variables or number literals.

  a != b
    Inequality check. Fails if the two numbers are equal. ``a`` and ``b`` may be bound variables or number literals.

  a => b
    Equivalent to ``==`` if ``b`` is a number literal. Binds new variable ``b`` to the value of ``a`` if ``b`` is an unbound variable. Invalid if ``b`` is a bound variable.

  a =!=> b
    Equivalent to ``!=`` if ``b`` is a number literal. Invalid if ``b`` is a variable (bound or unbound).

  case a of { b => ... }
    Switch-like premise for multiple cases. ``a`` must either be a number literal or a bound variable. ``b`` must either be a number literal or an unbound variable.

One can write reduction rules directly on numbers, for example:

.. code-block:: dynsem

  module nums

  signature
    arrows
      Int -inc-> Int

  rules
    3 -inc-> 4


.. _dynsem_int:

-----
Int
-----

The sort ``Int`` denotes positive and negative whole numbers, e.g. ``3, 99, -49``. The range of is the same as Java's ``int`` range: -2,147,483,648 to 2,147,483,647.

Integers can be typed literally, read or written from variables and matched against. Int terms are coerceable to :ref:`dynsem_float` where needed.

-----
Long
-----

Similar to :ref:`dynsem_int`, except for the range being the same as Java's ``long`` range: -9,223,372,036,854,775,808 to 9,223,372,036,854,775,807.

Long values are coercible to :ref:`dynsem_real` where needed.

.. _dynsem_float:

-----
Float
-----

The sort ``Float`` denotes positive and negative decimal numbers, e.g. ``3.14``, ``9.99``, ``-42.42``. The range is the same as Java's ``float`` range. ``Float`` inherits the precision of Java's ``float``.

All :ref:`dynsem_int` operations are supported on ``Float``. Note that due to precision issues equality/match checks between decimal vaues may unexpectedly fail.

Float values are coercible to :ref:`dynsem_real` where needed.

.. _dynsem_real:

-----
Real
-----

The sort ``Real`` denotes large positive and negative decimal numbers. The range is the same as Java's ``double``.

All :ref:`dynsem_int` operations are supported on ``Real``. Note that due to precision issues equality/match checks between decimal vaues may unexpectedly fail.

.. _dynsem_bool:

~~~~
Bool
~~~~

The sort ``Bool`` denotes logical values. Values are either ``true`` or ``false``.

.. describe:: Premises on booleans

  a == b
    Equality check. Fails if the two booleans are not equal. ``a`` and ``b`` may be bound variables or boolean literals.

  a != b
    Inequality check. Fails if the two boolean are equal. ``a`` and ``b`` may be bound variables or boolean literals.

  a => b
    Equivalent to ``==`` if ``b`` is a boolean literal. Binds new variable ``b`` to the value of ``a`` if ``b`` is an unbound variable. Invalid if ``b`` is a bound variable.

  a =!=> b
    Equivalent to ``!=`` if ``b`` is a boolean literal. Invalid if ``b`` is a variable (bound or unbound).

  case a of { b => ... }
    Switch-like premise for multiple cases. ``a`` must either be a boolean literal or a bound variable. ``b`` must either be a boolean literal or an unbound variable.

There are no built-in logical operations on the sort ``Bool``. One can define meta-functions for these operations, for example:

.. code-block:: dynsem

  module booleans

  signature
    arrows
      not(Bool) --> Bool

  rules
    not(true) --> false
    not(false) --> true

One can write reduction rules directly on boolean literals, for example:

.. code-block:: dynsem

  module booleans

  signature
    arrows
      Bool -not-> Bool

  rules
    true -not-> false

    false -not-> true

.. _dynsem_string:

~~~~~~
String
~~~~~~

The ``String`` sort denotes ASCII strings. The maximum length of a string is the maximum size of an ``Int``.

.. describe:: string operations

  building: "hello", "hello world"
    Builds a string from a literal

  matching: a => "hello", a =!=> "hello"
    see ``==`` and ``!=`` below

  s1 == s2
    Compare strings ``s1`` and ``s2`` for equality. Fail if the strings are not identical.

  s1 != s2
    Compare strings ``s1`` and ``s2`` for equality. Fail if the strings are identical.

.. _dynsem_list:

~~~~~
List
~~~~~

The ``List`` terms denote list terms of homogenously typed terms. Use of a list sort must specify the sort of the contained elements. For example, the following declares a constructor ``foo`` having a list of integers as child:

.. code-block:: dynsem

  module lists

  signature
    sorts
      F
    constructors
      foo: List(Int) -> F


.. describe:: list operations

  building: [], [a, b], [a, b | xs]
    Build an empty list, a list of two elements and a list of two or more elements, respectively. If ``a``, ``b`` and/or ``xs`` are variables they must be bound variables. If ``a`` is of sort ``S`` then ``b`` has to be of sort ``S`` and ``xs`` must be of sort ``List(S)`` or an empty list literal. Empty list literals - ``[]`` - are coercible to any list sort.

    Examples of list build premises:

    .. code-block:: dynsem

      [] => x
      [1, 2, 3] => x
      [1, 2 | []] => x
      [1, 2 | [3, 4]] => x
      [a, b | [a, b]] => x


  matching: [], [a, b], [a, b, c | xs], [_, _ | xs]
    Matches an empty list, a list of two elements, a list of three or more elements and a list of two or more elements, respectively. All variables in a list match must be unbound variables. Variables occuring in the pattern will be bound if the entire pattern match succeeds. If any of ``a``, ``b``, ``c``, ``xs`` is a term pattern (i.e. not a variable) then a pattern match will be attempted for that pattern.

    Examples of list pattern matching premises:

    .. code-block:: dynsem

      t => []
      t => [_, _]
      t => [_, _ | _]
      t => [1, 2]
      t => [a, b | [c, d | xs]]

    l1 == l2
      Check lists ``l1`` and ``l2`` for equality. Two lists are equal if they are of the same type, they have the same length and being element-wise equal. Premise fails if the two lists are not equal.

    l1 != l2
      Check lists ``l1`` and ``l2`` for inequality. See above for a definition of list equality. Premise fails if the two lists are equal.

  indexed access: l1[idx]
    Retrieves the element at index ``idx`` in the list ``l1``. Fails if the index is out of bounds.

  concat: l1 ++ l2
    Concatenates two lists of the same type: if the type of ``l1`` is ``List(S)``, then the type of ``l2`` has to be ``List(S)``, unless ``l2`` is an empty list literal. The elements in the ``l2`` list will be appended, in order, to the elements of ``l1``.

  reverse: `l1
    Reverses the list ``l1``. Example:

    .. code-block:: dynsem

      `[1, 2, 3] // => [3, 2, 1]
      `[] // => []
      `[1, 2, 3 | `[4, 5]] // => [4, 5, 3, 2, 1]

One may write reduction rules directly on list literals, but the type of the list has to be explicitly specified:

.. code-block:: dynsem

  module lists

  signature
    arrows
      List(Int) -empty-> Bool

  rules
    [] : List(Int) -empty-> true

    [_|_] : List(Int) -empty-> false

.. _dynsem_map:

~~~~
Map
~~~~

The sort ``Map`` denotes associative arrays, or dictionaries. A use of the map sort must declare the types of keys and the type of values. The following declares the sort ``Env`` as an alias to the sort mapping strings to integers:

.. code-block:: dynsem

  signature
    sort aliases
      Env = Map(String, Int)

.. note:: Maps are immutable. Adding or removing entries from a map does not modify the existent map, instead it creates a new map.

.. describe:: map operations

  building: {}, {k1 |--> v1}, {k1 |--> v1, k2 |--> v2, ...}
    Build an empty map, a map with one entry and a map with multiple entries, respectively. All appearing variables must be bound. All keys must be of the same type, and all values must be of the same type. Results in a new map, the old map is unmodified.

  extending: {k1 |--> v1, map}, {map, k1 |--> v1}
    Extend the map represented by variable ``map`` with a new binding from key ``k1`` to value ``v1``. Entries on the left map replace entries with the same key on the right. Multiple additions can be performed at once: ``{k1 |--> v1, map, k2 |--> v2}``. This is equivalent to writing: ``{k1 |--> v1, {map, k2 |--> v2}}``. Multiple maps can be merged into one:  ``{map1, map2, map3}``. Again, the left entries replace the right entries. It is equivalent to writing: ``{map1, {map2, map3}}``. The result is always a new map, the old map(s) remain(s) unmodified.

  removing: map1 \\ k1
    Return a new map containing all entries in map ``map1`` except for the entry with key ``k1``. Fails if ``map1`` has no entry for key ``k1``. Map ``map1`` remains unmodified.

  access: map1[k1]
    Return the value associated with key ``k1`` in map ``map1``. Fails if ``map1`` does not have an entry for key ``k1``.

  contains: map1[k1?]
    Check whether map ``map1`` has an entry for key ``k1``. Return ``true`` if an entry exists, ``false`` otherwise.

  matching
    Pattern matching is **not** possible on maps

Defining rules directly on maps is possible, but the type of the map has to be explicitly specified in the rule:

.. code-block:: dynsem

  signature
    arrows
      Map(String, Int) -global-> Int

  rules
    m : Map(String, Int) -global-> m["global"]

.. _dynsem_tuple:

~~~~~~
Tuple
~~~~~~

The ``Tuple`` sort denotes pairs of terms of arbitrary (higher than 0) arity. Tuple sort usages must be accompanied by declarations of the types of their elements. For example:

.. code-block:: dynsem

  signature
    sort aliases
      T = (S1 * S2 * S3)

declares sort ``T`` to be an alias of the 3-tuple of terms of type ``S1``, ``S2`` and ``S3``, respectively.


.. describe:: tuple operations

  building: (t1, t2, ...)
    Build a tuple literal. All variables appearing in the construction must be bound. If the types of children ``t1``, ``t2``, ... are ``S1``, ``S2``, ..., respectively, then the type of the resulting tuple is ``(S1 * S2 * ...)``.

  matching: (p1, p2, p3)
    Match a term against a 3-tuple pattern. The patterns ``p1``, ``p2``, ``p3`` are matched against the respective child of the incoming tuple. A tuple pattern match succeeds if the term matched is a tuple of equal arity and if the sub-pattern matches succeed. Variables appearing in the pattern must be unbound. Variables appearing in the pattern will be bound if the pattern match succeeds.

It is possible to define rules directly on tuple literals, but the type of the tuple has to be explicitly specified in the rule:

.. code-block:: dynsem

  signature
    arrows
      (Bool * Bool) -or-> Bool

  rules

    (true, _) : (Bool * Bool) -or-> true
    (_, true) : (Bool * Bool) -or-> true
    (false, false) : (Bool * Bool) -or-> false
