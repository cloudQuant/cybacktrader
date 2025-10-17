




Implementing the buffer protocol — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/buffer.html "/en/stable/src/userguide/buffer.html").

### Navigation

* [next](parallelism.html "Using Parallelism")
* [previous](memoryviews.html "Typed Memoryviews") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Implementing the buffer protocol

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Implementing the buffer protocol[¶](#implementing-the-buffer-protocol "Link to this heading")

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

Cython objects can expose memory buffers to Python code
by implementing the “buffer protocol”.
This chapter shows how to implement the protocol
and make use of the memory managed by an extension type from NumPy.

## A matrix class[¶](#a-matrix-class "Link to this heading")

The following Cython/C++ code implements a matrix of floats,
where the number of columns is fixed at construction time
but rows can be added dynamically.

Pure PythonCython

```
# distutils: language = c++

from cython.cimports.libcpp.vector import vector

@cython.cclass
class Matrix:
    ncols: cython.uint
    v: vector[cython.float]

    def __cinit__(self, ncols: cython.uint):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)
```

```
# distutils: language = c++

from libcpp.vector cimport vector


cdef class Matrix:
    cdef unsigned ncols
    cdef vector[float] v

    def __cinit__(self, unsigned ncols):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)
```

There are no methods to do anything productive with the matrices’ contents.
We could implement custom `__getitem__`, `__setitem__`, etc. for this,
but instead we’ll use the buffer protocol to expose the matrix’s data to Python
so we can use NumPy to do useful work.

Implementing the buffer protocol requires adding two methods,
`__getbuffer__` and `__releasebuffer__`,
which Cython handles specially.

Pure PythonCython

```
# distutils: language = c++
from cython.cimports.cpython import Py_buffer
from cython.cimports.libcpp.vector import vector

@cython.cclass
class Matrix:
    ncols: cython.Py_ssize_t
    shape: cython.Py_ssize_t[2]
    strides: cython.Py_ssize_t[2]
    v: vector[cython.float]

    def __cinit__(self, ncols: cython.Py_ssize_t):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, buffer: cython.pointer[Py_buffer], flags: cython.int):
        itemsize: cython.Py_ssize_t = cython.sizeof(self.v[0])

        self.shape[0] = self.v.size() // self.ncols
        self.shape[1] = self.ncols

        # Stride 1 is the distance, in bytes, between two items in a row;
        # this is the distance between two adjacent items in the vector.
        # Stride 0 is the distance between the first elements of adjacent rows.
        self.strides[1] = cython.cast(cython.Py_ssize_t, (
              cython.cast(cython.p_char, cython.address(self.v[1]))
            - cython.cast(cython.p_char, cython.address(self.v[0]))
        ))
        self.strides[0] = self.ncols * self.strides[1]

        buffer.buf = cython.cast(cython.p_char, cython.address(self.v[0]))
        buffer.format = 'f'                     # float
        buffer.internal = cython.NULL           # see References
        buffer.itemsize = itemsize
        buffer.len = self.v.size() * itemsize   # product(shape) * itemsize
        buffer.ndim = 2
        buffer.obj = self
        buffer.readonly = 0
        buffer.shape = self.shape
        buffer.strides = self.strides
        buffer.suboffsets = cython.NULL         # for pointer arrays only

    def __releasebuffer__(self, buffer: cython.pointer[Py_buffer]):
        pass
```

```
# distutils: language = c++
from cpython cimport Py_buffer
from libcpp.vector cimport vector


cdef class Matrix:
    cdef Py_ssize_t ncols
    cdef Py_ssize_t[2] shape
    cdef Py_ssize_t[2] strides
    cdef vector[float] v

    def __cinit__(self, Py_ssize_t ncols):
        self.ncols = ncols

    def add_row(self):
        """Adds a row, initially zero-filled."""
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        cdef Py_ssize_t itemsize = sizeof(self.v[0])

        self.shape[0] = self.v.size() // self.ncols
        self.shape[1] = self.ncols

        # Stride 1 is the distance, in bytes, between two items in a row;
        # this is the distance between two adjacent items in the vector.
        # Stride 0 is the distance between the first elements of adjacent rows.
        self.strides[1] = <Py_ssize_t>(
              <char *>&(self.v[1])
            - <char *>&(self.v[0])
        )
        self.strides[0] = self.ncols * self.strides[1]

        buffer.buf = <char *>&(self.v[0])
        buffer.format = 'f'                     # float
        buffer.internal = NULL                  # see References
        buffer.itemsize = itemsize
        buffer.len = self.v.size() * itemsize   # product(shape) * itemsize
        buffer.ndim = 2
        buffer.obj = self
        buffer.readonly = 0
        buffer.shape = self.shape
        buffer.strides = self.strides
        buffer.suboffsets = NULL                # for pointer arrays only

    def __releasebuffer__(self, Py_buffer *buffer):
        pass
```

The method `Matrix.__getbuffer__` fills a descriptor structure,
called a [`Py_buffer`](https://docs.python.org/3/c-api/buffer.html#c.Py_buffer "(in Python v3.14)"), that is defined by the Python C-API.
It contains a pointer to the actual buffer in memory,
as well as metadata about the shape of the array and the strides
(step sizes to get from one element or row to the next).
Its `shape` and `strides` members are pointers
that must point to arrays of type and size [Py\_ssize\_t](https://docs.python.org/3/c-api/intro.html#c.Py_ssize_t "(in Python v3.14)")[ndim].
These arrays have to stay alive as long as any buffer views the data,
so we store them on the `Matrix` object as members.

The code is not yet complete, but we can already compile it
and test the basic functionality.

```
>>> from matrix import Matrix
>>> import numpy as np
>>> m = Matrix(10)
>>> np.asarray(m)
array([], shape=(0, 10), dtype=float32)
>>> m.add_row()
>>> a = np.asarray(m)
>>> a[:] = 1
>>> m.add_row()
>>> a = np.asarray(m)
>>> a
array([[ 1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.,  1.],
       [ 0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.,  0.]], dtype=float32)
```

Now we can view the `Matrix` as a NumPy `ndarray`,
and modify its contents using standard NumPy operations.

## Memory safety and reference counting[¶](#memory-safety-and-reference-counting "Link to this heading")

The `Matrix` class as implemented so far is unsafe.
The `add_row` operation can move the underlying buffer,
which invalidates any NumPy (or other) view on the data.
If you try to access values after an `add_row` call,
you’ll get outdated values or a segfault.

This is where `__releasebuffer__` comes in.
We can add a reference count to each matrix,
and lock it for mutation whenever a view exists.

Pure PythonCython

```
# distutils: language = c++

from cython.cimports.cpython import Py_buffer
from cython.cimports.libcpp.vector import vector

@cython.cclass
class Matrix:

    view_count: cython.int

    ncols: cython.Py_ssize_t
    v: vector[cython.float]
    # ...

    def __cinit__(self, ncols: cython.Py_ssize_t):
        self.ncols = ncols
        self.view_count = 0

    def add_row(self):
        if self.view_count > 0:
            raise ValueError("can't add row while being viewed")
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, buffer: cython.pointer[Py_buffer], flags: cython.int):
        # ... as before

        self.view_count += 1

    def __releasebuffer__(self, buffer: cython.pointer[Py_buffer]):
        self.view_count -= 1
```

```
# distutils: language = c++

from cpython cimport Py_buffer
from libcpp.vector cimport vector


cdef class Matrix:

    cdef int view_count

    cdef Py_ssize_t ncols
    cdef vector[float] v
    # ...

    def __cinit__(self, Py_ssize_t ncols):
        self.ncols = ncols
        self.view_count = 0

    def add_row(self):
        if self.view_count > 0:
            raise ValueError("can't add row while being viewed")
        self.v.resize(self.v.size() + self.ncols)

    def __getbuffer__(self, Py_buffer *buffer, int flags):
        # ... as before

        self.view_count += 1

    def __releasebuffer__(self, Py_buffer *buffer):
        self.view_count -= 1
```

## Flags[¶](#flags "Link to this heading")

We skipped some input validation in the code.
The `flags` argument to `__getbuffer__` comes from `np.asarray`
(and other clients) and is an OR of boolean flags
that describe the kind of array that is requested.
Strictly speaking, if the flags contain `PyBUF_ND`, `PyBUF_SIMPLE`,
or `PyBUF_F_CONTIGUOUS`, `__getbuffer__` must raise a `BufferError`.
These macros can be `cimport`’d from `cpython.buffer`.

(The matrix-in-vector structure actually conforms to `PyBUF_ND`,
but that would prohibit `__getbuffer__` from filling in the strides.
A single-row matrix is F-contiguous, but a larger matrix is not.)

## References[¶](#references "Link to this heading")

The buffer interface used here is set out in
[PEP 3118](https://peps.python.org/pep-3118/ "https://peps.python.org/pep-3118/"), Revising the buffer protocol.

A tutorial for using this API from C is on Jake Vanderplas’s blog,
[An Introduction to the Python Buffer Protocol](https://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/ "https://jakevdp.github.io/blog/2014/05/05/introduction-to-the-python-buffer-protocol/").

Reference documentation is available for
[Python 3](https://docs.python.org/3/c-api/buffer.html "https://docs.python.org/3/c-api/buffer.html")
and [Python 2](https://docs.python.org/2.7/c-api/buffer.html "https://docs.python.org/2.7/c-api/buffer.html").
The Py2 documentation also describes an older buffer protocol
that is no longer in use;
since Python 2.6, the [PEP 3118](https://peps.python.org/pep-3118/ "https://peps.python.org/pep-3118/") protocol has been implemented,
and the older protocol is only relevant for legacy code.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Implementing the buffer protocol](# "#")
  + [A matrix class](#a-matrix-class "#a-matrix-class")
  + [Memory safety and reference counting](#memory-safety-and-reference-counting "#memory-safety-and-reference-counting")
  + [Flags](#flags "#flags")
  + [References](#references "#references")

#### Previous topic

[Typed Memoryviews](memoryviews.html "previous chapter")

#### Next topic

[Using Parallelism](parallelism.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/buffer.rst.txt "../../_sources/src/userguide/buffer.rst.txt")

### Quick search

### Navigation

* [next](parallelism.html "Using Parallelism")
* [previous](memoryviews.html "Typed Memoryviews") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Implementing the buffer protocol

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

