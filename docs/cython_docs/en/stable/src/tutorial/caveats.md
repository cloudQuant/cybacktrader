




Caveats — Cython 3.1.4 documentation

### Navigation

* [next](profiling_tutorial.html "Profiling")
* [previous](pxd_files.html "pxd files") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Caveats

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Caveats[¶](#caveats "Link to this heading")

Since Cython mixes C and Python semantics, some things may be a bit
surprising or unintuitive. Work always goes on to make Cython more natural
for Python users, so this list may change in the future.

* Given two typed `int` variables `a` and `b`, `a % b` has the
  same sign as the second argument (following Python semantics) rather than
  having the same sign as the first (as in C). The C behavior can be
  obtained, at some speed gain, by enabling the cdivision directive
  (versions prior to Cython 0.12 always followed C semantics).
* Care is needed with unsigned types. `cdef unsigned n = 10;
  print(range(-n, n))` will print an empty list, since `-n` wraps
  around to a large positive integer prior to being passed to the
  `range` function.
* Python’s `float` type actually wraps C `double` values, and
  the `int` type in Python 2.x wraps C `long` values.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[pxd files](pxd_files.html "previous chapter")

#### Next topic

[Profiling](profiling_tutorial.html "next chapter")

### This Page

* [Show Source](../../_sources/src/tutorial/caveats.rst.txt "../../_sources/src/tutorial/caveats.rst.txt")

### Quick search

### Navigation

* [next](profiling_tutorial.html "Profiling")
* [previous](pxd_files.html "pxd files") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Caveats

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

