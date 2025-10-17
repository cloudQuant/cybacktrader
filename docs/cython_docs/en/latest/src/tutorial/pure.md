




Pure Python Mode — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/tutorial/pure.html "/en/stable/src/tutorial/pure.html").

### Navigation

* [next](numpy.html "Working with NumPy")
* [previous](embedding.html "Embedding Cython modules in C/C++ applications") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Pure Python Mode

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Pure Python Mode[¶](#pure-python-mode "Link to this heading")

In some cases, it’s desirable to speed up Python code without losing the
ability to run it with the Python interpreter. While pure Python scripts
can be compiled with Cython, it usually results only in a speed gain of
about 20%-50%.

To go beyond that, Cython provides language constructs to add static typing
and cythonic functionalities to a Python module to make it run much faster
when compiled, while still allowing it to be interpreted.
This is accomplished via an augmenting `.pxd` file, via Python
type [PEP-484 type annotations](#pep484-type-annotations "#pep484-type-annotations") (following
[PEP 484](https://www.python.org/dev/peps/pep-0484/ "https://www.python.org/dev/peps/pep-0484/") and
[PEP 526](https://www.python.org/dev/peps/pep-0526/ "https://www.python.org/dev/peps/pep-0526/")), and/or
via special functions and decorators available after importing the magic
`cython` module. All three ways can be combined at need, although
projects would commonly decide on a specific way to keep the static type
information easy to manage.

Although it is not typically recommended over writing straight Cython code
in a `.pyx` file, there are legitimate reasons to do this - easier
testing and debugging, collaboration with pure Python developers, etc.
In pure mode, you are more or less restricted to code that can be expressed
(or at least emulated) in Python, plus static type declarations. Anything
beyond that can only be done in .pyx files with extended language syntax,
because it depends on features of the Cython compiler.

## Augmenting .pxd[¶](#augmenting-pxd "Link to this heading")

Using an augmenting `.pxd` allows to let the original `.py` file
completely untouched. On the other hand, one needs to maintain both the
`.pxd` and the `.py` to keep them in sync.

While declarations in a `.pyx` file must correspond exactly with those
of a `.pxd` file with the same name (and any contradiction results in
a compile time error, see [pxd files](pxd_files.html "pxd_files.html")), the untyped definitions in a
`.py` file can be overridden and augmented with static types by the more
specific ones present in a `.pxd`.

If a `.pxd` file is found with the same name as the `.py` file
being compiled, it will be searched for [`cdef`](../userguide/language_basics.html#cdef "../userguide/language_basics.html#cdef") classes and
[`cdef`](../userguide/language_basics.html#cdef "../userguide/language_basics.html#cdef")/[`cpdef`](../userguide/language_basics.html#cpdef "../userguide/language_basics.html#cpdef") functions and methods. The compiler will
then convert the corresponding classes/functions/methods in the `.py`
file to be of the declared type. Thus if one has a file `A.py`:

```
def myfunction(x, y=2):
    a = x - y
    return a + x * y

def _helper(a):
    return a + 1

class A:
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    def foo(self, x):
        print(x + _helper(1.0))
```

and adds `A.pxd`:

```
cpdef int myfunction(int x, int y=*)
cdef double _helper(double a)

cdef class A:
    cdef public int a, b
    cpdef foo(self, double x)
```

then Cython will compile the `A.py` as if it had been written as follows:

```
cpdef int myfunction(int x, int y=2):
    a = x - y
    return a + x * y

cdef double _helper(double a):
    return a + 1

cdef class A:
    cdef public int a, b
    def __init__(self, b=0):
        self.a = 3
        self.b = b

    cpdef foo(self, double x):
        print(x + _helper(1.0))
```

Notice how in order to provide the Python wrappers to the definitions
in the `.pxd`, that is, to be accessible from Python,

* Python visible function signatures must be declared as cpdef (with default
  arguments replaced by a \* to avoid repetition):

  ```
  cpdef int myfunction(int x, int y=*)
  ```
* C function signatures of internal functions can be declared as cdef:

  ```
  cdef double _helper(double a)
  ```
* cdef classes (extension types) are declared as cdef class;
* cdef class attributes must be declared as cdef public if read/write
  Python access is needed, cdef readonly for read-only Python access, or
  plain cdef for internal C level attributes;
* cdef class methods must be declared as cpdef for Python visible
  methods or cdef for internal C methods.

In the example above, the type of the local variable a in myfunction()
is not fixed and will thus be a [Python object](../userguide/glossary.html#term-Python-object "../userguide/glossary.html#term-Python-object"). To statically type it, one
can use Cython’s `@cython.locals` decorator (see [Magic Attributes](#magic-attributes "#magic-attributes"),
and [Magic Attributes within the .pxd](#magic-attributes-pxd "#magic-attributes-pxd")).

Normal Python ([`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.14)")) functions cannot be declared in `.pxd`
files. It is therefore currently impossible to override the types of plain
Python functions in `.pxd` files, e.g. to override types of their local
variables. In most cases, declaring them as cpdef will work as expected.

## Magic Attributes[¶](#magic-attributes "Link to this heading")

Special decorators are available from the magic `cython` module that can
be used to add static typing within the Python file, while being ignored
by the interpreter.

This option adds the `cython` module dependency to the original code, but
does not require to maintain a supplementary `.pxd` file. Cython
provides a fake version of this module as Cython.Shadow, which is available
as cython.py when Cython is installed, but can be copied to be used by other
modules when Cython is not installed.

### “Compiled” switch[¶](#compiled-switch "Link to this heading")

* `compiled` is a special variable which is set to `True` when the compiler
  runs, and `False` in the interpreter. Thus, the code

  ```
  import cython

  if cython.compiled:
      print("Yep, I'm compiled.")
  else:
      print("Just a lowly interpreted script.")
  ```

  will behave differently depending on whether or not the code is executed as a
  compiled extension (`.so`/`.pyd`) module or a plain `.py`
  file.

### Static typing[¶](#static-typing "Link to this heading")

* `cython.declare` declares a typed variable in the current scope, which can be
  used in place of the `cdef type var [= value]` construct. This has two forms,
  the first as an assignment (useful as it creates a declaration in interpreted
  mode as well):

  ```
  import cython

  x = cython.declare(cython.int)              # cdef int x
  y = cython.declare(cython.double, 0.57721)  # cdef double y = 0.57721
  ```

  and the second mode as a simple function call:

  ```
  import cython

  cython.declare(x=cython.int, y=cython.double)  # cdef int x; cdef double y
  ```

  It can also be used to define extension type private, readonly and public attributes:

  ```
  import cython


  @cython.cclass
  class A:
      cython.declare(a=cython.int, b=cython.int)
      c = cython.declare(cython.int, visibility='public')
      d = cython.declare(cython.int)  # private by default.
      e = cython.declare(cython.int, visibility='readonly')

      def __init__(self, a, b, c, d=5, e=3):
          self.a = a
          self.b = b
          self.c = c
          self.d = d
          self.e = e
  ```
* `@cython.locals` is a decorator that is used to specify the types of local
  variables in the function body (including the arguments):

  ```
  import cython

  @cython.locals(a=cython.long, b=cython.long, n=cython.longlong)
  def foo(a, b, x, y):
      n = a * b
      # ...
  ```
* `@cython.returns(<type>)` specifies the function’s return type.
* `@cython.exceptval(value=None, *, check=False)` specifies the function’s exception
  return value and exception check semantics as follows:

  ```
  @exceptval(-1)               # cdef int func() except -1:
  @exceptval(-1, check=False)  # cdef int func() except -1:
  @exceptval(check=True)       # cdef int func() except *:
  @exceptval(-1, check=True)   # cdef int func() except? -1:
  @exceptval(check=False)      # no exception checking/propagation
  ```

  If exception propagation is disabled, any Python exceptions that are raised
  inside of the function will be printed and ignored.

### C types[¶](#c-types "Link to this heading")

There are numerous types built into the Cython module. It provides all the
standard C types, namely `char`, `short`, `int`, `long`, `longlong`
as well as their unsigned versions `uchar`, `ushort`, `uint`, `ulong`,
`ulonglong`. The special `bint` type is used for C boolean values and
[`Py_ssize_t`](https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t "(in Python v3.14)") for (signed) sizes of Python containers.

For each type, there are pointer types `p_int`, `pp_int`, etc., up to
three levels deep in interpreted mode, and infinitely deep in compiled mode.
Further pointer types can be constructed with `cython.pointer[cython.int]`
(or `cython.pointer(cython.int)` for compatibility with Cython versions before 3.1),
and arrays as `cython.int[10]`. A limited attempt is made to emulate these
more complex types, but only so much can be done from the Python language.

The Python types int, long and bool are interpreted as C `int`, `long`
and `bint` respectively. Also, the Python builtin types `list`, `dict`,
`tuple`, etc. may be used, as well as any user defined types.

Typed C-tuples can be declared as a tuple of C types.

### Extension types and cdef functions[¶](#extension-types-and-cdef-functions "Link to this heading")

* The class decorator `@cython.cclass` creates a `cdef class`.
* The function/method decorator `@cython.cfunc` creates a [`cdef`](../userguide/language_basics.html#cdef "../userguide/language_basics.html#cdef") function.
* `@cython.ccall` creates a [`cpdef`](../userguide/language_basics.html#cpdef "../userguide/language_basics.html#cpdef") function, i.e. one that Cython code
  can call at the C level.
* `@cython.locals` declares local variables (see above). It can also be used to
  declare types for arguments, i.e. the local variables that are used in the
  signature.
* `@cython.inline` is the equivalent of the C `inline` modifier.
* `@cython.final` terminates the inheritance chain by preventing a type from
  being used as a base class, or a method from being overridden in subtypes.
  This enables certain optimisations such as inlined method calls.

Here is an example of a [`cdef`](../userguide/language_basics.html#cdef "../userguide/language_basics.html#cdef") function:

```
@cython.cfunc
@cython.returns(cython.bint)
@cython.locals(a=cython.int, b=cython.int)
def c_compare(a,b):
    return a == b
```

### Managing the Global Interpreter Lock[¶](#managing-the-global-interpreter-lock "Link to this heading")

* `cython.nogil` can be used as a context manager or as a decorator to replace the [`nogil`](../userguide/external_C_code.html#nogil "../userguide/external_C_code.html#nogil") keyword:

  ```
  with cython.nogil:
      # code block with the GIL released

  @cython.nogil
  @cython.cfunc
  def func_released_gil() -> cython.int:
      # function that can be run with the GIL released
  ```

  Note that the two uses differ: the context manager releases the GIL while the decorator marks that a
  function can be run without the GIL. See [Cython and the GIL](../userguide/nogil.html#cython-and-gil "../userguide/nogil.html#cython-and-gil") for more details.
* `cython.gil` can be used as a context manager to replace the [`gil`](../userguide/external_C_code.html#gil "../userguide/external_C_code.html#gil") keyword:

  ```
  with cython.gil:
      # code block with the GIL acquired
  ```

  Note

  Cython currently does not support the `@cython.with_gil` decorator.

Both directives accept an optional boolean parameter for conditionally
releasing or acquiring the GIL. The condition must be constant (at compile time):

```
with cython.nogil(False):
    # code block with the GIL not released

@cython.nogil(True)
@cython.cfunc
def func_released_gil() -> cython.int:
    # function with the GIL released

with cython.gil(False):
    # code block with the GIL not acquired

with cython.gil(True):
    # code block with the GIL acquired
```

A common use case for conditionally acquiring and releasing the GIL are fused types
that allow different GIL handling depending on the specific type (see [Conditional Acquiring / Releasing the GIL](../userguide/external_C_code.html#gil-conditional "../userguide/external_C_code.html#gil-conditional")).

### cimports[¶](#cimports "Link to this heading")

The special `cython.cimports` package name gives access to cimports
in code that uses Python syntax. Note that this does not mean that C
libraries become available to Python code. It only means that you can
tell Cython what cimports you want to use, without requiring special
syntax. Running such code in plain Python will fail.

```
from cython.cimports.libc import math

def use_libc_math():
    return math.ceil(5.5)
```

Since such code must necessarily refer to the non-existing
`cython.cimports` ‘package’, the plain cimport form
`cimport cython.cimports...` is not available.
You must use the form `from cython.cimports...`.

### Further Cython functions and declarations[¶](#further-cython-functions-and-declarations "Link to this heading")

* `address` is used in place of the `&` operator:

  ```
  cython.declare(x=cython.int, x_ptr=cython.p_int)
  x_ptr = cython.address(x)
  ```
* `sizeof` emulates the sizeof operator. It can take both types and
  expressions.

  ```
  cython.declare(n=cython.longlong)
  print(cython.sizeof(cython.longlong))
  print(cython.sizeof(n))
  ```
* `typeof` returns a string representation of the argument’s type for debugging purposes. It can take expressions.

  ```
  cython.declare(n=cython.longlong)
  print(cython.typeof(n))
  ```
* `struct` can be used to create struct types.:

  ```
  MyStruct = cython.struct(x=cython.int, y=cython.int, data=cython.double)
  a = cython.declare(MyStruct)
  ```

  is equivalent to the code:

  ```
  cdef struct MyStruct:
      int x
      int y
      double data

  cdef MyStruct a
  ```
* `union` creates union types with exactly the same syntax as `struct`.
* `typedef` defines a type under a given name:

  ```
  T = cython.typedef(cython.p_int)   # ctypedef int* T
  ```
* `cast` will (unsafely) reinterpret an expression type. `cython.cast(T, t)`
  is equivalent to `<T>t`. The first attribute must be a type, the second is
  the expression to cast. Specifying the optional keyword argument
  `typecheck=True` has the semantics of `<T?>t`.

  ```
  t1 = cython.cast(T, t)
  t2 = cython.cast(T, t, typecheck=True)
  ```
* `fused_type` creates a new type definition that refers to the multiple types.
  The following example declares a new type called `my_fused_type` which can
  be either an `int` or a `double`.:

  ```
  my_fused_type = cython.fused_type(cython.int, cython.float)
  ```

### Magic Attributes within the .pxd[¶](#magic-attributes-within-the-pxd "Link to this heading")

The special cython module can also be imported and used within the augmenting
`.pxd` file. For example, the following Python file `dostuff.py`:

```
def dostuff(n):
    t = 0
    for i in range(n):
        t += i
    return t
```

can be augmented with the following `.pxd` file `dostuff.pxd`:

```
import cython

@cython.locals(t=cython.int, i=cython.int)
cpdef int dostuff(int n)
```

The `cython.declare()` function can be used to specify types for global
variables in the augmenting `.pxd` file.

## PEP-484 type annotations[¶](#pep-484-type-annotations "Link to this heading")

Python [type hints](https://www.python.org/dev/peps/pep-0484 "https://www.python.org/dev/peps/pep-0484")
can be used to declare argument types, as shown in the
following example:

```
import cython

def func(foo: dict, bar: cython.int) -> tuple:
    foo["hello world"] = 3 + bar
    return foo, 5
```

Note the use of `cython.int` rather than `int` - Cython does not translate
an `int` annotation to a C integer by default since the behaviour can be
quite different with respect to overflow and division.

Annotations on global variables are currently ignored. This is because we expect
annotation-typed code to be in majority written for Python, and global type annotations
would turn the Python variable into an internal C variable, thus removing it from the
module dict. To declare global variables as typed C variables, use `@cython.declare()`.

Annotations can be combined with the `@cython.exceptval()` decorator for non-Python
return types:

```
import cython

@cython.exceptval(-1)
def func(x: cython.int) -> cython.int:
    if x < 0:
        raise ValueError("need integer >= 0")
    return x + 1
```

Note that the default exception handling behaviour when returning C numeric types
is to check for `-1`, and if that was returned, check Python’s error indicator
for an exception. This means, if no `@exceptval` decorator is provided, and the
return type is a numeric type, then the default with type annotations is
`@exceptval(-1, check=True)`, in order to make sure that exceptions are correctly
and efficiently reported to the caller. Exception propagation can be disabled
explicitly with `@exceptval(check=False)`, in which case any Python exceptions
raised inside of the function will be printed and ignored.

Since version 0.27, Cython also supports the variable annotations defined
in [PEP 526](https://www.python.org/dev/peps/pep-0526/ "https://www.python.org/dev/peps/pep-0526/"). This allows to
declare types of variables in a Python 3.6 compatible way as follows:

```
import cython

def func():
    # Cython types are evaluated as for cdef declarations
    x: cython.int               # cdef int x
    y: cython.double = 0.57721  # cdef double y = 0.57721
    z: cython.float = 0.57721   # cdef float z  = 0.57721

    # Python types shadow Cython types for compatibility reasons
    a: float = 0.54321          # cdef double a = 0.54321
    b: int = 5                  # cdef object b = 5
    c: long = 6                 # cdef object c = 6
    pass

@cython.cclass
class A:
    a: cython.int
    b: cython.int

    def __init__(self, b=0):
        self.a = 3
        self.b = b
```

There is currently no way to express the visibility of object attributes.

### Disabling annotations[¶](#disabling-annotations "Link to this heading")

To avoid conflicts with other kinds of annotation
usages, Cython’s use of annotations to specify types can be disabled with the
`annotation_typing` [compiler directive](../userguide/source_files_and_compilation.html#compiler-directives "../userguide/source_files_and_compilation.html#compiler-directives"). From Cython 3
you can use this as a decorator or a with statement, as shown in the following example:

```
import cython

@cython.annotation_typing(False)
def function_without_typing(a: int, b: int) -> int:
    """Cython is ignoring annotations in this function"""
    c: int = a + b
    return c * a


@cython.annotation_typing(False)
@cython.cclass
class NotAnnotatedClass:
    """Cython is ignoring annotatons in this class except annotated_method"""
    d: dict

    def __init__(self, dictionary: dict):
        self.d = dictionary

    @cython.annotation_typing(True)
    def annotated_method(self, key: str, a: cython.int, b: cython.int):
        prefixed_key: str = 'prefix_' + key
        self.d[prefixed_key] = a + b


def annotated_function(a: cython.int, b: cython.int):
    s: cython.int = a + b
    with cython.annotation_typing(False):
        # Cython is ignoring annotations within this code block
        c: list = []
    c.append(a)
    c.append(b)
    c.append(s)
    return c
```

### `typing` Module[¶](#typing-module "Link to this heading")

Support for the full range of annotations described by PEP-484 is not yet
complete. Cython 3 currently understands the following features from the
`typing` module:

* `Optional[tp]`, which is interpreted as `tp or None`;
* `Union[tp, None]` or `Union[None, tp]`, which is interpreted as `tp or None`;
* typed containers such as `List[str]`, which is interpreted as `list`. The
  hint that the elements are of type `str` is currently ignored;
* `Tuple[...]`, which is converted into a Cython C-tuple where possible
  and a regular Python `tuple` otherwise.
* `ClassVar[...]`, which is understood in the context of
  `cdef class` or `@cython.cclass`.

Some of the unsupported features are likely to remain
unsupported since these type hints are not relevant for the compilation to
efficient C code. In other cases, however, where the generated C code could
benefit from these type hints but does not currently, help is welcome to
improve the type analysis in Cython.

### Reference table[¶](#reference-table "Link to this heading")

The following reference table documents how type annotations are currently interpreted.
Cython 0.29 behaviour is only shown where it differs from Cython 3.0 behaviour.
The current limitations will likely be lifted at some point.

Annotation typing rules[¶](#id5 "Link to this table")




 Feature  Cython 0.29  Cython 3.0  `int`  Any Python object  Exact Python `int` (`language_level=3` only)  `float`  C `double`  Builtin type e.g. `dict`, `list`  Exact type (no subclasses), not `None`  Extension type defined in Cython  Specified type or a subclasses, not `None`  `cython.int`, `cython.long`, etc.  Equivalent C numeric type  `typing.Optional[any_type]`  Not supported  Specified type (which must be a Python object), allows `None`  `typing.Union[any_type, None]`  Not supported  Specified type (which must be a Python object), allows `None`  `any_type | None`  Not supported  Specified type (which must be a Python object), allows `None`  `typing.List[any_type]` (and similar)  Not supported  Exact `list`, with the element type ignored currently  `typing.ClassVar[...]`  Not supported  Python-object class variable (when used in a class definition) 

## Tips and Tricks[¶](#tips-and-tricks "Link to this heading")

### Avoiding the `cython` runtime dependency[¶](#avoiding-the-cython-runtime-dependency "Link to this heading")

Python modules that are intended to run both compiled and as plain Python
usually have the line `ìmport cython` in them and make use of the magic
attributes in that module. If not compiled, this creates a runtime dependency
on Cython’s shadow module that provides fake implementations of types and
decorators.

Code that does not want to require Cython or its shadow module as as runtime
dependency at all can often get away with a simple, stripped-down replacement
like the following:

```
try:
    import cython
except ImportError:
    class _fake_cython:
        compiled = False
        def cfunc(self, func): return func
        def ccall(self, func): return func
        def __getattr__(self, type_name): return "object"

    cython = _fake_cython()
```

### Calling C functions[¶](#calling-c-functions "Link to this heading")

The magic [`cython.cimports`](#module-cython.cimports "cython.cimports") package provides a way to cimport external
compile time C declarations from code written in plain Python. For convenience,
it also provides a fallback Python implementation for the `libc.math` module.

However, it is normally not possible to call C functions in pure Python
code as there is no general way to represent them in normal (uncompiled) Python.
But in cases where an equivalent Python function exists, this can be achieved
by combining C function coercion with a conditional import as follows:

```
# mymodule.pxd

# declare a C function as "cpdef" to export it to the module
cdef extern from "math.h":
    cpdef double sin(double x)
```

```
# mymodule.py

import cython

# override with Python import if not in compiled code
if not cython.compiled:
    from math import sin

# calls sin() from math.h when compiled with Cython and math.sin() in Python
print(sin(0))
```

Note that the “sin” function will show up in the module namespace of “mymodule”
here (i.e. there will be a `mymodule.sin()` function). You can mark it as an
internal name according to Python conventions by renaming it to “\_sin” in the
`.pxd` file as follows:

```
cdef extern from "math.h":
    cpdef double _sin "sin" (double x)
```

You would then also change the Python import to `from math import sin as _sin`
to make the names match again.

### Using C arrays for fixed size lists[¶](#using-c-arrays-for-fixed-size-lists "Link to this heading")

C arrays can automatically coerce to Python lists or tuples.
This can be exploited to replace fixed size Python lists in Python code by C
arrays when compiled. An example:

```
import cython


@cython.locals(counts=cython.int[10], digit=cython.int)
def count_digits(digits):
    """
    >>> digits = '01112222333334445667788899'
    >>> count_digits(map(int, digits))
    [1, 3, 4, 5, 3, 1, 2, 2, 3, 2]
    """
    counts = [0] * 10
    for digit in digits:
        assert 0 <= digit <= 9
        counts[digit] += 1
    return counts
```

In normal Python, this will use a Python list to collect the counts, whereas
Cython will generate C code that uses a C array of C ints.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Pure Python Mode](# "#")
  + [Augmenting .pxd](#augmenting-pxd "#augmenting-pxd")
  + [Magic Attributes](#magic-attributes "#magic-attributes")
    - [“Compiled” switch](#compiled-switch "#compiled-switch")
    - [Static typing](#static-typing "#static-typing")
    - [C types](#c-types "#c-types")
    - [Extension types and cdef functions](#extension-types-and-cdef-functions "#extension-types-and-cdef-functions")
    - [Managing the Global Interpreter Lock](#managing-the-global-interpreter-lock "#managing-the-global-interpreter-lock")
    - [cimports](#cimports "#cimports")
    - [Further Cython functions and declarations](#further-cython-functions-and-declarations "#further-cython-functions-and-declarations")
    - [Magic Attributes within the .pxd](#magic-attributes-within-the-pxd "#magic-attributes-within-the-pxd")
  + [PEP-484 type annotations](#pep-484-type-annotations "#pep-484-type-annotations")
    - [Disabling annotations](#disabling-annotations "#disabling-annotations")
    - [`typing` Module](#typing-module "#typing-module")
    - [Reference table](#reference-table "#reference-table")
  + [Tips and Tricks](#tips-and-tricks "#tips-and-tricks")
    - [Avoiding the `cython` runtime dependency](#avoiding-the-cython-runtime-dependency "#avoiding-the-cython-runtime-dependency")
    - [Calling C functions](#calling-c-functions "#calling-c-functions")
    - [Using C arrays for fixed size lists](#using-c-arrays-for-fixed-size-lists "#using-c-arrays-for-fixed-size-lists")

#### Previous topic

[Embedding Cython modules in C/C++ applications](embedding.html "previous chapter")

#### Next topic

[Working with NumPy](numpy.html "next chapter")

### This Page

* [Show Source](../../_sources/src/tutorial/pure.rst.txt "../../_sources/src/tutorial/pure.rst.txt")

### Quick search

### Navigation

* [next](numpy.html "Working with NumPy")
* [previous](embedding.html "Embedding Cython modules in C/C++ applications") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Pure Python Mode

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

