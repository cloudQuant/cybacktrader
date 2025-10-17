




Pythran as a Numpy backend — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/numpy_pythran.html "/en/stable/src/userguide/numpy_pythran.html").

### Navigation

* [next](nogil.html "Cython and the GIL")
* [previous](numpy_ufuncs.html "Creating Numpy ufuncs") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Pythran as a Numpy backend

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Pythran as a Numpy backend[¶](#pythran-as-a-numpy-backend "Link to this heading")

Using the flag `--np-pythran`, it is possible to use the [Pythran](https://github.com/serge-sans-paille/pythran "https://github.com/serge-sans-paille/pythran") numpy
implementation for numpy related operations. One advantage to use this backend
is that the Pythran implementation uses C++ expression templates to save memory
transfers and can benefit from SIMD instructions of modern CPU.

This can lead to really interesting speedup in some cases, going from 2 up to
16, depending on the targeted CPU architecture and the original algorithm.

Please note that this feature is experimental.

## Usage example with setuptools[¶](#usage-example-with-setuptools "Link to this heading")

You first need to install Pythran. See its [documentation](https://pythran.readthedocs.io/ "https://pythran.readthedocs.io/") for more information.

Then, simply add a `cython: np_pythran=True` directive at the top of the
Python files that needs to be compiled using Pythran numpy support.

Here is an example of a simple `setup.py` file using setuptools:

```
from setuptools import setup
from Cython.Build import cythonize
import numpy
import pythran

setup(
    name = "My hello app",
    ext_modules = cythonize('hello_pythran.pyx'),
    include_dirs = [numpy.get_include(), pythran.get_include()]
)
```

Then, with the following header in `hello_pythran.pyx`:

```
# cython: np_pythran=True
```

`hello_pythran.pyx` will be compiled using Pythran numpy support.

Please note that Pythran can further be tweaked by adding settings in the
`$HOME/.pythranrc` file. For instance, this can be used to enable [Boost.SIMD](https://github.com/NumScale/boost.simd "https://github.com/NumScale/boost.simd") support.
See the [Pythran user manual](https://pythran.readthedocs.io/en/latest/MANUAL.html#customizing-your-pythranrc "https://pythran.readthedocs.io/en/latest/MANUAL.html#customizing-your-pythranrc") for
more information.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Pythran as a Numpy backend](# "#")
  + [Usage example with setuptools](#usage-example-with-setuptools "#usage-example-with-setuptools")

#### Previous topic

[Creating Numpy ufuncs](numpy_ufuncs.html "previous chapter")

#### Next topic

[Cython and the GIL](nogil.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/numpy_pythran.rst.txt "../../_sources/src/userguide/numpy_pythran.rst.txt")

### Quick search

### Navigation

* [next](nogil.html "Cython and the GIL")
* [previous](numpy_ufuncs.html "Creating Numpy ufuncs") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Pythran as a Numpy backend

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

