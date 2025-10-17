




Early Binding for Speed — Cython 3.1.4 documentation

### Navigation

* [next](wrapping_CPlusPlus.html "Using C++ in Cython")
* [previous](source_files_and_compilation.html "Source Files and Compilation") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Early Binding for Speed

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Early Binding for Speed[¶](#early-binding-for-speed "Link to this heading")

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

As a dynamic language, Python encourages a programming style of considering
classes and objects in terms of their methods and attributes, more than where
they fit into the class hierarchy.

This can make Python a very relaxed and comfortable language for rapid
development, but with a price - the ‘red tape’ of managing data types is
dumped onto the interpreter. At run time, the interpreter does a lot of work
searching namespaces, fetching attributes and parsing argument and keyword
tuples. This run-time ‘late binding’ is a major cause of Python’s relative
slowness compared to ‘early binding’ languages such as C++.

However with Cython it is possible to gain significant speed-ups through the
use of ‘early binding’ programming techniques.

For example, consider the following (silly) code example:

Pure PythonCython

```
@cython.cclass
class Rectangle:
    x0: cython.int
    y0: cython.int
    x1: cython.int
    y1: cython.int

    def __init__(self, x0: cython.int, y0: cython.int, x1: cython.int, y1: cython.int):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def area(self):
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea(x0, y0, x1, y1):
    rect = Rectangle(x0, y0, x1, y1)
    return rect.area()
```

```
cdef class Rectangle:
    cdef int x0, y0
    cdef int x1, y1



    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    def area(self):
        area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea(x0, y0, x1, y1):
    rect = Rectangle(x0, y0, x1, y1)
    return rect.area()
```

In the `rectArea()` method, the call to `rect.area()` and the
`area()` method contain a lot of Python overhead.

However, in Cython, it is possible to eliminate a lot of this overhead in cases
where calls occur within Cython code. For example:

Pure PythonCython

```
@cython.cclass
class Rectangle:
    x0: cython.int
    y0: cython.int
    x1: cython.int
    y1: cython.int

    def __init__(self, x0: cython.int, y0: cython.int, x1: cython.int, y1: cython.int):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    @cython.cfunc
    def _area(self) -> cython.int:
        area: cython.int = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

    def area(self):
        return self._area()

def rectArea(x0, y0, x1, y1):
    rect: Rectangle = Rectangle(x0, y0, x1, y1)
    return rect._area()
```

```
cdef class Rectangle:
    cdef int x0, y0
    cdef int x1, y1



    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


    cdef int _area(self):
        cdef int area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

    def area(self):
        return self._area()

def rectArea(x0, y0, x1, y1):
    cdef Rectangle rect = Rectangle(x0, y0, x1, y1)
    return rect._area()
```

Here, in the Rectangle extension class, we have defined two different area
calculation methods, the efficient `_area()` C method, and the
Python-callable `area()` method which serves as a thin wrapper around
`_area()`. Note also in the function `rectArea()` how we ‘early bind’
by declaring the local variable `rect` which is explicitly given the type
Rectangle. By using this declaration, instead of just dynamically assigning to
`rect`, we gain the ability to access the much more efficient C-callable
`_area()` method.

But Cython offers us more simplicity again, by allowing us to declare
dual-access methods - methods that can be efficiently called at C level, but
can also be accessed from pure Python code at the cost of the Python access
overheads. Consider this code:

Pure PythonCython

```
@cython.cclass
class Rectangle:
    x0: cython.int
    y0: cython.int
    x1: cython.int
    y1: cython.int

    def __init__(self, x0: cython.int, y0: cython.int, x1: cython.int, y1: cython.int):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1

    @cython.ccall
    def area(self)-> cython.int:
        area: cython.int = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea(x0, y0, x1, y1):
    rect: Rectangle = Rectangle(x0, y0, x1, y1)
    return rect.area()
```

```
cdef class Rectangle:
    cdef int x0, y0
    cdef int x1, y1



    def __init__(self, int x0, int y0, int x1, int y1):
        self.x0 = x0
        self.y0 = y0
        self.x1 = x1
        self.y1 = y1


    cpdef int area(self):
        cdef int area = (self.x1 - self.x0) * (self.y1 - self.y0)
        if area < 0:
            area = -area
        return area

def rectArea(x0, y0, x1, y1):
    cdef Rectangle rect = Rectangle(x0, y0, x1, y1)
    return rect.area()
```

Here, we just have a single area method, declared as [`cpdef`](language_basics.html#cpdef "language_basics.html#cpdef") or with `@ccall` decorator
to make it efficiently callable as a C function, but still accessible from pure Python
(or late-binding Cython) code.

If within Cython code, we have a variable already ‘early-bound’ (ie, declared
explicitly as type Rectangle, (or cast to type Rectangle), then invoking its
area method will use the efficient C code path and skip the Python overhead.
But if in Cython or regular Python code we have a regular object variable
storing a Rectangle object, then invoking the area method will require:

* an attribute lookup for the area method
* packing a tuple for arguments and a dict for keywords (both empty in this case)
* using the Python API to call the method

and within the area method itself:

* parsing the tuple and keywords
* executing the calculation code
* converting the result to a python object and returning it

So within Cython, it is possible to achieve massive optimisations by
using strong typing in declaration and casting of variables. For tight loops
which use method calls, and where these methods are pure C, the difference can
be huge.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Source Files and Compilation](source_files_and_compilation.html "previous chapter")

#### Next topic

[Using C++ in Cython](wrapping_CPlusPlus.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/early_binding_for_speed.rst.txt "../../_sources/src/userguide/early_binding_for_speed.rst.txt")

### Quick search

### Navigation

* [next](wrapping_CPlusPlus.html "Using C++ in Cython")
* [previous](source_files_and_compilation.html "Source Files and Compilation") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Early Binding for Speed

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

