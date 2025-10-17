




Related work — Cython 3.1.4 documentation

### Navigation

* [next](appendix.html "Appendix: Installing MinGW on Windows")
* [previous](readings.html "Further reading") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Related work

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Related work[¶](#related-work "Link to this heading")

Pyrex [[Pyrex]](../quickstart/overview.html#pyrex "../quickstart/overview.html#pyrex") is the compiler project that Cython was originally
based on. Many features and the major design decisions of the Cython
language were developed by Greg Ewing as part of that project. Today,
Cython supersedes the capabilities of Pyrex by providing a
substantially higher compatibility with Python code and Python
semantics, as well as superior optimisations and better integration
with scientific Python extensions like NumPy.

ctypes [[ctypes]](#ctypes "#ctypes") is a foreign function interface (FFI) for Python. It
provides C compatible data types, and allows calling functions in DLLs
or shared libraries. It can be used to wrap these libraries in pure
Python code. Compared to Cython, it has the major advantage of being
in the standard library and being usable directly from Python code,
without any additional dependencies. The major drawback is its
performance, which suffers from the Python call overhead as all
operations must pass through Python code first. Cython, being a
compiled language, can avoid much of this overhead by moving more
functionality and long-running loops into fast C code.

SWIG [[SWIG]](#swig "#swig") is a wrapper code generator. It makes it very easy to
parse large API definitions in C/C++ header files, and to generate
straight forward wrapper code for a large set of programming
languages. As opposed to Cython, however, it is not a programming
language itself. Thin wrappers are easy to generate, but the more
functionality a wrapper needs to provide, the harder it gets to
implement it with SWIG. Cython, on the other hand, makes it very easy
to write very elaborate wrapper code specifically for the Python
language, and to make it as thin or thick as needed at any given
place. Also, there exists third party code for parsing C header files
and using it to generate Cython definitions and module skeletons.

ShedSkin [[ShedSkin]](#shedskin "#shedskin") is an experimental Python-to-C++ compiler. It
uses a very powerful whole-module type inference engine to generate a
C++ program from (restricted) Python source code. The main drawback
is that it has no support for calling the Python/C API for operations
it does not support natively, and supports very few of the standard
Python modules.

[[ctypes](#id2 "#id2")]

[https://docs.python.org/library/ctypes.html](https://docs.python.org/library/ctypes.html "https://docs.python.org/library/ctypes.html").

[[ShedSkin](#id4 "#id4")]

M. Dufour, J. Coughlan, ShedSkin,
[https://github.com/shedskin/shedskin](https://github.com/shedskin/shedskin "https://github.com/shedskin/shedskin")

[[SWIG](#id3 "#id3")]

David M. Beazley et al.,
SWIG: An Easy to Use Tool for Integrating Scripting Languages with C and C++,
[http://www.swig.org](http://www.swig.org "http://www.swig.org").

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Further reading](readings.html "previous chapter")

#### Next topic

[Appendix: Installing MinGW on Windows](appendix.html "next chapter")

### This Page

* [Show Source](../../_sources/src/tutorial/related_work.rst.txt "../../_sources/src/tutorial/related_work.rst.txt")

### Quick search

### Navigation

* [next](appendix.html "Appendix: Installing MinGW on Windows")
* [previous](readings.html "Further reading") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Related work

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

