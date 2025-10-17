




Differences between Cython and Pyrex — Cython 3.1.4 documentation

### Navigation

* [next](memoryviews.html "Typed Memoryviews")
* [previous](limitations.html "Limitations") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Differences between Cython and Pyrex

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Differences between Cython and Pyrex[¶](#differences-between-cython-and-pyrex "Link to this heading")

Warning

Both Cython and Pyrex are moving targets. It has come to the point
that an explicit list of all the differences between the two
projects would be laborious to list and track, but hopefully
this high-level list gives an idea of the differences that
are present. It should be noted that both projects make an effort
at mutual compatibility, but Cython’s goal is to be as close to
and complete as Python as reasonable.

## Python 3 Support[¶](#python-3-support "Link to this heading")

Cython creates `.c` files that can be built and used with both
Python 2.x and Python 3.x. In fact, compiling your module with
Cython may very well be an easy way to port code to Python 3.

Cython also supports various syntax additions that came with
Python 3.0 and later major Python releases. If they do not conflict
with existing Python 2.x syntax or semantics, they are usually just
accepted by the compiler. Everything else depends on the
compiler directive `language_level=3`
(see [compiler directives](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives")).

### List/Set/Dict Comprehensions[¶](#list-set-dict-comprehensions "Link to this heading")

Cython supports the different comprehensions defined by Python 3 for
lists, sets and dicts:

```
[expr(x) for x in A]             # list
{expr(x) for x in A}             # set
{key(x) : value(x) for x in A}   # dict
```

Looping is optimized if `A` is a list, tuple or dict. You can use
the [`for`](https://docs.python.org/3/reference/compound_stmts.html#for "(in Python v3.13)") … [`from`](https://docs.python.org/3/reference/simple_stmts.html#from "(in Python v3.13)") syntax, too, but it is
generally preferred to use the usual [`for`](https://docs.python.org/3/reference/compound_stmts.html#for "(in Python v3.13)") … [`in`](https://docs.python.org/3/reference/expressions.html#in "(in Python v3.13)")
`range(...)` syntax with a C run variable (e.g. `cdef int i`).

Note

see [Automatic range conversion](#automatic-range-conversion "#automatic-range-conversion")

Note that Cython also supports set literals starting from Python 2.4.

### Keyword-only arguments[¶](#keyword-only-arguments "Link to this heading")

Python functions can have keyword-only arguments listed after the `*`
parameter and before the `**` parameter if any, e.g.:

```
def f(a, b, *args, c, d = 42, e, **kwds):
    ...
```

Here `c`, `d` and `e` cannot be passed as position arguments and must be
passed as keyword arguments. Furthermore, `c` and `e` are required keyword
arguments, since they do not have a default value.

If the parameter name after the `*` is omitted, the function will not accept any
extra positional arguments, e.g.:

```
def g(a, b, *, c, d):
    ...
```

takes exactly two positional parameters and has two required keyword parameters.

## Conditional expressions “x if b else y”[¶](#conditional-expressions-x-if-b-else-y "Link to this heading")

Conditional expressions as described in
[https://www.python.org/dev/peps/pep-0308/](https://www.python.org/dev/peps/pep-0308/ "https://www.python.org/dev/peps/pep-0308/"):

```
X if C else Y
```

Only one of `X` and `Y` is evaluated (depending on the value of C).

## cdef inline[¶](#cdef-inline "Link to this heading")

Module level functions can now be declared inline, with the [`inline`](#inline "#inline")
keyword passed on to the C compiler. These can be as fast as macros.:

```
cdef inline int something_fast(int a, int b):
    return a*a + b
```

Note that class-level [`cdef`](language_basics.html#cdef "language_basics.html#cdef") functions are handled via a virtual
function table, so the compiler won’t be able to inline them in almost all
cases.

## Assignment on declaration (e.g. “cdef int spam = 5”)[¶](#assignment-on-declaration-e-g-cdef-int-spam-5 "Link to this heading")

In Pyrex, one must write:

```
cdef int i, j, k
i = 2
j = 5
k = 7
```

Now, with cython, one can write:

```
cdef int i = 2, j = 5, k = 7
```

The expression on the right hand side can be arbitrarily complicated, e.g.:

```
cdef int n = python_call(foo(x,y), a + b + c) - 32
```

## ‘by’ expression in for loop (e.g. “for i from 0 <= i < 10 by 2”)[¶](#by-expression-in-for-loop-e-g-for-i-from-0-i-10-by-2 "Link to this heading")

```
for i from 0 <= i < 10 by 2:
    print i
```

yields:

```
0
2
4
6
8
```

Note

Usage of this syntax is discouraged as it is redundant with the
normal Python [`for`](https://docs.python.org/3/reference/compound_stmts.html#for "(in Python v3.13)") loop.
See [Automatic range conversion](#automatic-range-conversion "#automatic-range-conversion").

## Boolean int type (e.g. it acts like a c int, but coerces to/from python as a boolean)[¶](#boolean-int-type-e-g-it-acts-like-a-c-int-but-coerces-to-from-python-as-a-boolean "Link to this heading")

In C, ints are used for truth values. In python, any object can be used as a
truth value (using the `__nonzero__()` method), but the canonical choices
are the two boolean objects `True` and `False`. The `bint` (for
“boolean int”) type is compiled to a C int, but coerces to and from
Python as booleans. The return type of comparisons and several builtins is a
`bint` as well. This reduces the need for wrapping things in
`bool()`. For example, one can write:

```
def is_equal(x):
    return x == y
```

which would return `1` or `0` in Pyrex, but returns `True` or `False` in
Cython. One can declare variables and return values for functions to be of the
`bint` type. For example:

```
cdef int i = x
cdef bint b = x
```

The first conversion would happen via `x.__int__()` whereas the second would
happen via `x.__bool__()` (a.k.a. `__nonzero__()`), with appropriate
optimisations for known builtin types.

## Executable class bodies[¶](#executable-class-bodies "Link to this heading")

Including a working [`classmethod()`](https://docs.python.org/3/library/functions.html#classmethod "(in Python v3.13)"):

```
cdef class Blah:
    def some_method(self):
        print self
    some_method = classmethod(some_method)
    a = 2*3
    print "hi", a
```

## cpdef functions[¶](#cpdef-functions "Link to this heading")

Cython adds a third function type on top of the usual [`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.13)") and
[`cdef`](language_basics.html#cdef "language_basics.html#cdef"). If a function is declared [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") it can be called
from and overridden by both extension and normal python subclasses. You can
essentially think of a [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") method as a [`cdef`](language_basics.html#cdef "language_basics.html#cdef") method +
some extras. (That’s how it’s implemented at least.) First, it creates a
[`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.13)") method that does nothing but call the underlying
[`cdef`](language_basics.html#cdef "language_basics.html#cdef") method (and does argument unpacking/coercion if needed). At
the top of the [`cdef`](language_basics.html#cdef "language_basics.html#cdef") method a little bit of code is added to see
if it’s overridden, similar to the following pseudocode:

```
if hasattr(type(self), '__dict__'):
    foo = self.foo
    if foo is not wrapper_foo:
        return foo(args)
[cdef method body]
```

To detect whether or not a type has a dictionary, it just checks the
`tp_dictoffset` slot, which is `NULL` (by default) for extension types,
but non- null for instance classes. If the dictionary exists, it does a single
attribute lookup and can tell (by comparing pointers) whether or not the
returned result is actually a new function. If, and only if, it is a new
function, then the arguments packed into a tuple and the method called. This
is all very fast. A flag is set so this lookup does not occur if one calls the
method on the class directly, e.g.:

```
cdef class A:
    cpdef foo(self):
        pass

x = A()
x.foo()  # will check to see if overridden
A.foo(x) # will call A's implementation whether overridden or not
```

See [Early Binding for Speed](early_binding_for_speed.html#early-binding-for-speed "early_binding_for_speed.html#early-binding-for-speed") for explanation and usage tips.

## Automatic range conversion[¶](#automatic-range-conversion "Link to this heading")

This will convert statements of the form `for i in range(...)` to `for i
from ...` when `i` is any cdef’d integer type, and the direction (i.e. sign
of step) can be determined.

Warning

This may change the semantics if the range causes
assignment to `i` to overflow. Specifically, if this option is set, an error
will be raised before the loop is entered, whereas without this option the loop
will execute until a overflowing value is encountered. If this affects you,
change `Cython/Compiler/Options.py` (eventually there will be a better
way to set this).

## More friendly type casting[¶](#more-friendly-type-casting "Link to this heading")

In Pyrex, if one types `<int>x` where `x` is a Python object, one will get
the memory address of `x`. Likewise, if one types `<object>i` where `i`
is a C int, one will get an “object” at location `i` in memory. This leads
to confusing results and segfaults.

In Cython `<type>x` will try and do a coercion (as would happen on assignment of
`x` to a variable of type type) if exactly one of the types is a python object.
It does not stop one from casting where there is no conversion (though it will
emit a warning). If one really wants the address, cast to a `void *` first.

As in Pyrex `<MyExtensionType>x` will cast `x` to type `MyExtensionType`
without any type checking. Cython supports the syntax `<MyExtensionType?>` to do
the cast with type checking (i.e. it will throw an error if `x` is not a
(subclass of) `MyExtensionType`.

## Optional arguments in cdef/cpdef functions[¶](#optional-arguments-in-cdef-cpdef-functions "Link to this heading")

Cython now supports optional arguments for [`cdef`](language_basics.html#cdef "language_basics.html#cdef") and
[`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") functions.

The syntax in the `.pyx` file remains as in Python, but one declares such
functions in the `.pxd` file by writing `cdef foo(x=*)`. The number of
arguments may increase on subclassing, but the argument types and order must
remain the same. There is a slight performance penalty in some cases when a
cdef/cpdef function without any optional is overridden with one that does have
default argument values.

For example, one can have the `.pxd` file:

```
cdef class A:
    cdef foo(self)

cdef class B(A):
    cdef foo(self, x=*)

cdef class C(B):
    cpdef foo(self, x=*, int k=*)
```

with corresponding `.pyx` file:

```
cdef class A:

    cdef foo(self):
        print("A")


cdef class B(A):

    cdef foo(self, x=None):
        print("B", x)


cdef class C(B):

    cpdef foo(self, x=True, int k=3):
        print("C", x, k)
```

Note

this also demonstrates how [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") functions can override
[`cdef`](language_basics.html#cdef "language_basics.html#cdef") functions.

## Function pointers in structs[¶](#function-pointers-in-structs "Link to this heading")

Functions declared in [`struct`](language_basics.html#struct "language_basics.html#struct") are automatically converted to
function pointers for convenience.

## C++ Exception handling[¶](#c-exception-handling "Link to this heading")

[`cdef`](language_basics.html#cdef "language_basics.html#cdef") functions can now be declared as:

```
cdef int foo(...) except +
cdef int foo(...) except +TypeError
cdef int foo(...) except +python_error_raising_function
```

in which case a Python exception will be raised when a C++ error is caught.
See [Using C++ in Cython](wrapping_CPlusPlus.html#wrapping-cplusplus "wrapping_CPlusPlus.html#wrapping-cplusplus") for more details.

## Synonyms[¶](#synonyms "Link to this heading")

`cdef import from` means the same thing as `cdef extern from`

## Source code encoding[¶](#source-code-encoding "Link to this heading")

Cython supports [PEP 3120](https://peps.python.org/pep-3120/ "https://peps.python.org/pep-3120/") and [PEP 263](https://peps.python.org/pep-0263/ "https://peps.python.org/pep-0263/"), i.e. you can start your Cython source
file with an encoding comment and generally write your source code in UTF-8.
This impacts the encoding of byte strings and the conversion of unicode string
literals like `u'abcd'` to unicode objects.

## Automatic `typecheck`[¶](#automatic-typecheck "Link to this heading")

Rather than introducing a new keyword `typecheck` as explained in the
[Pyrex docs](https://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/version/Doc/Manual/special_methods.html "https://www.cosc.canterbury.ac.nz/greg.ewing/python/Pyrex/version/Doc/Manual/special_methods.html"),
Cython emits a (non-spoofable and faster) typecheck whenever
[`isinstance()`](https://docs.python.org/3/library/functions.html#isinstance "(in Python v3.13)") is used with an extension type as the second parameter.

## From \_\_future\_\_ directives[¶](#from-future-directives "Link to this heading")

Cython supports several `from __future__ import ...` directives, namely
`absolute_import`, `unicode_literals`, `print_function` and `division`.

With statements are always enabled.

## Pure Python mode[¶](#pure-python-mode "Link to this heading")

Cython has support for compiling `.py` files, and
accepting type annotations using decorators and other
valid Python syntax. This allows the same source to
be interpreted as straight Python, or compiled for
optimized results. See [Pure Python Mode](../tutorial/pure.html#pure-mode "../tutorial/pure.html#pure-mode") for more details.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Differences between Cython and Pyrex](# "#")
  + [Python 3 Support](#python-3-support "#python-3-support")
    - [List/Set/Dict Comprehensions](#list-set-dict-comprehensions "#list-set-dict-comprehensions")
    - [Keyword-only arguments](#keyword-only-arguments "#keyword-only-arguments")
  + [Conditional expressions “x if b else y”](#conditional-expressions-x-if-b-else-y "#conditional-expressions-x-if-b-else-y")
  + [cdef inline](#cdef-inline "#cdef-inline")
  + [Assignment on declaration (e.g. “cdef int spam = 5”)](#assignment-on-declaration-e-g-cdef-int-spam-5 "#assignment-on-declaration-e-g-cdef-int-spam-5")
  + [‘by’ expression in for loop (e.g. “for i from 0 <= i < 10 by 2”)](#by-expression-in-for-loop-e-g-for-i-from-0-i-10-by-2 "#by-expression-in-for-loop-e-g-for-i-from-0-i-10-by-2")
  + [Boolean int type (e.g. it acts like a c int, but coerces to/from python as a boolean)](#boolean-int-type-e-g-it-acts-like-a-c-int-but-coerces-to-from-python-as-a-boolean "#boolean-int-type-e-g-it-acts-like-a-c-int-but-coerces-to-from-python-as-a-boolean")
  + [Executable class bodies](#executable-class-bodies "#executable-class-bodies")
  + [cpdef functions](#cpdef-functions "#cpdef-functions")
  + [Automatic range conversion](#automatic-range-conversion "#automatic-range-conversion")
  + [More friendly type casting](#more-friendly-type-casting "#more-friendly-type-casting")
  + [Optional arguments in cdef/cpdef functions](#optional-arguments-in-cdef-cpdef-functions "#optional-arguments-in-cdef-cpdef-functions")
  + [Function pointers in structs](#function-pointers-in-structs "#function-pointers-in-structs")
  + [C++ Exception handling](#c-exception-handling "#c-exception-handling")
  + [Synonyms](#synonyms "#synonyms")
  + [Source code encoding](#source-code-encoding "#source-code-encoding")
  + [Automatic `typecheck`](#automatic-typecheck "#automatic-typecheck")
  + [From \_\_future\_\_ directives](#from-future-directives "#from-future-directives")
  + [Pure Python mode](#pure-python-mode "#pure-python-mode")

#### Previous topic

[Limitations](limitations.html "previous chapter")

#### Next topic

[Typed Memoryviews](memoryviews.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/pyrex_differences.rst.txt "../../_sources/src/userguide/pyrex_differences.rst.txt")

### Quick search

### Navigation

* [next](memoryviews.html "Typed Memoryviews")
* [previous](limitations.html "Limitations") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Differences between Cython and Pyrex

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

