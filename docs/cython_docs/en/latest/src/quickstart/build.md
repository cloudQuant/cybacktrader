




Building Cython code — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/quickstart/build.html "/en/stable/src/quickstart/build.html").

### Navigation

* [next](cythonize.html "Faster code via static typing")
* [previous](install.html "Installing Cython") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Getting Started](index.html "index.html") »
* Building Cython code

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Building Cython code[¶](#building-cython-code "Link to this heading")

Cython code must, unlike Python, be compiled. This happens in two stages:

* A `.pyx` or `.py` file is compiled by Cython to a `.c` file, containing
  the code of a Python extension module.
* The `.c` file is compiled by a C compiler to
  a `.so` file (or `.pyd` on Windows) which can be
  `import`-ed directly into a Python session.
  [setuptools](https://setuptools.readthedocs.io/ "https://setuptools.readthedocs.io/") takes care of this part.
  Although Cython can call them for you in certain cases.

To understand fully the Cython + setuptools build process,
one may want to read more about
[distributing Python modules](https://packaging.python.org/en/latest/tutorials/packaging-projects/ "https://packaging.python.org/en/latest/tutorials/packaging-projects/").

There are several ways to build Cython code:

* Write a setuptools `setup.py`. This is the normal and recommended way.
* Run the `cythonize` command-line utility. This is a good approach for
  compiling a single Cython source file directly to an extension.
  A source file can be built “in place” (so that the extension module is created
  next to the source file, ready to be imported) with `cythonize -i filename.pyx`.
* Use [Pyximport](../userguide/source_files_and_compilation.html#pyximport "../userguide/source_files_and_compilation.html#pyximport"), importing Cython `.pyx` files as if they
  were `.py` files (using setuptools to compile and build in the background).
  This method is easier than writing a `setup.py`, but is not very flexible.
  So you’ll need to write a `setup.py` if, for example, you need certain compilations options.
* Run the `cython` command-line utility manually to produce the `.c` file
  from the `.pyx` file, then manually compiling the `.c` file into a shared
  object library or DLL suitable for import from Python.
  (These manual steps are mostly for debugging and experimentation.)
* Use the [[Jupyter]](#jupyter "#jupyter") notebook or the [[Sage]](install.html#sage "install.html#sage") notebook,
  both of which allow Cython code inline.
  This is the easiest way to get started writing Cython code and running it.

Currently, using setuptools is the most common way Cython files are built and distributed.
The other methods are described in more detail in the [Source Files and Compilation](../userguide/source_files_and_compilation.html#compilation "../userguide/source_files_and_compilation.html#compilation") section of the reference manual.

## Building a Cython module using setuptools[¶](#building-a-cython-module-using-setuptools "Link to this heading")

Imagine a simple “hello world” script in a file `hello.pyx`:

```
def say_hello_to(name):
    print(f"Hello {name}!")
```

The following could be a corresponding `setup.py` script:

```
from setuptools import setup
from Cython.Build import cythonize

setup(
    name='Hello world app',
    ext_modules=cythonize("hello.pyx"),
)
```

To build, run `python setup.py build_ext --inplace`. Then simply
start a Python session and do `from hello import say_hello_to` and
use the imported function as you see fit.

## Using the Jupyter notebook[¶](#using-the-jupyter-notebook "Link to this heading")

Cython can be used conveniently and interactively from a web browser
through the Jupyter notebook. To install Jupyter notebook, e.g. into a virtualenv,
use pip:

```
(venv)$ pip install jupyter
(venv)$ jupyter notebook
```

To enable support for Cython compilation, install Cython as described in [the installation guide](install.html#install "install.html#install")
and load the `Cython` extension from within the Jupyter notebook:

```
%load_ext Cython
```

Then, prefix a cell with the `%%cython` marker to compile it

Pure PythonCython

```
%%cython

a: cython.int = 0
for i in range(10):
    a += i
print(a)
```

```
%%cython

cdef int a = 0
for i in range(10):
    a += i
print(a)
```

You can show Cython’s code analysis by passing the `--annotate` option:

```
%%cython --annotate
...
```

![../../_images/jupyter.png](../../_images/jupyter.png)

For more information about the arguments of the `%%cython` magic, see
[Compiling with a Jupyter Notebook](../userguide/source_files_and_compilation.html#compiling-notebook "../userguide/source_files_and_compilation.html#compiling-notebook").

## Using the Sage notebook[¶](#using-the-sage-notebook "Link to this heading")

For users of the SageMath distribution, the Sage notebook uses Jupyter by default.
Sage provides its own implementation of the `%%cython` cell magic (see
[Sage Magics](https://doc.sagemath.org/html/en/reference/repl/sage/repl/ipython_extension.html#sage.repl.ipython_extension.SageMagics.cython "https://doc.sagemath.org/html/en/reference/repl/sage/repl/ipython_extension.html#sage.repl.ipython_extension.SageMagics.cython"))
which is loaded by default.
Alternatively, you can overwrite it with the implementation provided by Cython,
the procedure outlined for Jupyter notebooks also applies.

[[Jupyter](#id1 "#id1")]

[https://jupyter.org/](https://jupyter.org/ "https://jupyter.org/")

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Building Cython code](# "#")
  + [Building a Cython module using setuptools](#building-a-cython-module-using-setuptools "#building-a-cython-module-using-setuptools")
  + [Using the Jupyter notebook](#using-the-jupyter-notebook "#using-the-jupyter-notebook")
  + [Using the Sage notebook](#using-the-sage-notebook "#using-the-sage-notebook")

#### Previous topic

[Installing Cython](install.html "previous chapter")

#### Next topic

[Faster code via static typing](cythonize.html "next chapter")

### This Page

* [Show Source](../../_sources/src/quickstart/build.rst.txt "../../_sources/src/quickstart/build.rst.txt")

### Quick search

### Navigation

* [next](cythonize.html "Faster code via static typing")
* [previous](install.html "Installing Cython") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Getting Started](index.html "index.html") »
* Building Cython code

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

