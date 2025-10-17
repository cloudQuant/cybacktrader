




Using Parallelism — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/parallelism.html "/en/stable/src/userguide/parallelism.html").

### Navigation

* [next](debugging.html "Debugging your Cython program")
* [previous](buffer.html "Implementing the buffer protocol") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Using Parallelism

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Using Parallelism[¶](#using-parallelism "Link to this heading")

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

Cython supports native parallelism through the [`cython.parallel`](#module-cython.parallel "cython.parallel")
module. To use this kind of parallelism, the [GIL](glossary.html#term-Global-Interpreter-Lock-or-GIL "glossary.html#term-Global-Interpreter-Lock-or-GIL") must be released
(see [Releasing the GIL](external_C_code.html#nogil "external_C_code.html#nogil")).
It currently supports OpenMP, but later on more backends might be supported.

Note

Functionality in this module may only be used from the main thread
or parallel regions due to OpenMP restrictions.

cython.parallel.prange([start,] stop[, step][, nogil=False][, use\_threads\_if=CONDITION][, schedule=None[, chunksize=None]][, num\_threads=None])[¶](#cython.parallel.prange "Link to this definition")

This function can be used for parallel loops. OpenMP automatically
starts a thread pool and distributes the work according to the schedule
used.

Thread-locality and reductions are automatically inferred for variables.

If you assign to a variable in a prange block, it becomes lastprivate, meaning that the
variable will contain the value from the last iteration. If you use an
inplace operator on a variable, it becomes a reduction, meaning that the
values from the thread-local copies of the variable will be reduced with
the operator and assigned to the original variable after the loop. The
index variable is always lastprivate.
Variables assigned to in a parallel with block will be private and unusable
after the block, as there is no concept of a sequentially last value.

Parameters:

* start – The index indicating the start of the loop (same as the start argument in range).
* stop – The index indicating when to stop the loop (same as the stop argument in range).
* step – An integer giving the step of the sequence (same as the step argument in range).
  It must not be 0.
* nogil – This function can only be used with the GIL released.
  If `nogil` is true, the loop will be wrapped in a nogil section.
* use\_threads\_if – The loop is run in multiple threads only if `CONDITION`
  is evaluated as true. Otherwise the code is run sequentially. Running
  the loop sequentially can be handy in the cases when the cost of spawning
  threads is greater than the benefit of running the loop in parallel
  (e.g. for small data sets).
* schedule –

  The `schedule` is passed to OpenMP and can be one of the following:

  static:

  If a chunksize is provided, iterations are distributed to all
  threads ahead of time in blocks of the given chunksize. If no
  chunksize is given, the iteration space is divided into chunks that
  are approximately equal in size, and at most one chunk is assigned
  to each thread in advance.

  This is most appropriate when the scheduling overhead matters and
  the problem can be cut down into equally sized chunks that are
  known to have approximately the same runtime.

  dynamic:

  The iterations are distributed to threads as they request them,
  with a default chunk size of 1.

  This is suitable when the runtime of each chunk differs and is not
  known in advance and therefore a larger number of smaller chunks
  is used in order to keep all threads busy.

  guided:

  As with dynamic scheduling, the iterations are distributed to
  threads as they request them, but with decreasing chunk size. The
  size of each chunk is proportional to the number of unassigned
  iterations divided by the number of participating threads,
  decreasing to 1 (or the chunksize if provided).

  This has an advantage over pure dynamic scheduling when it turns
  out that the last chunks take more time than expected or are
  otherwise being badly scheduled, so that most threads start running
  idle while the last chunks are being worked on by only a smaller
  number of threads.

  runtime:

  The schedule and chunk size are taken from the runtime scheduling
  variable, which can be set through the `openmp.omp_set_schedule()`
  function call, or the `OMP_SCHEDULE` environment variable. Note that
  this essentially disables any static compile time optimisations of
  the scheduling code itself and may therefore show a slightly worse
  performance than when the same scheduling policy is statically
  configured at compile time.
  The default schedule is implementation defined. For more information consult
  the OpenMP specification [[1]](#id2 "#id2").
* num\_threads – The `num_threads` argument indicates how many threads the team should consist of. If not given,
  OpenMP will decide how many threads to use. Typically this is the number of cores available on
  the machine. However, this may be controlled through the `omp_set_num_threads()` function, or
  through the `OMP_NUM_THREADS` environment variable.
* chunksize – The `chunksize` argument indicates the chunksize to be used for dividing the iterations among threads.
  This is only valid for `static`, `dynamic` and `guided` scheduling, and is optional. Different chunksizes
  may give substantially different performance results, depending on the schedule, the load balance it provides,
  the scheduling overhead and the amount of false sharing (if any).

Example with a reduction:

Pure PythonCython

```
from cython.parallel import prange

i = cython.declare(cython.int)
n = cython.declare(cython.int, 30)
sum = cython.declare(cython.int, 0)

for i in prange(n, nogil=True):
    sum += i

print(sum)
```

```
from cython.parallel import prange

cdef int i
cdef int n = 30
cdef int sum = 0

for i in prange(n, nogil=True):
    sum += i

print(sum)
```

Example with a [typed memoryview](glossary.html#term-Typed-memoryview "glossary.html#term-Typed-memoryview") (e.g. a NumPy array)

Pure PythonCython

```
from cython.parallel import prange

def func(x: cython.double[:], alpha: cython.double):
    i: cython.Py_ssize_t

    for i in prange(x.shape[0], nogil=True):
        x[i] = alpha * x[i]
```

```
from cython.parallel import prange

def func(double[:] x, double alpha):
    cdef Py_ssize_t i

    for i in prange(x.shape[0], nogil=True):
        x[i] = alpha * x[i]
```

Example with conditional parallelism:

Pure PythonCython

```
from cython.parallel import prange

def psum(n: cython.int):

    i: cython.int
    sum: cython.int = 0

    for i in prange(n, nogil=True, use_threads_if=n>1000):
        sum += i

    return sum

psum(30)        # Executed sequentially
psum(10000)     # Executed in parallel
```

```
from cython.parallel import prange

def psum(int n):

    cdef int i
    cdef int sum = 0

    for i in prange(n, nogil=True, use_threads_if=n>1000):
        sum += i

    return sum

psum(30)        # Executed sequentially
psum(10000)     # Executed in parallel
```

cython.parallel.parallel(num\_threads=None, use\_threads\_if=CONDITION)[¶](#cython.parallel.parallel "Link to this definition")

This directive can be used as part of a `with` statement to execute code
sequences in parallel. This is currently useful to setup thread-local
buffers used by a `prange`. A contained `prange` will be a worksharing loop
that is not parallel, so any variable assigned to in the parallel section
is also private to the `prange`. Variables that are private in the parallel
block are unavailable after the parallel block.

Example with thread-local buffers

Pure PythonCython

```
from cython.parallel import parallel, prange
from cython.cimports.libc.stdlib import abort, malloc, free

@cython.nogil
@cython.cfunc
def func(buf: cython.p_int) -> cython.void:
    pass
    # ...

idx = cython.declare(cython.Py_ssize_t)
i = cython.declare(cython.Py_ssize_t)
j = cython.declare(cython.Py_ssize_t)
n = cython.declare(cython.Py_ssize_t, 100)
local_buf = cython.declare(cython.p_int)
size = cython.declare(cython.size_t, 10)

with cython.nogil, parallel():
    local_buf: cython.p_int = cython.cast(cython.p_int, malloc(cython.sizeof(cython.int) * size))
    if local_buf is cython.NULL:
        abort()

    # populate our local buffer in a sequential loop
    for i in range(size):
        local_buf[i] = i * 2

    # share the work using the thread-local buffer(s)
    for j in prange(n, schedule='guided'):
        func(local_buf)

    free(local_buf)
```

```
from cython.parallel import parallel, prange
from libc.stdlib cimport abort, malloc, free



cdef void func(int *buf) noexcept nogil:
    pass
    # ...

cdef Py_ssize_t idx, i, j, n = 100
cdef int * local_buf
cdef size_t size = 10




with nogil, parallel():
    local_buf = <int *> malloc(sizeof(int) * size)
    if local_buf is NULL:
        abort()

    # populate our local buffer in a sequential loop
    for i in range(size):
        local_buf[i] = i * 2

    # share the work using the thread-local buffer(s)
    for j in prange(n, schedule='guided'):
        func(local_buf)

    free(local_buf)
```

Later on sections might be supported in parallel blocks, to distribute
code sections of work among threads.

cython.parallel.threadid()[¶](#cython.parallel.threadid "Link to this definition")

Returns the id of the thread. For n threads, the ids will range from 0 to
n-1.

## Compiling[¶](#compiling "Link to this heading")

To actually use the OpenMP support, you need to tell the C or C++ compiler to
enable OpenMP. For gcc this can be done as follows in a `setup.py`:

Pure PythonCython

```
from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "hello",
        ["hello.py"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='hello-parallel-world',
    ext_modules=cythonize(ext_modules),
)
```

```
from setuptools import Extension, setup
from Cython.Build import cythonize

ext_modules = [
    Extension(
        "hello",
        ["hello.pyx"],
        extra_compile_args=['-fopenmp'],
        extra_link_args=['-fopenmp'],
    )
]

setup(
    name='hello-parallel-world',
    ext_modules=cythonize(ext_modules),
)
```

For the Microsoft Visual C++ compiler, use `'/openmp'` instead of `'-fopenmp'` for the `'extra_compile_args'` option. Don’t add any OpenMP flags to the `'extra_link_args'` option.

## Breaking out of loops[¶](#breaking-out-of-loops "Link to this heading")

The parallel with and prange blocks support the statements break, continue and
return in nogil mode. Additionally, it is valid to use a `with gil` block
inside these blocks, and have exceptions propagate from them.
However, because the blocks use OpenMP, they can not just be left, so the
exiting procedure is best-effort. For `prange()` this means that the loop
body is skipped after the first break, return or exception for any subsequent
iteration in any thread. It is undefined which value shall be returned if
multiple different values may be returned, as the iterations are in no
particular order:

Pure PythonCython

```
from cython.parallel import prange

@cython.exceptval(-1)
@cython.cfunc
def func(n: cython.Py_ssize_t) -> cython.int:
    i: cython.Py_ssize_t

    for i in prange(n, nogil=True):
        if i == 8:
            with cython.gil:
                raise Exception()
        elif i == 4:
            break
        elif i == 2:
            return i
```

```
from cython.parallel import prange



cdef int func(Py_ssize_t n) except -1:
    cdef Py_ssize_t i

    for i in prange(n, nogil=True):
        if i == 8:
            with gil:
                raise Exception()
        elif i == 4:
            break
        elif i == 2:
            return i
```

In the example above it is undefined whether an exception shall be raised,
whether it will simply break or whether it will return 2.

## Using OpenMP Functions[¶](#using-openmp-functions "Link to this heading")

OpenMP functions can be used by cimporting `openmp`:

Pure PythonCython

```
from cython.parallel import parallel
from cython.cimports.openmp import omp_set_dynamic, omp_get_num_threads

num_threads = cython.declare(cython.int)

omp_set_dynamic(1)
with cython.nogil, parallel():
    num_threads = omp_get_num_threads()
    # ...
```

```
from cython.parallel cimport parallel
cimport openmp

cdef int num_threads

openmp.omp_set_dynamic(1)
with nogil, parallel():
    num_threads = openmp.omp_get_num_threads()
    # ...
```

References

[[1](#id1 "#id1")]

[https://www.openmp.org/mp-documents/spec30.pdf](https://www.openmp.org/mp-documents/spec30.pdf "https://www.openmp.org/mp-documents/spec30.pdf")

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Using Parallelism](# "#")
  + [`prange()`](#cython.parallel.prange "#cython.parallel.prange")
  + [`parallel()`](#cython.parallel.parallel "#cython.parallel.parallel")
  + [`threadid()`](#cython.parallel.threadid "#cython.parallel.threadid")
  + [Compiling](#compiling "#compiling")
  + [Breaking out of loops](#breaking-out-of-loops "#breaking-out-of-loops")
  + [Using OpenMP Functions](#using-openmp-functions "#using-openmp-functions")

#### Previous topic

[Implementing the buffer protocol](buffer.html "previous chapter")

#### Next topic

[Debugging your Cython program](debugging.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/parallelism.rst.txt "../../_sources/src/userguide/parallelism.rst.txt")

### Quick search

### Navigation

* [next](debugging.html "Debugging your Cython program")
* [previous](buffer.html "Implementing the buffer protocol") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Using Parallelism

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

