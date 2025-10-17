




Using C++ in Cython — Cython 3.1.4 documentation

### Navigation

* [next](fusedtypes.html "Fused Types (Templates)")
* [previous](early_binding_for_speed.html "Early Binding for Speed") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Using C++ in Cython

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Using C++ in Cython[¶](#using-c-in-cython "Link to this heading")

## Overview[¶](#overview "Link to this heading")

Cython has native support for most of the C++ language. Specifically:

* C++ objects can be [dynamically allocated](glossary.html#term-Dynamic-allocation-or-Heap-allocation "glossary.html#term-Dynamic-allocation-or-Heap-allocation") with `new` and `del` keywords.
* C++ objects can be [stack-allocated](glossary.html#term-Stack-allocation "glossary.html#term-Stack-allocation").
* C++ classes can be declared with the new keyword `cppclass`.
* Templated classes and functions are supported.
* Overloaded functions are supported.
* Overloading of C++ operators (such as `operator+`, `operator[]`, …) is supported.

### Procedure Overview[¶](#procedure-overview "Link to this heading")

The general procedure for wrapping a C++ file can now be described as follows:

* Specify C++ language in a `setup.py` script or locally in a source file.
* Create one or more `.pxd` files with `cdef extern from` blocks and
  (if existing) the C++ namespace name. In these blocks:

  + declare classes as `cdef cppclass` blocks
  + declare public names (variables, methods and constructors)
* `cimport` them in one or more extension modules (`.pyx` files).

## A simple Tutorial[¶](#a-simple-tutorial "Link to this heading")

### An example C++ API[¶](#an-example-c-api "Link to this heading")

Here is a tiny C++ API which we will use as an example throughout this
document. Let’s assume it will be in a header file called
`Rectangle.h`:

```
#ifndef RECTANGLE_H
#define RECTANGLE_H

namespace shapes {
    class Rectangle {
        public:
            int x0, y0, x1, y1;
            Rectangle();
            Rectangle(int x0, int y0, int x1, int y1);
            ~Rectangle();
            int getArea();
            void getSize(int* width, int* height);
            void move(int dx, int dy);
    };
}

#endif
```

and the implementation in the file called `Rectangle.cpp`:

```
#include <iostream>
#include "Rectangle.h"

namespace shapes {

    // Default constructor
    Rectangle::Rectangle () {}

    // Overloaded constructor
    Rectangle::Rectangle (int x0, int y0, int x1, int y1) {
        this->x0 = x0;
        this->y0 = y0;
        this->x1 = x1;
        this->y1 = y1;
    }

    // Destructor
    Rectangle::~Rectangle () {}

    // Return the area of the rectangle
    int Rectangle::getArea () {
        return (this->x1 - this->x0) * (this->y1 - this->y0);
    }

    // Get the size of the rectangle.
    // Put the size in the pointer args
    void Rectangle::getSize (int *width, int *height) {
        (*width) = x1 - x0;
        (*height) = y1 - y0;
    }

    // Move the rectangle by dx dy
    void Rectangle::move (int dx, int dy) {
        this->x0 += dx;
        this->y0 += dy;
        this->x1 += dx;
        this->y1 += dy;
    }
}
```

This is pretty dumb, but should suffice to demonstrate the steps involved.

### Declaring a C++ class interface[¶](#declaring-a-c-class-interface "Link to this heading")

The procedure for wrapping a C++ class is quite similar to that for wrapping
normal C structs, with a couple of additions. Let’s start here by creating the
basic `cdef extern from` block:

```
cdef extern from "Rectangle.h" namespace "shapes":
```

This will make the C++ class def for Rectangle available. Note the namespace declaration.
Namespaces are simply used to make the fully qualified name of the object,
and can be nested (e.g. `"outer::inner"`) or even refer to
classes (e.g. `"namespace::MyClass` to declare static members on MyClass).

#### Declare class with cdef cppclass[¶](#declare-class-with-cdef-cppclass "Link to this heading")

Now, let’s add the Rectangle class to this extern from block - just copy the
class name from Rectangle.h and adjust for Cython syntax, so now it becomes:

```
cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
```

#### Add public attributes[¶](#add-public-attributes "Link to this heading")

We now need to declare the attributes and methods for use on Cython. We put those declarations
in a file called `Rectangle.pxd`. You can see it as a header file
which is readable by Cython:

```
cdef extern from "Rectangle.cpp":
    pass

# Declare the class with cdef
cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        Rectangle() except +
        Rectangle(int, int, int, int) except +
        int x0, y0, x1, y1
        int getArea()
        void getSize(int* width, int* height)
        void move(int, int)
```

Note that the constructor is declared as “except +”. If the C++ code or
the initial memory allocation raises an exception due to a failure, this
will let Cython safely raise an appropriate Python exception instead
(see below). Without this declaration, C++ exceptions originating from
the constructor will not be handled by Cython.

We use the lines:

```
cdef extern from "Rectangle.cpp":
    pass
```

to include the C++ code from `Rectangle.cpp`. It is also possible to specify to
setuptools that `Rectangle.cpp` is a source. To do that, you can add this directive at the
top of the `.pyx` (not `.pxd`) file:

```
# distutils: sources = Rectangle.cpp
```

Note that when you use `cdef extern from`, the path that you specify is relative to the current
file, but if you use the distutils directive, the path is relative to the
`setup.py`. If you want to discover the path of the sources when
running the `setup.py`, you can use the `aliases` argument
of the `cythonize()` function.

#### Declare a var with the wrapped C++ class[¶](#declare-a-var-with-the-wrapped-c-class "Link to this heading")

We’ll create a `.pyx` file named `rect.pyx` to build our wrapper. We’re
using a name other than `Rectangle`, but if you prefer giving the same name
to the wrapper as the C++ class, see the section on
[resolving naming conflicts](external_C_code.html#resolve-conflicts "external_C_code.html#resolve-conflicts").

Within, we use cdef to declare a var of the class with the C++ `new` statement:

```
# distutils: language = c++

from Rectangle cimport Rectangle

def main():
    rec_ptr = new Rectangle(1, 2, 3, 4)  # Instantiate a Rectangle object on the heap
    try:
        rec_area = rec_ptr.getArea()
    finally:
        del rec_ptr  # delete heap allocated object

    cdef Rectangle rec_stack  # Instantiate a Rectangle object on the stack
```

The line:

```
# distutils: language = c++
```

is to indicate to Cython that this `.pyx` file has to be compiled to C++.

It’s also possible to declare a stack allocated object, as long as it has
a “default” constructor:

```
cdef extern from "Foo.h":
    cdef cppclass Foo:
        Foo()

def func():
    cdef Foo foo
    ...
```

See the section on the [cpp\_locals directive](#cpp-locals-directive "#cpp-locals-directive") for a way
to avoid requiring a nullary/default constructor.

Note that, like C++, if the class has only one constructor and it
is a nullary one, it’s not necessary to declare it.

### Create Cython wrapper class[¶](#create-cython-wrapper-class "Link to this heading")

At this point, we have exposed into our pyx file’s namespace the interface
of the C++ Rectangle type. Now, we need to make this accessible from
external Python code (which is our whole point).

Common programming practice is to create a Cython extension type which
holds a C++ instance as an attribute and create a bunch of
forwarding methods. So we can implement the Python extension type as:

```
# distutils: language = c++

from Rectangle cimport Rectangle

# Create a Cython extension type which holds a C++ instance
# as an attribute and create a bunch of forwarding methods
# Python extension type.
cdef class PyRectangle:
    cdef Rectangle c_rect  # Hold a C++ instance which we're wrapping

    def __init__(self, int x0, int y0, int x1, int y1):
        self.c_rect = Rectangle(x0, y0, x1, y1)

    def get_area(self):
        return self.c_rect.getArea()

    def get_size(self):
        cdef int width, height
        self.c_rect.getSize(&width, &height)
        return width, height

    def move(self, dx, dy):
        self.c_rect.move(dx, dy)
```

And there we have it. From a Python perspective, this extension type will look
and feel just like a natively defined Rectangle class.
It should be noted that if you want to give
attribute access, you could just implement some properties:

```
# distutils: language = c++

from Rectangle cimport Rectangle

cdef class PyRectangle:
    cdef Rectangle c_rect

    def __init__(self, int x0, int y0, int x1, int y1):
        self.c_rect = Rectangle(x0, y0, x1, y1)

    def get_area(self):
        return self.c_rect.getArea()

    def get_size(self):
        cdef int width, height
        self.c_rect.getSize(&width, &height)
        return width, height

    def move(self, dx, dy):
        self.c_rect.move(dx, dy)

    # Attribute access
    @property
    def x0(self):
        return self.c_rect.x0
    @x0.setter
    def x0(self, x0):
        self.c_rect.x0 = x0

    # Attribute access
    @property
    def x1(self):
        return self.c_rect.x1
    @x1.setter
    def x1(self, x1):
        self.c_rect.x1 = x1

    # Attribute access
    @property
    def y0(self):
        return self.c_rect.y0
    @y0.setter
    def y0(self, y0):
        self.c_rect.y0 = y0

    # Attribute access
    @property
    def y1(self):
        return self.c_rect.y1
    @y1.setter
    def y1(self, y1):
        self.c_rect.y1 = y1
```

Cython initializes C++ class attributes of a cdef class using the nullary constructor.
If the class you’re wrapping does not have a nullary constructor, you must store a pointer
to the wrapped class and manually allocate and deallocate it. Alternatively, the
[cpp\_locals directive](#cpp-locals-directive "#cpp-locals-directive") avoids the need for the pointer and only initializes the
C++ class attribute when it is assigned to.
A convenient and safe place to do so is in the \_\_cinit\_\_ and \_\_dealloc\_\_ methods
which are guaranteed to be called exactly once upon creation and deletion of the Python
instance.

```
# distutils: language = c++

from Rectangle cimport Rectangle

cdef class PyRectangle:
    cdef Rectangle*c_rect  # hold a pointer to the C++ instance which we're wrapping

    def __cinit__(self):
        self.c_rect = new Rectangle()

    def __init__(self, int x0, int y0, int x1, int y1):
        self.c_rect.x0 = x0
        self.c_rect.y0 = y0
        self.c_rect.x1 = x1
        self.c_rect.y1 = y1

    def __dealloc__(self):
        del self.c_rect
```

## Compilation and Importing[¶](#compilation-and-importing "Link to this heading")

To compile a Cython module, it is necessary to have a `setup.py` file:

```
from setuptools import setup

from Cython.Build import cythonize

setup(ext_modules=cythonize("rect.pyx"))
```

Run `$ python setup.py build_ext --inplace`

To test it, open the Python interpreter:

```
>>> import rect
>>> x0, y0, x1, y1 = 1, 2, 3, 4
>>> rect_obj = rect.PyRectangle(x0, y0, x1, y1)
>>> print(dir(rect_obj))
['__class__', '__delattr__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__',
 '__getattribute__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__le__',
 '__lt__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__',
 '__setstate__', '__sizeof__', '__str__', '__subclasshook__', 'get_area', 'get_size', 'move']
```

## Advanced C++ features[¶](#advanced-c-features "Link to this heading")

We describe here all the C++ features that were not discussed in the above tutorial.

### Overloading[¶](#overloading "Link to this heading")

Overloading is very simple. Just declare the method with different parameters
and use any of them:

```
cdef extern from "Foo.h":
    cdef cppclass Foo:
        Foo(int)
        Foo(bool)
        Foo(int, bool)
        Foo(int, int)
```

### Overloading operators[¶](#overloading-operators "Link to this heading")

Cython uses C++ naming for overloading operators:

```
cdef extern from "foo.h":
    cdef cppclass Foo:
        Foo()
        Foo operator+(Foo)
        Foo operator-(Foo)
        int operator*(Foo)
        int operator/(int)
        int operator*(int, Foo) # allows 1*Foo()
    # nonmember operators can also be specified outside the class
    double operator/(double, Foo)


cdef Foo foo = new Foo()

foo2 = foo + foo
foo2 = foo - foo

x = foo * foo2
x = foo / 1

x = foo[0] * foo2
x = foo[0] / 1
x = 1*foo[0]

cdef double y
y = 2.0/foo[0]
```

Note that if one has pointers to C++ objects, dereferencing must be done
to avoid doing pointer arithmetic rather than arithmetic on the objects
themselves:

```
cdef Foo* foo_ptr = new Foo()
foo = foo_ptr[0] + foo_ptr[0]
x = foo_ptr[0] / 2

del foo_ptr
```

### Nested class declarations[¶](#nested-class-declarations "Link to this heading")

C++ allows nested class declaration. Class declarations can also be
nested in Cython:

```
# distutils: language = c++

cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[T]:
        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        vector()
        void push_back(T&)
        T& operator[](int)
        T& at(int)
        iterator begin()
        iterator end()

cdef vector[int].iterator iter  #iter is declared as being of type vector<int>::iterator
```

Note that the nested class is declared with a `cppclass` but without a `cdef`,
as it is already part of a `cdef` declaration section.

### C++ operators not compatible with Python syntax[¶](#c-operators-not-compatible-with-python-syntax "Link to this heading")

Cython tries to keep its syntax as close as possible to standard Python.
Because of this, certain C++ operators, like the preincrement `++foo`
or the dereferencing operator `*foo` cannot be used with the same
syntax as C++. Cython provides functions replacing these operators in
a special module `cython.operator`. The functions provided are:

* `cython.operator.dereference` for dereferencing. `dereference(foo)`
  will produce the C++ code `*(foo)`
* `cython.operator.preincrement` for pre-incrementation. `preincrement(foo)`
  will produce the C++ code `++(foo)`.
  Similarly for `predecrement`, `postincrement` and `postdecrement`.
* `cython.operator.comma` for the comma operator. `comma(a, b)`
  will produce the C++ code `((a), (b))`.

These functions need to be cimported. Of course, one can use a
`from ... cimport ... as` to have shorter and more readable functions.
For example: `from cython.operator cimport dereference as deref`.

For completeness, it’s also worth mentioning `cython.operator.address`
which can also be written `&foo`.

### Templates[¶](#templates "Link to this heading")

Cython uses a bracket syntax for templating. A simple example for wrapping C++ vector:

```
# distutils: language = c++

# import dereference and increment operators
from cython.operator cimport dereference as deref, preincrement as inc

cdef extern from "<vector>" namespace "std":
    cdef cppclass vector[T]:
        cppclass iterator:
            T operator*()
            iterator operator++()
            bint operator==(iterator)
            bint operator!=(iterator)
        vector()
        void push_back(T&)
        T& operator[](int)
        T& at(int)
        iterator begin()
        iterator end()

cdef vector[int] *v = new vector[int]()
cdef int i
for i in range(10):
    v.push_back(i)

cdef vector[int].iterator it = v.begin()
while it != v.end():
    print(deref(it))
    inc(it)

del v
```

Multiple template parameters can be defined as a list, such as `[T, U, V]`
or `[int, bool, char]`. Optional template parameters can be indicated
by writing `[T, U, V=*]`. In the event that Cython needs to explicitly
reference the type of a default template parameter for an incomplete template
instantiation, it will write `MyClass<T, U>::V`, so if the class provides
a typedef for its template parameters it is preferable to use that name here.

Template functions are defined similarly to class templates, with
the template parameter list following the function name:

```
# distutils: language = c++

cdef extern from "<algorithm>" namespace "std":
    T max[T](T a, T b)

print(max[long](3, 4))
print(max(1.5, 2.5))  # simple template argument deduction
```

### Standard library[¶](#standard-library "Link to this heading")

Most of the containers of the C++ Standard Library have been declared
in pxd files located
in [/Cython/Includes/libcpp](https://github.com/cython/cython/tree/master/Cython/Includes/libcpp "https://github.com/cython/cython/tree/master/Cython/Includes/libcpp").
These containers are: deque, list, map, pair, queue, set, stack, vector.

For example:

```
# distutils: language = c++

from libcpp.vector cimport vector

cdef vector[int] vect
cdef int i, x

for i in range(10):
    vect.push_back(i)

for i in range(10):
    print(vect[i])

for x in vect:
    print(x)
```

The pxd files
in [/Cython/Includes/libcpp](https://github.com/cython/cython/tree/master/Cython/Includes/libcpp "https://github.com/cython/cython/tree/master/Cython/Includes/libcpp")
also work as good examples on how to declare C++ classes.

The STL containers coerce from and to the
corresponding Python builtin types. The conversion is triggered
either by an assignment to a typed variable (including typed function
arguments) or by an explicit cast, e.g.:

```
# cython: language_level=3
# distutils: language=c++

from libcpp.complex cimport complex, conj
from libcpp.string cimport string
from libcpp.vector cimport vector

py_bytes_object = b'The knights who say ni'
py_unicode_object = u'Those who hear them seldom live to tell the tale.'

cdef string s = py_bytes_object
print(s)  # b'The knights who say ni'

cdef string cpp_string = <string> py_unicode_object.encode('utf-8')
print(cpp_string)  # b'Those who hear them seldom live to tell the tale.'

cdef vector[int] vect = range(1, 10, 2)
print(vect)  # [1, 3, 5, 7, 9]

cdef vector[string] cpp_strings = b'It is a good shrubbery'.split()
print(cpp_strings[1])   # b'is'

# creates a python object, then convert it to C++ complex
complex_val = 1+2j
cdef complex[double] c_value1 = complex_val
print(c_value1)  # (1+2j)

# transforms a C++ object to another one without Python conversion
cdef complex[double] c_value2 = conj(c_value1)
print(c_value2)  # (1-2j)
```

The following coercions are available:

 Python type =>  C++ type  => Python type  bytes  std::string  bytes  iterable  std::vector  list  iterable  std::list  list  iterable  std::set  set  iterable  std::unordered\_set  set  mapping  std::map  dict  mapping  std::unordered\_map  dict  iterable (len 2)  std::pair  tuple (len 2)  complex  std::complex  complex 

All conversions create a new container and copy the data into it.
The items in the containers are converted to a corresponding type
automatically, which includes recursively converting containers
inside of containers, e.g. a C++ vector of maps of strings.

Be aware that the conversions do have some pitfalls, which are
detailed in [the troubleshooting section](troubleshooting.html#automatic-conversion-pitfalls "troubleshooting.html#automatic-conversion-pitfalls").

Iteration over stl containers (or indeed any class with `begin()` and
`end()` methods returning an object supporting incrementing, dereferencing,
and comparison) is supported via the `for .. in` syntax (including in list
comprehensions). For example, one can write:

```
# distutils: language = c++

from libcpp.vector cimport vector

def main():
    cdef vector[int] v = [4, 6, 5, 10, 3]

    cdef int value
    for value in v:
        print(value)

    return [x*x for x in v if x % 2 == 0]
```

If the loop target variable is unspecified, an assignment from type
`*container.begin()` is used for [type inference](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives").

Note

Slicing stl containers is supported,
you can do `for x in my_vector[:5]: ...` but unlike pointers slices,
it will create a temporary Python object and iterate over it. Thus
making the iteration very slow. You might want to avoid slicing
C++ containers for performance reasons.

### Simplified wrapping with default constructor[¶](#simplified-wrapping-with-default-constructor "Link to this heading")

If your extension type instantiates a wrapped C++ class using the default
constructor (not passing any arguments), you may be able to simplify the
lifecycle handling by tying it directly to the lifetime of the Python wrapper
object. Instead of a pointer attribute, you can declare an instance:

```
# distutils: language = c++

from libcpp.vector cimport vector


cdef class VectorStack:
    cdef vector[int] v

    def push(self, x):
        self.v.push_back(x)

    def pop(self):
        if self.v.empty():
            raise IndexError()
        x = self.v.back()
        self.v.pop_back()
        return x
```

Cython will automatically generate code that instantiates the C++ object
instance when the Python object is created and deletes it when the Python
object is garbage collected.

### Exceptions[¶](#exceptions "Link to this heading")

Cython cannot throw C++ exceptions, or catch them with a try-except statement,
but it is possible to declare a function as potentially raising an C++
exception and converting it into a Python exception. For example,

```
cdef extern from "some_file.h":
    cdef int foo() except +
```

This will translate try and the C++ error into an appropriate Python exception.
The translation is performed according to the following table
(the `std::` prefix is omitted from the C++ identifiers):

 C++  Python  `bad_alloc`  `MemoryError`  `bad_cast`  `TypeError`  `bad_typeid`  `TypeError`  `domain_error`  `ValueError`  `invalid_argument`  `ValueError`  `ios_base::failure`  `IOError`  `out_of_range`  `IndexError`  `overflow_error`  `OverflowError`  `range_error`  `ArithmeticError`  `underflow_error`  `ArithmeticError`  (all others)  `RuntimeError` 

The `what()` message, if any, is preserved. Note that a C++
`ios_base_failure` can denote EOF, but does not carry enough information
for Cython to discern that, so watch out with exception masks on IO streams.

```
cdef int bar() except +MemoryError
```

This will catch any C++ error and raise a Python MemoryError in its place.
(Any Python exception is valid here.)

Cython also supports using a custom exception handler. This is an advanced feature
that most users won’t need, but for those that do a full example follows:

```
cdef int raise_py_error()
cdef int something_dangerous() except +raise_py_error
```

If something\_dangerous raises a C++ exception then raise\_py\_error will be
called, which allows one to do custom C++ to Python error “translations.” If
raise\_py\_error does not actually raise an exception a RuntimeError will be
raised. This approach may also be used to manage custom Python exceptions
created using the Python C API.

```
# raising.pxd
cdef extern from "Python.h" nogil:
    ctypedef struct PyObject

cdef extern from *:
    """
    #include <Python.h>
    #include <stdexcept>
    #include <ios>

    PyObject *CustomLogicError;

    void create_custom_exceptions() {
        CustomLogicError = PyErr_NewException("raiser.CustomLogicError", NULL, NULL);
    }

    void custom_exception_handler() {
        try {
            if (PyErr_Occurred()) {
                ; // let the latest Python exn pass through and ignore the current one
            } else {
                throw;
            }
        }  catch (const std::logic_error& exn) {
            // Add mapping of std::logic_error -> CustomLogicError
            PyErr_SetString(CustomLogicError, exn.what());
        } catch (...) {
            PyErr_SetString(PyExc_RuntimeError, "Unknown exception");
        }
    }

    class Raiser {
        public:
            Raiser () {}
            void raise_exception() {
                throw std::logic_error("Failure");
            }
    };
    """
    cdef PyObject* CustomLogicError
    cdef void create_custom_exceptions()
    cdef void custom_exception_handler()

    cdef cppclass Raiser:
        Raiser() noexcept
        void raise_exception() except +custom_exception_handler


# raising.pyx
create_custom_exceptions()
PyCustomLogicError = <object> CustomLogicError


cdef class PyRaiser:
    cdef Raiser c_obj

    def raise_exception(self):
        self.c_obj.raise_exception()
```

The above example leverages Cython’s ability to include [verbatim C code](external_C_code.html#verbatim-c "external_C_code.html#verbatim-c") in pxd files to create a new Python exception type
`CustomLogicError` and map it to the standard C++ `std::logic_error` using
the `custom_exception_handler` function. There is nothing special about using
a standard exception class here, `std::logic_error` could easily be replaced
with some new C++ exception type defined in this file. The
`Raiser::raise_exception` is marked with `+custom_exception_handler` to
indicate that this function should be called whenever an exception is raised.
The corresponding Python function `PyRaiser.raise_exception` will raise a
`CustomLogicError` whenever it is called. Defining `PyCustomLogicError`
allows other code to catch this exception, as shown below:

```
try:
    PyRaiser().raise_exception()
except PyCustomLogicError:
    print("Caught the exception")
```

When defining custom exception handlers it is typically good to also include
logic to handle all the standard exceptions that Cython typically handles as
listed in the table above. The code for this standard exception handler can be
found [here](https://github.com/cython/cython/blob/master/Cython/Utility/CppSupport.cpp "https://github.com/cython/cython/blob/master/Cython/Utility/CppSupport.cpp").

If you want to use std::exception\_ptr then you can `cimport` it from
`libcpp.exception`. That provides a special exception handler
`exception_ptr_error_handler` allowing you to declare a function:

```
cdef extern from "some_header":
    void some_function() except +exception_ptr_error_handler
```

The exception raised from `some_function` will always be an `Exception`
and the underlying `std::exception_ptr` can be retrieved with
`wrapped_exception_ptr_from_exception`. This is a slightly niche use,
but `std::exception_ptr` is a useful way to safely store arbitrary C++
exceptions for later.

There is also the special form:

```
cdef int raise_py_or_cpp() except +*
```

for those functions that may raise either a Python or a C++ exception.

### Static member method[¶](#static-member-method "Link to this heading")

If the Rectangle class has a static member:

```
namespace shapes {
    class Rectangle {
    ...
    public:
        static void do_something();

    };
}
```

you can declare it using the Python @staticmethod decorator, i.e.:

```
cdef extern from "Rectangle.h" namespace "shapes":
    cdef cppclass Rectangle:
        ...
        @staticmethod
        void do_something()
```

### Declaring/Using References[¶](#declaring-using-references "Link to this heading")

Cython supports declaring lvalue references using the standard `Type&` syntax.
Note, however, that it is unnecessary to declare the arguments of extern
functions as references (const or otherwise) as it has no impact on the
caller’s syntax.

### Scoped Enumerations[¶](#scoped-enumerations "Link to this heading")

Cython supports scoped enumerations (`enum class`) in C++ mode:

```
cdef enum class Cheese:
    cheddar = 1
    camembert = 2
```

As with “plain” enums, you may access the enumerators as attributes of the type.
Unlike plain enums however, the enumerators are not visible to the
enclosing scope:

```
cdef Cheese c1 = Cheese.cheddar  # OK
cdef Cheese c2 = cheddar  # ERROR!
```

Optionally, you may specify the underlying type of a scoped enumeration.
This is especially important when declaring an external scoped enumeration
with an underlying type:

```
cdef extern from "Foo.h":
    cdef enum class Spam(unsigned int):
        x = 10
        y = 20
        ...
```

Declaring an enum class as `cpdef` will create a [PEP 435](https://peps.python.org/pep-0435/ "https://peps.python.org/pep-0435/")-style Python wrapper.

### `auto` Keyword[¶](#auto-keyword "Link to this heading")

Though Cython does not have an `auto` keyword, Cython local variables
not explicitly typed with `cdef` are deduced from the types of the right hand
side of all their assignments (see the `infer_types`
[compiler directive](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives")). This is particularly handy
when dealing with functions that return complicated, nested, templated types,
e.g.:

```
cdef vector[int] v = ...
it = v.begin()
```

(Though of course the `for .. in` syntax is preferred for objects supporting
the iteration protocol.)

## RTTI and typeid()[¶](#rtti-and-typeid "Link to this heading")

Cython has support for the `typeid(...)` operator.

from cython.operator cimport typeid

The `typeid(...)` operator returns an object of the type `const type_info &`.

If you want to store a type\_info value in a C variable, you will need to store it
as a pointer rather than a reference:

```
from libcpp.typeinfo cimport type_info
cdef const type_info* info = &typeid(MyClass)
```

If an invalid type is passed to `typeid`, it will throw an `std::bad_typeid`
exception which is converted into a `TypeError` exception in Python.

An additional C++11-only RTTI-related class, `std::type_index`, is available
in `libcpp.typeindex`.

## Specify C++ language in setup.py[¶](#specify-c-language-in-setup-py "Link to this heading")

Instead of specifying the language and the sources in the source files, it is
possible to declare them in the `setup.py` file:

```
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(
           "rect.pyx",                 # our Cython source
           sources=["Rectangle.cpp"],  # additional source file(s)
           language="c++",             # generate C++ code
      ))
```

Cython will generate and compile the `rect.cpp` file (from
`rect.pyx`), then it will compile `Rectangle.cpp`
(implementation of the `Rectangle` class) and link both object files
together into `rect.so` on Linux, or `rect.pyd` on windows,
which you can then import in Python using
`import rect` (if you forget to link the `Rectangle.o`, you will
get missing symbols while importing the library in Python).

Note that the `language` option has no effect on user provided Extension
objects that are passed into `cythonize()`. It is only used for modules
found by file name (as in the example above).

The `cythonize()` function in Cython versions up to 0.21 does not
recognize the `language` option and it needs to be specified as an
option to an `Extension` that describes your extension and that
is then handled by `cythonize()` as follows:

```
from setuptools import Extension, setup
from Cython.Build import cythonize

setup(ext_modules = cythonize(Extension(
           "rect",                                # the extension name
           sources=["rect.pyx", "Rectangle.cpp"], # the Cython source and
                                                  # additional C++ source files
           language="c++",                        # generate and compile C++ code
      )))
```

The options can also be passed directly from the source file, which is
often preferable (and overrides any global option). Starting with
version 0.17, Cython also allows passing external source files into the
`cythonize()` command this way. Here is a simplified setup.py file:

```
from setuptools import setup
from Cython.Build import cythonize

setup(
    name = "rectangleapp",
    ext_modules = cythonize('*.pyx'),
)
```

And in the .pyx source file, write this into the first comment block, before
any source code, to compile it in C++ mode and link it statically against the
`Rectangle.cpp` code file:

```
# distutils: language = c++
# distutils: sources = Rectangle.cpp
```

Note

When using distutils directives, the paths are relative to the working
directory of the setuptools run (which is usually the project root where
the `setup.py` resides).

To compile manually (e.g. using `make`), the `cython` command-line
utility can be used to generate a C++ `.cpp` file, and then compile it
into a python extension. C++ mode for the `cython` command is turned
on with the `--cplus` option.

## `cpp_locals` directive[¶](#cpp-locals-directive "Link to this heading")

The `cpp_locals` compiler directive is an experimental feature that makes
C++ variables behave like normal Python object variables. With this
directive they are only initialized at their first assignment, and thus
they no longer require a nullary constructor to be stack-allocated. Trying to
access an uninitialized C++ variable will generate an `UnboundLocalError`
(or similar) in the same way as a Python variable would. For example:

```
def function(dont_write):
    cdef SomeCppClass c  # not initialized
    if dont_write:
        return c.some_cpp_function()  # UnboundLocalError
    else:
        c = SomeCppClass(...)  # initialized
        return c.some_cpp_function()  # OK
```

Additionally, the directive avoids initializing temporary C++ objects before
they are assigned, for cases where Cython needs to use such objects in its
own code-generation (often for return values of functions that can throw
exceptions).

For extra speed, the `initializedcheck` directive disables the check for an
unbound-local. With this directive on, accessing a variable that has not
been initialized will trigger undefined behaviour, and it is entirely the user’s
responsibility to avoid such access.

The `cpp_locals` directive is currently implemented using `std::optional`
and thus requires a C++17 compatible compiler. Defining
`CYTHON_USE_BOOST_OPTIONAL` (as define for the C++ compiler) uses `boost::optional`
instead (but is even more experimental and untested). The directive may
come with a memory and performance cost due to the need to store and check
a boolean that tracks if a variable is initialized, but the C++ compiler should
be able to eliminate the check in most cases.

## Caveats and Limitations[¶](#caveats-and-limitations "Link to this heading")

### Access to C-only functions[¶](#access-to-c-only-functions "Link to this heading")

Whenever generating C++ code, Cython generates declarations of and calls
to functions assuming these functions are C++ (ie, not declared as `extern "C"
{...}`. This is ok if the C functions have C++ entry points, but if they’re C
only, you will hit a roadblock. If you have a C++ Cython module needing
to make calls to pure-C functions, you will need to write a small C++ shim
module which:

* includes the needed C headers in an extern “C” block
* contains minimal forwarding functions in C++, each of which calls the
  respective pure-C function

### C++ left-values[¶](#c-left-values "Link to this heading")

C++ allows functions returning a reference to be left-values. This is currently
not supported in Cython. `cython.operator.dereference(foo)` is also not
considered a left-value.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Using C++ in Cython](# "#")
  + [Overview](#overview "#overview")
    - [Procedure Overview](#procedure-overview "#procedure-overview")
  + [A simple Tutorial](#a-simple-tutorial "#a-simple-tutorial")
    - [An example C++ API](#an-example-c-api "#an-example-c-api")
    - [Declaring a C++ class interface](#declaring-a-c-class-interface "#declaring-a-c-class-interface")
      * [Declare class with cdef cppclass](#declare-class-with-cdef-cppclass "#declare-class-with-cdef-cppclass")
      * [Add public attributes](#add-public-attributes "#add-public-attributes")
      * [Declare a var with the wrapped C++ class](#declare-a-var-with-the-wrapped-c-class "#declare-a-var-with-the-wrapped-c-class")
    - [Create Cython wrapper class](#create-cython-wrapper-class "#create-cython-wrapper-class")
  + [Compilation and Importing](#compilation-and-importing "#compilation-and-importing")
  + [Advanced C++ features](#advanced-c-features "#advanced-c-features")
    - [Overloading](#overloading "#overloading")
    - [Overloading operators](#overloading-operators "#overloading-operators")
    - [Nested class declarations](#nested-class-declarations "#nested-class-declarations")
    - [C++ operators not compatible with Python syntax](#c-operators-not-compatible-with-python-syntax "#c-operators-not-compatible-with-python-syntax")
    - [Templates](#templates "#templates")
    - [Standard library](#standard-library "#standard-library")
    - [Simplified wrapping with default constructor](#simplified-wrapping-with-default-constructor "#simplified-wrapping-with-default-constructor")
    - [Exceptions](#exceptions "#exceptions")
    - [Static member method](#static-member-method "#static-member-method")
    - [Declaring/Using References](#declaring-using-references "#declaring-using-references")
    - [Scoped Enumerations](#scoped-enumerations "#scoped-enumerations")
    - [`auto` Keyword](#auto-keyword "#auto-keyword")
  + [RTTI and typeid()](#rtti-and-typeid "#rtti-and-typeid")
  + [Specify C++ language in setup.py](#specify-c-language-in-setup-py "#specify-c-language-in-setup-py")
  + [`cpp_locals` directive](#cpp-locals-directive "#cpp-locals-directive")
  + [Caveats and Limitations](#caveats-and-limitations "#caveats-and-limitations")
    - [Access to C-only functions](#access-to-c-only-functions "#access-to-c-only-functions")
    - [C++ left-values](#c-left-values "#c-left-values")

#### Previous topic

[Early Binding for Speed](early_binding_for_speed.html "previous chapter")

#### Next topic

[Fused Types (Templates)](fusedtypes.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/wrapping_CPlusPlus.rst.txt "../../_sources/src/userguide/wrapping_CPlusPlus.rst.txt")

### Quick search

### Navigation

* [next](fusedtypes.html "Fused Types (Templates)")
* [previous](early_binding_for_speed.html "Early Binding for Speed") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Using C++ in Cython

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

