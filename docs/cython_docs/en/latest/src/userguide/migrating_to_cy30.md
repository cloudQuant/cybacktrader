




Migrating from Cython 0.29 to 3.0 — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/migrating_to_cy30.html "/en/stable/src/userguide/migrating_to_cy30.html").

### Navigation

* [next](limitations.html "Limitations")
* [previous](limited_api.html "The Limited API and Stable ABI") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Migrating from Cython 0.29 to 3.0

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Migrating from Cython 0.29 to 3.0[¶](#migrating-from-cython-0-29-to-3-0 "Link to this heading")

Cython 3.0 is a major revision of the compiler and the language
that comes with some backwards incompatible changes.
This document lists the important ones and explains how to deal with
them in existing code.

## Python 3 syntax/semantics[¶](#python-3-syntax-semantics "Link to this heading")

Cython 3.0 now uses Python 3 syntax and semantics by default, which previously
required setting the `language_level` directive <compiler-directives> to
either `3` or `3str`.
The new default setting is now `language_level=3str`, which means Python 3
semantics, but unprefixed strings are `str` objects, i.e. unicode text strings
under Python 3 and byte strings under Python 2.7.

You can revert your code to the previous (Python 2.x) semantics by setting
`language_level=2`.

Further semantic changes due to the language level include:

* `/`-division uses the true (float) division operator, unless `cdivision` is enabled.
* `print` is a function, not a statement.
* Python classes that are defined without bases (`class C: ...`) are “new-style”
  classes also in Py2.x (if you never heard about “old-style classes”, you’re probably
  happy without them).
* Annotations (type hints) are now stored as strings.
  ([PEP 563](https://github.com/cython/cython/issues/2863 "https://github.com/cython/cython/issues/2863"))
* `StopIteration` handling in generators has been changed according to
  [PEP 479](https://www.python.org/dev/peps/pep-0479/ "https://www.python.org/dev/peps/pep-0479/").

## Python semantics[¶](#python-semantics "Link to this heading")

Some Python compatibility bugs were fixed, e.g.

* Subscripting (`x[1]`) now tries the mapping protocol before the sequence protocol.
  ([https://github.com/cython/cython/issues/1807](https://github.com/cython/cython/issues/1807 "https://github.com/cython/cython/issues/1807"))
* Exponentiation of integer literals now follows Python semantics and not C semantics.
  ([https://github.com/cython/cython/issues/2133](https://github.com/cython/cython/issues/2133 "https://github.com/cython/cython/issues/2133"))

## Binding functions[¶](#binding-functions "Link to this heading")

The [binding directive](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives") is now enabled by default.
This makes Cython compiled Python (`def`) functions mostly compatible
with normal (non-compiled) Python functions, regarding signature introspection,
annotations, etc.

It also makes them bind as methods in Python classes on attribute assignments,
thus the name.
If this is not intended, i.e. if a function is really meant to be a function
and never a method, you can disable the binding (and all other Python function
features) by setting `binding=False` or selectively adding a decorator
`@cython.binding(False)`.
In pure Python mode, the decorator was not available in Cython 0.29.16 yet,
but compiled code does not suffer from this.

We recommend, however, to keep the new function features and instead deal
with the binding issue using the standard Python `staticmethod()` builtin.

```
def func(self, b): ...

class MyClass(object):
    binding_method = func

    no_method = staticmethod(func)
```

## Namespace packages[¶](#namespace-packages "Link to this heading")

Cython now has support for loading pxd files also from namespace packages
according to [PEP-420](https://www.python.org/dev/peps/pep-0420/ "https://www.python.org/dev/peps/pep-0420/").
This might have an impact on the import path.

## NumPy C-API[¶](#numpy-c-api "Link to this heading")

Cython used to generate code that depended on the deprecated pre-NumPy-1.7 C-API.
This is no longer the case with Cython 3.0.

You can now define the macro `NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION`
to get rid of the long-standing build warnings that the compiled C module
uses a deprecated API. Either per file:

```
# distutils: define_macros=NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION
```

or by setting it in your Extensions in `setup.py`:

```
Extension(...
    define_macros=[("NPY_NO_DEPRECATED_API", "NPY_1_7_API_VERSION")]
)
```

One side-effect of the different C-API usage is that your code may now
require a call to the [NumPy C-API initialisation function](https://docs.scipy.org/doc/numpy-1.17.0/reference/c-api.array.html#importing-the-api "https://docs.scipy.org/doc/numpy-1.17.0/reference/c-api.array.html#importing-the-api")
where it previously got away without doing so.

In order to reduce the user impact here, Cython 3.0 will now call it
automatically when it sees `numpy` being cimported, but the function
not being used.
In the (hopefully rare) cases where this gets in the way, the internal
C-API initialisation can be disabled by faking the use of the function
without actually calling it, e.g.

```
# Explicitly disable the automatic initialisation of NumPy's C-API.
<void>import_array
```

## Class-private name mangling[¶](#class-private-name-mangling "Link to this heading")

Cython has been updated to follow the [Python rules for class-private names](https://docs.python.org/3/tutorial/classes.html#private-variables "https://docs.python.org/3/tutorial/classes.html#private-variables")
more closely. Essentially any name that starts with and doesn’t end with
`__` within a class is mangled with the class name. Most user code
should be unaffected – unlike in Python unmangled global names will
still be matched to ensure it is possible to access C names
beginning with `__`:

```
cdef extern void __foo()

class C: # or "cdef class"
   def call_foo(self):
       return __foo() # still calls the global name
```

What will no-longer work is overriding methods starting with `__` in
a `cdef class`:

```
cdef class Base:
    cdef __bar(self):
        return 1

    def call_bar(self):
        return self.__bar()

cdef class Derived(Base):
    cdef __bar(self):
        return 2
```

Here `Base.__bar` is mangled to `_Base__bar` and `Derived.__bar`
to `_Derived__bar`. Therefore `call_bar` will always call
`_Base__bar`. This matches established Python behaviour and applies
for `def`, `cdef` and `cpdef` methods and attributes.

## Arithmetic special methods[¶](#arithmetic-special-methods "Link to this heading")

The behaviour of arithmetic special methods (for example `__add__`
and `__pow__`) of cdef classes has changed in Cython 3.0. They now
support separate “reversed” versions of these methods (e.g.
`__radd__`, `__rpow__`) that behave like in pure Python.
The main incompatible change is that the type of the first operand
(usually `__self__`) is now assumed to be that of the defining class,
rather than relying on the user to test and cast the type of each operand.

The old behaviour can be restored with the
[directive](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives") `c_api_binop_methods=True`.
More details are given in [Arithmetic methods](special_methods.html#arithmetic-methods "special_methods.html#arithmetic-methods").

## Exception values and `noexcept`[¶](#exception-values-and-noexcept "Link to this heading")

`cdef` functions that are not `extern` now safely propagate Python
exceptions by default. Previously, they needed to explicitly be declared
with an [exception value](language_basics.html#error-return-values "language_basics.html#error-return-values") to prevent them from
swallowing exceptions. A new `noexcept` modifier can be used to declare
`cdef` functions that really will not raise exceptions.

In existing code, you should mainly look out for `cdef` functions
that are declared without an exception value:

```
cdef int spam(int x):
    pass

cdef void silent(int x):
    pass
```

If you left out the exception value by mistake, i.e., the function
should propagate Python exceptions, then the new behaviour will take
care of this for you, and correctly propagate any exceptions.
This was a common mistake in Cython code and the main reason to change the behaviour.

On the other hand, if you didn’t declare an exception value because
you want to avoid exceptions propagating out of this function, the new behaviour
will result in slightly less efficient code being generated, now involving an exception check.
To prevent that, you must declare the function explicitly as being
`noexcept`:

```
cdef int spam(int x) noexcept:
    pass

cdef void silent(int x) noexcept:
    pass
```

The behaviour for `cdef` functions that are also `extern` is
unchanged as `extern` functions are less likely to raise Python
exceptions and rather tend to be plain C functions. This mitigates
the effect of this change for code that talks to C libraries.

The behaviour for any `cdef` function that is declared with an
explicit exception value (e.g., `cdef int spam(int x) except -1`) is
also unchanged.

There is an easy-to-encounter performance pitfall here with `nogil` functions
with an implicit exception specification of `except *`. This can happen
most commonly when the return type is `void` (but in principle applies
to most non-numeric return types). In this case, Cython is forced to
re-acquire the GIL briefly after each call to check the exception state.
To avoid this overhead, either change the signature to `noexcept` (if
you have determined that it’s suitable to do so), or to returning an `int`
instead to let Cython use the `int` as an error flag
(by default, `-1` triggers the exception check).

Note

The unsafe legacy behaviour of not propagating exceptions by default can be enabled by
setting `legacy_implicit_noexcept` [compiler directive](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives")
to `True`.

## Annotation typing[¶](#annotation-typing "Link to this heading")

Cython 3 has made substantial improvements in recognising types in
annotations and it is well worth reading
[the pure Python tutorial](../tutorial/pure.html#pep484-type-annotations "../tutorial/pure.html#pep484-type-annotations") to understand
some of the improvements.

A notable backwards-incompatible change is that `x: int` is now typed
such that `x` is an exact Python `int` (Cython 0.29 would accept
any Python object for `x`), unless the language level is explicitly
set to 2. To mitigate the effect, Cython 3.0 still accepts both Python
`int` and `long` values under Python 2.x.

One potential issue you may encounter is that types like `typing.List`
are now understood in annotations (where previously they were ignored)
and are interpreted to mean exact `list`. This is stricter than
the interpretation specified in PEP-484, which also allows subclasses.

To make it easier to handle cases where your interpretation of type
annotations differs from Cython’s, Cython 3 now supports setting the
`annotation_typing` [directive](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives") on a
per-class or per-function level.

## C++ postincrement/postdecrement operator[¶](#c-postincrement-postdecrement-operator "Link to this heading")

Cython 3 differentiates between pre/post-increment and pre/post-decrement
operators (Cython 0.29 implemented both as pre(in/de)crement operator).
This only has an effect when using `cython.operator.postdecrement` / `cython.operator.postincrement`.
When running into an error it is required to add the corresponding operator:

```
cdef cppclass Example:
    Example operator++(int)
    Example operator--(int)
```

## Public Declarations in C++[¶](#public-declarations-in-c "Link to this heading")

Public declarations in C++ mode are exported as C++ API in Cython 3, using `extern "C++"`.
This behaviour can be changed by setting the export keyword using the `CYTHON_EXTERN_C` macro
to allow Cython modules to be implemented in C++ but callable from C.

## `**` power operator[¶](#power-operator "Link to this heading")

Cython 3 has changed the behaviour of the power operator to be
more like Python. The consequences are that

1. `a**b` of two ints may return a floating point type,
2. `a**b` of one or more non-complex floating point numbers may
   return a complex number.

The old behaviour can be restored by setting the `cpow`
[compiler directive](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives") to `True`.

## Deprecation of `DEF` / `IF`[¶](#deprecation-of-def-if "Link to this heading")

The [conditional compilation feature](language_basics.html#conditional-compilation "language_basics.html#conditional-compilation") has been
deprecated and should no longer be used in new code.
It is expected to get removed in some future release.

Usages of `DEF` should be replaced by:

* global cdef constants
* global enums (C or Python)
* C macros, e.g. defined in [verbatim C code](external_C_code.html#verbatim-c "external_C_code.html#verbatim-c")
* the usual Python mechanisms for sharing values across modules and usages

Usages of `IF` should be replaced by runtime conditions and conditional Python imports,
i.e. the usual Python patterns. Specifically:

* Non-trivial or platform specific functionalities can often be separated out into optional
  Cython modules that can be imported/used at need (with regular runtime Python imports).
* Version specific struct field names that are unused can be left out of a Cython
  [extern struct definition](external_C_code.html#external-c-code "external_C_code.html#external-c-code") (which does not have to be complete).
  If they are used, C shims to access them with functions or macros can often be used,
  easily defined in [verbatim C code](external_C_code.html#verbatim-c "external_C_code.html#verbatim-c").
* Largely different layouts of extern structs can be declared in Cython as separate structs
  with different Cython names and different (e.g. version/platform dependent) attributes,
  but with the C struct name provided as [same cname string](external_C_code.html#resolve-conflicts "external_C_code.html#resolve-conflicts").
  This allows their usage from more use case specific code that can be included and
  reused from different optional modules.
* If all else fails, code generation using the [Tempita template engine](tempita.html#tempita "tempita.html#tempita") can be used as a last resort.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Migrating from Cython 0.29 to 3.0](# "#")
  + [Python 3 syntax/semantics](#python-3-syntax-semantics "#python-3-syntax-semantics")
  + [Python semantics](#python-semantics "#python-semantics")
  + [Binding functions](#binding-functions "#binding-functions")
  + [Namespace packages](#namespace-packages "#namespace-packages")
  + [NumPy C-API](#numpy-c-api "#numpy-c-api")
  + [Class-private name mangling](#class-private-name-mangling "#class-private-name-mangling")
  + [Arithmetic special methods](#arithmetic-special-methods "#arithmetic-special-methods")
  + [Exception values and `noexcept`](#exception-values-and-noexcept "#exception-values-and-noexcept")
  + [Annotation typing](#annotation-typing "#annotation-typing")
  + [C++ postincrement/postdecrement operator](#c-postincrement-postdecrement-operator "#c-postincrement-postdecrement-operator")
  + [Public Declarations in C++](#public-declarations-in-c "#public-declarations-in-c")
  + [`**` power operator](#power-operator "#power-operator")
  + [Deprecation of `DEF` / `IF`](#deprecation-of-def-if "#deprecation-of-def-if")

#### Previous topic

[The Limited API and Stable ABI](limited_api.html "previous chapter")

#### Next topic

[Limitations](limitations.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/migrating_to_cy30.rst.txt "../../_sources/src/userguide/migrating_to_cy30.rst.txt")

### Quick search

### Navigation

* [next](limitations.html "Limitations")
* [previous](limited_api.html "The Limited API and Stable ABI") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Migrating from Cython 0.29 to 3.0

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

