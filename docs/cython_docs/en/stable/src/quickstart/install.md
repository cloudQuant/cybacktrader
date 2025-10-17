




Installing Cython — Cython 3.1.4 documentation

### Navigation

* [next](build.html "Building Cython code")
* [previous](overview.html "Cython - an overview") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Getting Started](index.html "index.html") »
* Installing Cython

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Installing Cython[¶](#installing-cython "Link to this heading")

Many scientific Python distributions, such as Anaconda [[Anaconda]](#anaconda "#anaconda"),
Enthought Canopy [[Canopy]](#canopy "#canopy"), and Sage [[Sage]](#sage "#sage"),
bundle Cython and no setup is needed. Note however that if your
distribution ships a version of Cython which is too old you can still
use the instructions below to update Cython.

Unlike most Python software, Cython requires a C compiler to be
present on the system. The details of getting a C compiler varies
according to the system used:

* Linux The GNU C Compiler (gcc) is usually present, or easily
  available through the package system. On Ubuntu or Debian, for
  instance, it is part of the `build-essential` package. Next to a
  C compiler, Cython requires the Python header files. On Ubuntu or
  Debian, the command `sudo apt-get install build-essential python3-dev`
  will fetch everything you need.
* Mac OS X To retrieve gcc, one option is to install Apple’s
  XCode, which can be retrieved from the Mac OS X’s install DVDs or
  from [https://developer.apple.com/](https://developer.apple.com/ "https://developer.apple.com/").
* Windows The CPython project recommends building extension modules
  (including Cython modules) with the same compiler that Python was
  built with. This is usually a specific version of Microsoft Visual
  C/C++ (MSVC) - see [https://wiki.python.org/moin/WindowsCompilers](https://wiki.python.org/moin/WindowsCompilers "https://wiki.python.org/moin/WindowsCompilers").
  MSVC is the only compiler that Cython is currently tested with on
  Windows. If you’re having difficulty making setuptools detect
  MSVC then [PyMSVC](https://github.com/kdschlosser/python_msvc "https://github.com/kdschlosser/python_msvc")
  aims to solve this.

  A possible alternative is the open source MinGW (a
  Windows distribution of gcc). See the appendix for instructions for
  setting up MinGW manually. Enthought Canopy and Python(x,y) bundle
  MinGW, but some of the configuration steps in the appendix might
  still be necessary.

The simplest way of installing Cython is by using `pip`:

```
pip install Cython
```

On platforms that are covered by one of the binary wheel packages provided on PyPI,
this will install an accelerated wheel which contains some Cython compiled modules.
Other platforms will use pure Python wheels that install quickly but run somewhat
slower, which is still well adapted for one-time builds e.g. in CI build servers.

For installations on systems where Cython is executed a lot, it is worth checking that
the installation uses a binary module, or otherwise to build a binary wheel locally.

The newest Cython release can always be downloaded from
[https://cython.org/](https://cython.org/ "https://cython.org/"). Unpack the tarball or zip file, enter the
directory, and then run:

```
pip install .
```

For one-time installations from a Cython source checkout, it is substantially
faster than a full binary build to just install the uncompiled (slower) version
of Cython with something like

```
NO_CYTHON_COMPILE=true  pip install .
```

[[Anaconda](#id1 "#id1")]

[https://docs.anaconda.com/anaconda/](https://docs.anaconda.com/anaconda/ "https://docs.anaconda.com/anaconda/")

[[Canopy](#id2 "#id2")]

[https://www.enthought.com/product/canopy/](https://www.enthought.com/product/canopy/ "https://www.enthought.com/product/canopy/")

[[Sage](#id3 "#id3")]

23. Stein et al., Sage Mathematics Software, [https://www.sagemath.org/](https://www.sagemath.org/ "https://www.sagemath.org/")

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Cython - an overview](overview.html "previous chapter")

#### Next topic

[Building Cython code](build.html "next chapter")

### This Page

* [Show Source](../../_sources/src/quickstart/install.rst.txt "../../_sources/src/quickstart/install.rst.txt")

### Quick search

### Navigation

* [next](build.html "Building Cython code")
* [previous](overview.html "Cython - an overview") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Getting Started](index.html "index.html") »
* Installing Cython

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

