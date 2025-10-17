




Sharing Declarations Between Cython Modules — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/sharing_declarations.html "/en/stable/src/userguide/sharing_declarations.html").

### Navigation

* [next](external_C_code.html "Interfacing with External C Code")
* [previous](special_methods.html "Special Methods of Extension Types") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Sharing Declarations Between Cython Modules

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Sharing Declarations Between Cython Modules[¶](#sharing-declarations-between-cython-modules "Link to this heading")

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

This section describes how to make C declarations, functions and extension
types in one Cython module available for use in another Cython module.
These facilities are closely modeled on the Python import mechanism,
and can be thought of as a compile-time version of it.

## Definition and Implementation files[¶](#definition-and-implementation-files "Link to this heading")

A Cython module can be split into two parts: a definition file with a `.pxd`
suffix, containing C declarations that are to be available to other Cython
modules, and an implementation file with a `.pyx`/`.py` suffix, containing
everything else. When a module wants to use something declared in another
module’s definition file, it imports it using the [`cimport`](#cimport "#cimport")
statement or using special [`cython.cimports`](../tutorial/pure.html#module-cython.cimports "cython.cimports") package.

A `.pxd` file that consists solely of extern declarations does not need
to correspond to an actual `.pyx`/`.py` file or Python module. This can make it a
convenient place to put common declarations, for example declarations of
functions from an [external library](external_C_code.html#external-c-code "external_C_code.html#external-c-code") that one
wants to use in several modules.

## What a Definition File contains[¶](#what-a-definition-file-contains "Link to this heading")

A definition file can contain:

* Any kind of C type declaration.
* extern C function or variable declarations.
* Declarations of C functions defined in the module.
* The definition part of an extension type (see below).

It cannot contain the implementations of any C or Python functions, or any
Python class definitions, or any executable statements. It is needed when one
wants to access [`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@cfunc` attributes and methods, or to inherit from
[`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@cclass` classes defined in this module.

Note

You don’t need to (and shouldn’t) declare anything in a declaration file
public in order to make it available to other Cython modules; its mere
presence in a definition file does that. You only need a public
declaration if you want to make something available to external C code.

## What an Implementation File contains[¶](#what-an-implementation-file-contains "Link to this heading")

An implementation file can contain any kind of Cython statement, although there
are some restrictions on the implementation part of an extension type if the
corresponding definition file also defines that type (see below).
If one doesn’t need to [`cimport`](#cimport "#cimport") anything from this module, then this
is the only file one needs.

## The cimport statement[¶](#the-cimport-statement "Link to this heading")

The [`cimport`](#cimport "#cimport") statement is used in a definition or
implementation file to gain access to names declared in another definition
file. Its syntax exactly parallels that of the normal Python import
statement. When pure python syntax is used, the same effect can be done by
importing from special [`cython.cimports`](../tutorial/pure.html#module-cython.cimports "cython.cimports") package. In later text the term
to `cimport` refers to using both [`cimport`](#cimport "#cimport") statement or
[`cython.cimports`](../tutorial/pure.html#module-cython.cimports "cython.cimports") package.

Pure PythonCython

```
from cython.cimports.module import name [as name][, name [as name] ...]
```

```
cimport module [, module...]

from module cimport name [as name] [, name [as name] ...]
```

Here is an example. `dishes.pxd` is a definition file which exports a
C data type. `restaurant.pyx`/`restaurant.py` is an implementation file
which imports and uses it.

dishes.pxd[¶](#id3 "Link to this code")

```
cdef enum otherstuff:
    sausage, eggs, lettuce

cdef struct spamdish:
    int oz_of_spam
    otherstuff filler
```

Pure PythonCython

dishes.py[¶](#id4 "Link to this code")

```
import cython
from cython.cimports.dishes import spamdish, sausage

@cython.cfunc
def prepare(d: cython.pointer[spamdish]) -> cython.void:
    d.oz_of_spam = 42
    d.filler = sausage

def serve():
    d: spamdish
    prepare(cython.address(d))
    print(f'{d.oz_of_spam} oz spam, filler no. {d.filler}')
```

dishes.pyx[¶](#id5 "Link to this code")

```
cimport dishes
from dishes cimport spamdish

cdef void prepare(spamdish *d):
    d.oz_of_spam = 42
    d.filler = dishes.sausage

def serve():
    cdef spamdish d
    prepare(&d)
    print(f'{d.oz_of_spam} oz spam, filler no. {d.filler}')
```

It is important to understand that the [`cimport`](#cimport "#cimport") statement can only
be used to import C data types, C functions and variables, and extension
types. It cannot be used to import any Python objects, and (with one
exception) it doesn’t imply any Python import at run time. If you want to
refer to any Python names from a module that you have cimported, you will have
to include a regular import statement for it as well.

The exception is that when you use [`cimport`](#cimport "#cimport") to import an extension type, its
type object is imported at run time and made available by the name under which
you imported it. Using [`cimport`](#cimport "#cimport") to import extension types is covered in more
detail below.

If a `.pxd` file changes, any modules that [`cimport`](#cimport "#cimport") from it may need to be
recompiled. The `Cython.Build.cythonize` utility can take care of this for you.

### Search paths for definition files[¶](#search-paths-for-definition-files "Link to this heading")

When you [`cimport`](#cimport "#cimport") a module called `modulename`, the Cython
compiler searches for a file called `modulename.pxd`.
It searches for this file along the path for include files
(as specified by `-I` command line options or the `include_path`
option to `cythonize()`), as well as `sys.path`.

Using `package_data` to install `.pxd` files in your `setup.py` script
allows other packages to cimport items from your module as a dependency.

Also, whenever you compile a file `modulename.pyx`/`modulename.py`,
the corresponding definition file `modulename.pxd` is first searched for along the
include path (but not `sys.path`), and if found, it is processed before
processing the `.pyx` file.

### Using cimport to resolve naming conflicts[¶](#using-cimport-to-resolve-naming-conflicts "Link to this heading")

The [`cimport`](#cimport "#cimport") mechanism provides a clean and simple way to solve the
problem of wrapping external C functions with Python functions of the same
name. All you need to do is put the extern C declarations into a `.pxd` file
for an imaginary module, and [`cimport`](#cimport "#cimport") that module. You can then
refer to the C functions by qualifying them with the name of the module.
Here’s an example:

c\_lunch.pxd[¶](#id6 "Link to this code")

```
cdef extern from "lunch.h":
    void eject_tomato(float)
```

Pure PythonCython

lunch.py[¶](#id7 "Link to this code")

```
import cython
from cython.cimports.c_lunch import eject_tomato as c_eject_tomato

def eject_tomato(speed: cython.float):
    c_eject_tomato(speed)
```

lunch.pyx[¶](#id8 "Link to this code")

```
cimport c_lunch

def eject_tomato(float speed):
    c_lunch.eject_tomato(speed)
```

You don’t need any `c_lunch.pyx`/`c_lunch.py` file, because the only
things defined in `c_lunch.pxd` are extern C entities. There won’t be any actual
`c_lunch` module at run time, but that doesn’t matter; the
`c_lunch.pxd` file has done its job of providing an additional namespace
at compile time.

## Sharing C Functions[¶](#sharing-c-functions "Link to this heading")

C functions defined at the top level of a module can be made available via
[`cimport`](#cimport "#cimport") by putting headers for them in the `.pxd` file, for
example:

volume.pxd[¶](#id9 "Link to this code")

```
cdef float cube(float x)
```

Pure PythonCython

volume.py[¶](#id10 "Link to this code")

```
def cube(x):
    return x * x * x
```

spammery.py[¶](#id11 "Link to this code")

```
import cython
from cython.cimports.volume import cube

def menu(description, size):
    print(description, ":", cube(size),
          "cubic metres of spam")

menu("Entree", 1)
menu("Main course", 3)
menu("Dessert", 2)
```

Note

Type definitions of function `cube()` in `volume.py` are not provided
since they are used from .pxd definition file. See [Augmenting .pxd](../tutorial/pure.html#augmenting-pxd "../tutorial/pure.html#augmenting-pxd") and
GitHub issue [#4388](https://github.com/cython/cython/issues/4388 "https://github.com/cython/cython/issues/4388").

volume.pyx[¶](#id12 "Link to this code")

```
cdef float cube(float x):
    return x * x * x
```

spammery.pyx[¶](#id13 "Link to this code")

```
from volume cimport cube

def menu(description, size):
    print(description, ":", cube(size),
          "cubic metres of spam")

menu("Entree", 1)
menu("Main course", 3)
menu("Dessert", 2)
```

## Sharing Extension Types[¶](#sharing-extension-types "Link to this heading")

An extension type can be made available via [`cimport`](#cimport "#cimport") by splitting
its definition into two parts, one in a definition file and the other in the
corresponding implementation file.

The definition part of the extension type can only declare C attributes and C
methods, not Python methods, and it must declare all of that type’s C
attributes and C methods.

The implementation part must implement all of the C methods declared in the
definition part, and may not add any further C attributes. It may also define
Python methods.

Here is an example of a module which defines and exports an extension type,
and another module which uses it:

shrubbing.pxd[¶](#id14 "Link to this code")

```
cdef class Shrubbery:
    cdef int width
    cdef int length
```

Pure PythonCython

shrubbing.py[¶](#id15 "Link to this code")

```
import cython

@cython.cclass
class Shrubbery:
    def __cinit__(self, w: cython.int, l: cython.int):
        self.width = w
        self.length = l

def standard_shrubbery():
    return Shrubbery(3, 7)
```

landscaping.py[¶](#id16 "Link to this code")

```
from cython.cimports.shrubbing import Shrubbery
import shrubbing

def main():
    sh: Shrubbery
    sh = shrubbing.standard_shrubbery()
    print("Shrubbery size is", sh.width, 'x', sh.length)
```

One would then need to compile both of these modules, e.g. using

setup.py[¶](#id17 "Link to this code")

```
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(["landscaping.py", "shrubbing.py"]))
```

shrubbing.pyx[¶](#id18 "Link to this code")

```
cdef class Shrubbery:
    def __init__(self, int w, int l):
        self.width = w
        self.length = l

def standard_shrubbery():
    return Shrubbery(3, 7)
```

landscaping.pyx[¶](#id19 "Link to this code")

```
cimport shrubbing
import shrubbing

def main():
    cdef shrubbing.Shrubbery sh
    sh = shrubbing.standard_shrubbery()
    print("Shrubbery size is", sh.width, 'x', sh.length)
```

One would then need to compile both of these modules, e.g. using

setup.py[¶](#id20 "Link to this code")

```
from setuptools import setup
from Cython.Build import cythonize

setup(ext_modules=cythonize(["landscaping.pyx", "shrubbing.pyx"]))
```

Some things to note about this example:

* There is a [`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@cclass` class Shrubbery declaration in both
  `shrubbing.pxd` and `shrubbing.pyx`. When the shrubbing module
  is compiled, these two declarations are combined into one.
* In `landscaping.pyx`/`landscaping.py`, the [`cimport`](#cimport "#cimport") shrubbing
  declaration allows us to refer to the Shrubbery type as `shrubbing.Shrubbery`.
  But it doesn’t bind the name shrubbing in landscaping’s module namespace at run
  time, so to access `shrubbing.standard_shrubbery()` we also need to
  `import shrubbing`.

## Versioning[¶](#versioning "Link to this heading")

`.pxd` files can be labelled with a minimum Cython version as part of
their file name, similar to the version tagging of `.so` files in PEP 3149.
For example a file called `shrubbing.cython-30.pxd` will only be
found by `cimport shrubbing` on Cython 3.0 and higher. Cython will use the
file tagged with the highest compatible version number.

Note that versioned files that are distributed across different directories
will not be found. Only the first directory in the Python module search
path in which a matching `.pxd` file is found will be considered.

The purpose of this feature is to allow third-party packages to release
Cython interfaces to their packages that take advantage of the latest Cython
features while not breaking compatibility for users with older versions of Cython.
Users intending to use `.pxd` files solely within their own project
need not produce these tagged files.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Sharing Declarations Between Cython Modules](# "#")
  + [Definition and Implementation files](#definition-and-implementation-files "#definition-and-implementation-files")
  + [What a Definition File contains](#what-a-definition-file-contains "#what-a-definition-file-contains")
  + [What an Implementation File contains](#what-an-implementation-file-contains "#what-an-implementation-file-contains")
  + [The cimport statement](#the-cimport-statement "#the-cimport-statement")
    - [Search paths for definition files](#search-paths-for-definition-files "#search-paths-for-definition-files")
    - [Using cimport to resolve naming conflicts](#using-cimport-to-resolve-naming-conflicts "#using-cimport-to-resolve-naming-conflicts")
  + [Sharing C Functions](#sharing-c-functions "#sharing-c-functions")
  + [Sharing Extension Types](#sharing-extension-types "#sharing-extension-types")
  + [Versioning](#versioning "#versioning")

#### Previous topic

[Special Methods of Extension Types](special_methods.html "previous chapter")

#### Next topic

[Interfacing with External C Code](external_C_code.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/sharing_declarations.rst.txt "../../_sources/src/userguide/sharing_declarations.rst.txt")

### Quick search

### Navigation

* [next](external_C_code.html "Interfacing with External C Code")
* [previous](special_methods.html "Special Methods of Extension Types") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Sharing Declarations Between Cython Modules

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

