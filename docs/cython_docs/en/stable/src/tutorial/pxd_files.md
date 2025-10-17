




pxd files — Cython 3.1.4 documentation

### Navigation

* [next](caveats.html "Caveats")
* [previous](cdef_classes.html "Extension types (aka. cdef classes)") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* pxd files

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# pxd files[¶](#pxd-files "Link to this heading")

Note

This page uses two different syntax variants:

* Cython specific `cdef` syntax, which was designed to make type declarations
  concise and easily readable from a C/C++ perspective.
* Pure Python syntax which allows static Cython type declarations in
  [pure Python code](pure.html#pep484-type-annotations "pure.html#pep484-type-annotations"),
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

In addition to the `.pyx` and `.py` source files, Cython uses `.pxd` files
which work like C header files – they contain Cython declarations
(and sometimes code sections) which are only meant for inclusion by
Cython modules. A `.pxd` file is imported into a `.pyx` module by
using the `cimport` keyword.

`.pxd` files have many use-cases:

1. They can be used for sharing external C declarations.
2. They can contain functions which are well suited for inlining by
   the C compiler. Such functions should be marked `inline`, example:

   inline.pxd[¶](#id2 "Link to this code")

   ```
   cdef inline int int_min(int a, int b):
       return b if b < a else a
   ```
3. When accompanying an equally named `.pyx` / `.py` file, they
   provide a Cython interface to the Cython module so that other
   Cython modules can communicate with it using a more efficient
   protocol than the Python one.

In our integration example, we might break it up into `.pxd` files like this:

1. Add a `cmath.pxd`:

   cmath.pxd[¶](#id3 "Link to this code")

   ```
   cdef extern from "math.h":
       cpdef double sin(double x)
   ```

   Then one would simply do

   Pure PythonCython

   integrate.py[¶](#id4 "Link to this code")

   ```
   from cython.cimports.cmath import sin
   ```

   Warning

   The code provided above / on this page uses an external
   native (non-Python) library through a `cimport` (`cython.cimports`).
   Cython compilation enables this, but there is no support for this from
   plain Python. Trying to run this code from Python (without compilation)
   will fail when accessing the external library.
   This is described in more detail in [Calling C functions](pure.html#calling-c-functions "pure.html#calling-c-functions").

   integrate.pyx[¶](#id5 "Link to this code")

   ```
   from cmath cimport sin
   ```
2. Add a `integrate.pxd` so that other modules written in Cython
   can define fast custom functions to integrate:

   integrate.pxd[¶](#id6 "Link to this code")

   ```
   cdef class Function:
      cpdef evaluate(self, double x)

   cpdef integrate(Function f, double a, double b, int N)
   ```

   Note that if you have a cdef class with attributes, the attributes must
   be declared in the class declaration `.pxd` file (if you use one), not
   the `.pyx` / `.py` file. The compiler will tell you about this.

## \_\_init\_\_.pxd[¶](#init-pxd "Link to this heading")

Cython also supports `__init__.pxd` files for declarations in package’s
namespaces, similar to `__init__.py` files in Python.

Continuing the integration example, we could package the module as follows:

1. Place the module files in a directory tree as one usually would for
   Python:

   Pure PythonCython

   ```
   CyIntegration/
   ├── __init__.py
   ├── __init__.pxd
   ├── integrate.py
   └── integrate.pxd
   ```

   ```
   CyIntegration/
   ├── __init__.pyx
   ├── __init__.pxd
   ├── integrate.pyx
   └── integrate.pxd
   ```
2. In `__init__.pxd`, use `cimport` for any declarations that one
   would want to be available from the package’s main namespace:

   Pure PythonCython

   ```
   from cython.cimports.CyIntegration import integrate
   ```

   ```
   from CyIntegration cimport integrate
   ```

   Other modules would then be able to use `cimport` on the package in
   order to recursively gain faster, Cython access to the entire package
   and the data declared in its modules:

   Pure PythonCython

   ```
   from cython.cimports import CyIntegration

   @cython.ccall
   def do_integration(f: CyIntegration.integrate.Function):
       return CyIntegration.integrate.integrate(f, 0., 2., 1)
   ```

   Warning

   The code provided above / on this page uses an external
   native (non-Python) library through a `cimport` (`cython.cimports`).
   Cython compilation enables this, but there is no support for this from
   plain Python. Trying to run this code from Python (without compilation)
   will fail when accessing the external library.
   This is described in more detail in [Calling C functions](pure.html#calling-c-functions "pure.html#calling-c-functions").

   ```
   cimport CyIntegration


   cpdef do_integration(CyIntegration.integrate.Function f):
       return CyIntegration.integrate.integrate(f, 0., 2., 1)
   ```

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [pxd files](# "#")
  + [\_\_init\_\_.pxd](#init-pxd "#init-pxd")

#### Previous topic

[Extension types (aka. cdef classes)](cdef_classes.html "previous chapter")

#### Next topic

[Caveats](caveats.html "next chapter")

### This Page

* [Show Source](../../_sources/src/tutorial/pxd_files.rst.txt "../../_sources/src/tutorial/pxd_files.rst.txt")

### Quick search

### Navigation

* [next](caveats.html "Caveats")
* [previous](cdef_classes.html "Extension types (aka. cdef classes)") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* pxd files

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

