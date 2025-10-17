




Limitations — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/limitations.html "/en/stable/src/userguide/limitations.html").

### Navigation

* [next](pyrex_differences.html "Differences between Cython and Pyrex")
* [previous](migrating_to_cy30.html "Migrating from Cython 0.29 to 3.0") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Limitations

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Limitations[¶](#limitations "Link to this heading")

This page used to list bugs in Cython that made the semantics of
compiled code differ from that in Python. Most of the missing
features have been fixed in Cython 0.15. A future version of
Cython is planned to provide full Python language compatibility.
For now, the issue tracker can provide an overview of deviations
that we are aware of and would like to see fixed.

[https://github.com/cython/cython/labels/Python%20Semantics](https://github.com/cython/cython/labels/Python%20Semantics "https://github.com/cython/cython/labels/Python%20Semantics")

Below is a list of differences that we will probably not be addressing.
Most of these things that fall more into the implementation details rather
than semantics, and we may decide not to fix (or require a –pedantic flag to get).

## Nested tuple argument unpacking[¶](#nested-tuple-argument-unpacking "Link to this heading")

```
def f((a,b), c):
    pass
```

This was removed in Python 3.

## Inspect support[¶](#inspect-support "Link to this heading")

While it is quite possible to emulate the interface of functions in
Cython’s own function type, and recent Cython releases have seen several
improvements here, the “inspect” module does not consider a Cython
implemented function a “function”, because it tests the object type
explicitly instead of comparing an abstract interface or an abstract
base class. This has a negative impact on code that uses inspect to
inspect function objects, but would require a change to Python itself.

## Stack frames[¶](#stack-frames "Link to this heading")

Currently we generate fake tracebacks as part of exception propagation,
but don’t fill in locals and can’t fill in co\_code.
To be fully compatible, we would have to generate these stack frame objects at
function call time (with a potential performance penalty). We may have an
option to enable this for debugging.

## Identity vs. equality for inferred literals[¶](#identity-vs-equality-for-inferred-literals "Link to this heading")

```
a = 1.0          # a inferred to be C type 'double'
b = c = None     # b and c inferred to be type 'object'
if some_runtime_expression:
    b = a        # creates a new Python float object
    c = a        # creates a new Python float object
print(b is c)     # most likely not the same object
```

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Limitations](# "#")
  + [Nested tuple argument unpacking](#nested-tuple-argument-unpacking "#nested-tuple-argument-unpacking")
  + [Inspect support](#inspect-support "#inspect-support")
  + [Stack frames](#stack-frames "#stack-frames")
  + [Identity vs. equality for inferred literals](#identity-vs-equality-for-inferred-literals "#identity-vs-equality-for-inferred-literals")

#### Previous topic

[Migrating from Cython 0.29 to 3.0](migrating_to_cy30.html "previous chapter")

#### Next topic

[Differences between Cython and Pyrex](pyrex_differences.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/limitations.rst.txt "../../_sources/src/userguide/limitations.rst.txt")

### Quick search

### Navigation

* [next](pyrex_differences.html "Differences between Cython and Pyrex")
* [previous](migrating_to_cy30.html "Migrating from Cython 0.29 to 3.0") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Limitations

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

