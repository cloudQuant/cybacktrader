




Extension Types — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/extension_types.html "/en/stable/src/userguide/extension_types.html").

### Navigation

* [next](special_methods.html "Special Methods of Extension Types")
* [previous](language_basics.html "Language Basics") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Extension Types

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Extension Types[¶](#extension-types "Link to this heading")

## Introduction[¶](#introduction "Link to this heading")

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

As well as creating normal user-defined classes with the Python class
statement, Cython also lets you create new built-in Python types, known as
[extension types](glossary.html#term-Extension-type "glossary.html#term-Extension-type"). You define an extension type using the [`cdef`](language_basics.html#cdef "language_basics.html#cdef") class
statement or decorating the class with the `@cclass` decorator. Here’s an example:

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

As you can see, a Cython extension type definition looks a lot like a Python
class definition. Within it, you use the [`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.14)") statement to define methods that
can be called from Python code. You can even define many of the special
methods such as `__init__()` as you would in Python.

The main difference is that you can define attributes using

* the [`cdef`](language_basics.html#cdef "language_basics.html#cdef") statement,
* the `cython.declare()` function or
* the annotation of an attribute name.

Pure PythonCython

```
@cython.cclass
class Shrubbery:
    width = cython.declare(cython.int)
    height: cython.int
```

```
cdef class Shrubbery:

    cdef int width
    cdef int height
```

The attributes may be Python objects (either generic or of a
particular extension type), or they may be of any C data type. So you can use
extension types to wrap arbitrary C data structures and provide a Python-like
interface to them.

## Static Attributes[¶](#static-attributes "Link to this heading")

Attributes of an extension type are stored directly in the object’s C struct.
The set of attributes is fixed at compile time; you can’t add attributes to an
extension type instance at run time simply by assigning to them, as you could
with a Python class instance. However, you can explicitly enable support
for dynamically assigned attributes, or subclass the extension type with a normal
Python class, which then supports arbitrary attribute assignments.
See [Dynamic Attributes](#dynamic-attributes "#dynamic-attributes").

There are two ways that attributes of an extension type can be accessed: by
Python attribute lookup, or by direct access to the C struct from Cython code.
Python code is only able to access attributes of an extension type by the
first method, but Cython code can use either method.

By default, extension type attributes are only accessible by direct access,
not Python access, which means that they are not accessible from Python code.
To make them accessible from Python code, you need to declare them as
[`public`](#public "#public") or [`readonly`](#readonly "#readonly"). For example:

Pure PythonCython

```
import cython

@cython.cclass
class Shrubbery:
    width = cython.declare(cython.int, visibility='public')
    height = cython.declare(cython.int, visibility='public')
    depth = cython.declare(cython.float, visibility='readonly')
```

```
cdef class Shrubbery:
    cdef public int width, height

    cdef readonly float depth
```

makes the width and height attributes readable and writable from Python code,
and the depth attribute readable but not writable.

Note

You can only expose simple C types, such as ints, floats, and
strings, for Python access. You can also expose Python-valued attributes.

Note

Also the [`public`](#public "#public") and [`readonly`](#readonly "#readonly") options apply only to
Python access, not direct access. All the attributes of an extension type
are always readable and writable by C-level access.

## Dynamic Attributes[¶](#dynamic-attributes "Link to this heading")

It is not possible to add attributes to an extension type at runtime by default.
You have two ways of avoiding this limitation, both add an overhead when
a method is called from Python code. Especially when calling hybrid methods declared
with [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") in .pyx files or with the `@ccall` decorator.

The first approach is to create a Python subclass:

Pure PythonCython

```
@cython.cclass
class Animal:

    number_of_legs: cython.int

    def __cinit__(self, number_of_legs: cython.int):
        self.number_of_legs = number_of_legs


class ExtendableAnimal(Animal):  # Note that we use class, not cdef class
    pass


dog = ExtendableAnimal(4)
dog.has_tail = True
```

```
cdef class Animal:

    cdef int number_of_legs

    def __init__(self, int number_of_legs):
        self.number_of_legs = number_of_legs


class ExtendableAnimal(Animal):  # Note that we use class, not cdef class
    pass


dog = ExtendableAnimal(4)
dog.has_tail = True
```

Declaring a `__dict__` attribute is the second way of enabling dynamic attributes:

Pure PythonCython

```
@cython.cclass
class Animal:

    number_of_legs: cython.int
    __dict__: dict

    def __cinit__(self, number_of_legs: cython.int):
        self.number_of_legs = number_of_legs


dog = Animal(4)
dog.has_tail = True
```

```
cdef class Animal:

    cdef int number_of_legs
    cdef dict __dict__

    def __init__(self, int number_of_legs):
        self.number_of_legs = number_of_legs


dog = Animal(4)
dog.has_tail = True
```

## Type declarations[¶](#type-declarations "Link to this heading")

Before you can directly access the attributes of an extension type, the Cython
compiler must know that you have an instance of that type, and not just a
generic Python object. It knows this already in the case of the `self`
parameter of the methods of that type, but in other cases you will have to use
a type declaration.

For example, in the following function:

Pure PythonCython

```
@cython.cfunc
def widen_shrubbery(sh, extra_width): # BAD
    sh.width = sh.width + extra_width
```

```
cdef widen_shrubbery(sh, extra_width): # BAD
    sh.width = sh.width + extra_width
```

because the `sh` parameter hasn’t been given a type, the width attribute
will be accessed by a Python attribute lookup. If the attribute has been
declared [`public`](#public "#public") or [`readonly`](#readonly "#readonly") then this will work, but it
will be very inefficient. If the attribute is private, it will not work at all
– the code will compile, but an attribute error will be raised at run time.

The solution is to declare `sh` as being of type `Shrubbery`, as
follows:

Pure PythonCython

```
import cython
from cython.cimports.my_module import Shrubbery

@cython.cfunc
def widen_shrubbery(sh: Shrubbery, extra_width):
    sh.width = sh.width + extra_width
```

```
from my_module cimport Shrubbery


cdef widen_shrubbery(Shrubbery sh, extra_width):
    sh.width = sh.width + extra_width
```

Now the Cython compiler knows that `sh` has a C attribute called
`width` and will generate code to access it directly and efficiently.
The same consideration applies to local variables, for example:

Pure PythonCython

```
import cython
from cython.cimports.my_module import Shrubbery

@cython.cfunc
def another_shrubbery(sh1: Shrubbery) -> Shrubbery:
    sh2: Shrubbery
    sh2 = Shrubbery()
    sh2.width = sh1.width
    sh2.height = sh1.height
    return sh2
```

```
from my_module cimport Shrubbery


cdef Shrubbery another_shrubbery(Shrubbery sh1):
    cdef Shrubbery sh2
    sh2 = Shrubbery()
    sh2.width = sh1.width
    sh2.height = sh1.height
    return sh2
```

Note

Here, we cimport the class `Shrubbery` (using the [`cimport`](sharing_declarations.html#cimport "sharing_declarations.html#cimport") statement
or importing from special `cython.cimports` package), and this is necessary
to declare the type at compile time. To be able to cimport an extension type,
we split the class definition into two parts, one in a definition file and
the other in the corresponding implementation file. You should read
[Sharing Extension Types](sharing_declarations.html#sharing-extension-types "sharing_declarations.html#sharing-extension-types") to learn to do that.

### Type Testing and Casting[¶](#type-testing-and-casting "Link to this heading")

Suppose I have a method `quest()` which returns an object of type `Shrubbery`.
To access its width I could write:

Pure PythonCython

```
sh: Shrubbery = quest()
print(sh.width)
```

```
cdef Shrubbery sh = quest()
print(sh.width)
```

which requires the use of a local variable and performs a type test on assignment.
If you know the return value of `quest()` will be of type `Shrubbery`
you can use a cast to write:

Pure PythonCython

```
print( cython.cast(Shrubbery, quest()).width )
```

```
print( (<Shrubbery>quest()).width )
```

This may be dangerous if `quest()` is not actually a `Shrubbery`, as it
will try to access width as a C struct member which may not exist. At the C level,
rather than raising an [`AttributeError`](https://docs.python.org/3/library/exceptions.html#AttributeError "(in Python v3.14)"), either an nonsensical result will be
returned (interpreting whatever data is at that address as an int) or a segfault
may result from trying to access invalid memory. Instead, one can write:

Pure PythonCython

```
print( cython.cast(Shrubbery, quest(), typecheck=True).width )
```

```
print( (<Shrubbery?>quest()).width )
```

which performs a type check (possibly raising a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)")) before making the
cast and allowing the code to proceed.

To explicitly test the type of an object, use the `isinstance()` builtin function.
For known builtin or extension types, Cython translates these into a
fast and safe type check that ignores changes to
the object’s `__class__` attribute etc., so that after a successful
`isinstance()` test, code can rely on the expected C structure of the
extension type and its C-level attributes (stored in the object’s C struct) and
[`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@cfunc` methods.

## Extension types and None[¶](#extension-types-and-none "Link to this heading")

Cython handles `None` values differently in C-like type declarations and when Python annotations are used.

In [`cdef`](language_basics.html#cdef "language_basics.html#cdef") declarations and C-like function argument declarations (`func(list x)`),
when you declare an argument or C variable as having an extension or Python builtin type,
Cython will allow it to take on the value `None` as well as values of its
declared type. This is analogous to the way a C pointer can take on the value
`NULL`, and you need to exercise the same caution because of it. There is no
problem as long as you are performing Python operations on it, because full
dynamic type checking will be applied. However, when you access C attributes
of an extension type (as in the widen\_shrubbery function above), it’s up to
you to make sure the reference you’re using is not `None` – in the
interests of efficiency, Cython does not check this.

With the C-like declaration syntax, you need to be particularly careful when
exposing Python functions which take extension types as arguments:

```
def widen_shrubbery(Shrubbery sh, extra_width): # This is
    sh.width = sh.width + extra_width           # dangerous!
```

The users of our module could crash it by passing `None` for the `sh`
parameter.

As in Python, whenever it is unclear whether a variable can be `None`,
but the code requires a non-None value, an explicit check can help:

```
def widen_shrubbery(Shrubbery sh, extra_width):
    if sh is None:
        raise TypeError
    sh.width = sh.width + extra_width
```

but since this is anticipated to be such a frequent requirement, Cython language
provides a more convenient way. Parameters of a Python function declared as an
extension type can have a `not None` clause:

```
def widen_shrubbery(Shrubbery sh not None, extra_width):
    sh.width = sh.width + extra_width
```

Now the function will automatically check that `sh` is `not None` along
with checking that it has the right type.

When annotations are used, the behaviour follows the Python typing semantics of
[PEP-484](https://www.python.org/dev/peps/pep-0484/ "https://www.python.org/dev/peps/pep-0484/") instead.
The value `None` is not allowed when a variable is annotated only with its plain type:

```
def widen_shrubbery(sh: Shrubbery, extra_width):  # TypeError is raised
    sh.width = sh.width + extra_width             # when sh is None
```

To also allow `None`, `typing.Optional[ ]` must be used explicitly.
For function arguments, this is also automatically allowed when they have a
default argument of None`, e.g. `func(x: list = None)` does not require `typing.Optional`:

```
import typing
def widen_shrubbery(sh: typing.Optional[Shrubbery], extra_width):
    if sh is None:
        # We want to raise a custom exception in case of a None value.
        raise ValueError
    sh.width = sh.width + extra_width
```

The upside of using annotations here is that they are safe by default because
you need to explicitly allow `None` values for them.

Note

The `not None` and `typing.Optional` can only be used in Python functions (defined with
[`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.14)") and without `@cython.cfunc` decorator) and not C functions
(defined with [`cdef`](language_basics.html#cdef "language_basics.html#cdef") or decorated using `@cython.cfunc`). If
you need to check whether a parameter to a C function is `None`, you will
need to do it yourself.

Note

Some more things:

* The `self` parameter of a method of an extension type is guaranteed never to
  be `None`.
* When comparing a value with `None`, keep in mind that, if `x` is a Python
  object, `x is None` and `x is not None` are very efficient because they
  translate directly to C pointer comparisons, whereas `x == None` and
  `x != None`, or simply using `x` as a boolean value (as in `if x: ...`)
  will invoke Python operations and therefore be much slower.
* `typing.Union[tp, None]` and `tp | None` can be used as alternatives to `typing.Optional`

## Special methods[¶](#special-methods "Link to this heading")

Although the principles are similar, there are substantial differences between
many of the `__xxx__()` special methods of extension types and their Python
counterparts. There is a [separate page](special_methods.html#special-methods "special_methods.html#special-methods") devoted to this subject, and you should
read it carefully before attempting to use any special methods in your
extension types.

## Properties[¶](#properties "Link to this heading")

You can declare properties in an extension class using the same syntax as in ordinary Python code:

Pure PythonCython

```
@cython.cclass
class Spam:
    @property
    def cheese(self):
        # This is called when the property is read.
        ...

    @cheese.setter
    def cheese(self, value):
        # This is called when the property is written.
        ...

    @cheese.deleter
    def cheese(self):
        # This is called when the property is deleted.
```

```
cdef class Spam:

    @property
    def cheese(self):
        # This is called when the property is read.
        ...

    @cheese.setter
    def cheese(self, value):
        # This is called when the property is written.
        ...

    @cheese.deleter
    def cheese(self):
        # This is called when the property is deleted.
```

There is also a special (deprecated) legacy syntax for defining properties in an extension class:

```
cdef class Spam:

    property cheese:

        "A doc string can go here."

        def __get__(self):
            # This is called when the property is read.
            ...

        def __set__(self, value):
            # This is called when the property is written.
            ...

        def __del__(self):
            # This is called when the property is deleted.
```

The `__get__()`, `__set__()` and `__del__()` methods are all
optional; if they are omitted, an exception will be raised when the
corresponding operation is attempted.

Here’s a complete example. It defines a property which adds to a list each
time it is written to, returns the list when it is read, and empties the list
when it is deleted:

Pure PythonCython

```
import cython

@cython.cclass
class CheeseShop:

    cheeses: object

    def __cinit__(self):
        self.cheeses = []

    @property
    def cheese(self):
        return f"We don't have: {self.cheeses}"

    @cheese.setter
    def cheese(self, value):
        self.cheeses.append(value)

    @cheese.deleter
    def cheese(self):
        del self.cheeses[:]

# Test input
from cheesy import CheeseShop

shop = CheeseShop()
print(shop.cheese)

shop.cheese = "camembert"
print(shop.cheese)

shop.cheese = "cheddar"
print(shop.cheese)

del shop.cheese
print(shop.cheese)
```

```
cdef class CheeseShop:

    cdef object cheeses

    def __cinit__(self):
        self.cheeses = []

    @property
    def cheese(self):
        return f"We don't have: {self.cheeses}"

    @cheese.setter
    def cheese(self, value):
        self.cheeses.append(value)

    @cheese.deleter
    def cheese(self):
        del self.cheeses[:]

# Test input
from cheesy import CheeseShop

shop = CheeseShop()
print(shop.cheese)

shop.cheese = "camembert"
print(shop.cheese)

shop.cheese = "cheddar"
print(shop.cheese)

del shop.cheese
print(shop.cheese)
```

```
# Test output
We don't have: []
We don't have: ['camembert']
We don't have: ['camembert', 'cheddar']
We don't have: []
```

## C methods[¶](#c-methods "Link to this heading")

Extension types can have C methods as well as Python methods. Like C
functions, C methods are declared using

* [`cdef`](language_basics.html#cdef "language_basics.html#cdef") instead of [`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.14)") or `@cfunc` decorator for C methods, or
* [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") instead of [`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.14)") or `@ccall` decorator for hybrid methods.

C methods are “virtual”, and may be overridden in derived extension types.
In addition, [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef")/`@ccall` methods can even be overridden by Python
methods when called as C method. This adds a little to their calling overhead
compared to a [`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@cfunc` method:

Pure PythonCython

```
import cython

@cython.cclass
class Parrot:

    @cython.cfunc
    def describe(self) -> cython.void:
        print("This parrot is resting.")

@cython.cclass
class Norwegian(Parrot):

    @cython.cfunc
    def describe(self) -> cython.void:
        Parrot.describe(self)
        print("Lovely plumage!")

cython.declare(p1=Parrot, p2=Parrot)
p1 = Parrot()
p2 = Norwegian()
print("p2:")
p2.describe()
```

```
cdef class Parrot:



    cdef void describe(self):
        print("This parrot is resting.")


cdef class Norwegian(Parrot):


    cdef void describe(self):
        Parrot.describe(self)
        print("Lovely plumage!")

cdef Parrot p1, p2
p1 = Parrot()
p2 = Norwegian()
print("p2:")
p2.describe()
```

```
# Output
p1:
This parrot is resting.
p2:
This parrot is resting.
Lovely plumage!
```

The above example also illustrates that a C method can call an inherited C
method using the usual Python technique, i.e.:

```
Parrot.describe(self)
```

[`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@ccall` methods can be declared static by using the `@staticmethod` decorator.
This can be especially useful for constructing classes that take non-Python compatible types:

Pure PythonCython

```
import cython
from cython.cimports.libc.stdlib import free

@cython.cclass
class OwnedPointer:
    ptr: cython.p_void

    def __dealloc__(self):
        if self.ptr is not cython.NULL:
            free(self.ptr)

    @staticmethod
    @cython.cfunc
    def create(ptr: cython.p_void):
        p = OwnedPointer()
        p.ptr = ptr
        return p
```

```
from libc.stdlib cimport free


cdef class OwnedPointer:
    cdef void* ptr

    def __dealloc__(self):
        if self.ptr is not NULL:
            free(self.ptr)


    @staticmethod
    cdef create(void* ptr):
        p = OwnedPointer()
        p.ptr = ptr
        return p
```

Note

Cython currently does not support decorating [`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@ccall` methods with
the `@classmethod` decorator.

## Subclassing[¶](#subclassing "Link to this heading")

If an extension type inherits from other types, the first base class must be
a built-in type or another extension type:

Pure PythonCython

```
@cython.cclass
class Parrot:
    ...

@cython.cclass
class Norwegian(Parrot):
    ...
```

```
cdef class Parrot:
    ...


cdef class Norwegian(Parrot):
    ...
```

A complete definition of the base type must be available to Cython, so if the
base type is a built-in type, it must have been previously declared as an
extern extension type. If the base type is defined in another Cython module, it
must either be declared as an extern extension type or imported using the
[`cimport`](sharing_declarations.html#cimport "sharing_declarations.html#cimport") statement or importing from the special `cython.cimports` package.

Multiple inheritance is supported, however the second and subsequent base
classes must be an ordinary Python class (not an extension type or a built-in
type).

Cython extension types can also be subclassed in Python. A Python class can
inherit from multiple extension types provided that the usual Python rules for
multiple inheritance are followed (i.e. the C layouts of all the base classes
must be compatible).

There is a way to prevent extension types from
being subtyped in Python. This is done via the `final` directive,
usually set on an extension type or C method using a decorator:

Pure PythonCython

```
import cython

@cython.final
@cython.cclass
class Parrot:
   def describe(self): pass

@cython.cclass
class Lizard:

   @cython.final
   @cython.cfunc
   def done(self): pass
```

```
cimport cython

@cython.final
cdef class Parrot:
   def describe(self): pass



cdef class Lizard:


   @cython.final
   cdef done(self): pass
```

Trying to create a Python subclass from a final type or overriding a final method will raise
a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") at runtime. Cython will also prevent subtyping a
final type or overriding a final method inside of the same module, i.e. creating
an extension type that uses a final type as its base type will fail at compile time.
Note, however, that this restriction does not currently propagate to
other extension modules, so Cython is unable to prevent final extension types
from being subtyped at the C level by foreign code.

## Forward-declaring extension types[¶](#forward-declaring-extension-types "Link to this heading")

Extension types can be forward-declared, like [`struct`](language_basics.html#struct "language_basics.html#struct") and
[`union`](language_basics.html#union "language_basics.html#union") types. This is usually not necessary and violates the
DRY principle (Don’t Repeat Yourself).

If you are forward-declaring an extension type that has a base class, you must
specify the base class in both the forward declaration and its subsequent
definition, for example,:

```
cdef class A(B)

...

cdef class A(B):
    # attributes and methods
```

## Fast instantiation[¶](#fast-instantiation "Link to this heading")

Cython provides two ways to speed up the instantiation of extension types.
The first one is a direct call to the `__new__()` special static method,
as known from Python. For an extension type `Penguin`, you could use
the following code:

Pure PythonCython

```
import cython

@cython.cclass
class Penguin:
    food: object

    def __cinit__(self, food):
        self.food = food

    def __init__(self, food):
        print("eating!")

normal_penguin = Penguin('fish')
fast_penguin = Penguin.__new__(Penguin, 'wheat')  # note: not calling __init__() !
```

```
cdef class Penguin:
    cdef object food

    def __cinit__(self, food):
        self.food = food

    def __init__(self, food):
        print("eating!")

normal_penguin = Penguin('fish')
fast_penguin = Penguin.__new__(Penguin, 'wheat')  # note: not calling __init__() !
```

Note that the path through `__new__()` will not call the type’s
`__init__()` method (again, as known from Python). Thus, in the example
above, the first instantiation will print `eating!`, but the second will
not. This is only one of the reasons why the `__cinit__()` method is
safer than the normal `__init__()` method for initialising extension types
and bringing them into a correct and safe state.
See the [Initialisation Methods Section](special_methods.html#initialisation-methods "special_methods.html#initialisation-methods") about
the differences.

The second performance improvement applies to types that are often created
and deleted in a row, so that they can benefit from a freelist. Cython
provides the decorator `@cython.freelist(N)` for this, which creates a
statically sized freelist of `N` instances for a given type. Example:

Pure PythonCython

```
import cython

@cython.freelist(8)
@cython.cclass
class Penguin:
    food: object
    def __cinit__(self, food):
        self.food = food

penguin = Penguin('fish 1')
penguin = None
penguin = Penguin('fish 2')  # does not need to allocate memory!
```

```
cimport cython


@cython.freelist(8)
cdef class Penguin:
    cdef object food
    def __cinit__(self, food):
        self.food = food

penguin = Penguin('fish 1')
penguin = None
penguin = Penguin('fish 2')  # does not need to allocate memory!
```

## Instantiation from existing C/C++ pointers[¶](#instantiation-from-existing-c-c-pointers "Link to this heading")

It is quite common to want to instantiate an extension class from an existing
(pointer to a) data structure, often as returned by external C/C++ functions.

As extension classes can only accept Python objects as arguments in their
constructors, this necessitates the use of factory functions or factory methods. For example:

Pure PythonCython

```
import cython
from cython.cimports.libc.stdlib import malloc, free

# Example C struct
my_c_struct = cython.struct(
    a = cython.int,
    b = cython.int,
)

@cython.cclass
class WrapperClass:
    """A wrapper class for a C/C++ data structure"""
    _ptr: cython.pointer[my_c_struct]
    ptr_owner: cython.bint

    def __cinit__(self):
        self.ptr_owner = False

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self._ptr is not cython.NULL and self.ptr_owner is True:
            free(self._ptr)
            self._ptr = cython.NULL

    def __init__(self):
        # Prevent accidental instantiation from normal Python code
        # since we cannot pass a struct pointer into a Python constructor.
        raise TypeError("This class cannot be instantiated directly.")

    # Extension class properties
    @property
    def a(self):
        return self._ptr.a if self._ptr is not cython.NULL else None

    @property
    def b(self):
        return self._ptr.b if self._ptr is not cython.NULL else None

    @staticmethod
    @cython.cfunc
    def from_ptr(_ptr: cython.pointer[my_c_struct], owner: cython.bint=False) -> WrapperClass:
        """Factory function to create WrapperClass objects from
        given my_c_struct pointer.

        Setting ``owner`` flag to ``True`` causes
        the extension type to ``free`` the structure pointed to by ``_ptr``
        when the wrapper object is deallocated."""
        # Fast call to __new__() that bypasses the __init__() constructor.
        wrapper: WrapperClass  = WrapperClass.__new__(WrapperClass)
        wrapper._ptr = _ptr
        wrapper.ptr_owner = owner
        return wrapper

    @staticmethod
    @cython.cfunc
    def new_struct() -> WrapperClass:
        """Factory function to create WrapperClass objects with
        newly allocated my_c_struct"""
        _ptr: cython.pointer[my_c_struct] = cython.cast(
                cython.pointer[my_c_struct], malloc(cython.sizeof(my_c_struct)))
        if _ptr is cython.NULL:
            raise MemoryError
        _ptr.a = 0
        _ptr.b = 0
        return WrapperClass.from_ptr(_ptr, owner=True)
```

```
from libc.stdlib cimport malloc, free

# Example C struct
ctypedef struct my_c_struct:
    int a
    int b



cdef class WrapperClass:
    """A wrapper class for a C/C++ data structure"""
    cdef my_c_struct *_ptr
    cdef bint ptr_owner

    def __cinit__(self):
        self.ptr_owner = False

    def __dealloc__(self):
        # De-allocate if not null and flag is set
        if self._ptr is not NULL and self.ptr_owner is True:
            free(self._ptr)
            self._ptr = NULL

    def __init__(self):
        # Prevent accidental instantiation from normal Python code
        # since we cannot pass a struct pointer into a Python constructor.
        raise TypeError("This class cannot be instantiated directly.")

    # Extension class properties
    @property
    def a(self):
        return self._ptr.a if self._ptr is not NULL else None

    @property
    def b(self):
        return self._ptr.b if self._ptr is not NULL else None


    @staticmethod
    cdef WrapperClass from_ptr(my_c_struct *_ptr, bint owner=False):
        """Factory function to create WrapperClass objects from
        given my_c_struct pointer.

        Setting ``owner`` flag to ``True`` causes
        the extension type to ``free`` the structure pointed to by ``_ptr``
        when the wrapper object is deallocated."""
        # Fast call to __new__() that bypasses the __init__() constructor.
        cdef WrapperClass wrapper = WrapperClass.__new__(WrapperClass)
        wrapper._ptr = _ptr
        wrapper.ptr_owner = owner
        return wrapper


    @staticmethod
    cdef WrapperClass new_struct():
        """Factory function to create WrapperClass objects with
        newly allocated my_c_struct"""
        cdef my_c_struct *_ptr = <my_c_struct *>malloc(sizeof(my_c_struct))

        if _ptr is NULL:
            raise MemoryError
        _ptr.a = 0
        _ptr.b = 0
        return WrapperClass.from_ptr(_ptr, owner=True)
```

To then create a `WrapperClass` object from an existing `my_c_struct`
pointer, `WrapperClass.from_ptr(ptr)` can be used in Cython code. To allocate
a new structure and wrap it at the same time, `WrapperClass.new_struct` can be
used instead.

It is possible to create multiple Python objects all from the same pointer
which point to the same in-memory data, if that is wanted, though care must be
taken when de-allocating as can be seen above.
Additionally, the `ptr_owner` flag can be used to control which
`WrapperClass` object owns the pointer and is responsible for de-allocation -
this is set to `False` by default in the example and can be enabled by calling
`from_ptr(ptr, owner=True)`.

The GIL must not be released in `__dealloc__` either, or another lock used
if it is, in such cases or race conditions can occur with multiple
de-allocations.

Being a part of the object constructor, the `__cinit__` method has a Python
signature, which makes it unable to accept a `my_c_struct` pointer as an
argument.

Attempts to use pointers in a Python signature will result in errors like:

```
Cannot convert 'my_c_struct *' to Python object
```

This is because Cython cannot automatically convert a pointer to a Python
object, unlike with native types like `int`.

Note that for native types, Cython will copy the value and create a new Python
object while in the above case, data is not copied and deallocating memory is
a responsibility of the extension class.

## Making extension types weak-referenceable[¶](#making-extension-types-weak-referenceable "Link to this heading")

By default, extension types do not support having weak references made to
them. You can enable weak referencing by declaring a C attribute of type
object called `__weakref__`. For example:

Pure PythonCython

```
@cython.cclass
class ExplodingAnimal:
    """This animal will self-destruct when it is
    no longer strongly referenced."""

    __weakref__: object
```

```
cdef class ExplodingAnimal:
    """This animal will self-destruct when it is
    no longer strongly referenced."""

    cdef object __weakref__
```

## Controlling deallocation and garbage collection in CPython[¶](#controlling-deallocation-and-garbage-collection-in-cpython "Link to this heading")

Note

This section only applies to the usual CPython implementation
of Python. Other implementations like PyPy work differently.

### Introduction[¶](#dealloc-intro "Link to this heading")

First of all, it is good to understand that there are two ways to
trigger deallocation of Python objects in CPython:
CPython uses reference counting for all objects and any object with a
reference count of zero is immediately deallocated. This is the most
common way of deallocating an object. For example, consider

```
>>> x = "foo"
>>> x = "bar"
```

After executing the second line, the string `"foo"` is no longer referenced,
so it is deallocated. This is done using the [`PyTypeObject.tp_dealloc`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_dealloc "(in Python v3.14)") slot, which can be
customized in Cython by implementing `__dealloc__`.

The second mechanism is the cyclic garbage collector.
This is meant to resolve cyclic reference cycles such as

```
>>> class Object:
...     pass
>>> def make_cycle():
...     x = Object()
...     y = [x]
...     x.attr = y
```

When calling `make_cycle`, a reference cycle is created since `x`
references `y` and vice versa. Even though neither `x` or `y`
are accessible after `make_cycle` returns, both have a reference count
of 1, so they are not immediately deallocated. At regular times, the garbage
collector runs, which will notice the reference cycle
(using the [`PyTypeObject.tp_traverse`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_traverse "(in Python v3.14)") slot) and break it.
Breaking a reference cycle means taking an object in the cycle
and removing all references from it to other Python objects (we call this
clearing an object). Clearing is almost the same as deallocating, except
that the actual object is not yet freed. For `x` in the example above,
the attributes of `x` would be removed from `x`.

Note that it suffices to clear just one object in the reference cycle,
since there is no longer a cycle after clearing one object. Once the cycle
is broken, the usual refcount-based deallocation will actually remove the
objects from memory. Clearing is implemented in the [`PyTypeObject.tp_clear`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_clear "(in Python v3.14)") slot.
As we just explained, it is sufficient that one object in the cycle
implements [`PyTypeObject.tp_clear`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_clear "(in Python v3.14)").

### Enabling the deallocation trashcan[¶](#enabling-the-deallocation-trashcan "Link to this heading")

In CPython, it is possible to create deeply recursive objects. For example:

```
>>> L = None
>>> for i in range(2**20):
...     L = [L]
```

Now imagine that we delete the final `L`. Then `L` deallocates
`L[0]`, which deallocates `L[0][0]` and so on until we reach a
recursion depth of `2**20`. This deallocation is done in C and such
a deep recursion will likely overflow the C call stack, crashing Python.

CPython invented a mechanism for this called the trashcan. It limits the
recursion depth of deallocations by delaying some deallocations.

By default, Cython extension types do not use the trashcan but it can be
enabled by setting the `trashcan` directive to `True`. For example:

Pure PythonCython

```
import cython
@cython.trashcan(True)
@cython.cclass
class Object:
    __dict__: dict
```

```
cimport cython
@cython.trashcan(True)
cdef class Object:
    cdef dict __dict__
```

Trashcan usage is inherited by subclasses
(unless explicitly disabled by `@cython.trashcan(False)`).
Some builtin types like `list` use the trashcan, so subclasses of it
use the trashcan by default.

### Disabling cycle breaking (`tp_clear`)[¶](#disabling-cycle-breaking-tp-clear "Link to this heading")

By default, each extension type will support the cyclic garbage collector of
CPython. If any Python objects can be referenced, Cython will automatically
generate the [`PyTypeObject.tp_traverse`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_traverse "(in Python v3.14)") and [`PyTypeObject.tp_clear`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_clear "(in Python v3.14)") slots. This is usually what you
want.

There is at least one reason why this might not be what you want: If you need
to cleanup some external resources in the `__dealloc__` special function and
your object happened to be in a reference cycle, the garbage collector may
have triggered a call to [`PyTypeObject.tp_clear`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_clear "(in Python v3.14)") to clear the object
(see [Introduction](#dealloc-intro "#dealloc-intro")).

In that case, any object references have vanished when `__dealloc__`
is called. Now your cleanup code lost access to the objects it has to clean up.
To fix this, you can disable clearing instances of a specific class by using
the `no_gc_clear` directive:

Pure PythonCython

```
@cython.no_gc_clear
@cython.cclass
class DBCursor:
    conn: DBConnection
    raw_cursor: cython.pointer[DBAPI_Cursor]
    # ...
    def __dealloc__(self):
        DBAPI_close_cursor(self.conn.raw_conn, self.raw_cursor)
```

```
@cython.no_gc_clear
cdef class DBCursor:
    cdef DBConnection conn
    cdef DBAPI_Cursor *raw_cursor
    # ...
    def __dealloc__(self):
        DBAPI_close_cursor(self.conn.raw_conn, self.raw_cursor)
```

This example tries to close a cursor via a database connection when the Python
object is destroyed. The `DBConnection` object is kept alive by the reference
from `DBCursor`. But if a cursor happens to be in a reference cycle, the
garbage collector may delete the database connection reference,
which makes it impossible to clean up the cursor.

If you use `no_gc_clear`, it is important that any given reference cycle
contains at least one object without `no_gc_clear`. Otherwise, the cycle
cannot be broken, which is a memory leak.

### Disabling cyclic garbage collection[¶](#disabling-cyclic-garbage-collection "Link to this heading")

In rare cases, extension types can be guaranteed not to participate in cycles,
but the compiler won’t be able to prove this. This would be the case if
the class can never reference itself, even indirectly.
In that case, you can manually disable cycle collection by using the
`no_gc` directive, but beware that doing so when in fact the extension type
can participate in cycles could cause memory leaks:

Pure PythonCython

```
@cython.no_gc
@cython.cclass
class UserInfo:
    name: str
    addresses: tuple
```

```
@cython.no_gc
cdef class UserInfo:

    cdef str name
    cdef tuple addresses
```

If you can be sure addresses will contain only references to strings,
the above would be safe, and it may yield a significant speedup, depending on
your usage pattern.

## Controlling pickling[¶](#controlling-pickling "Link to this heading")

By default, Cython will generate a `__reduce__()` method to allow pickling
an extension type if and only if each of its members are convertible to Python
and it has no `__cinit__` method.
To require this behavior (i.e. throw an error at compile time if a class
cannot be pickled) decorate the class with `@cython.auto_pickle(True)`.
One can also annotate with `@cython.auto_pickle(False)` to get the old
behavior of not generating a `__reduce__` method in any case.

Manually implementing a `__reduce__` or `__reduce_ex__` method will also
disable this auto-generation and can be used to support pickling of more
complicated types.

## Public and external extension types[¶](#public-and-external-extension-types "Link to this heading")

Extension types can be declared extern or public. An extern extension type
declaration makes an extension type defined in external C code available to a
Cython module. A public extension type declaration makes an extension type
defined in a Cython module available to external C code.

Note

Cython currently does not support Extension types declared as extern or public
in Pure Python mode. This is not considered an issue since public/extern extension
types are most commonly declared in .pxd files and not in .py files.

### External extension types[¶](#external-extension-types "Link to this heading")

An extern extension type allows you to gain access to the internals of Python
objects defined in the Python core or in a non-Cython extension module.

Note

In previous versions of Pyrex, extern extension types were also used to
reference extension types defined in another Pyrex module. While you can still
do that, Cython provides a better mechanism for this. See
[Sharing Declarations Between Cython Modules](sharing_declarations.html#sharing-declarations "sharing_declarations.html#sharing-declarations").

Here is an example which will let you get at the C-level members of the
built-in complex object:

```
cdef extern from "complexobject.h":

    struct Py_complex:
        double real
        double imag

    ctypedef class __builtin__.complex [object PyComplexObject]:
        cdef Py_complex cval

# A function which uses the above type
def spam(complex c):
    print("Real:", c.cval.real)
    print("Imag:", c.cval.imag)
```

Note

Some important things:

1. In this example, [`ctypedef`](language_basics.html#ctypedef "language_basics.html#ctypedef") class has been used. This is
   because, in the Python header files, the `PyComplexObject` struct is
   declared with:

   ```
   typedef struct {
       ...
   } PyComplexObject;
   ```

   At runtime, a check will be performed when importing the Cython
   c-extension module that `__builtin__.complex`’s [`PyTypeObject.tp_basicsize`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_basicsize "(in Python v3.14)")
   matches `` sizeof(`PyComplexObject) ``. This check can fail if the Cython
   c-extension module was compiled with one version of the
   `complexobject.h` header but imported into a Python with a changed
   header. This check can be tweaked by using `check_size` in the name
   specification clause.
2. As well as the name of the extension type, the module in which its type
   object can be found is also specified. See the implicit importing section
   below.
3. When declaring an external extension type, you don’t declare any
   methods. Declaration of methods is not required in order to call them,
   because the calls are Python method calls. Also, as with
   [`struct`](language_basics.html#struct "language_basics.html#struct") and [`union`](language_basics.html#union "language_basics.html#union"), if your extension class
   declaration is inside a [`cdef`](language_basics.html#cdef "language_basics.html#cdef") extern from block, you only need to
   declare those C members which you wish to access.

### Name specification clause[¶](#name-specification-clause "Link to this heading")

The part of the class declaration in square brackets is a special feature only
available for extern or public extension types. The full form of this clause
is:

```
[object object_struct_name, type type_object_name, check_size cs_option]
```

Where:

* `object_struct_name` is the name to assume for the type’s C struct.
* `type_object_name` is the name to assume for the type’s statically
  declared type object.
* `cs_option` is `warn` (the default), `error`, or `ignore` and is only
  used for external extension types. If `error`, the `sizeof(object_struct)`
  that was found at compile time must match the type’s runtime [`PyTypeObject.tp_basicsize`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_basicsize "(in Python v3.14)")
  exactly, otherwise the module import will fail with an error. If `warn`
  or `ignore`, the `object_struct` is allowed to be smaller than the type’s
  [`PyTypeObject.tp_basicsize`](https://docs.python.org/3/c-api/typeobj.html#c.PyTypeObject.tp_basicsize "(in Python v3.14)"), which indicates the runtime type may be part of an updated
  module, and that the external module’s developers extended the object in a
  backward-compatible fashion (only adding new fields to the end of the object).
  If `warn`, a warning will be emitted in this case.

The clauses can be written in any order.

If the extension type declaration is inside a [`cdef`](language_basics.html#cdef "language_basics.html#cdef") extern from
block, the object clause is required, because Cython must be able to generate
code that is compatible with the declarations in the header file. Otherwise,
for extern extension types, the object clause is optional.

For public extension types, the object and type clauses are both required,
because Cython must be able to generate code that is compatible with external C
code.

### Attribute name matching and aliasing[¶](#attribute-name-matching-and-aliasing "Link to this heading")

Sometimes the type’s C struct as specified in `object_struct_name` may use
different labels for the fields than those in the [`PyTypeObject`](https://docs.python.org/3/c-api/type.html#c.PyTypeObject "(in Python v3.14)"). This can
easily happen in hand-coded C extensions where the `PyTypeObject_Foo` has a
getter method, but the name does not match the name in the `PyFooObject`. In
NumPy, for instance, python-level `dtype.itemsize` is a getter for the C
struct field `elsize`. Cython supports aliasing field names so that one can
write `dtype.itemsize` in Cython code which will be compiled into direct
access of the C struct field, without going through a C-API equivalent of
`dtype.__getattr__('itemsize')`.

For example, we may have an extension module `foo_extension`:

```
cdef class Foo:
    cdef public int field0, field1, field2;

    def __init__(self, f0, f1, f2):
        self.field0 = f0
        self.field1 = f1
        self.field2 = f2
```

but a C struct in a file `foo_nominal.h`:

```
typedef struct {
     PyObject_HEAD
     int f0;
     int f1;
     int f2;
 } FooStructNominal;
```

Note that the struct uses `f0`, `f1`, `f2` but they are `field0`,
`field1`, and `field2` in `Foo`. We are given this situation, including
a header file with that struct, and we wish to write a function to sum the
values. If we write an extension module `wrapper`:

```
cdef extern from "foo_nominal.h":

    ctypedef class foo_extension.Foo [object FooStructNominal]:
        cdef:
            int field0
            int field1
            int field2

def sum(Foo f):
    return f.field0 + f.field1 + f.field2
```

then `wrapper.sum(f)` (where `f = foo_extension.Foo(1, 2, 3)`) will still
use the C-API equivalent of:

```
return f.__getattr__('field0') +
       f.__getattr__('field1') +
       f.__getattr__('field1')
```

instead of the desired C equivalent of `return f->f0 + f->f1 + f->f2`. We can
alias the fields by using:

```
cdef extern from "foo_nominal.h":

    ctypedef class foo_extension.Foo [object FooStructNominal]:
        cdef:
            int field0 "f0"
            int field1 "f1"
            int field2 "f2"

def sum(Foo f) except -1:
    return f.field0 + f.field1 + f.field2
```

and now Cython will replace the slow `__getattr__` with direct C access to
the FooStructNominal fields. This is useful when directly processing Python
code. No changes to Python need be made to achieve significant speedups, even
though the field names in Python and C are different. Of course, one should
make sure the fields are equivalent.

### C inline properties[¶](#c-inline-properties "Link to this heading")

Similar to Python property attributes, Cython provides a way to declare C-level
properties on external extension types. This is often used to shadow Python
attributes through faster C level data access, but can also be used to add certain
functionality to existing types when using them from Cython. The declarations
must use cdef inline.

For example, the above `complex` type could also be declared like this:

```
cdef extern from "complexobject.h":

    struct Py_complex:
        double real
        double imag

    ctypedef class __builtin__.complex [object PyComplexObject]:
        cdef Py_complex cval

        @property
        cdef inline double real(self):
            return self.cval.real

        @property
        cdef inline double imag(self):
            return self.cval.imag


def cprint(complex c):
    print(f"{c.real :.4f}{c.imag :+.4f}j")  # uses C calls to the above property methods.
```

### Implicit importing[¶](#implicit-importing "Link to this heading")

Cython requires you to include a module name in an extern extension class
declaration, for example,:

```
cdef extern class MyModule.Spam:
    ...
```

The type object will be implicitly imported from the specified module and
bound to the corresponding name in this module. In other words, in this
example an implicit:

```
from MyModule import Spam
```

statement will be executed at module load time.

The module name can be a dotted name to refer to a module inside a package
hierarchy, for example,:

```
cdef extern class My.Nested.Package.Spam:
    ...
```

You can also specify an alternative name under which to import the type using
an as clause, for example,:

```
cdef extern class My.Nested.Package.Spam as Yummy:
   ...
```

which corresponds to the implicit import statement:

```
from My.Nested.Package import Spam as Yummy
```

### Type names vs. constructor names[¶](#type-names-vs-constructor-names "Link to this heading")

Inside a Cython module, the name of an extension type serves two distinct
purposes. When used in an expression, it refers to a module-level global
variable holding the type’s constructor (i.e. its type-object). However, it
can also be used as a C type name to declare variables, arguments and return
values of that type.

When you declare:

```
cdef extern class MyModule.Spam:
    ...
```

the name Spam serves both these roles. There may be other names by which you
can refer to the constructor, but only Spam can be used as a type name. For
example, if you were to explicitly import MyModule, you could use
`MyModule.Spam()` to create a Spam instance, but you wouldn’t be able to use
`MyModule.Spam` as a type name.

When an as clause is used, the name specified in the as clause also takes over
both roles. So if you declare:

```
cdef extern class MyModule.Spam as Yummy:
    ...
```

then Yummy becomes both the type name and a name for the constructor. Again,
there are other ways that you could get hold of the constructor, but only
Yummy is usable as a type name.

## Public extension types[¶](#public-extension-types "Link to this heading")

An extension type can be declared public, in which case a `.h` file is
generated containing declarations for its object struct and type object. By
including the `.h` file in external C code that you write, that code can
access the attributes of the extension type.

## Dataclass extension types[¶](#dataclass-extension-types "Link to this heading")

Cython supports extension types that behave like the dataclasses defined in
the Python 3.7+ standard library. The main benefit of using a dataclass is
that it can auto-generate simple `__init__`, `__repr__` and comparison
functions. The Cython implementation behaves as much like the Python
standard library implementation as possible and therefore the documentation
here only briefly outlines the differences - if you plan on using them
then please read [the documentation for the standard library module](https://docs.python.org/3/library/dataclasses.html "https://docs.python.org/3/library/dataclasses.html").

Dataclasses can be declared using the `@dataclasses.dataclass`
decorator on a Cython extension type (types marked `cdef` or created with the
`cython.cclass` decorator). Alternatively the `@cython.dataclasses.dataclass`
decorator can be applied to any class to both turn it into an extension type and
a dataclass. If
you need to define special properties on a field then use `dataclasses.field`
(or `cython.dataclasses.field` will work too)

Pure PythonCython

```
import cython
try:
    import typing
    import dataclasses
except ImportError:
    pass  # The modules don't actually have to exists for Cython to use them as annotations

@dataclasses.dataclass
@cython.cclass
class MyDataclass:
    # fields can be declared using annotations
    a: cython.int = 0
    b: double = dataclasses.field(default_factory = lambda: 10, repr=False)


    c: str = 'hello'


    # typing.InitVar and typing.ClassVar also work
    d: dataclasses.InitVar[double] = 5
    e: typing.ClassVar[list] = []
```

```
cimport cython
try:
    import typing
    import dataclasses
except ImportError:
    pass  # The modules don't actually have to exists for Cython to use them as annotations


@dataclasses.dataclass
cdef class MyDataclass:
    # fields can be declared using annotations
    a: cython.int = 0
    b: cython.double = dataclasses.field(default_factory = lambda: 10, repr=False)

    # fields can also be declared using `cdef`:
    cdef str c   # add `readonly` or `public` to if `c` needs to be accessible from Python
    c = "hello"  # assignment of default value on a separate line
    # note: `@dataclass(frozen)` is not enforced on `cdef` attributes

    # typing.InitVar and typing.ClassVar also work
    d: dataclasses.InitVar[cython.double] = 5
    e: typing.ClassVar[list] = []
```

You may use C-level types such as structs, pointers, or C++ classes.
However, you may find these types are not compatible with the auto-generated
special methods - for example if they cannot be converted from a Python
type they cannot be passed to a constructor, and so you must use a
`default_factory` to initialize them. Like with the Python implementation, you can also control
which special functions an attribute is used in using `field()`.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Extension Types](# "#")
  + [Introduction](#introduction "#introduction")
  + [Static Attributes](#static-attributes "#static-attributes")
  + [Dynamic Attributes](#dynamic-attributes "#dynamic-attributes")
  + [Type declarations](#type-declarations "#type-declarations")
    - [Type Testing and Casting](#type-testing-and-casting "#type-testing-and-casting")
  + [Extension types and None](#extension-types-and-none "#extension-types-and-none")
  + [Special methods](#special-methods "#special-methods")
  + [Properties](#properties "#properties")
  + [C methods](#c-methods "#c-methods")
  + [Subclassing](#subclassing "#subclassing")
  + [Forward-declaring extension types](#forward-declaring-extension-types "#forward-declaring-extension-types")
  + [Fast instantiation](#fast-instantiation "#fast-instantiation")
  + [Instantiation from existing C/C++ pointers](#instantiation-from-existing-c-c-pointers "#instantiation-from-existing-c-c-pointers")
  + [Making extension types weak-referenceable](#making-extension-types-weak-referenceable "#making-extension-types-weak-referenceable")
  + [Controlling deallocation and garbage collection in CPython](#controlling-deallocation-and-garbage-collection-in-cpython "#controlling-deallocation-and-garbage-collection-in-cpython")
    - [Introduction](#dealloc-intro "#dealloc-intro")
    - [Enabling the deallocation trashcan](#enabling-the-deallocation-trashcan "#enabling-the-deallocation-trashcan")
    - [Disabling cycle breaking (`tp_clear`)](#disabling-cycle-breaking-tp-clear "#disabling-cycle-breaking-tp-clear")
    - [Disabling cyclic garbage collection](#disabling-cyclic-garbage-collection "#disabling-cyclic-garbage-collection")
  + [Controlling pickling](#controlling-pickling "#controlling-pickling")
  + [Public and external extension types](#public-and-external-extension-types "#public-and-external-extension-types")
    - [External extension types](#external-extension-types "#external-extension-types")
    - [Name specification clause](#name-specification-clause "#name-specification-clause")
    - [Attribute name matching and aliasing](#attribute-name-matching-and-aliasing "#attribute-name-matching-and-aliasing")
    - [C inline properties](#c-inline-properties "#c-inline-properties")
    - [Implicit importing](#implicit-importing "#implicit-importing")
    - [Type names vs. constructor names](#type-names-vs-constructor-names "#type-names-vs-constructor-names")
  + [Public extension types](#public-extension-types "#public-extension-types")
  + [Dataclass extension types](#dataclass-extension-types "#dataclass-extension-types")

#### Previous topic

[Language Basics](language_basics.html "previous chapter")

#### Next topic

[Special Methods of Extension Types](special_methods.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/extension_types.rst.txt "../../_sources/src/userguide/extension_types.rst.txt")

### Quick search

### Navigation

* [next](special_methods.html "Special Methods of Extension Types")
* [previous](language_basics.html "Language Basics") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Extension Types

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

