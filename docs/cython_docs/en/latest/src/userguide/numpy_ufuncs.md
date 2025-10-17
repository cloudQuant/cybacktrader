




Creating Numpy ufuncs — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/numpy_ufuncs.html "/en/stable/src/userguide/numpy_ufuncs.html").

### Navigation

* [next](numpy_pythran.html "Pythran as a Numpy backend")
* [previous](numpy_tutorial.html "Cython for NumPy users") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Creating Numpy ufuncs

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Creating Numpy ufuncs[¶](#creating-numpy-ufuncs "Link to this heading")

Note

This page uses two different syntax variants:

* Cython specific `cdef` syntax, which was designed to make type declarations
  concise and easily readable from a C/C++ perspective.
* Pure Python syntax which allows static Cython type declarations in
  [pure Python code](../tutorial/pure.html#pep484-type-annotations "../tutorial/pure.html#pep484-type-annotations"),
  following [PEP-484](https://www.python.org/dev/peps/pep-0484/ "https://www.python.org/dev/peps/pep-0484/") type hints
  and [PEP 526](https://www.python.org/dev/peps/pep-0526/ "https://www.python.org/dev/peps/pep-0526/") variable annotations.

  To make use of C data types in Python syntax, you need to import the special
  `cython` module in the Python module that you want to compile, e.g.

  ```
  import cython
  ```

  If you use the pure Python syntax we strongly recommend you use a recent
  Cython 3 release, since significant improvements have been made here
  compared to the 0.29.x releases.

Numpy supports a [special type of function called a ufunc](https://numpy.org/doc/stable/reference/ufuncs.html "https://numpy.org/doc/stable/reference/ufuncs.html") .
These support array broadcasting (i.e. the ability to handle arguments with any
number of dimensions), alongside other useful features.

Cython can generate a ufunc from a Cython C function by tagging it with the `@cython.ufunc`
decorator. The input and output argument types should be scalar variables (“generic ufuncs” are
not yet supported) and should either by Python objects or simple numeric types. The body
of such a function is inserted into an efficient, compiled loop.

Pure PythonCython

```
import cython

@cython.ufunc
@cython.cfunc
def add_one(x: cython.double) -> cython.double:
    # of course, this simple operation can already by done efficiently in Numpy!
    return x+1
```

```
cimport cython


@cython.ufunc
cdef double add_one(double x):
    # of course, this simple operation can already by done efficiently in Numpy!
    return x+1
```

You can have as many arguments to your function as you like. If you want to have multiple
output arguments then you can use the [ctuple syntax](language_basics.html#typing-types "language_basics.html#typing-types"):

Pure PythonCython

```
import cython

@cython.ufunc
@cython.cfunc
def add_one_add_two(x: cython.int) -> tuple[cython.int, cython.int]:
    return x+1, x+2
```

```
cimport cython


@cython.ufunc
cdef (int, int) add_one_add_two(int x):
    return x+1, x+2
```

If you want to accept multiple different argument types then you can use [Fused Types (Templates)](fusedtypes.html#fusedtypes "fusedtypes.html#fusedtypes"):

Pure PythonCython

```
import cython

@cython.ufunc
@cython.cfunc
def generic_add_one(x: cython.numeric) -> cython.numeric:
    return x+1
```

```
cimport cython


@cython.ufunc
cdef cython.numeric generic_add_one(cython.numeric x):
    return x+1
```

Finally, if you declare the `cdef`/`@cfunc` function as `nogil` then Cython will release the
[GIL](glossary.html#term-Global-Interpreter-Lock-or-GIL "glossary.html#term-Global-Interpreter-Lock-or-GIL") once in the generated ufunc. This is a slight difference
from the general behaviour of `nogil` functions (they generally do not automatically
release the GIL, but instead can be run without the GIL).

This feature relies on Numpy. Therefore if you create a ufunc in
Cython, you must have the Numpy headers available when you build the generated C code, and
users of your module must have Numpy installed when they run it.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Cython for NumPy users](numpy_tutorial.html "previous chapter")

#### Next topic

[Pythran as a Numpy backend](numpy_pythran.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/numpy_ufuncs.rst.txt "../../_sources/src/userguide/numpy_ufuncs.rst.txt")

### Quick search

### Navigation

* [next](numpy_pythran.html "Pythran as a Numpy backend")
* [previous](numpy_tutorial.html "Cython for NumPy users") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Creating Numpy ufuncs

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

