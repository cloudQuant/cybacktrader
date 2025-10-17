




“Where does that C code come from?” — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/devguide/debugging_the_cython_compiler.html "/en/stable/src/devguide/debugging_the_cython_compiler.html").

### Navigation

* [next](cython_internals.html "Cython internals")
* [previous](getting_started.html "Getting started working on Cython") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Welcome, and thank you for your interest in contributing!](../../CONTRIBUTING.html "../../CONTRIBUTING.html") »
* “Where does that C code come from?”

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# “Where does that C code come from?”[¶](#where-does-that-c-code-come-from "Link to this heading")

Most often, when you are new to Cython development, you have an idea about the Cython code you want to debug.
So, looking at the generated C code, your main question will be: »where is that C code generated?«.

One simple and useful feature to help you start: by default Cython injects the source
Python code into the C code as comments in the form:

```
/* "source_file.pyx":2
 * def print_hello():
 *    print("Hello world")       # <<<<<<<<<<<<<<
 */

__pyx_t_1 = /* some complicated C expression */;
```

so searching the generated C code file for the line of Python/Cython code you’re interested in can be
a good place to start. Some lines may appear in more than one place. For example, functions appear
in both the implementation of the function and the place where it’s added to the module namespace.

To get more detail, the Cython compiler has a couple of debug features that you
can use to pin-point the relevant code sections. They can be enabled in
the module [Cython.Compiler.DebugFlags](https://github.com/cython/cython/blob/master/Cython/Compiler/DebugFlags.py "https://github.com/cython/cython/blob/master/Cython/Compiler/DebugFlags.py").
Read the comments in that file, enable the relevant debug features
(usually `debug_trace_code_generation` to get started), and then
read the C code that Cython generates to find out what is going on.

One trick to identify the origin of a specific line of C code is
to use the Python debugger to stop when that specific line is
written by adding a conditional breakpoint to stop on that line to the
`CCodeWriter.write` function in Code.py. From there you can go up
the call stack and investigate it “live”.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Getting started working on Cython](getting_started.html "previous chapter")

#### Next topic

[Cython internals](cython_internals.html "next chapter")

### This Page

* [Show Source](../../_sources/src/devguide/debugging_the_cython_compiler.rst.txt "../../_sources/src/devguide/debugging_the_cython_compiler.rst.txt")

### Quick search

### Navigation

* [next](cython_internals.html "Cython internals")
* [previous](getting_started.html "Getting started working on Cython") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Welcome, and thank you for your interest in contributing!](../../CONTRIBUTING.html "../../CONTRIBUTING.html") »
* “Where does that C code come from?”

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

