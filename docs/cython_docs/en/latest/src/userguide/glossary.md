




Glossary — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/glossary.html "/en/stable/src/userguide/glossary.html").

### Navigation

* [next](../reference/index.html "Reference Guide")
* [previous](faq.html "FAQ") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* Glossary

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Glossary[¶](#glossary "Link to this heading")

Extension type[¶](#term-Extension-type "Link to this term")

“Extension type” can refer to either a Cython class defined with `cdef class` or `@cclass`,
or more generally to any Python type that is ultimately implemented as a
native C struct (including the built-in types like int or dict).

Dynamic allocation or Heap allocation[¶](#term-Dynamic-allocation-or-Heap-allocation "Link to this term")

A C variable allocated with `malloc` (in C) or `new` (in C++) is
[allocated dynamically/heap allocated](https://en.wikipedia.org/wiki/C_dynamic_memory_allocation "https://en.wikipedia.org/wiki/C_dynamic_memory_allocation").
Its lifetime is until the user deletes it explicitly (with `free` in C or `del` in C++).
This can happen in a different function than the allocation.

Global Interpreter Lock or GIL[¶](#term-Global-Interpreter-Lock-or-GIL "Link to this term")

A lock inside the Python interpreter to ensure that only one Python thread is run at once.
This lock is purely to ensure that race conditions do not corrupt internal Python state.
Python objects cannot be manipulated unless the GIL is held.
It is most relevant to Cython when writing code that should be run in parallel. If you are
not aiming to write parallel code then there is usually no benefit to releasing the GIL in
Cython. You should not use the GIL as a general locking mechanism in your code since many
operations on Python objects can lead to it being released and to control being passed to
another thread. Also see the [CPython project’s glossary entry](https://docs.python.org/dev/glossary.html#term-global-interpreter-lock "https://docs.python.org/dev/glossary.html#term-global-interpreter-lock").

pointer[¶](#term-pointer "Link to this term")

A pointer is a variable that stores the address of another variable
(i.e. direct address of the memory location). They allow for
dynamic memory allocation and deallocation. They can be used to build
dynamic data structures.
[Read more](https://en.wikipedia.org/wiki/Pointer_(computer_programming)#C_pointers "https://en.wikipedia.org/wiki/Pointer_(computer_programming)#C_pointers").

Python object[¶](#term-Python-object "Link to this term")

When using Python, the contents of every variable is a Python object
(including Cython extension types). Key features of Python objects are that
they are passed by reference and that their lifetime is managed automatically
so that they are destroyed when no more references exist to them.
In Cython, they are distinct from C types, which are passed by value and whose
lifetime is managed depending on whether they are allocated on the stack or heap.
To explicitly declare a Python object variable in Cython use `cdef object abc`.
Internally in C, they are referred to as `PyObject*`.

Stack allocation[¶](#term-Stack-allocation "Link to this term")

A C variable declared within a function as `cdef SomeType a`
is said to be allocated on the stack.
It exists for the duration of the function only.

Typed memoryview[¶](#term-Typed-memoryview "Link to this term")

A useful Cython type for getting quick access to blocks of memory.
A memoryview alone does not actually own any memory.
However, it can be initialized with a Python object that supports the
[buffer protocol](https://docs.python.org/3/c-api/buffer.html "https://docs.python.org/3/c-api/buffer.html") (typically “array” types, for example a Numpy array).
The memoryview keeps a reference to that Python object alive
and provides quick access to the memory without needing to go
through the Python API of the object and its
`__getitem__()` / `__setitem__()` methods.
For more information, see [Typed Memoryviews](memoryviews.html#memoryviews "memoryviews.html#memoryviews").

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[FAQ](faq.html "previous chapter")

#### Next topic

[Reference Guide](../reference/index.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/glossary.rst.txt "../../_sources/src/userguide/glossary.rst.txt")

### Quick search

### Navigation

* [next](../reference/index.html "Reference Guide")
* [previous](faq.html "FAQ") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* Glossary

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

