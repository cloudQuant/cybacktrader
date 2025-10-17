




Typed Memoryviews — Cython 3.1.4 documentation

### Navigation

* [next](buffer.html "Implementing the buffer protocol")
* [previous](pyrex_differences.html "Differences between Cython and Pyrex") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Typed Memoryviews

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Typed Memoryviews[¶](#typed-memoryviews "Link to this heading")

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

Typed memoryviews allow efficient access to memory buffers, such as those
underlying NumPy arrays, without incurring any Python overhead.
Memoryviews are similar to the current NumPy array buffer support
(`np.ndarray[np.float64_t, ndim=2]`), but
they have more features and cleaner syntax.

Memoryviews are more general than the old NumPy array buffer support, because
they can handle a wider variety of sources of array data. For example, they can
handle C arrays and the Cython array type ([Cython arrays](#view-cython-arrays "#view-cython-arrays")).

A memoryview can be used in any context (function parameters, module-level, cdef
class attribute, etc) and can be obtained from nearly any object that
exposes writable buffer through the [PEP 3118](https://www.python.org/dev/peps/pep-3118/ "https://www.python.org/dev/peps/pep-3118/") buffer interface.

## Quickstart[¶](#quickstart "Link to this heading")

If you are used to working with NumPy, the following examples should get you
started with Cython memory views.

Pure PythonCython

```
from cython.cimports.cython.view import array as cvarray
import numpy as np

# Memoryview on a NumPy array
narr = np.arange(27, dtype=np.dtype("i")).reshape((3, 3, 3))
narr_view = cython.declare(cython.int[:, :, :], narr)

# Memoryview on a C array
carr = cython.declare(cython.int[3][3][3])
carr_view = cython.declare(cython.int[:, :, :], carr)

# Memoryview on a Cython array
cyarr = cvarray(shape=(3, 3, 3), itemsize=cython.sizeof(cython.int), format="i")
cyarr_view = cython.declare(cython.int[:, :, :], cyarr)

# Show the sum of all the arrays before altering it
print(f"NumPy sum of the NumPy array before assignments: {narr.sum()}")

# We can copy the values from one memoryview into another using a single
# statement, by either indexing with ... or (NumPy-style) with a colon.
carr_view[...] = narr_view
cyarr_view[:] = narr_view
# NumPy-style syntax for assigning a single value to all elements.
narr_view[:, :, :] = 3

# Just to distinguish the arrays
carr_view[0, 0, 0] = 100
cyarr_view[0, 0, 0] = 1000

# Assigning into the memoryview on the NumPy array alters the latter
print(f"NumPy sum of NumPy array after assignments: {narr.sum()}")

# A function using a memoryview does not usually need the GIL
@cython.nogil
@cython.ccall
def sum3d(arr: cython.int[:, :, :]) -> cython.int:
    i: cython.size_t
    j: cython.size_t
    k: cython.size_t
    I: cython.size_t
    J: cython.size_t
    K: cython.size_t
    total: cython.int = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total

# A function accepting a memoryview knows how to use a NumPy array,
# a C array, a Cython array...
print(f"Memoryview sum of NumPy array is {sum3d(narr)}")
print(f"Memoryview sum of C array is {sum3d(carr)}")
print(f"Memoryview sum of Cython array is {sum3d(cyarr)}")
# ... and of course, a memoryview.
print(f"Memoryview sum of C memoryview is {sum3d(carr_view)}")
```

```
from cython.view cimport array as cvarray
import numpy as np

# Memoryview on a NumPy array
narr = np.arange(27, dtype=np.dtype("i")).reshape((3, 3, 3))
cdef int [:, :, :] narr_view = narr

# Memoryview on a C array
cdef int[3][3][3] carr
cdef int [:, :, :] carr_view = carr

# Memoryview on a Cython array
cyarr = cvarray(shape=(3, 3, 3), itemsize=sizeof(int), format="i")
cdef int [:, :, :] cyarr_view = cyarr

# Show the sum of all the arrays before altering it
print(f"NumPy sum of the NumPy array before assignments: {narr.sum()}")

# We can copy the values from one memoryview into another using a single
# statement, by either indexing with ... or (NumPy-style) with a colon.
carr_view[...] = narr_view
cyarr_view[:] = narr_view
# NumPy-style syntax for assigning a single value to all elements.
narr_view[:, :, :] = 3

# Just to distinguish the arrays
carr_view[0, 0, 0] = 100
cyarr_view[0, 0, 0] = 1000

# Assigning into the memoryview on the NumPy array alters the latter
print(f"NumPy sum of NumPy array after assignments: {narr.sum()}")

# A function using a memoryview does not usually need the GIL
cpdef int sum3d(int[:, :, :] arr) nogil:
    cdef size_t i, j, k, I, J, K
    cdef int total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total








# A function accepting a memoryview knows how to use a NumPy array,
# a C array, a Cython array...
print(f"Memoryview sum of NumPy array is {sum3d(narr)}")
print(f"Memoryview sum of C array is {sum3d(carr)}")
print(f"Memoryview sum of Cython array is {sum3d(cyarr)}")
# ... and of course, a memoryview.
print(f"Memoryview sum of C memoryview is {sum3d(carr_view)}")
```

This code should give the following output:

```
NumPy sum of the NumPy array before assignments: 351
NumPy sum of NumPy array after assignments: 81
Memoryview sum of NumPy array is 81
Memoryview sum of C array is 451
Memoryview sum of Cython array is 1351
Memoryview sum of C memoryview is 451
```

## Using memoryviews[¶](#using-memoryviews "Link to this heading")

### Syntax[¶](#syntax "Link to this heading")

Memory views use Python slicing syntax in a similar way as NumPy.

To create a complete view on a one-dimensional `int` buffer:

Pure PythonCython

```
view1D: cython.int[:] = exporting_object
```

```
cdef int[:] view1D = exporting_object
```

A complete 3D view:

Pure PythonCython

```
view3D: cython.int[:,:,:] = exporting_object
```

```
cdef int[:,:,:] view3D = exporting_object
```

They also work conveniently as function arguments:

Pure PythonCython

```
def process_3d_buffer(view: cython.int[:,:,:]):
    ...
```

```
def process_3d_buffer(int[:,:,:] view not None):
    ...
```

The Cython `not None` declaration for the argument automatically rejects
`None` values as input, which would otherwise be allowed. The reason why
`None` is allowed by default is that it is conveniently used for return
arguments. On the other hand, when pure python mode is used, `None` value
is rejected by default. It is allowed only when type is declared as `Optional`:

Pure PythonCython

```
import numpy as np
import typing

def process_buffer(input_view: cython.int[:,:],
                   output_view: typing.Optional[cython.int[:,:]] = None):

    if output_view is None:
        # Creating a default view, e.g.
        output_view = np.empty_like(input_view)

    # process 'input_view' into 'output_view'
    return output_view

process_buffer(None, None)
```

```
import numpy as np


def process_buffer(int[:,:] input_view not None,
                   int[:,:] output_view=None):

    if output_view is None:
        # Creating a default view, e.g.
        output_view = np.empty_like(input_view)

    # process 'input_view' into 'output_view'
    return output_view

process_buffer(None, None)
```

Cython will reject incompatible buffers automatically, e.g. passing a
three dimensional buffer into a function that requires a two
dimensional buffer will raise a `ValueError`.

To use a memory view on a numpy array with a custom dtype, you’ll need to
declare an equivalent packed struct that mimics the dtype:

```
import numpy as np

CUSTOM_DTYPE = np.dtype([
    ('x', np.uint8),
    ('y', np.float32),
])

a = np.zeros(100, dtype=CUSTOM_DTYPE)

cdef packed struct custom_dtype_struct:
    # The struct needs to be packed since by default numpy dtypes aren't
    # aligned
    unsigned char x
    float y

def sum(custom_dtype_struct [:] a):

    cdef:
        unsigned char sum_x = 0
        float sum_y = 0.

    for i in range(a.shape[0]):
        sum_x += a[i].x
        sum_y += a[i].y

    return sum_x, sum_y
```

Note

Pure python mode currently does not support packed structs

### Indexing[¶](#indexing "Link to this heading")

In Cython, index access on memory views is automatically translated
into memory addresses. The following code requests a two-dimensional
memory view of C `int` typed items and indexes into it:

Pure PythonCython

```
buf: cython.int[:,:] = exporting_object

print(buf[1,2])
```

```
cdef int[:,:] buf = exporting_object

print(buf[1,2])
```

Negative indices work as well, counting from the end of the respective
dimension:

```
print(buf[-1,-2])
```

The following function loops over each dimension of a 2D array and
adds 1 to each item:

Pure PythonCython

```
import numpy as np

def add_one(buf: cython.int[:,:]):
    for x in range(buf.shape[0]):
        for y in range(buf.shape[1]):
            buf[x, y] += 1

# exporting_object must be a Python object
# implementing the buffer interface, e.g. a numpy array.
exporting_object = np.zeros((10, 20), dtype=np.intc)

add_one(exporting_object)
```

```
import numpy as np

def add_one(int[:,:] buf):
    for x in range(buf.shape[0]):
        for y in range(buf.shape[1]):
            buf[x, y] += 1

# exporting_object must be a Python object
# implementing the buffer interface, e.g. a numpy array.
exporting_object = np.zeros((10, 20), dtype=np.intc)

add_one(exporting_object)
```

Indexing and slicing can be done with or without the GIL. It basically works
like NumPy. If indices are specified for every dimension you will get an element
of the base type (e.g. `int`). Otherwise, you will get a new view. An Ellipsis
means you get consecutive slices for every unspecified dimension:

Pure PythonCython

```
import numpy as np

def main():
    exporting_object = np.arange(0, 15 * 10 * 20, dtype=np.intc).reshape((15, 10, 20))

    my_view: cython.int[:, :, :] = exporting_object

    # These are all equivalent
    my_view[10]
    my_view[10, :, :]
    my_view[10, ...]
```

```
import numpy as np


exporting_object = np.arange(0, 15 * 10 * 20, dtype=np.intc).reshape((15, 10, 20))

cdef int[:, :, :] my_view = exporting_object

# These are all equivalent
my_view[10]
my_view[10, :, :]
my_view[10, ...]
```

### Copying[¶](#copying "Link to this heading")

Memory views can be copied in place:

Pure PythonCython

```
import numpy as np

def main():

    to_view: cython.int[:, :, :] = np.empty((20, 15, 30), dtype=np.intc)
    from_view: cython.int[:, :, :] = np.ones((20, 15, 30), dtype=np.intc)

    # copy the elements in from_view to to_view
    to_view[...] = from_view
    # or
    to_view[:] = from_view
    # or
    to_view[:, :, :] = from_view
```

```
import numpy as np


cdef int[:, :, :] to_view, from_view
to_view = np.empty((20, 15, 30), dtype=np.intc)
from_view = np.ones((20, 15, 30), dtype=np.intc)

# copy the elements in from_view to to_view
to_view[...] = from_view
# or
to_view[:] = from_view
# or
to_view[:, :, :] = from_view
```

They can also be copied with the `copy()` and `copy_fortran()` methods; see
[C and Fortran contiguous copies](#view-copy-c-fortran "#view-copy-c-fortran").

### Transposing[¶](#transposing "Link to this heading")

In most cases (see below), the memoryview can be transposed in the same way that
NumPy slices can be transposed:

Pure PythonCython

```
import numpy as np

def main():
    array = np.arange(20, dtype=np.intc).reshape((2, 10))

    c_contig: cython.int[:, ::1] = array
    f_contig: cython.int[::1, :] = c_contig.T
```

```
import numpy as np


array = np.arange(20, dtype=np.intc).reshape((2, 10))

cdef int[:, ::1] c_contig = array
cdef int[::1, :] f_contig = c_contig.T
```

This gives a new, transposed, view on the data.

Transposing requires that all dimensions of the memoryview have a
direct access memory layout (i.e., there are no indirections through pointers).
See [Specifying more general memory layouts](#view-general-layouts "#view-general-layouts") for details.

### Newaxis[¶](#newaxis "Link to this heading")

As for NumPy, new axes can be introduced by indexing an array with `None` :

Pure PythonCython

```
myslice: cython.double[:] = np.linspace(0, 10, num=50)

# 2D array with shape (1, 50)
myslice[None] # or
myslice[None, :]

# 2D array with shape (50, 1)
myslice[:, None]

# 3D array with shape (1, 10, 1)
myslice[None, 10:-20:2, None]
```

```
cdef double[:] myslice = np.linspace(0, 10, num=50)

# 2D array with shape (1, 50)
myslice[None] # or
myslice[None, :]

# 2D array with shape (50, 1)
myslice[:, None]

# 3D array with shape (1, 10, 1)
myslice[None, 10:-20:2, None]
```

One may mix new axis indexing with all other forms of indexing and slicing.
See also an [example](https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html "https://docs.scipy.org/doc/numpy/reference/arrays.indexing.html").

### Read-only views[¶](#read-only-views "Link to this heading")

Note

Pure python mode currently does not support read-only views.

Since Cython 0.28, the memoryview item type can be declared as `const` to
support read-only buffers as input:

```
import numpy as np

cdef const double[:] myslice   # const item type => read-only view

a = np.linspace(0, 10, num=50)
a.setflags(write=False)
myslice = a
```

Using a non-const memoryview with a binary Python string produces a runtime error.
You can solve this issue with a `const` memoryview:

```
cdef bint is_y_in(const unsigned char[:] string_view):
    cdef int i
    for i in range(string_view.shape[0]):
        if string_view[i] == b'y':
            return True
    return False

print(is_y_in(b'hello world'))   # False
print(is_y_in(b'hello Cython'))  # True
```

Note that this does not require the input buffer to be read-only:

```
a = np.linspace(0, 10, num=50)
myslice = a   # read-only view of a writable buffer
```

Writable buffers are still accepted by `const` views, but read-only
buffers are not accepted for non-const, writable views:

```
cdef double[:] myslice   # a normal read/write memory view

a = np.linspace(0, 10, num=50)
a.setflags(write=False)
myslice = a   # ERROR: requesting writable memory view from read-only buffer!
```

## Comparison to the old buffer support[¶](#comparison-to-the-old-buffer-support "Link to this heading")

You will probably prefer memoryviews to the older syntax because:

* The syntax is cleaner
* Memoryviews do not usually need the GIL (see [Memoryviews and the GIL](#view-needs-gil "#view-needs-gil"))
* Memoryviews are considerably faster

For example, this is the old syntax equivalent of the `sum3d` function above:

```
cpdef int old_sum3d(object[int, ndim=3, mode='strided'] arr):
    cdef int I, J, K, total = 0
    I = arr.shape[0]
    J = arr.shape[1]
    K = arr.shape[2]
    for i in range(I):
        for j in range(J):
            for k in range(K):
                total += arr[i, j, k]
    return total
```

Note that we can’t use `nogil` for the buffer version of the function as we
could for the memoryview version of `sum3d` above, because buffer objects
are Python objects. However, even if we don’t use `nogil` with the
memoryview, it is significantly faster. This is a output from an IPython
session after importing both versions:

```
In [2]: import numpy as np

In [3]: arr = np.zeros((40, 40, 40), dtype=int)

In [4]: timeit -r15 old_sum3d(arr)
1000 loops, best of 15: 298 us per loop

In [5]: timeit -r15 sum3d(arr)
1000 loops, best of 15: 219 us per loop
```

## Python buffer support[¶](#python-buffer-support "Link to this heading")

Cython memoryviews support nearly all objects exporting the interface of Python
[new style buffers](https://docs.python.org/3/c-api/buffer.html "https://docs.python.org/3/c-api/buffer.html"). This is the buffer interface described in [PEP 3118](https://www.python.org/dev/peps/pep-3118/ "https://www.python.org/dev/peps/pep-3118/").
NumPy arrays support this interface, as do [Cython arrays](#view-cython-arrays "#view-cython-arrays"). The
“nearly all” is because the Python buffer interface allows the elements in the
data array to themselves be pointers; Cython memoryviews do not yet support
this.

## Memory layout[¶](#memory-layout "Link to this heading")

The buffer interface allows objects to identify the underlying memory in a
variety of ways. With the exception of pointers for data elements, Cython
memoryviews support all Python new-type buffer layouts. It can be useful to know
or specify memory layout if the memory has to be in a particular format for an
external routine, or for code optimization.

### Background[¶](#background "Link to this heading")

The concepts are as follows: there is data access and data packing. Data access
means either direct (no pointer) or indirect (pointer). Data packing means your
data may be contiguous or not contiguous in memory, and may use strides to
identify the jumps in memory consecutive indices need to take for each dimension.

NumPy arrays provide a good model of strided direct data access, so we’ll use
them for a refresher on the concepts of C and Fortran contiguous arrays, and
data strides.

### Brief recap on C, Fortran and strided memory layouts[¶](#brief-recap-on-c-fortran-and-strided-memory-layouts "Link to this heading")

The simplest data layout might be a C contiguous array. This is the default
layout in NumPy and Cython arrays. C contiguous means that the array data is
continuous in memory (see below) and that neighboring elements in the first
dimension of the array are furthest apart in memory, whereas neighboring
elements in the last dimension are closest together. For example, in NumPy:

```
In [2]: arr = np.array([['0', '1', '2'], ['3', '4', '5']], dtype='S1')
```

Here, `arr[0, 0]` and `arr[0, 1]` are one byte apart in memory, whereas
`arr[0, 0]` and `arr[1, 0]` are 3 bytes apart. This leads us to the idea of
strides. Each axis of the array has a stride length, which is the number of
bytes needed to go from one element on this axis to the next element. In the
case above, the strides for axes 0 and 1 will obviously be:

```
In [3]: arr.strides
Out[4]: (3, 1)
```

For a 3D C contiguous array:

```
In [5]: c_contig = np.arange(24, dtype=np.int8).reshape((2,3,4))
In [6] c_contig.strides
Out[6]: (12, 4, 1)
```

A Fortran contiguous array has the opposite memory ordering, with the elements
on the first axis closest together in memory:

```
In [7]: f_contig = np.array(c_contig, order='F')
In [8]: np.all(f_contig == c_contig)
Out[8]: True
In [9]: f_contig.strides
Out[9]: (1, 2, 6)
```

A contiguous array is one for which a single continuous block of memory contains
all the data for the elements of the array, and therefore the memory block
length is the product of number of elements in the array and the size of the
elements in bytes. In the example above, the memory block is 2 \* 3 \* 4 \* 1 bytes
long, where 1 is the length of an `np.int8`.

An array can be contiguous without being C or Fortran order:

```
In [10]: c_contig.transpose((1, 0, 2)).strides
Out[10]: (4, 12, 1)
```

Slicing an NumPy array can easily make it not contiguous:

```
In [11]: sliced = c_contig[:,1,:]
In [12]: sliced.strides
Out[12]: (12, 1)
In [13]: sliced.flags
Out[13]:
C_CONTIGUOUS : False
F_CONTIGUOUS : False
OWNDATA : False
WRITEABLE : True
ALIGNED : True
UPDATEIFCOPY : False
```

### Default behavior for memoryview layouts[¶](#default-behavior-for-memoryview-layouts "Link to this heading")

As you’ll see in [Specifying more general memory layouts](#view-general-layouts "#view-general-layouts"), you can specify memory layout for
any dimension of an memoryview. For any dimension for which you don’t specify a
layout, then the data access is assumed to be direct, and the data packing
assumed to be strided. For example, that will be the assumption for memoryviews
like:

Pure PythonCython

```
my_memoryview: cython.int[:, :, :]  = obj
```

```
int [:, :, :] my_memoryview = obj
```

### C and Fortran contiguous memoryviews[¶](#c-and-fortran-contiguous-memoryviews "Link to this heading")

You can specify C and Fortran contiguous layouts for the memoryview by using the
`::1` step syntax at definition. For example, if you know for sure your
memoryview will be on top of a 3D C contiguous layout, you could write:

Pure PythonCython

```
c_contiguous: cython.int[:, :, ::1] = c_contig
```

```
cdef int[:, :, ::1] c_contiguous = c_contig
```

where `c_contig` could be a C contiguous NumPy array. The `::1` at the 3rd
position means that the elements in this 3rd dimension will be one element apart
in memory. If you know you will have a 3D Fortran contiguous array:

Pure PythonCython

```
f_contiguous: cython.int[::1, :, :] = f_contig
```

```
cdef int[::1, :, :] f_contiguous = f_contig
```

If you pass a non-contiguous buffer, for example:

Pure PythonCython

```
# This array is C contiguous
c_contig = np.arange(24).reshape((2,3,4))
c_contiguous: cython.int[:, :, ::1] = c_contig

# But this isn't
c_contiguous = np.array(c_contig, order='F')
```

```
# This array is C contiguous
c_contig = np.arange(24).reshape((2,3,4))
cdef int[:, :, ::1] c_contiguous = c_contig

# But this isn't
c_contiguous = np.array(c_contig, order='F')
```

you will get a `ValueError` at runtime:

```
/Users/mb312/dev_trees/minimal-cython/mincy.pyx in init mincy (mincy.c:17267)()
    69
    70 # But this isn't
---> 71 c_contiguous = np.array(c_contig, order='F')
    72
    73 # Show the sum of all the arrays before altering it

/Users/mb312/dev_trees/minimal-cython/stringsource in View.MemoryView.memoryview_cwrapper (mincy.c:9995)()

/Users/mb312/dev_trees/minimal-cython/stringsource in View.MemoryView.memoryview.__cinit__ (mincy.c:6799)()

ValueError: ndarray is not C-contiguous
```

Thus the `::1` in the slice type specification indicates in which dimension the
data is contiguous. It can only be used to specify full C or Fortran
contiguity.

### C and Fortran contiguous copies[¶](#c-and-fortran-contiguous-copies "Link to this heading")

Copies can be made C or Fortran contiguous using the `.copy()` and
`.copy_fortran()` methods:

Pure PythonCython

```
# This view is C contiguous
c_contiguous: cython.int[:, :, ::1] = myview.copy()

# This view is Fortran contiguous
f_contiguous_slice: cython.int[::1, :] = myview.copy_fortran()
```

```
# This view is C contiguous
cdef int[:, :, ::1] c_contiguous = myview.copy()

# This view is Fortran contiguous
cdef int[::1, :] f_contiguous_slice = myview.copy_fortran()
```

### Specifying more general memory layouts[¶](#specifying-more-general-memory-layouts "Link to this heading")

Data layout can be specified using the previously seen `::1` slice syntax, or
by using any of the constants in `cython.view`. If no specifier is given in
any dimension, then the data access is assumed to be direct, and the data
packing assumed to be strided. If you don’t know whether a dimension will be
direct or indirect (because you’re getting an object with a buffer interface
from some library perhaps), then you can specify the `generic` flag, in which
case it will be determined at runtime.

The flags are as follows:

* `generic` - strided and direct or indirect
* `strided` - strided and direct (this is the default)
* `indirect` - strided and indirect
* `contiguous` - contiguous and direct
* `indirect_contiguous` - the list of pointers is contiguous

and they can be used like this:

Pure PythonCython

```
from cython.cimports.cython import view

def main():
    # direct access in both dimensions, strided in the first dimension, contiguous in the last
    a: cython.int[:, ::view.contiguous]

    # contiguous list of pointers to contiguous lists of ints
    b: cython.int[::view.indirect_contiguous, ::1]

    # direct or indirect in the first dimension, direct in the second dimension
    # strided in both dimensions
    c: cython.int[::view.generic, :]
```

```
from cython cimport view

def main():
    # direct access in both dimensions, strided in the first dimension, contiguous in the last
    cdef int[:, ::view.contiguous] a

    # contiguous list of pointers to contiguous lists of ints
    cdef int[::view.indirect_contiguous, ::1] b

    # direct or indirect in the first dimension, direct in the second dimension
    # strided in both dimensions
    cdef int[::view.generic, :] c
```

Only the first, last or the dimension following an indirect dimension may be
specified contiguous:

Pure PythonCython

```
from cython.cimports.cython import view

def main():
    # VALID
    a: cython.int[::view.indirect, ::1, :]
    b: cython.int[::view.indirect, :, ::1]
    c: cython.int[::view.indirect_contiguous, ::1, :]

    # INVALID
    d: cython.int[::view.contiguous, ::view.indirect, :]
    e: cython.int[::1, ::view.indirect, :]
```

```
from cython cimport view

def main():
    # VALID
    cdef int[::view.indirect, ::1, :] a
    cdef int[::view.indirect, :, ::1] b
    cdef int[::view.indirect_contiguous, ::1, :] c

    # INVALID
    cdef int[::view.contiguous, ::view.indirect, :] d
    cdef int[::1, ::view.indirect, :] e
```

The difference between the `contiguous` flag and the `::1` specifier is that the
former specifies contiguity for only one dimension, whereas the latter specifies
contiguity for all following (Fortran) or preceding (C) dimensions:

Pure PythonCython

```
c_contig: cython.int[:, ::1] = ...

# VALID
myslice: cython.int[:, ::view.contiguous] = c_contig[::2]

# INVALID
myslice: cython.int[:, ::1] = c_contig[::2]
```

```
cdef int[:, ::1] c_contig = ...

# VALID
cdef int[:, ::view.contiguous] myslice = c_contig[::2]

# INVALID
cdef int[:, ::1] myslice = c_contig[::2]
```

The former case is valid because the last dimension remains contiguous, but the
first dimension does not “follow” the last one anymore (meaning, it was strided
already, but it is not C or Fortran contiguous any longer), since it was sliced.

## Memoryviews and the GIL[¶](#memoryviews-and-the-gil "Link to this heading")

As you will see from the [Quickstart](#view-quickstart "#view-quickstart") section, memoryviews often do
not need the GIL:

Pure PythonCython

```
@cython.nogil
@cython.ccall
def sum3d(arr: cython.int[:, :, :]) -> cython.int:
    ...
```

```
cpdef int sum3d(int[:, :, :] arr) nogil:
    ...
```

In particular, you do not need the GIL for memoryview indexing, slicing or
transposing. Memoryviews require the GIL for the copy methods
([C and Fortran contiguous copies](#view-copy-c-fortran "#view-copy-c-fortran")), or when the dtype is object and an object
element is read or written.

## Memoryview Objects and Cython Arrays[¶](#memoryview-objects-and-cython-arrays "Link to this heading")

These typed memoryviews can be converted to Python memoryview objects
(`cython.view.memoryview`). These Python objects are indexable, sliceable and
transposable in the same way that the original memoryviews are. They can also be
converted back to Cython-space memoryviews at any time.

They have the following attributes:

* `shape`: size in each dimension, as a tuple.
* `strides`: stride along each dimension, in bytes.
* `suboffsets`
* `ndim`: number of dimensions.
* `size`: total number of items in the view (product of the shape).
* `itemsize`: size, in bytes, of the items in the view.
* `nbytes`: equal to `size` times `itemsize`.
* `base`

And of course the aforementioned `T` attribute ([Transposing](#view-transposing "#view-transposing")).
These attributes have the same semantics as in [NumPy](https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html#memory-layout "https://docs.scipy.org/doc/numpy/reference/arrays.ndarray.html#memory-layout"). For instance, to
retrieve the original object:

Pure PythonCython

```
import numpy
from cython.cimports.numpy import int32_t

def main():
    a: int32_t[:] = numpy.arange(10, dtype=numpy.int32)
    a = a[::2]

    print(a)
    print(numpy.asarray(a))
    print(a.base)

# this prints:
#    <MemoryView of 'ndarray' object>
#    [0 2 4 6 8]
#    [0 1 2 3 4 5 6 7 8 9]
```

```
import numpy
cimport numpy as cnp


cdef cnp.int32_t[:] a = numpy.arange(10, dtype=numpy.int32)
a = a[::2]

print(a)
print(numpy.asarray(a))
print(a.base)

# this prints:
#    <MemoryView of 'ndarray' object>
#    [0 2 4 6 8]
#    [0 1 2 3 4 5 6 7 8 9]
```

Note that this example returns the original object from which the view was
obtained, and that the view was resliced in the meantime.

## Cython arrays[¶](#cython-arrays "Link to this heading")

Whenever a Cython memoryview is copied (using any of the `copy()` or
`copy_fortran()` methods), you get a new memoryview slice of a newly created
`cython.view.array` object. This array can also be used manually, and will
automatically allocate a block of data. It can later be assigned to a C or
Fortran contiguous slice (or a strided slice). It can be used like:

Pure PythonCython

```
from cython.cimports.cython import view

my_array = view.array(shape=(10, 2), itemsize=cython.sizeof(cython.int), format="i")
my_slice: cython.int[:, :] = my_array
```

```
from cython cimport view

my_array = view.array(shape=(10, 2), itemsize=sizeof(int), format="i")
cdef int[:, :] my_slice = my_array
```

It also takes an optional argument `mode` (‘c’ or ‘fortran’) and a boolean
`allocate_buffer`, that indicates whether a buffer should be allocated and freed
when it goes out of scope:

Pure PythonCython

```
my_array: view.array = view.array(..., mode="fortran", allocate_buffer=False)
my_array.data = cython.cast(cython.p_char, my_data_pointer)

# define a function that can deallocate the data (if needed)
my_array.callback_free_data = free
```

```
cdef view.array my_array = view.array(..., mode="fortran", allocate_buffer=False)
my_array.data = <char *> my_data_pointer

# define a function that can deallocate the data (if needed)
my_array.callback_free_data = free
```

You can also cast pointers to array, or C arrays to arrays:

Pure PythonCython

```
my_array: view.array = cython.cast(cython.int[:10, :2], my_data_pointer)
my_array: view.array = cython.cast(cython.int[:, :], my_c_array)
```

```
cdef view.array my_array = <int[:10, :2]> my_data_pointer
cdef view.array my_array = <int[:, :]> my_c_array
```

Of course, you can also immediately assign a cython.view.array to a typed memoryview slice. A C array
may be assigned directly to a memoryview slice:

Pure PythonCython

```
myslice: cython.int[:, ::1] = my_2d_c_array
```

```
cdef int[:, ::1] myslice = my_2d_c_array
```

The arrays are indexable and sliceable from Python space just like memoryview objects, and have the same
attributes as memoryview objects.

## CPython array module[¶](#cpython-array-module "Link to this heading")

An alternative to `cython.view.array` is the `array` module in the
Python standard library. In Python 3, the `array.array` type supports
the buffer interface natively, so memoryviews work on top of it without
additional setup.

Starting with Cython 0.17, however, it is possible to use these arrays
as buffer providers also in Python 2. This is done through explicitly
cimporting the `cpython.array` module as follows:

Pure PythonCython

```
def sum_array(view: cython.int[:]):
    """
    >>> from array import array
    >>> sum_array( array('i', [1,2,3]) )
    6
    """
    total: cython.int = 0
    for i in range(view.shape[0]):
        total += view[i]
    return total
```

```
def sum_array(int[:] view):
    """
    >>> from array import array
    >>> sum_array( array('i', [1,2,3]) )
    6
    """
    cdef int total = 0
    for i in range(view.shape[0]):
        total += view[i]
    return total
```

Note that the cimport also enables the old buffer syntax for the array
type. Therefore, the following also works:

Pure PythonCython

```
from cython.cimports.cpython import array

def sum_array(arr: array.array[cython.int]):  # using old buffer syntax
    ...
```

```
from cpython cimport array

def sum_array(array.array[int] arr):  # using old buffer syntax
    ...
```

## Coercion to NumPy[¶](#coercion-to-numpy "Link to this heading")

Memoryview (and array) objects can be coerced to a NumPy ndarray, without having
to copy the data. You can e.g. do:

Pure PythonCython

```
from cython.cimports.numpy import int32_t
import numpy as np

numpy_array = np.asarray(cython.cast(int32_t[:10, :10], my_pointer))
```

```
cimport numpy as cnp
import numpy as np

numpy_array = np.asarray(<cnp.int32_t[:10, :10]> my_pointer)
```

Of course, you are not restricted to using NumPy’s type (such as `cnp.int32_t`
here), you can use any usable type.

## None Slices[¶](#none-slices "Link to this heading")

Although memoryview slices are not objects they can be set to `None` and they can
be checked for being `None` as well:

Pure PythonCython

```
def func(myarray: typing.Optional[cython.double[:]] = None):
    print(myarray is None)
```

```
def func(double[:] myarray = None):
    print(myarray is None)
```

If the function requires real memory views as input, it is therefore best to
reject `None` input straight away in the signature:

Pure PythonCython

```
def func(myarray: cython.double[:]):
    ...
```

```
def func(double[:] myarray not None):
    ...
```

Unlike object attributes of extension classes, memoryview slices are not
initialized to `None`.

## Pass data from a C function via pointer[¶](#pass-data-from-a-c-function-via-pointer "Link to this heading")

Since use of pointers in C is ubiquitous, here we give a quick example of how
to call C functions whose arguments contain pointers. Let’s suppose you want to
manage an array (allocate and deallocate) with NumPy (it can also be Python arrays, or
anything that supports the buffer interface), but you want to perform computation on this
array with an external C function implemented in `C_func_file.c`:

C\_func\_file.c[¶](#id3 "Link to this code")

```
1#include "C_func_file.h"
2
3void multiply_by_10_in_C(double arr[], unsigned int n)
4{
5    unsigned int i;
6    for (i = 0; i < n; i++) {
7        arr[i] *= 10;
8    }
9}
```

This file comes with a header file called `C_func_file.h` containing:

C\_func\_file.h[¶](#id4 "Link to this code")

```
1#ifndef C_FUNC_FILE_H
2#define C_FUNC_FILE_H
3
4void multiply_by_10_in_C(double arr[], unsigned int n);
5
6#endif
```

where `arr` points to the array and `n` is its size.

You can call the function in a Cython file in the following way:

Pure PythonCython

memview\_to\_c.pxd[¶](#id5 "Link to this code")

```
1cdef extern from "C_func_file.c":
2    # The C file is include directly so that it doesn't need to be compiled separately.
3    pass
4
5cdef extern from "C_func_file.h":
6    void multiply_by_10_in_C(double *, unsigned int)
```

memview\_to\_c.py[¶](#id6 "Link to this code")

```
 1import numpy as np
 2
 3def multiply_by_10(arr):  # 'arr' is a one-dimensional numpy array
 4
 5    if not arr.flags['C_CONTIGUOUS']:
 6        arr = np.ascontiguousarray(arr)  # Makes a contiguous copy of the numpy array.
 7
 8    arr_memview: cython.double[::1] = arr
 9
10    multiply_by_10_in_C(cython.address(arr_memview[0]), arr_memview.shape[0])
11
12    return arr
13
14
15a = np.ones(5, dtype=np.double)
16print(multiply_by_10(a))
17
18b = np.ones(10, dtype=np.double)
19b = b[::2]  # b is not contiguous.
20
21print(multiply_by_10(b))  # but our function still works as expected.
```

memview\_to\_c.pyx[¶](#id7 "Link to this code")

```
 1cdef extern from "C_func_file.c":
 2    # C is include here so that it doesn't need to be compiled externally
 3    pass
 4
 5cdef extern from "C_func_file.h":
 6    void multiply_by_10_in_C(double *, unsigned int)
 7
 8import numpy as np
 9
10def multiply_by_10(arr):  # 'arr' is a one-dimensional numpy array
11
12    if not arr.flags['C_CONTIGUOUS']:
13        arr = np.ascontiguousarray(arr)  # Makes a contiguous copy of the numpy array.
14
15    cdef double[::1] arr_memview = arr
16
17    multiply_by_10_in_C(&arr_memview[0], arr_memview.shape[0])
18
19    return arr
20
21
22a = np.ones(5, dtype=np.double)
23print(multiply_by_10(a))
24
25b = np.ones(10, dtype=np.double)
26b = b[::2]  # b is not contiguous.
27
28print(multiply_by_10(b))  # but our function still works as expected.
```

Several things to note:

* `::1` requests a C contiguous view, and fails if the buffer is not C contiguous.
  See [C and Fortran contiguous memoryviews](#c-and-fortran-contiguous-memoryviews "#c-and-fortran-contiguous-memoryviews").
* `&arr_memview[0]` and `cython.address(arr_memview[0]` can be understood as ‘the address of the first element of the
  memoryview’. For contiguous arrays, this is equivalent to the
  start address of the flat memory buffer.
* `arr_memview.shape[0]` could have been replaced by `arr_memview.size`,
  `arr.shape[0]` or `arr.size`. But `arr_memview.shape[0]` is more efficient
  because it doesn’t require any Python interaction.
* `multiply_by_10` will perform computation in-place if the array passed is contiguous,
  and will return a new numpy array if `arr` is not contiguous.
* If you are using Python arrays instead of numpy arrays, you don’t need to check
  if the data is stored contiguously as this is always the case. See [Working with Python arrays](../tutorial/array.html#array-array "../tutorial/array.html#array-array").

This way, you can call the C function similar to a normal Python function,
and leave all the memory management and cleanup to NumPy arrays and Python’s
object handling. For the details of how to compile and
call functions in C files, see [Using C libraries](../tutorial/clibraries.html#using-c-libraries "../tutorial/clibraries.html#using-c-libraries").

## Performance: Disabling initialization checks[¶](#performance-disabling-initialization-checks "Link to this heading")

Every time the memoryview is accessed, Cython adds a check to make sure that it has been initialized.

If you are looking for performance, you can disable them by setting the
`initializedcheck` directive to `False`.
See: [Compiler directives](source_files_and_compilation.html#compiler-directives "source_files_and_compilation.html#compiler-directives") for more information about this directive.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Typed Memoryviews](# "#")
  + [Quickstart](#quickstart "#quickstart")
  + [Using memoryviews](#using-memoryviews "#using-memoryviews")
    - [Syntax](#syntax "#syntax")
    - [Indexing](#indexing "#indexing")
    - [Copying](#copying "#copying")
    - [Transposing](#transposing "#transposing")
    - [Newaxis](#newaxis "#newaxis")
    - [Read-only views](#read-only-views "#read-only-views")
  + [Comparison to the old buffer support](#comparison-to-the-old-buffer-support "#comparison-to-the-old-buffer-support")
  + [Python buffer support](#python-buffer-support "#python-buffer-support")
  + [Memory layout](#memory-layout "#memory-layout")
    - [Background](#background "#background")
    - [Brief recap on C, Fortran and strided memory layouts](#brief-recap-on-c-fortran-and-strided-memory-layouts "#brief-recap-on-c-fortran-and-strided-memory-layouts")
    - [Default behavior for memoryview layouts](#default-behavior-for-memoryview-layouts "#default-behavior-for-memoryview-layouts")
    - [C and Fortran contiguous memoryviews](#c-and-fortran-contiguous-memoryviews "#c-and-fortran-contiguous-memoryviews")
    - [C and Fortran contiguous copies](#c-and-fortran-contiguous-copies "#c-and-fortran-contiguous-copies")
    - [Specifying more general memory layouts](#specifying-more-general-memory-layouts "#specifying-more-general-memory-layouts")
  + [Memoryviews and the GIL](#memoryviews-and-the-gil "#memoryviews-and-the-gil")
  + [Memoryview Objects and Cython Arrays](#memoryview-objects-and-cython-arrays "#memoryview-objects-and-cython-arrays")
  + [Cython arrays](#cython-arrays "#cython-arrays")
  + [CPython array module](#cpython-array-module "#cpython-array-module")
  + [Coercion to NumPy](#coercion-to-numpy "#coercion-to-numpy")
  + [None Slices](#none-slices "#none-slices")
  + [Pass data from a C function via pointer](#pass-data-from-a-c-function-via-pointer "#pass-data-from-a-c-function-via-pointer")
  + [Performance: Disabling initialization checks](#performance-disabling-initialization-checks "#performance-disabling-initialization-checks")

#### Previous topic

[Differences between Cython and Pyrex](pyrex_differences.html "previous chapter")

#### Next topic

[Implementing the buffer protocol](buffer.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/memoryviews.rst.txt "../../_sources/src/userguide/memoryviews.rst.txt")

### Quick search

### Navigation

* [next](buffer.html "Implementing the buffer protocol")
* [previous](pyrex_differences.html "Differences between Cython and Pyrex") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Typed Memoryviews

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

