




Language Basics — Cython 3.1.4 documentation

### Navigation

* [next](extension_types.html "Extension Types")
* [previous](index.html "Users Guide") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Language Basics

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Language Basics[¶](#ctypedef "Link to this heading")

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

## Declaring Data Types[¶](#declaring-data-types "Link to this heading")

As a dynamic language, Python encourages a programming style of considering
classes and objects in terms of their methods and attributes, more than where
they fit into the class hierarchy.

This can make Python a very relaxed and comfortable language for rapid
development, but with a price - the ‘red tape’ of managing data types is
dumped onto the interpreter. At run time, the interpreter does a lot of work
searching namespaces, fetching attributes and parsing argument and keyword tuples.
This run-time ‘late binding’ is a major cause of Python’s relative slowness
compared to ‘early binding’ languages such as C++.

However with Cython it is possible to gain significant speed-ups through
the use of ‘early binding’ programming techniques.

Note

Typing is not a necessity

Providing static typing to parameters and variables is convenience to
speed up your code, but it is not a necessity. Optimize where and when needed.
In fact, typing can slow down your code in the case where the
typing does not allow optimizations but where Cython still needs to
check that the type of some object matches the declared type.

## C variable and type definitions[¶](#c-variable-and-type-definitions "Link to this heading")

C variables can be declared by

* using the Cython specific [`cdef`](#cdef "#cdef") statement,
* using PEP-484/526 type annotations with C data types or
* using the function `cython.declare()`.

The [`cdef`](#cdef "#cdef") statement and `declare()` can define function-local and
module-level variables as well as attributes in classes, but type annotations only
affect local variables and attributes and are ignored at the module level.
This is because type annotations are not Cython specific, so Cython keeps
the variables in the module dict (as Python values) instead of making them
module internal C variables. Use `declare()` in Python code to explicitly
define global C variables.

Pure PythonCython

```
a_global_variable = declare(cython.int)

def func():
    i: cython.int
    j: cython.int
    k: cython.int
    f: cython.float
    g: cython.float[42]
    h: cython.p_float

    i = j = 5
```

```
cdef int a_global_variable

def func():
    cdef int i, j, k
    cdef float f
    cdef float[42] g
    cdef float *h
    # cdef float f, g[42], *h  # mix of pointers, arrays and values in a single line is deprecated

    i = j = 5
```

As known from C, declared global variables are automatically initialised to
`0`, `NULL` or `None`, depending on their type. However, also as known
from both Python and C, for a local variable, simply declaring it is not enough
to initialise it. If you use a local variable but did not assign a value, both
Cython and the C compiler will issue a warning “local variable … referenced
before assignment”. You need to assign a value at some point before first
using the variable, but you can also assign a value directly as part of
the declaration in most cases:

Pure PythonCython

```
a_global_variable = declare(cython.int, 42)

def func():
    i: cython.int = 10
    f: cython.float = 2.5
    g: cython.int[4] = [1, 2, 3, 4]
    h: cython.p_float = cython.address(f)
    c: cython.doublecomplex = 2 + 3j
```

```
cdef int a_global_variable = 42

def func():
    cdef int i = 10, j, k
    cdef float f = 2.5
    cdef int[4] g = [1, 2, 3, 4]
    cdef float *h = &f
    cdef double complex c = 2 + 3j
```

Note

There is also support for giving names to types using the
`ctypedef` statement or the `cython.typedef()` function, e.g.

Pure PythonCython

```
ULong = cython.typedef(cython.ulong)

IntPtr = cython.typedef(cython.p_int)
```

```
ctypedef unsigned long ULong

ctypedef int* IntPtr
```

### C Arrays[¶](#c-arrays "Link to this heading")

C array can be declared by adding `[ARRAY_SIZE]` to the type of variable:

Pure PythonCython

```
def func():
    g: cython.float[42]
    f: cython.int[5][5][5]
    ptr_char_array: cython.pointer[cython.char[4]]  # pointer to the array of 4 chars
    array_ptr_char: cython.p_char[4]                # array of 4 char pointers
```

```
def func():
    cdef float[42] g
    cdef int[5][5][5] f
    cdef char[4] *ptr_char_array     # pointer to the array of 4 chars
    cdef (char *)[4] array_ptr_char  # array of 4 char pointers
```

Note

Cython syntax currently supports two ways to declare an array:

```
cdef int arr1[4], arr2[4]  # C style array declaration
cdef int[4] arr1, arr2     # Java style array declaration
```

Both of them generate the same C code, but the Java style is more
consistent with [Typed Memoryviews](memoryviews.html#memoryviews "memoryviews.html#memoryviews") and [Fused Types (Templates)](fusedtypes.html#fusedtypes "fusedtypes.html#fusedtypes"). The C style
declaration is soft-deprecated and it’s recommended to use Java style
declaration instead.

The soft-deprecated C style array declaration doesn’t support
initialization.

```
cdef int g[4] = [1, 2, 3, 4]  # error

cdef int[4] g = [1, 2, 3, 4]  # OK

cdef int g[4]        # OK but not recommended
g = [1, 2, 3, 4]
```

### Structs, Unions, Enums[¶](#structs-unions-enums "Link to this heading")

In addition to the basic types, C [`struct`](#struct "#struct"), [`union`](#union "#union") and [`enum`](#enum "#enum")
are supported:

Pure PythonCython

```
Grail = cython.struct(
    age=cython.int,
    volume=cython.float)

def main():
    grail: Grail = Grail(5, 3.0)
    print(grail.age, grail.volume)
```

```
cdef struct Grail:
    int age
    float volume

def main():
    cdef Grail grail = Grail(5, 3.0)
    print(grail.age, grail.volume)
```

Structs can be declared as `cdef packed struct`, which has
the same effect as the C directive `#pragma pack(1)`:

```
cdef packed struct StructArray:
    int[4] spam
    signed char[5] eggs
```

Note

This declaration removes the empty
space between members that C automatically to ensure that they’re aligned in memory
(see [Wikipedia article](https://en.wikipedia.org/wiki/Data_structure_alignment "https://en.wikipedia.org/wiki/Data_structure_alignment") for more details).
The main use is that numpy structured arrays store their data in packed form, so a `cdef packed struct`
can be [used in a memoryview](memoryviews.html#using-memoryviews "memoryviews.html#using-memoryviews") to match that.

Pure python mode does not support packed structs.

The following example shows a declaration of unions:

Pure PythonCython

```
Food = cython.union(
    spam=cython.p_char,
    eggs=cython.p_float)

def main():
    arr: cython.p_float = [1.0, 2.0]
    spam: Food = Food(spam='b')
    eggs: Food = Food(eggs=arr)
    print(spam.spam, eggs.eggs[0])
```

```
cdef union Food:
    char *spam
    float *eggs

def main():
    cdef float *arr = [1.0, 2.0]
    cdef Food spam = Food(spam='b')
    cdef Food eggs = Food(eggs=arr)
    print(spam.spam, eggs.eggs[0])
```

Enums are created by `cdef enum` statement:

```
cdef enum CheeseType:
    cheddar, edam,
    camembert

cdef enum CheeseState:
    hard = 1
    soft = 2
    runny = 3

print(CheeseType.cheddar)
print(CheeseState.hard)
```

Note

Currently, Pure Python mode does not support enums. (GitHub issue [#4252](https://github.com/cython/cython/issues/4252 "https://github.com/cython/cython/issues/4252"))

Declaring an enum as `cpdef` will create a [PEP 435](https://peps.python.org/pep-0435/ "https://peps.python.org/pep-0435/")-style Python wrapper:

```
cpdef enum CheeseState:
    hard = 1
    soft = 2
    runny = 3
```

Up to Cython version 3.0.x, this used to copy all item names into the global
module namespace, so that they were available both as attributes of the Python
enum type (`CheseState` above) and as global constants.
This was changed in Cython 3.1 to distinguish between anonymous cpdef enums,
which only create global Python constants for their items, and named cpdef enums,
where the items live only in the namespace of the enum type and do not create
global Python constants.

To create global constants also for the items of a declared named enum type,
you can copy the enum items into the global Python module namespace manually.
In Cython before 3.1, this will simply overwrite the global names with
their own value, which makes it backwards compatible.

```
globals().update(getattr(CheeseState, '__members__'))
```

There is currently no special syntax for defining a constant, but you can use
an anonymous [`enum`](#enum "#enum") declaration for this purpose, for example,:

```
cdef enum:
    tons_of_spam = 3
```

Note

In the Cython syntax, the words `struct`, `union` and `enum` are used only when
defining a type, not when referring to it. For example, to declare a variable
pointing to a `Grail` struct, you would write:

```
cdef Grail *gp
```

and not:

```
cdef struct Grail *gp  # WRONG
```

### Types[¶](#types "Link to this heading")

The Cython language uses the normal C syntax for C types, including pointers. It provides
all the standard C types, namely `char`, `short`, `int`, `long`,
`long long` as well as their `unsigned` versions,
e.g. `unsigned int` (`cython.uint` in Python code):

Numeric Types[¶](#id25 "Link to this table")



 Cython type  Pure Python type  `bint`  `cython.bint`  `char`  `cython.char`  `signed char`  `cython.schar`  `unsigned char`  `cython.uchar`  `short`  `cython.short`  `unsigned short`  `cython.ushort`  `int`  `cython.int`  `unsigned int`  `cython.uint`  `long`  `cython.long`  `unsigned long`  `cython.ulong`  `long long`  `cython.longlong`  `unsigned long long`  `cython.ulonglong`  `float`  `cython.float`  `double`  `cython.double`  `long double`  `cython.longdouble`  `float complex`  `cython.floatcomplex`  `double complex`  `cython.doublecomplex`  `long double complex`  `cython.longdoublecomplex`  `size_t`  `cython.size_t`  `Py_ssize_t`  `cython.Py_ssize_t`  `Py_hash_t`  `cython.Py_hash_t`  `Py_UCS4`  `cython.Py_UCS4` 

Note

Additional types are declared in the [stdint pxd file](https://github.com/cython/cython/blob/master/Cython/Includes/libc/stdint.pxd "https://github.com/cython/cython/blob/master/Cython/Includes/libc/stdint.pxd").

The special `bint` type is used for C boolean values (`int` with 0/non-0
values for False/True) and [`Py_ssize_t`](https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t "(in Python v3.13)") for (signed) sizes of Python
containers.

Pointer types are constructed as in C when using Cython syntax, by appending a `*` to the base type
they point to, e.g. `int**` for a pointer to a pointer to a C int. In Pure python mode, simple pointer types
use a naming scheme with “p”s instead, separated from the type name with an underscore, e.g. `cython.pp_int` for a pointer to
a pointer to a C int. Further pointer types can be constructed with the `cython.pointer[]` type construct,
e.g. `cython.p_int` is equivalent to `cython.pointer[cython.int]`.

Arrays use the normal C array syntax, e.g. `int[10]`, and the size must be known
at compile time for stack allocated arrays. Cython doesn’t support variable length arrays from C99.
Note that Cython uses array access for pointer dereferencing, as `*x` is not valid Python syntax,
whereas `x[0]` is.

Also, the Python types `list`, `dict`, `tuple`, etc. may be used for
static typing, as well as any user defined [Extension Types](extension_types.html#extension-types "extension_types.html#extension-types").
For example

Pure PythonCython

```
def main():
    foo: list = []
```

```
cdef list foo = []
```

This requires an exact match of the class, it does not allow subclasses.
This allows Cython to optimize code by accessing internals of the builtin class,
which is the main reason for declaring builtin types in the first place.

Since Cython 3.1, builtin exception types generally no longer fall under the “exact type” restriction.
Thus, declarations like `exc: BaseException` accept all exception objects, as they probably intend.

For declared builtin types, Cython uses internally a C variable of type [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject "(in Python v3.13)")\*.

Note

The Python types `int`, `long`, and `float` are not available for static
typing in `.pyx` files and instead interpreted as C `int`, `long`, and `float`
respectively, as statically typing variables with these Python
types has zero advantages. On the other hand, annotating in Pure Python with
`int`, `long`, and `float` Python types will be interpreted as
Python object types.

Cython provides an accelerated and typed equivalent of a Python tuple, the `ctuple`.
A `ctuple` is assembled from any valid C types. For example

Pure PythonCython

```
def main():
    bar: tuple[cython.double, cython.int]
```

```
cdef (double, int) bar
```

They compile down to C-structures and can be used as efficient alternatives to
Python tuples.

While these C types can be vastly faster, they have C semantics.
Specifically, the integer types overflow
and the C `float` type only has 32 bits of precision
(as opposed to the 64-bit C `double` which Python floats wrap
and is typically what one wants).
If you want to use these numeric Python types simply omit the
type declaration and let them be objects.

### Type qualifiers[¶](#type-qualifiers "Link to this heading")

Cython supports `const` and `volatile` [C type qualifiers](https://en.wikipedia.org/wiki/Type_qualifier "https://en.wikipedia.org/wiki/Type_qualifier")

Pure PythonCython

```
def use_volatile():
    i: cython.volatile[cython.int] = 5

@cython.cfunc
def sum(a: cython.const[cython.int], b: cython.const[cython.int]) -> cython.const[cython.int]:
    return a + b

@cython.cfunc
def pointer_to_const_int(value: cython.pointer[cython.const[cython.int]]) -> cython.void:
    # Declares value as pointer to const int type (alias: "cython.p_const_int").
    # The value can be modified but the object pointed to by value cannot be modified.
    new_value: cython.int = 10
    print(value[0])
    value = cython.address(new_value)
    print(value[0])

@cython.cfunc
def const_pointer_to_int(value: cython.const[cython.pointer[cython.int]]) -> cython.void:
    # Declares value as const pointer to int type (alias: "cython.const[cython.p_int]").
    # Value cannot be modified but the object pointed to by value can be modified.
    print(value[0])
    value[0] = 10
    print(value[0])

@cython.cfunc
def const_pointer_to_const_int(value: cython.const[cython.pointer[cython.const[cython.int]]]) -> cython.void:
    # Declares value as const pointer to const int type (alias: "cython.const[cython.p_const_int]").
    # Neither the value variable nor the int pointed to can be modified.
    print(value[0])
```

```
def use_volatile():
    cdef volatile int i = 5


cdef const int sum(const int a, const int b):
    return a + b


cdef void pointer_to_const_int(const int *value):
    # Declares value as pointer to const int type.
    # The value can be modified but the object pointed to by value cannot be modified.
    cdef int new_value = 10
    print(value[0])
    value = &new_value
    print(value[0])


cdef void const_pointer_to_int(int * const value):
    # Declares value as const pointer to int type.
    # Value cannot be modified but the object pointed to by value can be modified.
    print(value[0])
    value[0] = 10
    print(value[0])


cdef void const_pointer_to_const_int(const int * const value):
    # Declares value as const pointer to const int type.
    # Neither the value variable nor the int pointed to can be modified.
    print(value[0])
```

Similar to pointers Cython supports shortcut types that can be used in pure python mode. The following table shows several examples:

Type qualifiers shortcut types[¶](#id26 "Link to this table")




 Cython  Full Annotation type  Shortcut type  `const float`  `cython.const[cython.float]`  `cython.const_float`  `const void *`  `cython.pointer[cython.const[cython.void]]`  `cython.p_const_void`  `const int *`  `cython.pointer[cython.const[cython.int]]`  `cython.p_const_int`  `const long **`  `cython.pointer[cython.pointer[cython.const[cython.long]]]`  `cython.pp_const_long` 

For full list of shortcut types see the `Shadow.pyi` file.

The `const` qualifier supports declaration of global constants:

```
cdef const int i = 5

# constant pointers are defined as pointer to a constant value.
cdef const char *msg = "Dummy string"
msg = "Another dummy string"
```

Note

The `const` modifier is unusable
in a lot of contexts since Cython needs to generate definitions and their assignments separately. Therefore
we suggest using it mainly for function argument and pointer types where `const` is necessary to
work with an existing C/C++ interface.

### Extension Types[¶](#extension-types "Link to this heading")

It is also possible to declare [Extension Types](extension_types.html#extension-types "extension_types.html#extension-types") (declared with `cdef class` or the `@cclass` decorator).
Those will have a behaviour very close to python classes (e.g. creating subclasses),
but access to their members is faster from Cython code. Typing a variable
as extension type is mostly used to access `cdef`/`@cfunc` methods and attributes of the extension type.
The C code uses a variable which is a pointer to a structure of the
specific type, something like `struct MyExtensionTypeObject*`.

Here is a simple example:

Pure PythonCython

```
@cython.cclass
class Shrubbery:
    width: cython.int
    height: cython.int

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def describe(self):
        print("This shrubbery is", self.width,
              "by", self.height, "cubits.")
```

```
cdef class Shrubbery:
    cdef int width
    cdef int height

    def __init__(self, w, h):
        self.width = w
        self.height = h

    def describe(self):
        print("This shrubbery is", self.width,
              "by", self.height, "cubits.")
```

You can read more about them in [Extension Types](extension_types.html#extension-types "extension_types.html#extension-types").

### Grouping multiple C declarations[¶](#grouping-multiple-c-declarations "Link to this heading")

If you have a series of declarations that all begin with [`cdef`](#cdef "#cdef"), you
can group them into a [`cdef`](#cdef "#cdef") block like this:

Note

This is supported only in Cython’s `cdef` syntax.

```
cdef:
    struct Spam:
        int tons

    int i
    float a
    Spam *p

    void f(Spam *s) except *:
        print(s.tons, "Tons of spam")
```

## Python functions vs. C functions[¶](#python-functions-vs-c-functions "Link to this heading")

There are two kinds of function definition in Cython:

Python functions are defined using the [`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.13)") statement, as in Python. They take
[Python objects](glossary.html#term-Python-object "glossary.html#term-Python-object") as parameters and return Python objects.

C functions are defined using the [`cdef`](#cdef "#cdef") statement in Cython syntax or with the `@cfunc` decorator. They take
either Python objects or C values as parameters, and can return either Python
objects or C values.

Within a Cython module, Python functions and C functions can call each other
freely, but only Python functions can be called from outside the module by
interpreted Python code. So, any functions that you want to “export” from your
Cython module must be declared as Python functions using `def`.
There is also a hybrid function, declared with [`cpdef`](#cpdef "#cpdef") in `.pyx`
files or with the `@ccall` decorator. These functions
can be called from anywhere, but use the faster C calling convention
when being called from other Cython code. They can also be overridden
by a Python method on a subclass or an instance attribute, even when called from Cython.
If this happens, most performance gains are of course lost and even if it does not,
there is a tiny overhead in calling such a method from Cython compared to
calling a C method.

Parameters of either type of function can be declared to have C data types,
using normal C declaration syntax. For example,

Pure PythonCython

```
def spam(i: cython.int, s: cython.p_char):
    ...

@cython.cfunc
def eggs(l: cython.ulong, f: cython.float) -> cython.int:
    ...
```

```
def spam(int i, char *s):
    ...


cdef int eggs(unsigned long l, float f):
    ...
```

`ctuples` may also be used

Pure PythonCython

```
@cython.cfunc
def chips(t: tuple[cython.long, cython.long, cython.double]) -> tuple[cython.int, cython.float]:
    ...
```

```
cdef (int, float) chips((long, long, double) t):
    ...
```

When a parameter of a Python function is declared to have a C data type, it is
passed in as a Python object and automatically converted to a C value, if
possible. In other words, the definition of `spam` above is equivalent to
writing

Pure PythonCython

```
def spam(python_i, python_s):
    i: cython.int = python_i
    s: cython.p_char = python_s
    ...
```

```
def spam(python_i, python_s):
    cdef int i = python_i
    cdef char* s = python_s
    ...
```

Automatic conversion is currently only possible for numeric types,
string types and structs (composed recursively of any of these types);
attempting to use any other type for the parameter of a
Python function will result in a compile-time error.
Care must be taken with strings to ensure a reference if the pointer is to be used
after the call. Structs can be obtained from Python mappings, and again care must be taken
with string attributes if they are to be used after the function returns.

C functions, on the other hand, can have parameters of any type, since they’re
passed in directly using a normal C function call.

C Functions declared using [`cdef`](#cdef "#cdef") or the `@cfunc` decorator with a
Python object return type, like Python functions, will return a `None`
value when execution leaves the function body without an explicit return value. This is in
contrast to C/C++, which leaves the return value undefined.
In the case of non-Python object return types, the equivalent of zero is returned, for example, 0 for `int`, `False` for `bint` and `NULL` for pointer types.

A more complete comparison of the pros and cons of these different method
types can be found at [Early Binding for Speed](early_binding_for_speed.html#early-binding-for-speed "early_binding_for_speed.html#early-binding-for-speed").

### Python objects as parameters and return values[¶](#python-objects-as-parameters-and-return-values "Link to this heading")

If no type is specified for a parameter or return value, it is assumed to be a
Python object. (Note that this is different from the C convention, where it
would default to `int`.) For example, the following defines a C function that
takes two Python objects as parameters and returns a Python object

Pure PythonCython

```
@cython.cfunc
def spamobjs(x, y):
    ...
```

```
cdef spamobjs(x, y):
    ...
```

Reference counting for these objects is performed automatically according to
the standard Python/C API rules (i.e. borrowed references are taken as
parameters and a new reference is returned).

Warning

This only applies to Cython code. Other Python packages which
are implemented in C like NumPy may not follow these conventions.

The type name `object` can also be used to explicitly declare something as a Python
object. This can be useful if the name being declared would otherwise be taken
as the name of a type, for example,

Pure PythonCython

```
@cython.cfunc
def ftang(int: object):
    ...
```

```
cdef ftang(object int):
    ...
```

declares a parameter called `int` which is a Python object. You can also use
`object` as the explicit return type of a function, e.g.

Pure PythonCython

```
@cython.cfunc
def ftang(int: object) -> object:
    ...
```

```
cdef object ftang(object int):
    ...
```

In the interests of clarity, it is probably a good idea to always be explicit
about object parameters in C functions.

To create a borrowed reference, specify the parameter type as [PyObject](https://docs.python.org/3/c-api/structures.html#c.PyObject "(in Python v3.13)")\*.
Cython won’t perform automatic [`Py_INCREF()`](https://docs.python.org/3/c-api/refcounting.html#c.Py_INCREF "(in Python v3.13)"), or [`Py_DECREF()`](https://docs.python.org/3/c-api/refcounting.html#c.Py_DECREF "(in Python v3.13)"), e.g.:

Pure PythonCython

```
# Py_REFCNT and _Py_REFCNT are the same, except _Py_REFCNT takes
# a raw pointer and Py_REFCNT takes a normal Python object
from cython.cimports.cpython.ref import PyObject, _Py_REFCNT, Py_REFCNT

import sys

python_dict = {"abc": 123}
python_dict_refcount = Py_REFCNT(python_dict)

@cython.cfunc
def owned_reference(obj: object):
    refcount1 = Py_REFCNT(obj)
    print(f'Inside owned_reference initially: {refcount1}')
    another_ref_to_object = obj
    refcount2 = Py_REFCNT(obj)
    print(f'Inside owned_reference after new ref: {refcount2}')

@cython.cfunc
def borrowed_reference(obj: cython.pointer[PyObject]):
    refcount1 = _Py_REFCNT(obj)
    print(f'Inside borrowed_reference initially: {refcount1}')
    another_ptr_to_object = obj
    refcount2 = _Py_REFCNT(obj)
    print(f'Inside borrowed_reference after new pointer: {refcount2}')
    # Casting to a managed reference to call a cdef function doesn't increase the count
    refcount3 = Py_REFCNT(cython.cast(object, obj))
    print(f'Inside borrowed_reference with temporary managed reference: {refcount3}')
    # However calling a Python function may depending on the Python version and the number
    # of arguments.


print(f'Initial refcount: {python_dict_refcount}')
owned_reference(python_dict)
borrowed_reference(cython.cast(cython.pointer[PyObject], python_dict))
```

```
# Py_REFCNT and _Py_REFCNT are the same, except _Py_REFCNT takes
# a raw pointer and Py_REFCNT takes a normal Python object
from cpython.ref cimport PyObject, _Py_REFCNT, Py_REFCNT

import sys

python_dict = {"abc": 123}
python_dict_refcount = Py_REFCNT(python_dict)


cdef owned_reference(object obj):
    refcount1 = Py_REFCNT(obj)
    print(f'Inside owned_reference initially: {refcount1}')
    another_ref_to_object = obj
    refcount2 = Py_REFCNT(obj)
    print(f'Inside owned_reference after new ref: {refcount2}')


cdef borrowed_reference(PyObject * obj):
    refcount1 = _Py_REFCNT(obj)
    print(f'Inside borrowed_reference initially: {refcount1}')
    another_ptr_to_object = obj
    refcount2 = _Py_REFCNT(obj)
    print(f'Inside borrowed_reference after new pointer: {refcount2}')
    # Casting to a managed reference to call a cdef function doesn't increase the count
    refcount3 = Py_REFCNT(<object>obj)
    print(f'Inside borrowed_reference with temporary managed reference: {refcount3}')
    # However calling a Python function may depending on the Python version and the number
    # of arguments.


print(f'Initial refcount: {python_dict_refcount}')
owned_reference(python_dict)
borrowed_reference(<PyObject *>python_dict)
```

will display:

```
Initial refcount: 2
Inside owned_reference initially: 2
Inside owned_reference after new ref: 3
Inside borrowed_reference initially: 2
Inside borrowed_reference after new pointer: 2
Inside borrowed_reference with temporary managed reference: 2
```

### Optional Arguments[¶](#optional-arguments "Link to this heading")

Unlike C, it is possible to use optional arguments in C and `cpdef`/`@ccall` functions.
There are differences though whether you declare them in a `.pyx`/`.py`
file or the corresponding `.pxd` file.

To avoid repetition (and potential future inconsistencies), default argument values are
not visible in the declaration (in `.pxd` files) but only in
the implementation (in `.pyx` files).

When in a `.pyx`/`.py` file, the signature is the same as it is in Python itself:

Pure PythonCython

optional\_subclassing.py[¶](#id27 "Link to this code")

```
@cython.cclass
class A:
    @cython.cfunc
    def foo(self):
        print("A")

@cython.cclass
class B(A):
    @cython.cfunc
    def foo(self, x=None):
        print("B", x)

@cython.cclass
class C(B):
    @cython.ccall
    def foo(self, x=True, k:cython.int = 3):
        print("C", x, k)
```

optional\_subclassing.pyx[¶](#id28 "Link to this code")

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

When in a `.pxd` file, the signature is different like this example: `cdef foo(x=*)`.
This is because the program calling the function just needs to know what signatures are
possible in C, but doesn’t need to know the value of the default arguments.:

optional\_subclassing.pxd[¶](#id29 "Link to this code")

```
cdef class A:
    cdef foo(self)

cdef class B(A):
    cdef foo(self, x=*)

cdef class C(B):
    cpdef foo(self, x=*, int k=*)
```

Note

The number of arguments may increase when subclassing,
but the arg types and order must be the same, as shown in the example above.

There may be a slight performance penalty when the optional arg is overridden
with one that does not have default values.

### Keyword-only Arguments[¶](#keyword-only-arguments "Link to this heading")

As in Python 3, `def` functions can have keyword-only arguments
listed after a `"*"` parameter and before a `"**"` parameter if any:

```
def f(a, b, *args, c, d = 42, e, **kwds):
    ...


# We cannot call f with less verbosity than this.
foo = f(4, "bar", c=68, e=1.0)
```

As shown above, the `c`, `d` and `e` arguments can not be
passed as positional arguments and must be passed as keyword arguments.
Furthermore, `c` and `e` are required keyword arguments
since they do not have a default value.

A single `"*"` without argument name can be used to
terminate the list of positional arguments:

```
def g(a, b, *, c, d):
    ...

# We cannot call g with less verbosity than this.
foo = g(4.0, "something", c=68, d="other")
```

Shown above, the signature takes exactly two positional
parameters and has two required keyword parameters.

### Function Pointers[¶](#function-pointers "Link to this heading")

Note

Pointers to functions are currently not supported by pure Python mode. (GitHub issue [#4279](https://github.com/cython/cython/issues/4279 "https://github.com/cython/cython/issues/4279"))

The following example shows declaring a `ptr_add` function pointer and assigning the `add` function to it:

```
cdef int(*ptr_add)(int, int)

cdef int add(int a, int b):
    return a + b

ptr_add = add

print(ptr_add(1, 3))
```

Functions declared in a `struct` are automatically converted to function pointers:

```
cdef struct Bar:
    int sum(int a, int b)

cdef int add(int a, int b):
    return a + b

cdef Bar bar = Bar(add)

print(bar.sum(1, 2))
```

For using error return values with function pointers, see the note at the bottom
of [Error return values](#error-return-values "#error-return-values").

### Error return values[¶](#error-return-values "Link to this heading")

In Python (more specifically, in the CPython runtime), exceptions that occur
inside of a function are signaled to the caller and propagated up the call stack
through defined error return values. For functions that return a Python object
(and thus, a pointer to such an object), the error return value is simply the
`NULL` pointer, so any function returning a Python object has a well-defined
error return value.

While this is always the case for Python functions, functions
defined as C functions or `cpdef`/`@ccall` functions can return arbitrary C types,
which do not have such a well-defined error return value.
By default Cython uses a dedicated return value to signal that an exception has been raised from non-external `cpdef`/`@ccall`
functions. However, how Cython handles exceptions from these functions can be changed if needed.

A `cdef` function may be declared with an exception return value for it
as a contract with the caller. Here is an example:

Pure PythonCython

```
@cython.cfunc
@cython.exceptval(-1)
def spam() -> cython.int:
    ...
```

```
cdef int spam() except -1:
    ...
```

With this declaration, whenever an exception occurs inside `spam`, it will
immediately return with the value `-1`. From the caller’s side, whenever
a call to spam returns `-1`, the caller will assume that an exception has
occurred and can now process or propagate it. Calling `spam()` is roughly translated to the following C code:

```
ret_val = spam();
if (ret_val == -1) goto error_handler;
```

When you declare an exception value for a function, you should never explicitly
or implicitly return that value. This includes empty [`return`](https://docs.python.org/3/reference/simple_stmts.html#return "(in Python v3.13)")
statements, without a return value, for which Cython inserts the default return
value (e.g. `0` for C number types). In general, exception return values
are best chosen from invalid or very unlikely return values of the function,
such as a negative value for functions that return only non-negative results,
or a very large value like `INT_MAX` for a function that “usually” only
returns small results.

If all possible return values are legal and you
can’t reserve one entirely for signalling errors, you can use an alternative
form of exception value declaration

Pure PythonCython

```
@cython.cfunc
@cython.exceptval(-1, check=True)
def spam() -> cython.int:
    ...
```

The keyword argument `check=True` indicates that the value `-1` may signal an error.

```
cdef int spam() except? -1:
    ...
```

The `?` indicates that the value `-1` may signal an error.

In this case, Cython generates a call to [`PyErr_Occurred()`](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_Occurred "(in Python v3.13)") if the exception value
is returned, to make sure it really received an exception and not just a normal
result. Calling `spam()` is roughly translated to the following C code:

```
ret_val = spam();
if (ret_val == -1 && PyErr_Occurred()) goto error_handler;
```

There is also a third form of exception value declaration

Pure PythonCython

```
@cython.cfunc
@cython.exceptval(check=True)
def spam() -> cython.void:
    ...
```

```
cdef void spam() except *:
    ...
```

This form causes Cython to generate a call to [`PyErr_Occurred()`](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_Occurred "(in Python v3.13)") after
every call to spam, regardless of what value it returns. Calling `spam()` is roughly translated to the following C code:

```
spam()
if (PyErr_Occurred()) goto error_handler;
```

If you have a
function returning `void` that needs to propagate errors, you will have to
use this form, since there isn’t any error return value to test.
Otherwise, an explicit error return value allows the C compiler to generate
more efficient code and is thus generally preferable.

An external C++ function that may raise an exception can be declared with:

```
cdef int spam() except +
```

Note

These declarations are not used in Python code, only in `.pxd` and `.pyx` files.

See [Using C++ in Cython](wrapping_CPlusPlus.html#wrapping-cplusplus "wrapping_CPlusPlus.html#wrapping-cplusplus") for more details.

Finally, if you are certain that your function should not raise an exception, (e.g., it
does not use Python objects at all, or you plan to use it as a callback in C code that
is unaware of Python exceptions), you can declare it as such using `noexcept` or by `@cython.exceptval(check=False)`:

Pure PythonCython

```
@cython.cfunc
@cython.exceptval(check=False)
def spam() -> cython.int:
    ...
```

```
cdef int spam() noexcept:
    ...
```

If a `noexcept` function does finish with an exception then it will print a warning message but not allow the exception to propagate further.
On the other hand, calling a `noexcept` function has zero overhead related to managing exceptions, unlike the previous declarations.

Some things to note:

* `cdef` functions that are also `extern` are implicitly declared `noexcept` or `@cython.exceptval(check=False)`.
  In the uncommon case of external C/C++ functions that can raise Python exceptions,
  e.g., external functions that use the Python C API, you should explicitly declare
  them with an exception value.
* `cdef` functions that are not `extern` are implicitly declared with a suitable
  exception specification for the return type (e.g. `except *` or `@cython.exceptval(check=True)` for a `void` return
  type, `except? -1` or `@cython.exceptval(-1, check=True)` for an `int` return type).
* Exception values can only be declared for functions returning a C integer,
  enum, float or pointer type, and the value must be a constant expression.
  Functions that return `void`, or a struct/union by value, can only use
  the `except *` or `exceptval(check=True)` form.
* The exception value specification is part of the signature of the function.
  If you’re passing a pointer to a function as a parameter or assigning it
  to a variable, the declared type of the parameter or variable must have
  the same exception value specification (or lack thereof). Here is an
  example of a pointer-to-function declaration with an exception value:

  ```
  int (*grail)(int, char*) except -1
  ```

  Note

  Pointers to functions are currently not supported by pure Python mode. (GitHub issue [#4279](https://github.com/cython/cython/issues/4279 "https://github.com/cython/cython/issues/4279"))
* If the returning type of a `cdef` function with `except *` or `@cython.exceptval(check=True)` is C integer,
  enum, float or pointer type, Cython calls [`PyErr_Occurred()`](https://docs.python.org/3/c-api/exceptions.html#c.PyErr_Occurred "(in Python v3.13)") only when
  dedicated value is returned instead of checking after every call of the function.
* You don’t need to (and shouldn’t) declare exception values for functions
  which return Python objects. Remember that a function with no declared
  return type implicitly returns a Python object. (Exceptions on such
  functions are implicitly propagated by returning `NULL`.)
* There’s a known performance pitfall when combining `nogil` and
  `except *` `@cython.exceptval(check=True)`.
  In this case Cython must always briefly re-acquire the GIL after a function
  call to check if an exception has been raised. This can commonly happen with a
  function returning nothing (C `void`). Simple workarounds are to mark the
  function as `noexcept` if you’re certain that exceptions cannot be thrown, or
  to change the return type to `int` and just let Cython use the return value
  as an error flag (by default, `-1` triggers the exception check).

### Checking return values of non-Cython functions[¶](#checking-return-values-of-non-cython-functions "Link to this heading")

It’s important to understand that the except clause does not cause an error to
be raised when the specified value is returned. For example, you can’t write
something like:

```
cdef extern FILE *fopen(char *filename, char *mode) except NULL # WRONG!
```

and expect an exception to be automatically raised if a call to `fopen()`
returns `NULL`. The except clause doesn’t work that way; its only purpose is
for propagating Python exceptions that have already been raised, either by a Cython
function or a C function that calls Python/C API routines. To get an exception
from a non-Python-aware function such as `fopen()`, you will have to check the
return value and raise it yourself, for example:

Pure PythonCython

```
from cython.cimports.libc.stdio import FILE, fopen
from cython.cimports.libc.stdlib import malloc, free
from cython.cimports.cpython.exc import PyErr_SetFromErrnoWithFilenameObject

def open_file():
    p = fopen("spam.txt", "r")   # The type of "p" is "FILE*", as returned by fopen().

    if p is cython.NULL:
        PyErr_SetFromErrnoWithFilenameObject(OSError, "spam.txt")
    ...


def allocating_memory(number=10):
    # Note that the type of the variable "my_array" is automatically inferred from the assignment.
    my_array = cython.cast(p_double, malloc(number * cython.sizeof(double)))
    if not my_array:  # same as 'is NULL' above
        raise MemoryError()
    ...
    free(my_array)
```

```
from libc.stdio cimport FILE, fopen
from libc.stdlib cimport malloc, free
from cpython.exc cimport PyErr_SetFromErrnoWithFilenameObject

def open_file():
    cdef FILE* p
    p = fopen("spam.txt", "r")
    if p is NULL:
        PyErr_SetFromErrnoWithFilenameObject(OSError, "spam.txt")
    ...


def allocating_memory(number=10):
    cdef double *my_array = <double *> malloc(number * sizeof(double))
    if not my_array:  # same as 'is NULL' above
        raise MemoryError()
    ...
    free(my_array)
```

### Overriding in extension types[¶](#overriding-in-extension-types "Link to this heading")

`cpdef`/`@ccall` methods can override C methods:

Pure PythonCython

```
@cython.cclass
class A:
    @cython.cfunc
    def foo(self):
        print("A")

@cython.cclass
class B(A):
    @cython.cfunc
    def foo(self, x=None):
        print("B", x)

@cython.cclass
class C(B):
    @cython.ccall
    def foo(self, x=True, k:cython.int = 3):
        print("C", x, k)
```

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

When subclassing an extension type with a Python class,
Python methods can override `cpdef`/`@ccall` methods but not plain C methods:

Pure PythonCython

```
@cython.cclass
class A:
    @cython.cfunc
    def foo(self):
        print("A")

@cython.cclass
class B(A):
    @cython.ccall
    def foo(self):
        print("B")

class C(B):  # NOTE: no cclass decorator
    def foo(self):
        print("C")
```

```
cdef class A:

    cdef foo(self):
        print("A")


cdef class B(A):

    cpdef foo(self):
        print("B")

class C(B):  # NOTE: not cdef class
    def foo(self):
        print("C")
```

If `C` above would be an extension type (`cdef class`),
this would not work correctly.
The Cython compiler will give a warning in that case.

## Automatic type conversions[¶](#automatic-type-conversions "Link to this heading")

In most situations, automatic conversions will be performed for the basic
numeric and string types when a Python object is used in a context requiring a
C value, or vice versa. The following table summarises the conversion
possibilities.

 C types  From Python types  To Python types  [unsigned] char,
[unsigned] short,
int, long  int, long  int  unsigned int,
unsigned long,
[unsigned] long long  int, long  long  float, double, long double  int, long, float  float  char\*  str/bytes  str/bytes [[3]](#id15 "#id15")  C array  iterable  list [[6]](#id17 "#id17")  struct,
union  dict [[5]](#id16 "#id16") [[7]](#id18 "#id18") 

[[3](#id11 "#id11")]

The conversion is to/from str for Python 2.x, and bytes for Python 3.x.


[[5](#id13 "#id13")]

The conversion from a C union type to a Python dict will add
a value for each of the union fields. Cython 0.23 and later, however,
will refuse to automatically convert a union with unsafe type
combinations. An example is a union of an `int` and a `char*`,
in which case the pointer value may or may not be a valid pointer.


[[6](#id12 "#id12")]

Other than signed/unsigned char[].
The conversion will fail if the length of C array is not known at compile time,
and when using a slice of a C array.


[[7](#id14 "#id14")]

The automatic conversion of a struct to a `dict` (and vice
versa) does have some potential pitfalls detailed
[elsewhere in the documentation](troubleshooting.html#automatic-conversion-pitfalls "troubleshooting.html#automatic-conversion-pitfalls").

### Caveats when using a Python string in a C context[¶](#caveats-when-using-a-python-string-in-a-c-context "Link to this heading")

You need to be careful when using a Python string in a context expecting a
`char*`. In this situation, a pointer to the contents of the Python string is
used, which is only valid as long as the Python string exists. So you need to
make sure that a reference to the original Python string is held for as long
as the C string is needed. If you can’t guarantee that the Python string will
live long enough, you will need to copy the C string.

Cython detects and prevents some mistakes of this kind. For instance, if you
attempt something like

Pure PythonCython

```
def main():
    s: cython.p_char
    s = pystring1 + pystring2
```

```
cdef char *s
s = pystring1 + pystring2
```

then Cython will produce the error message `Storing unsafe C derivative of temporary
Python reference`. The reason is that concatenating the two Python strings
produces a new Python string object that is referenced only by a temporary
internal variable that Cython generates. As soon as the statement has finished,
the temporary variable will be decrefed and the Python string deallocated,
leaving `s` dangling. Since this code could not possibly work, Cython refuses to
compile it.

The solution is to assign the result of the concatenation to a Python
variable, and then obtain the `char*` from that, i.e.

Pure PythonCython

```
def main():
    s: cython.p_char
    p = pystring1 + pystring2
    s = p
```

```
cdef char *s
p = pystring1 + pystring2
s = p
```

It is then your responsibility to hold the reference p for as long as
necessary.

Keep in mind that the rules used to detect such errors are only heuristics.
Sometimes Cython will complain unnecessarily, and sometimes it will fail to
detect a problem that exists. Ultimately, you need to understand the issue and
be careful what you do.

### Type Casting[¶](#type-casting "Link to this heading")

The Cython language supports type casting in a similar way as C. Where C uses `"("` and `")"`,
Cython uses `"<"` and `">"`. In pure python mode, the `cython.cast()` function is used. For example:

Pure PythonCython

```
def main():
    p: cython.p_char
    q: cython.p_float
    p = cython.cast(cython.p_char, q)
```

When casting a C value to a Python object type or vice versa,
Cython will attempt a coercion. Simple examples are casts like `cast(int, pyobj_value)`,
which convert a Python number to a plain C `int` value, or the statement `cast(bytes, charptr_value)`,
which copies a C `char*` string into a new Python bytes object.

Note

Cython will not prevent a redundant cast, but emits a warning for it.

To get the address of some Python object, use a cast to a pointer type
like `cast(p_void, ...)` or `cast(pointer[PyObject], ...)`.
You can also cast a C pointer back to a Python object reference
with `cast(object, ...)`, or to a more specific builtin or extension type
(e.g. `cast(MyExtType, ptr)`). This will increase the reference count of
the object by one, i.e. the cast returns an owned reference.
Here is an example:

```
cdef char *p
cdef float *q
p = <char*>q
```

When casting a C value to a Python object type or vice versa,
Cython will attempt a coercion. Simple examples are casts like `<int>pyobj_value`,
which convert a Python number to a plain C `int` value, or the statement `<bytes>charptr_value`,
which copies a C `char*` string into a new Python bytes object.

Note

Cython will not prevent a redundant cast, but emits a warning for it.

To get the address of some Python object, use a cast to a pointer type
like `<void*>` or `<PyObject*>`.
You can also cast a C pointer back to a Python object reference
with `<object>`, or to a more specific builtin or extension type
(e.g. `<MyExtType>ptr`). This will increase the reference count of
the object by one, i.e. the cast returns an owned reference.
Here is an example:

Pure PythonCython

casting\_python.pxd[¶](#id30 "Link to this code")

```
cdef extern from *:
    ctypedef Py_ssize_t Py_intptr_t
```

casting\_python.py[¶](#id31 "Link to this code")

```
from cython.cimports.cpython.ref import PyObject

def main():

    python_string = "foo"

    # Note that the variables below are automatically inferred
    # as the correct pointer type that is assigned to them.
    # They do not need to be typed explicitly.

    ptr = cython.cast(cython.p_void, python_string)
    adress_in_c = cython.cast(Py_intptr_t, ptr)
    address_from_void = adress_in_c        # address_from_void is a python int

    ptr2 = cython.cast(cython.pointer[PyObject], python_string)
    address_in_c2 = cython.cast(Py_intptr_t, ptr2)
    address_from_PyObject = address_in_c2  # address_from_PyObject is a python int

    assert address_from_void == address_from_PyObject == id(python_string)

    print(cython.cast(object, ptr))                     # Prints "foo"
    print(cython.cast(object, ptr2))                    # prints "foo"
```

Casting with `cast(object, ...)` creates an owned reference. Cython will automatically
perform a [`Py_INCREF()`](https://docs.python.org/3/c-api/refcounting.html#c.Py_INCREF "(in Python v3.13)") and [`Py_DECREF()`](https://docs.python.org/3/c-api/refcounting.html#c.Py_DECREF "(in Python v3.13)") operation. Casting to
`cast(pointer[PyObject], ...)` creates a borrowed reference, leaving the refcount unchanged.

casting\_python.pxd[¶](#id32 "Link to this code")

```
cdef extern from *:
    ctypedef Py_ssize_t Py_intptr_t
```

casting\_python.pyx[¶](#id33 "Link to this code")

```
from cpython.ref cimport PyObject

python_string = "foo"

cdef void* ptr = <void*>python_string
cdef Py_intptr_t adress_in_c = <Py_intptr_t>ptr
address_from_void = adress_in_c        # address_from_void is a python int

cdef PyObject* ptr2 = <PyObject*>python_string
cdef Py_intptr_t address_in_c2 = <Py_intptr_t>ptr2
address_from_PyObject = address_in_c2  # address_from_PyObject is a python int

assert address_from_void == address_from_PyObject == id(python_string)

print(<object>ptr)                     # Prints "foo"
print(<object>ptr2)                    # prints "foo"
```

The precedence of `<...>` is such that `<type>a.b.c` is interpreted as `<type>(a.b.c)`.

Casting to `<object>` creates an owned reference. Cython will automatically
perform a [`Py_INCREF()`](https://docs.python.org/3/c-api/refcounting.html#c.Py_INCREF "(in Python v3.13)") and [`Py_DECREF()`](https://docs.python.org/3/c-api/refcounting.html#c.Py_DECREF "(in Python v3.13)") operation. Casting to
`<PyObject *>` creates a borrowed reference, leaving the refcount unchanged.

### Checked Type Casts[¶](#checked-type-casts "Link to this heading")

A cast like `<MyExtensionType>x` or `cast(MyExtensionType, x)` will cast `x` to the class
`MyExtensionType` without any checking at all.

To have a cast checked, use `<MyExtensionType?>x` in Cython syntax
or `cast(MyExtensionType, x, typecheck=True)`.
In this case, Cython will apply a runtime check that raises a `TypeError`
if `x` is not an instance of `MyExtensionType`.
This tests for the exact class for builtin types,
but allows subclasses for [Extension Types](extension_types.html#extension-types "extension_types.html#extension-types").

## Statements and expressions[¶](#statements-and-expressions "Link to this heading")

Control structures and expressions follow Python syntax for the most part.
When applied to Python objects, they have the same semantics as in Python
(unless otherwise noted). Most of the Python operators can also be applied to
C values, with the obvious semantics.

If Python objects and C values are mixed in an expression, conversions are
performed automatically between Python objects and C numeric or string types.

Reference counts are maintained automatically for all Python objects, and all
Python operations are automatically checked for errors, with appropriate
action taken.

### Differences between C and Cython expressions[¶](#differences-between-c-and-cython-expressions "Link to this heading")

There are some differences in syntax and semantics between C expressions and
Cython expressions, particularly in the area of C constructs which have no
direct equivalent in Python.

* An integer literal is treated as a C constant, and will
  be truncated to whatever size your C compiler thinks appropriate.
  To get a Python integer (of arbitrary precision), cast immediately to
  an object (e.g. `<object>100000000000000000000` or `cast(object, 100000000000000000000)`). The `L`, `LL`,
  and `U` suffixes have the same meaning in Cython syntax as in C.
* There is no `->` operator in Cython. Instead of `p->x`, use `p.x`
* There is no unary `*` operator in Cython. Instead of `*p`, use `p[0]`
* There is an `&` operator in Cython, with the same semantics as in C.
  In pure python mode, use the `cython.address()` function instead.
* The null C pointer is called `NULL`, not `0`. `NULL` is a reserved word in Cython
  and `cython.NULL` is a special object in pure python mode.
* Type casts are written `<type>value` or `cast(type, value)`, for example,

  Pure PythonCython

  ```
  def main():
      p: cython.p_char
      q: cython.p_float

      p = cython.cast(cython.p_char, q)
  ```

  ```
  cdef char* p
  cdef float* q

  p = <char*>q
  ```

### Scope rules[¶](#scope-rules "Link to this heading")

Cython determines whether a variable belongs to a local scope, the module
scope, or the built-in scope completely statically. As with Python, assigning
to a variable which is not otherwise declared implicitly declares it to be a
variable residing in the scope where it is assigned. The type of the variable
depends on type inference, except for the global module scope, where it is
always a Python object.

### Built-in Functions[¶](#built-in-functions "Link to this heading")

Cython compiles calls to most built-in functions into direct calls to
the corresponding Python/C API routines, making them particularly fast.

Only direct function calls using these names are optimised. If you do
something else with one of these names that assumes it’s a Python object,
such as assign it to a Python variable, and later call it, the call will
be made as a Python function call.

 Function and arguments  Return type  Python/C API Equivalent  abs(obj)  object,
double, …  PyNumber\_Absolute, fabs,
fabsf, …  callable(obj)  bint  PyObject\_Callable  delattr(obj, name)  None  PyObject\_DelAttr  exec(code, [glob, [loc]])  object 


 dir(obj)  list  PyObject\_Dir  divmod(a, b)  tuple  PyNumber\_Divmod  getattr(obj, name, [default])
(Note 1)  object  PyObject\_GetAttr  hasattr(obj, name)  bint  PyObject\_HasAttr  hash(obj)  int / long  PyObject\_Hash  intern(obj)  object  Py\*\_InternFromString  isinstance(obj, type)  bint  PyObject\_IsInstance  issubclass(obj, type)  bint  PyObject\_IsSubclass  iter(obj, [sentinel])  object  PyObject\_GetIter  len(obj)  Py\_ssize\_t  PyObject\_Length  pow(x, y, [z])  object  PyNumber\_Power  reload(obj)  object  PyImport\_ReloadModule  repr(obj)  object  PyObject\_Repr  setattr(obj, name)  void  PyObject\_SetAttr 

Note 1: Pyrex originally provided a function `getattr3(obj, name, default)()`
corresponding to the three-argument form of the Python builtin [`getattr()`](https://docs.python.org/3/library/functions.html#getattr "(in Python v3.13)").
Cython still supports this function, but the usage is deprecated in favour of
the normal builtin, which Cython can optimise in both forms.

### Operator Precedence[¶](#operator-precedence "Link to this heading")

Keep in mind that there are some differences in operator precedence between
Python and C, and that Cython uses the Python precedences, not the C ones.

### Integer for-loops[¶](#integer-for-loops "Link to this heading")

Note

This syntax is supported only in Cython files. Use a normal for-in-range() loop instead.

Cython recognises the usual Python for-in-range integer loop pattern:

```
for i in range(n):
    ...
```

If `i` is declared as a [`cdef`](#cdef "#cdef") integer type, it will
optimise this into a pure C loop. This restriction is required as
otherwise the generated code wouldn’t be correct due to potential
integer overflows on the target architecture. If you are worried that
the loop is not being converted correctly, use the annotate feature of
the cython commandline (`-a`) to easily see the generated C code.
See [Automatic range conversion](pyrex_differences.html#automatic-range-conversion "pyrex_differences.html#automatic-range-conversion")

For backwards compatibility to Pyrex, Cython also supports a more verbose
form of for-loop which you might find in legacy code:

```
for i from 0 <= i < n:
    ...
```

or:

```
for i from 0 <= i < n by s:
    ...
```

where `s` is some integer step size.

Note

This syntax is deprecated and should not be used in new code.
Use the normal Python for-loop instead.

Some things to note about the for-from loop:

* The target expression must be a plain variable name.
* The name between the lower and upper bounds must be the same as the target
  name.
* The direction of iteration is determined by the relations. If they are both
  from the set {`<`, `<=`} then it is upwards; if they are both from the set
  {`>`, `>=`} then it is downwards. (Any other combination is disallowed.)

Like other Python looping statements, break and continue may be used in the
body, and the loop may have an else clause.

## Cython file types[¶](#cython-file-types "Link to this heading")

There are three file types in Cython:

* The implementation files, carrying a `.py` or `.pyx` suffix.
* The definition files, carrying a `.pxd` suffix.
* The include files, carrying a `.pxi` suffix.

### The implementation file[¶](#the-implementation-file "Link to this heading")

The implementation file, as the name suggest, contains the implementation
of your functions, classes, extension types, etc. Nearly all the
python syntax is supported in this file. Most of the time, a `.py`
file can be renamed into a `.pyx` file without changing
any code, and Cython will retain the python behavior.

It is possible for Cython to compile both `.py` and `.pyx` files.
The name of the file isn’t important if one wants to use only the Python syntax,
and Cython won’t change the generated code depending on the suffix used.
Though, if one want to use the Cython syntax, using a `.pyx` file is necessary.

In addition to the Python syntax, the user can also
leverage Cython syntax (such as `cdef`) to use C variables, can
declare functions as `cdef` or `cpdef` and can import C definitions
with [`cimport`](sharing_declarations.html#cimport "sharing_declarations.html#cimport"). Many other Cython features usable in implementation files
can be found throughout this page and the rest of the Cython documentation.

There are some restrictions on the implementation part of some [Extension Types](extension_types.html#extension-types "extension_types.html#extension-types")
if the corresponding definition file also defines that type.

Note

When a `.pyx` file is compiled, Cython first checks to see if a corresponding
`.pxd` file exists and processes it first. It acts like a header file for
a Cython `.pyx` file. You can put inside functions that will be used by
other Cython modules. This allows different Cython modules to use functions
and classes from each other without the Python overhead. To read more about
what how to do that, you can see [pxd files](../tutorial/pxd_files.html#pxd-files "../tutorial/pxd_files.html#pxd-files").

### The definition file[¶](#the-definition-file "Link to this heading")

A definition file is used to declare various things.

Any C declaration can be made, and it can be also a declaration of a C variable or
function implemented in a C/C++ file. This can be done with `cdef extern from`.
Sometimes, `.pxd` files are used as a translation of C/C++ header files
into a syntax that Cython can understand. This allows then the C/C++ variable and
functions to be used directly in implementation files with [`cimport`](sharing_declarations.html#cimport "sharing_declarations.html#cimport").
You can read more about it in [Interfacing with External C Code](external_C_code.html#external-c-code "external_C_code.html#external-c-code") and [Using C++ in Cython](wrapping_CPlusPlus.html#wrapping-cplusplus "wrapping_CPlusPlus.html#wrapping-cplusplus").

It can also contain the definition part of an extension type and the declarations
of functions for an external library.

It cannot contain the implementations of any C or Python functions, or any
Python class definitions, or any executable statements. It is needed when one
wants to access [`cdef`](#cdef "#cdef") attributes and methods, or to inherit from
[`cdef`](#cdef "#cdef") classes defined in this module.

Note

You don’t need to (and shouldn’t) declare anything in a declaration file
[`public`](extension_types.html#public "extension_types.html#public") in order to make it available to other Cython modules; its mere
presence in a definition file does that. You only need a public
declaration if you want to make something available to external C code.

### The include statement and include files[¶](#the-include-statement-and-include-files "Link to this heading")

Warning

Historically the `include` statement was used for sharing declarations.
Use [Sharing Declarations Between Cython Modules](sharing_declarations.html#sharing-declarations "sharing_declarations.html#sharing-declarations") instead.

A Cython source file can include material from other files using the include
statement, for example,:

```
include "spamstuff.pxi"
```

The contents of the named file are textually included at that point. The
included file can contain any complete statements or declarations that are
valid in the context where the include statement appears, including other
include statements. The contents of the included file should begin at an
indentation level of zero, and will be treated as though they were indented to
the level of the include statement that is including the file. The include
statement cannot, however, be used outside of the module scope, such as inside
of functions or class bodies.

Note

There are other mechanisms available for splitting Cython code into
separate parts that may be more appropriate in many cases. See
[Sharing Declarations Between Cython Modules](sharing_declarations.html#sharing-declarations "sharing_declarations.html#sharing-declarations").

## Conditional Compilation[¶](#conditional-compilation "Link to this heading")

Some language features are available for conditional compilation and compile-time
constants within a Cython source file.

Note

This feature has been deprecated and should not be used in new code.
It is very foreign to the Python language and also behaves
differently from the C preprocessor. It is often misunderstood by users.
For the current deprecation status, see [https://github.com/cython/cython/issues/4310](https://github.com/cython/cython/issues/4310 "https://github.com/cython/cython/issues/4310").
For alternatives, see [Deprecation of DEF / IF](migrating_to_cy30.html#deprecated-def-if "migrating_to_cy30.html#deprecated-def-if").

Note

This feature has very little use cases. Specifically, it is not a good
way to adapt code to platform and environment. Use runtime conditions,
conditional Python imports, or C compile time adaptation for this.
See, for example, [Including verbatim C code](external_C_code.html#verbatim-c "external_C_code.html#verbatim-c") or [Resolving naming conflicts - C name specifications](external_C_code.html#resolve-conflicts "external_C_code.html#resolve-conflicts").

Note

Cython currently does not support conditional compilation and compile-time
definitions in Pure Python mode. As it stands, this is unlikely to change.

### Compile-Time Definitions[¶](#compile-time-definitions "Link to this heading")

A compile-time constant can be defined using the DEF statement:

```
DEF FavouriteFood = u"spam"
DEF ArraySize = 42
DEF OtherArraySize = 2 * ArraySize + 17
```

The right-hand side of the `DEF` must be a valid compile-time expression.
Such expressions are made up of literal values and names defined using `DEF`
statements, combined using any of the Python expression syntax.

Note

Cython does not intend to copy literal compile-time values 1:1 into the generated code.
Instead, these values are internally represented and calculated as plain Python
values and use Python’s `repr()` when a serialisation is needed. This means
that values defined using `DEF` may lose precision or change their type
depending on the calculation rules of the Python environment where Cython parses and
translates the source code. Specifically, using `DEF` to define high-precision
floating point constants may not give the intended result and may generate different
C values in different Python versions.

The following compile-time names are predefined, corresponding to the values
returned by [`os.uname()`](https://docs.python.org/3/library/os.html#os.uname "(in Python v3.13)"). As noted above, they are not considered good ways
to adapt code to different platforms and are mostly provided for legacy reasons.

UNAME\_SYSNAME, UNAME\_NODENAME, UNAME\_RELEASE,
UNAME\_VERSION, UNAME\_MACHINE

The following selection of builtin constants and functions are also available:

None, True, False,
abs, all, any, ascii, bin, bool, bytearray, bytes, chr, cmp, complex, dict,
divmod, enumerate, filter, float, format, frozenset, hash, hex, int, len,
list, long, map, max, min, oct, ord, pow, range, reduce, repr, reversed,
round, set, slice, sorted, str, sum, tuple, xrange, zip

Note that some of these builtins may not be available when compiling under
Python 2.x or 3.x, or may behave differently in both.

A name defined using `DEF` can be used anywhere an identifier can appear,
and it is replaced with its compile-time value as though it were written into
the source at that point as a literal. For this to work, the compile-time
expression must evaluate to a Python value of type `int`, `long`,
`float`, `bytes` or `unicode` (`str` in Py3).

```
DEF FavouriteFood = u"spam"
DEF ArraySize = 42
DEF OtherArraySize = 2 * ArraySize + 17

cdef int[ArraySize] a1
cdef int[OtherArraySize] a2
print("I like", FavouriteFood)
```

Note

Compile-time constants are deprecated. The preferred way for declaring global
constants is using global `const` variables. See [Type qualifiers](#type-qualifiers "#type-qualifiers").

### Conditional Statements[¶](#conditional-statements "Link to this heading")

The `IF` statement can be used to conditionally include or exclude sections
of code at compile time. It works in a similar way to the `#if` preprocessor
directive in C.

```
IF ARRAY_SIZE > 64:
    include "large_arrays.pxi"
ELIF ARRAY_SIZE > 16:
    include "medium_arrays.pxi"
ELSE:
    include "small_arrays.pxi"
```

The `ELIF` and `ELSE` clauses are optional. An `IF` statement can appear
anywhere that a normal statement or declaration can appear, and it can contain
any statements or declarations that would be valid in that context, including
`DEF` statements and other `IF` statements.

The expressions in the `IF` and `ELIF` clauses must be valid compile-time
expressions as for the `DEF` statement, although they can evaluate to any
Python value, and the truth of the result is determined in the usual Python
way.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Language Basics](# "#")
  + [Declaring Data Types](#declaring-data-types "#declaring-data-types")
  + [C variable and type definitions](#c-variable-and-type-definitions "#c-variable-and-type-definitions")
    - [C Arrays](#c-arrays "#c-arrays")
    - [Structs, Unions, Enums](#structs-unions-enums "#structs-unions-enums")
    - [Types](#types "#types")
    - [Type qualifiers](#type-qualifiers "#type-qualifiers")
    - [Extension Types](#extension-types "#extension-types")
    - [Grouping multiple C declarations](#grouping-multiple-c-declarations "#grouping-multiple-c-declarations")
  + [Python functions vs. C functions](#python-functions-vs-c-functions "#python-functions-vs-c-functions")
    - [Python objects as parameters and return values](#python-objects-as-parameters-and-return-values "#python-objects-as-parameters-and-return-values")
    - [Optional Arguments](#optional-arguments "#optional-arguments")
    - [Keyword-only Arguments](#keyword-only-arguments "#keyword-only-arguments")
    - [Function Pointers](#function-pointers "#function-pointers")
    - [Error return values](#error-return-values "#error-return-values")
    - [Checking return values of non-Cython functions](#checking-return-values-of-non-cython-functions "#checking-return-values-of-non-cython-functions")
    - [Overriding in extension types](#overriding-in-extension-types "#overriding-in-extension-types")
  + [Automatic type conversions](#automatic-type-conversions "#automatic-type-conversions")
    - [Caveats when using a Python string in a C context](#caveats-when-using-a-python-string-in-a-c-context "#caveats-when-using-a-python-string-in-a-c-context")
    - [Type Casting](#type-casting "#type-casting")
    - [Checked Type Casts](#checked-type-casts "#checked-type-casts")
  + [Statements and expressions](#statements-and-expressions "#statements-and-expressions")
    - [Differences between C and Cython expressions](#differences-between-c-and-cython-expressions "#differences-between-c-and-cython-expressions")
    - [Scope rules](#scope-rules "#scope-rules")
    - [Built-in Functions](#built-in-functions "#built-in-functions")
    - [Operator Precedence](#operator-precedence "#operator-precedence")
    - [Integer for-loops](#integer-for-loops "#integer-for-loops")
  + [Cython file types](#cython-file-types "#cython-file-types")
    - [The implementation file](#the-implementation-file "#the-implementation-file")
    - [The definition file](#the-definition-file "#the-definition-file")
    - [The include statement and include files](#the-include-statement-and-include-files "#the-include-statement-and-include-files")
  + [Conditional Compilation](#conditional-compilation "#conditional-compilation")
    - [Compile-Time Definitions](#compile-time-definitions "#compile-time-definitions")
    - [Conditional Statements](#conditional-statements "#conditional-statements")

#### Previous topic

[Users Guide](index.html "previous chapter")

#### Next topic

[Extension Types](extension_types.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/language_basics.rst.txt "../../_sources/src/userguide/language_basics.rst.txt")

### Quick search

### Navigation

* [next](extension_types.html "Extension Types")
* [previous](index.html "Users Guide") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Language Basics

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

