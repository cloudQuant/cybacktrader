




Faster code via static typing — Cython 3.1.4 documentation

### Navigation

* [next](../tutorial/index.html "Tutorials")
* [previous](build.html "Building Cython code") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Getting Started](index.html "index.html") »
* Faster code via static typing

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Faster code via static typing[¶](#faster-code-via-static-typing "Link to this heading")

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

Cython is a Python compiler. This means that it can compile normal
Python code without changes (with a few obvious exceptions of some as-yet
unsupported language features, see [Cython limitations](../userguide/limitations.html#cython-limitations "../userguide/limitations.html#cython-limitations")).
However, for performance critical code, it is often helpful to add
static type declarations, as they will allow Cython to step out of the
dynamic nature of the Python code and generate simpler and faster C code
- sometimes faster by orders of magnitude.

It must be noted, however, that type declarations can make the source
code more verbose and thus less readable. It is therefore discouraged
to use them without good reason, such as where benchmarks prove
that they really make the code substantially faster in a performance
critical section. Typically a few types in the right spots go a long way.

All C types are available for type declarations: integer and floating
point types, complex numbers, structs, unions and pointer types.
Cython can automatically and correctly convert between the types on
assignment. This also includes Python’s arbitrary size integer types,
where value overflows on conversion to a C type will raise a Python
`OverflowError` at runtime. (It does not, however, check for overflow
when doing arithmetic.) The generated C code will handle the
platform dependent sizes of C types correctly and safely in this case.

Types are declared via the cdef keyword.

## Typing Variables[¶](#typing-variables "Link to this heading")

Consider the following pure Python code:

integrate.py[¶](#id2 "Link to this code")

```
def f(x):
    return x ** 2 - x


def integrate_f(a, b, N):
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
```

Simply compiling this in Cython merely gives a 35% speedup. This is
better than nothing, but adding some static types can make a much larger
difference.

With additional type declarations, this might look like:

Pure PythonCython

integrate\_cy.py[¶](#id3 "Link to this code")

```
def f(x: cython.double):
    return x ** 2 - x


def integrate_f(a: cython.double, b: cython.double, N: cython.int):
    i: cython.int
    s: cython.double
    dx: cython.double
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
```

integrate\_cy.pyx[¶](#id4 "Link to this code")

```
def f(double x):
    return x ** 2 - x


def integrate_f(double a, double b, int N):
    cdef int i
    cdef double s
    cdef double dx
    s = 0
    dx = (b - a) / N
    for i in range(N):
        s += f(a + i * dx)
    return s * dx
```

Since the iterator variable `i` is typed with C semantics, the for-loop will be compiled
to pure C code. Typing `a`, `s` and `dx` is important as they are involved
in arithmetic within the for-loop; typing `b` and `N` makes less of a
difference, but in this case it is not much extra work to be
consistent and type the entire function.

This results in a 4 times speedup over the pure Python version.

## Typing Functions[¶](#typing-functions "Link to this heading")

Python function calls can be expensive – in Cython doubly so because
one might need to convert to and from Python objects to do the call.
In our example above, the argument is assumed to be a C double both inside `f()`
and in the call to it, yet a Python `float` object must be constructed around the
argument in order to pass it.

Therefore, Cython provides a way for declaring a C-style function,
the Cython specific `cdef` statement, as well as the `@cfunc` decorator to
declare C-style functions in Python syntax. Both approaches are
equivalent and produce the same C code:

Pure PythonCython

```
@cython.cfunc
@cython.exceptval(-2, check=True)
def f(x: cython.double) -> cython.double:
    return x ** 2 - x
```

```
cdef double f(double x) except? -2:
    return x ** 2 - x
```

Some form of except-modifier should usually be added, otherwise Cython
will not be able to propagate exceptions raised in the function (or a
function it calls). The `except? -2` means that an error will be checked
for if `-2` is returned (though the `?` indicates that `-2` may also
be used as a valid return value). The same can be expressed using only Python
syntax with the decorator `@exceptval(-2, check=True)`.

Alternatively, the slower `except *` is always
safe. An except clause can be left out if the function returns a Python
object or if it is guaranteed that an exception will not be raised
within the function call. Again, Cython provides the decorator `@exceptval(check=True)`
providing the same functionality.

A side-effect of `cdef` (and the `@cfunc` decorator) is that the function is no longer
visible from Python-space, as Python wouldn’t know how to call it. It is also no
longer possible to change `f()` at runtime.

Using the `cpdef` keyword instead of `cdef`, a Python wrapper is also
created, so that the function is available both from Cython (fast, passing
typed values directly) and from Python (wrapping values in Python
objects). In fact, `cpdef` does not just provide a Python wrapper, it also
installs logic to allow the method to be overridden by python methods, even
when called from within cython. This does add a tiny overhead compared to `cdef`
methods. Again, Cython provides a `@ccall` decorator which provides the same
functionality as `cpdef` keyword.

Speedup: 150 times over pure Python.

## Determining where to add types[¶](#determining-where-to-add-types "Link to this heading")

Because static typing is often the key to large speed gains, beginners
often have a tendency to type everything in sight. This cuts down on both
readability and flexibility, and can even slow things down (e.g. by adding
unnecessary type checks, conversions, or slow buffer unpacking).
On the other hand, it is easy to kill
performance by forgetting to type a critical loop variable. Two essential
tools to help with this task are profiling and annotation.
Profiling should be the first step of any optimization effort, and can
tell you where you are spending your time. Cython’s annotation can then
tell you why your code is taking time.

Using the `-a` switch to the `cython` command line program (or
following a link from the Sage notebook) results in an HTML report
of Cython code interleaved with the generated C code. Lines are
colored according to the level of “typedness” –
white lines translate to pure C,
while lines that require the Python C-API are yellow
(darker as they translate to more C-API interaction).
Lines that translate to C code have a plus (`+`) in front
and can be clicked to show the generated code.

This report is invaluable when optimizing a function for speed,
and for determining when it is possible to [release the GIL](../userguide/external_C_code.html#nogil "../userguide/external_C_code.html#nogil")
(be aware that releasing the GIL is only useful under limited
circumstances, see [Cython and the GIL](../userguide/nogil.html#cython-and-gil "../userguide/nogil.html#cython-and-gil") for more details):
in general, a `nogil` block may contain only “white” code.

Pure PythonCython

![../../_images/htmlreport_py.png](../../_images/htmlreport_py.png)

![../../_images/htmlreport_pyx.png](../../_images/htmlreport_pyx.png)

Note that Cython deduces the type of local variables based on their assignments
(including as loop variable targets) which can also cut down on the need to
explicitly specify types everywhere.
For example, declaring `dx` to be of type double above is unnecessary,
as is declaring the type of `s` in the last version (where the return type
of `f` is known to be a C double.) A notable exception, however, is
integer types used in arithmetic expressions, as Cython is unable to ensure
that an overflow would not occur (and so falls back to `object` in case
Python’s bignums are needed). To allow inference of C integer types, set the
`infer_types` [directive](../userguide/source_files_and_compilation.html#compiler-directives "../userguide/source_files_and_compilation.html#compiler-directives") to `True`. This directive
does a work similar to the `auto` keyword in C++ for the readers who are familiar
with this language feature. It can be of great help to cut down on the need to type
everything, but it also can lead to surprises. Especially if one isn’t familiar with
arithmetic expressions with c types. A quick overview of those
can be found [here](https://www.eskimo.com/~scs/cclass/int/sx4cb.html "https://www.eskimo.com/~scs/cclass/int/sx4cb.html").

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Faster code via static typing](# "#")
  + [Typing Variables](#typing-variables "#typing-variables")
  + [Typing Functions](#typing-functions "#typing-functions")
  + [Determining where to add types](#determining-where-to-add-types "#determining-where-to-add-types")

#### Previous topic

[Building Cython code](build.html "previous chapter")

#### Next topic

[Tutorials](../tutorial/index.html "next chapter")

### This Page

* [Show Source](../../_sources/src/quickstart/cythonize.rst.txt "../../_sources/src/quickstart/cythonize.rst.txt")

### Quick search

### Navigation

* [next](../tutorial/index.html "Tutorials")
* [previous](build.html "Building Cython code") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Getting Started](index.html "index.html") »
* Faster code via static typing

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

