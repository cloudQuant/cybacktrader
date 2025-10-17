




Fused Types (Templates) — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/fusedtypes.html "/en/stable/src/userguide/fusedtypes.html").

### Navigation

* [next](pypy.html "Porting Cython code to PyPy")
* [previous](wrapping_CPlusPlus.html "Using C++ in Cython") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Fused Types (Templates)

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Fused Types (Templates)[¶](#fused-types-templates "Link to this heading")

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

Fused types allow you to have one type definition that can refer to multiple
types. This allows you to write a single static-typed cython algorithm that can
operate on values of multiple types. Thus fused types allow [generic
programming](https://en.wikipedia.org/wiki/Generic_programming "https://en.wikipedia.org/wiki/Generic_programming") and are akin to templates in C++ or generics in languages like
Java / C#.

Note

Fused types are not currently supported as attributes of extension
types. Only variables and function/method arguments can be declared
with fused types.

## Quickstart[¶](#quickstart "Link to this heading")

Pure PythonCython

```
char_or_float = cython.fused_type(cython.char, cython.double)



@cython.ccall
def plus_one(var: char_or_float) -> char_or_float:
    return var + 1


def show_me():

    a: cython.char = 127
    b: cython.double = 127
    print('char', plus_one(a))
    print('float', plus_one(b))
```

```
ctypedef fused char_or_float:
    char
    double


cpdef char_or_float plus_one(char_or_float var):
    return var + 1


def show_me():
    cdef:
        char a = 127
        float b = 127
    print('char', plus_one(a))
    print('float', plus_one(b))
```

This gives:

```
>>> show_me()
char -128
float 128.0
```

`plus_one(a)` “specializes” the fused type `char_or_float` as a `char`,
whereas `plus_one(b)` specializes `char_or_float` as a `float`.

## Declaring Fused Types[¶](#declaring-fused-types "Link to this heading")

Fused types may be declared as follows:

Pure PythonCython

```
my_fused_type = cython.fused_type(cython.int, cython.float)
```

```
ctypedef fused my_fused_type:
    int
    double
```

This declares a new type called `my_fused_type` which can be either an
`int` or a `double`.

Only names may be used for the constituent types, but they may be any
(non-fused) type, including a typedef. I.e. one may write:

Pure PythonCython

```
my_double = cython.typedef(cython.double)
my_fused_type = cython.fused_type(cython.int, my_double)
```

```
ctypedef double my_double
ctypedef fused fused_type:
    int
    my_double
```

## Using Fused Types[¶](#using-fused-types "Link to this heading")

Fused types can be used to declare parameters of functions or methods:

Pure PythonCython

```
@cython.cfunc
def cfunc(arg: my_fused_type):
    return arg + 1
```

```
cdef cfunc(my_fused_type arg):
    return arg + 1
```

If the same fused type appears more than once in the function arguments,
then they will all have the same specialised type:

Pure PythonCython

```
@cython.cfunc
def cfunc(arg1: my_fused_type, arg2: my_fused_type):
    # arg1 and arg2 always have the same type here
    return arg1 + arg2
```

```
cdef cfunc(my_fused_type arg1, my_fused_type arg2):
    # arg1 and arg2 always have the same type here
    return arg1 + arg2
```

Here, the type of both parameters is either an int, or a double
(according to the previous examples), because they use the same fused type
name `my_fused_type`. Mixing different fused types (or differently named
fused types) in the arguments will specialise them independently:

Pure PythonCython

```
def func(x: A, y: B):
    ...
```

```
def func(A x, B y):
    ...
```

This will result in specialized code paths for all combinations of types
contained in `A` and `B`, e.g.:

Pure PythonCython

```
my_fused_type = cython.fused_type(cython.int, cython.double)



my_fused_type2 = cython.fused_type(cython.int, cython.double)


@cython.cfunc
def func(a: my_fused_type, b: my_fused_type2):
    # a and b may have the same or different types here
    print("SAME!" if my_fused_type is my_fused_type2 else "NOT SAME!")
    return a + b
```

```
ctypedef fused my_fused_type:
    int
    double

ctypedef fused my_fused_type2:
    int
    double

cdef func(my_fused_type a, my_fused_type2 b):
    # a and b may have the same or different types here
    print("SAME!" if my_fused_type is my_fused_type2 else "NOT SAME!")
    return a + b
```

Note

A simple typedef to rename the fused type does not currently work here.
See Github issue [#4302](https://github.com/cython/cython/issues/4302 "https://github.com/cython/cython/issues/4302").

### Fused types and arrays[¶](#fused-types-and-arrays "Link to this heading")

Note that specializations of only numeric types may not be very useful, as one
can usually rely on promotion of types. This is not true for arrays, pointers
and typed views of memory however. Indeed, one may write:

Pure PythonCython

```
@cython.cfunc
def myfunc(x: A[:, :]):
    ...

# and

@cython.cfunc
cdef otherfunc(x: cython.pointer[A]):
    ...
```

```
cdef myfunc(A[:, :] x):
    ...

# and

cdef otherfunc(A *x):
    ...
```

Following code snippet shows an example with pointer to the fused type:

Pure PythonCython

```
my_fused_type = cython.fused_type(cython.int, cython.float)


@cython.cfunc
def func(a: cython.pointer[my_fused_type]):
    print(a[0])

def main():
    a: cython.int = 3
    b: cython.float = 5.0

    func(cython.address(a))
    func(cython.address(b))
```

```
ctypedef fused my_fused_type:
    int
    double

cdef func(my_fused_type *a):
    print(a[0])


cdef int b = 3
cdef double c = 3.0

func(&b)
func(&c)
```

Note

In Cython 0.20.x and earlier, the compiler generated the full cross
product of all type combinations when a fused type was used by more than one
memory view in a type signature, e.g.

```
def myfunc(A[:] a, A[:] b):
    # a and b had independent item types in Cython 0.20.x and earlier.
    ...
```

This was unexpected for most users, unlikely to be desired, and also inconsistent
with other structured type declarations like C arrays of fused types, which were
considered the same type. It was thus changed in Cython 0.21 to use the same
type for all memory views of a fused type. In order to get the original
behaviour, it suffices to declare the same fused type under different names, and
then use these in the declarations:

```
ctypedef fused A:
    int
    long

ctypedef fused B:
    int
    long

def myfunc(A[:] a, B[:] b):
    # a and b are independent types here and may have different item types
    ...
```

To get only identical types also in older Cython versions (pre-0.21), a `ctypedef`
can be used:

```
ctypedef A[:] A_1d

def myfunc(A_1d a, A_1d b):
    # a and b have identical item types here, also in older Cython versions
    ...
```

## Selecting Specializations[¶](#selecting-specializations "Link to this heading")

You can select a specialization (an instance of the function with specific or
specialized (i.e., non-fused) argument types) in two ways: either by indexing or
by calling.

### Indexing[¶](#indexing "Link to this heading")

You can index functions with types to get certain specializations, i.e.:

Pure PythonCython

indexing.py[¶](#id1 "Link to this code")

```
import cython

fused_type1 = cython.fused_type(cython.double, cython.float)



fused_type2 = cython.fused_type(cython.double, cython.float)


@cython.cfunc
def cfunc(arg1: fused_type1, arg2: fused_type1):
    print("cfunc called:", cython.typeof(arg1), arg1, cython.typeof(arg2), arg2)

@cython.ccall
def cpfunc(a: fused_type1, b: fused_type2):
    print("cpfunc called:", cython.typeof(a), a, cython.typeof(b), b)

def func(a: fused_type1, b: fused_type2):
    print("func called:", cython.typeof(a), a, cython.typeof(b), b)

# called from Cython space
cfunc[cython.double](5.0, 1.0)
cpfunc[cython.float, cython.double](1.0, 2.0)
# Indexing def functions in Cython code requires string names
func["float", "double"](1.0, 2.0)
```

indexing.pyx[¶](#id2 "Link to this code")

```
cimport cython

ctypedef fused fused_type1:
    double
    float

ctypedef fused fused_type2:
    double
    float

cdef cfunc(fused_type1 arg1, fused_type1 arg2):
    print("cfunc called:", cython.typeof(arg1), arg1, cython.typeof(arg2), arg2)


cpdef cpfunc(fused_type1 a, fused_type2 b):
    print("cpfunc called:", cython.typeof(a), a, cython.typeof(b), b)

def func(fused_type1 a, fused_type2 b):
    print("func called:", cython.typeof(a), a, cython.typeof(b), b)

# called from Cython space
cfunc[double](5.0, 1.0)
cpfunc[float, double](1.0, 2.0)
# Indexing def function in Cython code requires string names
func["float", "double"](1.0, 2.0)
```

Indexed functions can be called directly from Python:

```
>>> import cython
>>> import indexing
cfunc called: double 5.0 double 1.0
cpfunc called: float 1.0 double 2.0
func called: float 1.0 double 2.0
>>> indexing.cpfunc[cython.float, cython.float](1, 2)
cpfunc called: float 1.0 float 2.0
>>> indexing.func[cython.float, cython.float](1, 2)
func called: float 1.0 float 2.0
```

If a fused type is used as a component of a more complex type
(for example a pointer to a fused type, or a memoryview of a fused type),
then you should index the function with the individual component and
not the full argument type:

Pure PythonCython

```
@cython.cfunc
def myfunc(x: cython.pointer[A]):
    ...

# Specialize using int, not int *
myfunc[cython.int](myint)
```

```
cdef myfunc(A *x):
    ...

# Specialize using int, not int *
myfunc[int](myint)
```

For memoryview indexing from python space we can do the following:

Pure PythonCython

```
import numpy as np
import cython

myarray: cython.int[:, ::1] = np.arange(20, dtype=np.intc).reshape((2, 10))

my_fused_type = cython.fused_type(cython.int[:, ::1], cython.float[:, ::1])



def func(array: my_fused_type):
    print("func called:", cython.typeof(array))

func["int[:, ::1]"](myarray)
```

```
import numpy as np
import cython

myarray: cython.int[:, ::1] = np.arange(20, dtype=np.intc).reshape((2, 10))

ctypedef fused my_fused_type:
    int[:, ::1]
    float[:, ::1]

def func(my_fused_type array):
    print("func called:", cython.typeof(array))

func["int[:, ::1]"](myarray)
```

The same goes for when using e.g. `cython.numeric[:, :]`.

### Calling[¶](#calling "Link to this heading")

A fused function can also be called with arguments, where the dispatch is
figured out automatically:

Pure PythonCython

```
def main():
    p1: cython.double = 1.0
    p2: cython.float = 2.0
    cfunc(p1, p1)          # prints "cfunc called: double 1.0 double 1.0"
    cpfunc(p1, p2)         # prints "cpfunc called: double 1.0 float 2.0"
```

```
def main():
    cdef double p1 = 1.0
    cdef float p2 = 2.0
    cfunc(p1, p1)          # prints "cfunc called: double 1.0 double 1.0"
    cpfunc(p1, p2)         # prints "cpfunc called: double 1.0 float 2.0"
```

For a `cdef` or `cpdef` function called from Cython this means that the
specialization is figured out at compile time. For `def` functions the
arguments are typechecked at runtime, and a best-effort approach is performed to
figure out which specialization is needed. This means that this may result in a
runtime `TypeError` if no specialization was found. A `cpdef` function is
treated the same way as a `def` function if the type of the function is
unknown (e.g. if it is external and there is no cimport for it).

The automatic dispatching rules are typically as follows, in order of
preference:

* try to find an exact match
* choose the biggest corresponding numerical type (biggest float, biggest
  complex, biggest int)

## Built-in Fused Types[¶](#built-in-fused-types "Link to this heading")

There are some built-in fused types available for convenience, these are:

```
cython.integral # short, int, long
cython.floating # float, double
cython.numeric  # short, int, long, float, double, float complex, double complex
```

## Casting Fused Functions[¶](#casting-fused-functions "Link to this heading")

Note

Pointers to functions are currently not supported by pure Python mode. (GitHub issue [#4279](https://github.com/cython/cython/issues/4279 "https://github.com/cython/cython/issues/4279"))

Fused `cdef` and `cpdef` functions may be cast or assigned to C function pointers as follows:

```
cdef myfunc(cython.floating, cython.integral):
    ...

# assign directly
cdef object (*funcp)(float, int)
funcp = myfunc
funcp(f, i)

# alternatively, cast it
(<object (*)(float, int)> myfunc)(f, i)

# This is also valid
funcp = myfunc[float, int]
funcp(f, i)
```

## Type Checking Specializations[¶](#type-checking-specializations "Link to this heading")

Decisions can be made based on the specializations of the fused parameters.
False conditions are pruned to avoid invalid code. One may check with `is`,
`is not` and `==` and `!=` to see if a fused type is equal to a certain
other non-fused type (to check the specialization), or use `in` and `not in`
to figure out whether a specialization is part of another set of types
(specified as a fused type). In example:

Pure PythonCython

```
bunch_of_types = cython.fused_type(bytes, cython.int, cython.float)






string_t = cython.fused_type(cython.p_char, bytes, unicode)



@cython.cfunc
def myfunc(i: cython.integral, s: bunch_of_types) -> cython.integral:
    # Only one of these branches will be compiled for each specialization!
    if cython.integral is int:
        print('i is an int')
    elif cython.integral is long:
        print('i is a long')
    else:
        print('i is a short')

    if bunch_of_types in string_t:
        print("s is a string!")
    return i * 2

myfunc(cython.cast(cython.int, 5), b'm')  # will print "i is an int" and "s is a string"
myfunc(cython.cast(cython.long, 5), 3)    # will print "i is a long"
myfunc(cython.cast(cython.short, 5), 3)   # will print "i is a short"
```

```
cimport cython

ctypedef fused bunch_of_types:
    bytes
    int
    float

ctypedef fused string_t:
    cython.p_char
    bytes
    unicode

cdef cython.integral myfunc(cython.integral i, bunch_of_types s):
    # Only one of these branches will be compiled for each specialization!
    if cython.integral is int:
        print('i is int')
    elif cython.integral is long:
        print('i is long')
    else:
        print('i is short')

    if bunch_of_types in string_t:
        print("s is a string!")
    return i * 2

myfunc(<int> 5, b'm')  # will print "i is an int" and "s is a string"
myfunc(<long> 5, 3)    # will print "i is a long"
myfunc(<short> 5, 3)   # will print "i is a short"
```

## Conditional GIL Acquiring / Releasing[¶](#conditional-gil-acquiring-releasing "Link to this heading")

Acquiring and releasing the GIL can be controlled by a condition
which is known at compile time (see [Conditional Acquiring / Releasing the GIL](external_C_code.html#gil-conditional "external_C_code.html#gil-conditional")).

This is most useful when combined with fused types.
A fused type function may have to handle both cython native types
(e.g. cython.int or cython.double) and python types (e.g. object or bytes).
Conditional Acquiring / Releasing the GIL provides a method for running
the same piece of code either with the GIL released (for cython native types)
and with the GIL held (for python types):

Pure PythonCython

```
import cython

double_or_object = cython.fused_type(cython.double, object)

def increment(x: double_or_object):
    with cython.nogil(double_or_object is not object):
        # Same code handles both cython.double (GIL is released)
        # and python object (GIL is not released).
        x = x + 1
    return x

increment(5.0)  # GIL is released during increment
increment(5)    # GIL is acquired during increment
```

```
cimport cython

ctypedef fused double_or_object:
    double
    object

def increment(double_or_object x):
    with nogil(double_or_object is not object):
        # Same code handles both cython.double (GIL is released)
        # and python object (GIL is not released).
        x = x + 1
    return x

increment(5.0)  # GIL is released during increment
increment(5)    # GIL is acquired during increment
```

## \_\_signatures\_\_[¶](#signatures "Link to this heading")

Finally, function objects from `def` or `cpdef` functions have an attribute
`__signatures__`, which maps the signature strings to the actual specialized
functions. This may be useful for inspection:

Pure PythonCython

indexing.py[¶](#id3 "Link to this code")

```
import cython

fused_type1 = cython.fused_type(cython.double, cython.float)



fused_type2 = cython.fused_type(cython.double, cython.float)


@cython.ccall
def cpfunc(a: fused_type1, b: fused_type2):
    print("cpfunc called:", cython.typeof(a), a, cython.typeof(b), b)
```

indexing.pyx[¶](#id4 "Link to this code")

```
cimport cython

ctypedef fused fused_type1:
    double
    float

ctypedef fused fused_type2:
    double
    float

cpdef cpfunc(fused_type1 a, fused_type2 b):
    print("cpfunc called:", cython.typeof(a), a, cython.typeof(b), b)
```

```
>>> from indexing import cpfunc
>>> cpfunc.__signatures__,
({'double|double': <cyfunction __pyx_fuse_0_0cpfunc at 0x107292f20>, 'double|float': <cyfunction __pyx_fuse_0_1cpfunc at 0x1072a6040>, 'float|double': <cyfunction __pyx_fuse_1_0cpfunc at 0x1072a6120>, 'float|float': <cyfunction __pyx_fuse_1_1cpfunc at 0x1072a6200>},)
```

Listed signature strings may also
be used as indices to the fused function, but the index format may change between
Cython versions

```
>>> specialized_function = cpfunc["double|float"]
>>> specialized_function(5.0, 1.0)
cpfunc called: double 5.0 float 1.0
```

However, the better way how to index is by providing list of types as mentioned in [Indexing](#fusedtypes-indexing "#fusedtypes-indexing") section.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Fused Types (Templates)](# "#")
  + [Quickstart](#quickstart "#quickstart")
  + [Declaring Fused Types](#declaring-fused-types "#declaring-fused-types")
  + [Using Fused Types](#using-fused-types "#using-fused-types")
    - [Fused types and arrays](#fused-types-and-arrays "#fused-types-and-arrays")
  + [Selecting Specializations](#selecting-specializations "#selecting-specializations")
    - [Indexing](#indexing "#indexing")
    - [Calling](#calling "#calling")
  + [Built-in Fused Types](#built-in-fused-types "#built-in-fused-types")
  + [Casting Fused Functions](#casting-fused-functions "#casting-fused-functions")
  + [Type Checking Specializations](#type-checking-specializations "#type-checking-specializations")
  + [Conditional GIL Acquiring / Releasing](#conditional-gil-acquiring-releasing "#conditional-gil-acquiring-releasing")
  + [\_\_signatures\_\_](#signatures "#signatures")

#### Previous topic

[Using C++ in Cython](wrapping_CPlusPlus.html "previous chapter")

#### Next topic

[Porting Cython code to PyPy](pypy.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/fusedtypes.rst.txt "../../_sources/src/userguide/fusedtypes.rst.txt")

### Quick search

### Navigation

* [next](pypy.html "Porting Cython code to PyPy")
* [previous](wrapping_CPlusPlus.html "Using C++ in Cython") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Fused Types (Templates)

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

