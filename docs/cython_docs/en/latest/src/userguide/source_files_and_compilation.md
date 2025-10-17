




Source Files and Compilation — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/source_files_and_compilation.html "/en/stable/src/userguide/source_files_and_compilation.html").

### Navigation

* [next](early_binding_for_speed.html "Early Binding for Speed")
* [previous](external_C_code.html "Interfacing with External C Code") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Source Files and Compilation

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Source Files and Compilation[¶](#source-files-and-compilation "Link to this heading")

Cython source file names consist of the name of the module followed by a
`.pyx` extension, for example a module called primes would have a source
file named `primes.pyx`.

Cython code, unlike Python, must be compiled. This happens in two stages:

* A `.pyx` (or `.py`) file is compiled by Cython to a `.c` file.
* The `.c` file is compiled by a C compiler to a `.so` file (or a
  `.pyd` file on Windows)

Once you have written your `.pyx`/`.py` file, there are a couple of ways
how to turn it into an extension module.

The following sub-sections describe several ways to build your
extension modules, and how to pass directives to the Cython compiler.

There are also a number of tools that process `.pyx` files apart from Cython, e.g.

* Linting: [https://pypi.org/project/cython-lint/](https://pypi.org/project/cython-lint/ "https://pypi.org/project/cython-lint/")

## Compiling from the command line[¶](#compiling-from-the-command-line "Link to this heading")

There are two ways of compiling from the command line.

* The cython command takes a `.py` or `.pyx` file and
  compiles it into a C/C++ file.
* The cythonize command takes a `.py` or `.pyx` file and
  compiles it into a C/C++ file. It then compiles the C/C++ file into
  an extension module which is directly importable from Python.

### Compiling with the cython command[¶](#compiling-with-the-cython-command "Link to this heading")

One way is to compile it manually with the Cython
compiler, e.g.:

```
$ cython primes.pyx
```

This will produce a file called `primes.c`, which then needs to be
compiled with the C compiler using whatever options are appropriate on your
platform for generating an extension module. For these options look at the
official Python documentation.

The other, and probably better, way is to use the `setuptools` extension
provided with Cython. The benefit of this method is that it will give the
platform specific compilation options, acting like a stripped down autotools.

### Compiling with the cythonize command[¶](#compiling-with-the-cythonize-command "Link to this heading")

Run the cythonize compiler command with your options and list of
`.pyx` files to generate an extension module. For example:

```
$ cythonize -a -i yourmod.pyx
```

This creates a `yourmod.c` file (or `yourmod.cpp` in C++ mode), compiles it,
and puts the resulting extension module (`.so` or `.pyd`, depending on your
platform) next to the source file for direct import (`-i` builds “in place”).
The `-a` switch additionally produces an annotated html file of the source code.

The cythonize command accepts multiple source files and glob patterns like
`**/*.pyx` as argument and also understands the common `-j` option for
running multiple parallel build jobs. When called without further options, it
will only translate the source files to `.c` or `.cpp` files. Pass the
`-h` flag for a complete list of supported options.

There simpler command line tool cython only invokes the source code translator.

In the case of manual compilation, how to compile your `.c` files will vary
depending on your operating system and compiler. The Python documentation for
writing extension modules should have some details for your system. On a Linux
system, for example, it might look similar to this:

```
$ gcc -shared -pthread -fPIC -fwrapv -O2 -Wall -fno-strict-aliasing \
      -I/usr/include/python3.5 -o yourmod.so yourmod.c
```

(gcc will need to have paths to your included header files and paths
to libraries you want to link with.)

After compilation, a `yourmod.so` (`yourmod.pyd` for Windows)
file is written into the target directory
and your module, `yourmod`, is available for you to import as with any other
Python module. Note that if you are not relying on cythonize or `setuptools`,
you will not automatically benefit from the platform specific file extension
that CPython generates for disambiguation, such as
`yourmod.cpython-35m-x86_64-linux-gnu.so` on a regular 64bit Linux installation
of CPython 3.5.

## Basic `setup.py`[¶](#basic-setup-py "Link to this heading")

The setuptools extension provided with Cython allows you to pass `.pyx` files
directly to the [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") constructor in your setup file.

If you have a single Cython file that you want to turn into a compiled
extension, say with filename `example.pyx` the associated `setup.py`
would be:

setup.py[¶](#id14 "Link to this code")

```
from setuptools import setup
from Cython.Build import cythonize

setup(
    ext_modules = cythonize("example.pyx")
)
```

If your build depends directly on Cython in this way,
then you may also want to inform pip that `Cython` is required for
`setup.py` to execute, following [PEP 518](https://peps.python.org/pep-0518/ "https://peps.python.org/pep-0518/"),
creating a `pyproject.toml` file containing, at least:

pyproject.toml[¶](#id15 "Link to this code")

```
[build-system]
requires = ["setuptools", "Cython"]
```

To understand the `setup.py` more fully look at the official
[setuptools documentation](https://setuptools.pypa.io/en/latest/index.html "(in setuptools v80.9.0)").
To compile the extension for use in the current directory use:

```
$ python setup.py build_ext --inplace
```

Note

setuptools 74.1.0 adds experimental support for extensions in `pyproject.toml` (instead of `setup.py`):

pyproject.toml[¶](#id16 "Link to this code")

```
[build-system]
requires = ["setuptools", "cython"]
build-backend = "setuptools.build_meta"

[project]
name = "mylib-foo"
version = "0.42"

[tool.setuptools]
ext-modules = [
  {name = "example", sources = ["example.pyx"]}
]
```

In this case, you can use any build frontend - e.g. [build](https://pypi.org/project/build/ "https://pypi.org/project/build/")

```
$ python -m build
```

### Configuring the C-Build[¶](#configuring-the-c-build "Link to this heading")

Note

More details on building Cython modules that use cimport numpy can be found in the [Numpy section](numpy_tutorial.html#numpy-compilation "numpy_tutorial.html#numpy-compilation") of the user guide.

If you have [Cython include files](language_basics.html#include-statement "language_basics.html#include-statement") or [Cython definition files](language_basics.html#definition-file "language_basics.html#definition-file") in non-standard places you can pass an
`include_path` parameter to `cythonize`:

```
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="My hello app",
    ext_modules=cythonize("src/*.pyx", include_path=[...]),
)
```

If you need to specify compiler options, libraries to link with or other
linker options you will need to create [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") instances manually
(note that glob syntax can still be used to specify multiple extensions
in one line):

```
from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension("primes", ["primes.pyx"],
        include_dirs=[...],
        libraries=[...],
        library_dirs=[...]),
    # Everything but primes.pyx is included here.
    Extension("*", ["*.pyx"],
        include_dirs=[...],
        libraries=[...],
        library_dirs=[...]),
]
setup(
    name="My hello app",
    ext_modules=cythonize(extensions),
)
```

Some useful options to know about are

* `include_dirs`- list of directories to search for C/C++ header files (in Unix form for portability),
* `libraries` - list of library names (not filenames or paths) to link against,
* `library_dirs` - list of directories to search for C/C++ libraries at link time.

Note that when using setuptools, you should import it before Cython, otherwise,
both might disagree about the class to use here.

Often, Python packages that offer a C-level API provide a way to find
the necessary C header files:

```
from setuptools import Extension, setup
from Cython.Build import cythonize

extensions = [
    Extension("*", ["*.pyx"],
        include_dirs=["/usr/local/include"]),
]
setup(
    name="My hello app",
    ext_modules=cythonize(extensions),
)
```

If your options are static (for example you do not need to call a tool like
`pkg-config` to determine them) you can also provide them directly in your
`.pyx` or `.pxd` source file using a special comment block at the start of the file:

```
# distutils: libraries = spam eggs
# distutils: include_dirs = /opt/food/include
```

If you cimport multiple .pxd files defining libraries, then Cython
merges the list of libraries, so this works as expected (similarly
with other options, like `include_dirs` above).

If you have some C files that have been wrapped with Cython and you want to
compile them into your extension, you can define the setuptools `sources`
parameter:

```
# distutils: sources = [helper.c, another_helper.c]
```

Note that these sources are added to the list of sources of the current
extension module. Spelling this out in the `setup.py` file looks
as follows:

```
from setuptools import Extension, setup
from Cython.Build import cythonize

sourcefiles = ['example.pyx', 'helper.c', 'another_helper.c']

extensions = [Extension("example", sourcefiles)]

setup(
    ext_modules=cythonize(extensions)
)
```

The [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") class takes many options, and a fuller explanation can
be found in the [setuptools documentation](https://setuptools.pypa.io/en/latest/index.html "(in setuptools v80.9.0)").

Sometimes this is not enough and you need finer customization of the
setuptools [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)").
To do this, you can provide a custom function `create_extension`
to create the final [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") object after Cython has processed
the sources, dependencies and `# distutils` directives but before the
file is actually Cythonized.
This function takes 2 arguments `template` and `kwds`, where
`template` is the [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") object given as input to Cython
and `kwds` is a [`dict`](https://docs.python.org/3/library/stdtypes.html#dict "(in Python v3.14)") with all keywords which should be used
to create the [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)").
The function `create_extension` must return a 2-tuple
`(extension, metadata)`, where `extension` is the created
[`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") and `metadata` is metadata which will be written
as JSON at the top of the generated C files. This metadata is only used
for debugging purposes, so you can put whatever you want in there
(as long as it can be converted to JSON).
The default function (defined in `Cython.Build.Dependencies`) is:

```
def default_create_extension(template, kwds):
    if 'depends' in kwds:
        include_dirs = kwds.get('include_dirs', []) + ["."]
        depends = resolve_depends(kwds['depends'], include_dirs)
        kwds['depends'] = sorted(set(depends + template.depends))

    t = template.__class__
    ext = t(**kwds)
    if hasattr(template, "py_limited_api"):
        ext.py_limited_api = template.py_limited_api
    metadata = dict(distutils=kwds, module_name=kwds['name'])
    return ext, metadata
```

In case that you pass a string instead of an [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") to
`cythonize()`, the `template` will be an [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") without
sources. For example, if you do `cythonize("*.pyx")`,
the `template` will be `Extension(name="*.pyx", sources=[])`.

Just as an example, this adds `mylib` as library to every extension:

```
from Cython.Build.Dependencies import default_create_extension

def my_create_extension(template, kwds):
    libs = kwds.get('libraries', []) + ["mylib"]
    kwds['libraries'] = libs
    return default_create_extension(template, kwds)

ext_modules = cythonize(..., create_extension=my_create_extension)
```

Note

If you Cythonize in parallel (using the `nthreads` argument),
then the argument to `create_extension` must be pickleable.
In particular, it cannot be a lambda function.

### Cythonize arguments[¶](#cythonize-arguments "Link to this heading")

The function `cythonize()` can take extra arguments which will allow you to
customize your build.

Cython.Build.cythonize(module\_list, exclude=None, nthreads=0, aliases=None, quiet=False, force=None, language=None, exclude\_failures=False, show\_all\_warnings=False, \*\*options)[¶](#Cython.Build.cythonize "Link to this definition")

Compile a set of source modules into C/C++ files and return a list of distutils
Extension objects for them.

Parameters:

* module\_list – As module list, pass either a glob pattern, a list of glob
  patterns or a list of Extension objects. The latter
  allows you to configure the extensions separately
  through the normal distutils options.
  You can also pass Extension objects that have
  glob patterns as their sources. Then, cythonize
  will resolve the pattern and create a
  copy of the Extension for every matching file.
* exclude – When passing glob patterns as `module_list`, you can exclude certain
  module names explicitly by passing them into the `exclude` option.
* nthreads – The number of concurrent builds for parallel compilation
  (requires the `multiprocessing` module).
* aliases – If you want to use compiler directives like `# distutils: ...` but
  can only know at compile time (when running the `setup.py`) which values
  to use, you can use aliases and pass a dictionary mapping those aliases
  to Python strings when calling [`cythonize()`](#Cython.Build.cythonize "Cython.Build.cythonize"). As an example, say you
  want to use the compiler
  directive `# distutils: include_dirs = ../static_libs/include/`
  but this path isn’t always fixed and you want to find it when running
  the `setup.py`. You can then do `# distutils: include_dirs = MY_HEADERS`,
  find the value of `MY_HEADERS` in the `setup.py`, put it in a python
  variable called `foo` as a string, and then call
  `cythonize(..., aliases={'MY_HEADERS': foo})`.
* quiet – If True, Cython won’t print error, warning, or status messages during the
  compilation.
* force – Forces the recompilation of the Cython modules, even if the timestamps
  don’t indicate that a recompilation is necessary.
* language – To globally enable C++ mode, you can pass `language='c++'`. Otherwise, this
  will be determined at a per-file level based on compiler directives. This
  affects only modules found based on file names. Extension instances passed
  into [`cythonize()`](#Cython.Build.cythonize "Cython.Build.cythonize") will not be changed. It is recommended to rather
  use the compiler directive `# distutils: language = c++` than this option.
* exclude\_failures – For a broad ‘try to compile’ mode that ignores compilation
  failures and simply excludes the failed extensions,
  pass `exclude_failures=True`. Note that this only
  really makes sense for compiling `.py` files which can also
  be used without compilation.
* show\_all\_warnings – By default, not all Cython warnings are printed.
  Set to true to show all warnings.
* annotate – If `True`, will produce a HTML file for each of the `.pyx` or `.py`
  files compiled. The HTML file gives an indication
  of how much Python interaction there is in
  each of the source code lines, compared to plain C code.
  It also allows you to see the C/C++ code
  generated for each line of Cython code. This report is invaluable when
  optimizing a function for speed,
  and for determining when to [release the GIL](external_C_code.html#nogil "external_C_code.html#nogil"):
  in general, a `nogil` block may contain only “white” code.
  See examples in [Determining where to add types](../quickstart/cythonize.html#determining-where-to-add-types "../quickstart/cythonize.html#determining-where-to-add-types") or
  [Primes](../tutorial/cython_tutorial.html#primes "../tutorial/cython_tutorial.html#primes").
* annotate-fullc – If `True` will produce a colorized HTML version of
  the source which includes entire generated C/C++-code.
* compiler\_directives – Allow to set compiler directives in the `setup.py` like this:
  `compiler_directives={'embedsignature': True}`.
  See [Compiler directives](#compiler-directives "#compiler-directives").
* depfile – produce depfiles for the sources if True.
* cache – If `True` the cache enabled with default path. If the value is a path to a directory,
  then the directory is used to cache generated `.c`/`.cpp` files. By default cache is disabled.
  See [Cython cache](#cython-cache "#cython-cache").

## Multiple Cython Files in a Package[¶](#multiple-cython-files-in-a-package "Link to this heading")

To automatically compile multiple Cython files without listing all of them
explicitly, you can use glob patterns:

```
setup(
    ext_modules = cythonize("package/*.pyx")
)
```

You can also use glob patterns in [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)") objects if you pass
them through `cythonize()`:

```
extensions = [Extension("*", ["*.pyx"])]

setup(
    ext_modules = cythonize(extensions)
)
```

### Distributing Cython modules[¶](#distributing-cython-modules "Link to this heading")

Following recent improvements in the distribution toolchain, it is
not recommended to include generated files in source distributions.
Instead, require Cython at build-time to generate the C/C++ files,
as defined in [PEP 518](https://peps.python.org/pep-0518/ "https://peps.python.org/pep-0518/") and [PEP 621](https://peps.python.org/pep-0621/ "https://peps.python.org/pep-0621/"). See [Basic setup.py](#basic-setup-py "#basic-setup-py").

It is, however, possible to distribute the generated `.c` files together with
your Cython sources, so that users can install your module without needing
to have Cython available.

Doing so allows you to make Cython compilation optional in the
version you distribute. Even if the user has Cython installed, they may not
want to use it just to install your module. Also, the installed version
may not be the same one you used, and may not compile your sources correctly.

This simply means that the `setup.py` file that you ship with will just
be a normal setuptools file on the generated .c files, for the basic example
we would have instead:

```
from setuptools import Extension, setup

setup(
    ext_modules = [Extension("example", ["example.c"])]
)
```

This is easy to combine with `cythonize()` by changing the file extension
of the extension module sources:

```
from setuptools import Extension, setup

USE_CYTHON = ...   # command line option, try-import, ...

ext = '.pyx' if USE_CYTHON else '.c'

extensions = [Extension("example", ["example"+ext])]

if USE_CYTHON:
    from Cython.Build import cythonize
    extensions = cythonize(extensions)

setup(
    ext_modules = extensions
)
```

If you have many extensions and want to avoid the additional complexity in the
declarations, you can declare them with their normal Cython sources and then
call the following function instead of `cythonize()` to adapt the sources
list in the [`Extension`](https://setuptools.pypa.io/en/latest/userguide/ext_modules.html#setuptools.Extension "(in setuptools v80.9.0)")s when not using Cython:

```
import os.path

def no_cythonize(extensions, **_ignore):
    for extension in extensions:
        sources = []
        for sfile in extension.sources:
            path, ext = os.path.splitext(sfile)
            if ext in ('.pyx', '.py'):
                if extension.language == 'c++':
                    ext = '.cpp'
                else:
                    ext = '.c'
                sfile = path + ext
            sources.append(sfile)
        extension.sources[:] = sources
    return extensions
```

If you want to expose the C-level interface of your library for other
libraries to cimport from, use package\_data to install the `.pxd` files,
e.g.:

```
setup(
    package_data = {
        'my_package': ['*.pxd'],
        'my_package/sub_package': ['*.pxd'],
    },
    ...
)
```

These `.pxd` files need not have corresponding `.pyx`
modules if they contain purely declarations of external libraries.

## Shared utility module[¶](#shared-utility-module "Link to this heading")

When a `.pyx`/`.py` file is compiled to `.c` file, Cython automatically embeds
internal utility code into the resulting `.c` file. For projects containing multiple
Cython modules, this can result in a larger total size of compiled extensions.
To avoid redundant code, the common utility code can be extracted into a separate extension
module which is automatically cimported and used by the user-written extension modules.

Note

Currently, only memoryview utility code can be moved to the shared utility module.

Consider the following example package:

```
mypkg/
+-- __init__.py
+-- shared/
|   +-- __init__.py
|   +-- _cyutility.c
+-- subpkg1/
    +-- __init__.py
    +-- module.pyx
```

The `_cyutility.c` file contains the shared utility code and `module.pyx` is
a standard Cython source file which will be compiled into an extension cimporting the
`mypkg.shared._cyutility` module (automatically).
The compilation process now consist of three steps:

1. Generating the shared utility code. This is done via the `--generate-shared` argument:

   ```
   $ cython --generate-shared=mypkg/shared/_cyutility.c
   ```
2. Translating all `.pyx` files to `.c` files with the `--shared` argument to provide
   the fully qualified name of the shared module:

   ```
   $ cython --shared=mypkg.shared._cyutility module.pyx
   ```
3. Compiling the shared utility module and all other (user defined) extension modules.
   The shared utility module needs to be compiled as regular `.c` extension module,
   either by using the C compiler directly, or through setuptools, etc.

Warning

An extension module compiled with the `--shared=...` argument automatically
imports the shared module under the fully qualified name provided via the
argument parameter. Failing to import the shared module will cause a failure
to import the extension module that uses it.

### Compiling shared module using setuptools[¶](#compiling-shared-module-using-setuptools "Link to this heading")

If `setuptools` is used in the build process, the fully qualified module name
of the shared utility module can be specified using the `shared_utility_qualified_name`
parameter of `cythonize()` (instead of the `--shared` command line argument).
To generate the extension sources of the shared module from `cythonize()`,
you need to explicitly pass an `Extension` object describing the module.
The `setup.py` file would be:

setup.py[¶](#id17 "Link to this code")

```
from Cython.Build import cythonize
from Cython.Compiler import Options
from setuptools import setup, Extension

extensions = [
    Extension("*", ["**/*.pyx"]),
    # Providing 'sources' is optional for the shared module.
    # If missing, the module package will be used for the path in 'build_dir'.
    Extension("mypkg.shared._cyutility", sources=["mypkg/shared/_cyutility.c"]),
]

setup(
  ext_modules = cythonize(extensions, shared_utility_qualified_name = 'mypkg.shared._cyutility')
)
```

## Integrating multiple modules[¶](#integrating-multiple-modules "Link to this heading")

In some scenarios, it can be useful to link multiple Cython modules
(or other extension modules) into a single binary, e.g. when embedding
Python in another application. This can be done through the inittab
import mechanism of CPython.

Create a new C file to integrate the extension modules and add this
macro to it:

```
#if PY_MAJOR_VERSION < 3
# define MODINIT(name)  init ## name
#else
# define MODINIT(name)  PyInit_ ## name
#endif
```

If you are only targeting Python 3.x, just use `PyInit_` as prefix.

Then, for each of the modules, declare its module init function
as follows, replacing `some_module_name` with the name of the module:

```
PyMODINIT_FUNC  MODINIT(some_module_name) (void);
```

In C++, declare them as `extern C`.

If you are not sure of the name of the module init function, refer
to your generated module source file and look for a function name
starting with `PyInit_`.

Next, before you start the Python runtime from your application code
with [`Py_Initialize()`](https://docs.python.org/3/c-api/init.html#c.Py_Initialize "(in Python v3.14)"), you need to initialise the modules at runtime
using the [`PyImport_AppendInittab()`](https://docs.python.org/3/c-api/import.html#c.PyImport_AppendInittab "(in Python v3.14)") C-API function, again inserting
the name of each of the modules:

```
PyImport_AppendInittab("some_module_name", MODINIT(some_module_name));
```

This enables normal imports for the embedded extension modules.

In order to prevent the joined binary from exporting all of the module
init functions as public symbols, Cython 0.28 and later can hide these
symbols if the macro `CYTHON_NO_PYINIT_EXPORT` is defined while
C-compiling the module C files.

Also take a look at the [cython\_freeze](https://github.com/cython/cython/blob/master/bin/cython_freeze "https://github.com/cython/cython/blob/master/bin/cython_freeze") tool.
It can generate the necessary boilerplate code for linking one or more
modules into a single Python executable.

## Compiling with `pyximport`[¶](#compiling-with-pyximport "Link to this heading")

For building Cython modules during development without explicitly
running `setup.py` after each change, you can use `pyximport`:

```
>>> import pyximport; pyximport.install()
>>> import helloworld
Hello World
```

This allows you to automatically run Cython on every `.pyx` that
Python is trying to import. You should use this for simple Cython
builds only where no extra C libraries and no special building setup
is needed.

It is also possible to compile new `.py` modules that are being
imported (including the standard library and installed packages). For
using this feature, just tell that to `pyximport`:

```
>>> pyximport.install(pyimport=True)
```

In the case that Cython fails to compile a Python module, `pyximport`
will fall back to loading the source modules instead.

Note that it is not recommended to let `pyximport` build code
on end user side as it hooks into their import system. The best way
to cater for end users is to provide pre-built binary packages in the
[wheel](https://wheel.readthedocs.io/en/latest/index.html "(in wheel v0.46.1)") packaging format.

### Arguments[¶](#arguments "Link to this heading")

The function [`pyximport.install()`](#pyximport.install "pyximport.install") can take several arguments to
influence the compilation of Cython or Python files.

pyximport.install(pyximport=True, pyimport=False, build\_dir=None, build\_in\_temp=True, setup\_args=None, reload\_support=False, load\_py\_module\_on\_import\_failure=False, inplace=False, language\_level=None)[¶](#pyximport.install "Link to this definition")

Main entry point for pyxinstall.

Call this to install the `.pyx` import hook in
your meta-path for a single Python process. If you want it to be
installed whenever you use Python, add it to your `sitecustomize`
(as described above).

Parameters:

* pyximport – If set to False, does not try to import `.pyx` files.
* pyimport – You can pass `pyimport=True` to also
  install the `.py` import hook
  in your meta-path. Note, however, that it is rather experimental,
  will not work at all for some `.py` files and packages, and will
  heavily slow down your imports due to search and compilation.
  Use at your own risk.
* build\_dir – By default, compiled modules will end up in a `.pyxbld`
  directory in the user’s home directory. Passing a different path
  as `build_dir` will override this.
* build\_in\_temp – If `False`, will produce the C files locally. Working
  with complex dependencies and debugging becomes more easy. This
  can principally interfere with existing files of the same name.
* setup\_args – Dict of arguments for Distribution.
  See `distutils.core.setup()`.
* reload\_support – Enables support for dynamic
  `reload(my_module)`, e.g. after a change in the Cython code.
  Additional files `<so_path>.reloadNN` may arise on that account, when
  the previously loaded module file cannot be overwritten.
* load\_py\_module\_on\_import\_failure – If the compilation of a `.py`
  file succeeds, but the subsequent import fails for some reason,
  retry the import with the normal `.py` module instead of the
  compiled module. Note that this may lead to unpredictable results
  for modules that change the system state during their import, as
  the second import will rerun these modifications in whatever state
  the system was left after the import of the compiled module
  failed.
* inplace – Install the compiled module
  (`.so` for Linux and Mac / `.pyd` for Windows)
  next to the source file.
* language\_level – The source language level to use: 2 or 3.
  The default is to use the language level of the current Python
  runtime for .py files and Py2 for `.pyx` files.

### Dependency Handling[¶](#dependency-handling "Link to this heading")

Since `pyximport` does not use `cythonize()` internally, it currently
requires a different setup for dependencies. It is possible to declare that
your module depends on multiple files, (likely `.h` and `.pxd` files).
If your Cython module is named `foo` and thus has the filename
`foo.pyx` then you should create another file in the same directory
called `foo.pyxdep`. The `modname.pyxdep` file can be a list of
filenames or “globs” (like `*.pxd` or `include/*.h`). Each filename or
glob must be on a separate line. Pyximport will check the file date for each
of those files before deciding whether to rebuild the module. In order to
keep track of the fact that the dependency has been handled, Pyximport updates
the modification time of your “.pyx” source file. Future versions may do
something more sophisticated like informing setuptools of the dependencies
directly.

### Limitations[¶](#limitations "Link to this heading")

`pyximport` does not use `cythonize()`. Thus it is not
possible to do things like using compiler directives at
the top of Cython files or compiling Cython code to C++.

Pyximport does not give you any control over how your Cython file is
compiled. Usually the defaults are fine. You might run into problems if
you wanted to write your program in half-C, half-Cython and build them
into a single library.

Pyximport does not hide the setuptools/GCC warnings and errors generated
by the import process. Arguably this will give you better feedback if
something went wrong and why. And if nothing went wrong it will give you
the warm fuzzy feeling that pyximport really did rebuild your module as it
was supposed to.

Basic module reloading support is available with the option `reload_support=True`.
Note that this will generate a new module filename for each build and thus
end up loading multiple shared libraries into memory over time. CPython has limited
support for reloading shared libraries as such,
see [PEP 489](https://peps.python.org/pep-0489/ "https://peps.python.org/pep-0489/").

Pyximport puts both your `.c` file and the platform-specific binary into
a separate build directory, usually `$HOME/.pyxblx/`. To copy it back
into the package hierarchy (usually next to the source file) for manual
reuse, you can pass the option `inplace=True`.

## Compiling with `cython.inline`[¶](#compiling-with-cython-inline "Link to this heading")

One can also compile Cython in a fashion similar to SciPy’s `weave.inline`.
For example:

```
>>> import cython
>>> def f(a):
...     ret = cython.inline("return a+b", b=3)
...
```

Unbound variables are automatically pulled from the surrounding local
and global scopes, and the result of the compilation is cached for
efficient reuse.

## Compiling with `cython.compile`[¶](#compiling-with-cython-compile "Link to this heading")

Cython supports transparent compiling of the cython code in a function using the
`@cython.compile` decorator:

```
@cython.compile
def plus(a, b):
    return a + b
```

Parameters of the decorated function cannot have type declarations. Their types are
automatically determined from values passed to the function, thus leading to one or more
specialised compiled functions for the respective argument types.
Executing example:

```
import cython

@cython.compile
def plus(a, b):
    return a + b

print(plus('3', '5'))
print(plus(3, 5))
```

will produce following output:

```
35
8
```

## Compiling with Sage[¶](#compiling-with-sage "Link to this heading")

The Sage notebook allows transparently editing and compiling Cython
code simply by typing `%cython` at the top of a cell and evaluate
it. Variables and functions defined in a Cython cell are imported into the
running session. Please check [Sage documentation](https://www.sagemath.org/doc/ "https://www.sagemath.org/doc/") for details.

You can tailor the behavior of the Cython compiler by specifying the
directives below.

## Compiling with a Jupyter Notebook[¶](#compiling-with-a-jupyter-notebook "Link to this heading")

It’s possible to compile code in a notebook cell with Cython.
For this you need to load the Cython magic:

```
%load_ext cython
```

Then you can define a Cython cell by writing `%%cython` on top of it.
Like this:

```
%%cython

cdef int a = 0
for i in range(10):
    a += i
print(a)
```

Note that each cell will be compiled into a separate extension module. So if you use a package in a Cython
cell, you will have to import this package in the same cell. It’s not enough to
have imported the package in a previous cell. Cython will tell you that there are
“undefined global names” at compilation time if you don’t comply.

The global names (top level functions, classes, variables and modules) of the
cell are then loaded into the global namespace of the notebook. So in the
end, it behaves as if you executed a Python cell.

Additional allowable arguments to the Cython magic are listed below.
You can see them also by typing `` `%%cython? `` in IPython or a Jupyter notebook.

 -a, –annotate  Produce a colorized HTML version of the source.  –annotate-fullc  Produce a colorized HTML version of the source which includes entire generated C/C++-code.  -+, –cplus  Output a C++ rather than C file.  -f, –force  Force the compilation of a new module, even if the source has been previously compiled.  -3  Select Python 3 syntax  -2  Select Python 2 syntax  -c=COMPILE\_ARGS, –compile-args=COMPILE\_ARGS  Extra flags to pass to compiler via the extra\_compile\_args.  –link-args LINK\_ARGS  Extra flags to pass to linker via the extra\_link\_args.  -l LIB, –lib LIB  Add a library to link the extension against (can be specified multiple times).  -L dir  Add a path to the list of library directories (can be specified multiple times).  -I INCLUDE, –include INCLUDE  Add a path to the list of include directories (can be specified multiple times).  -S, –src  Add a path to the list of src files (can be specified multiple times).  -n NAME, –name NAME  Specify a name for the Cython module.  –pgo  Enable profile guided optimisation in the C compiler. Compiles the cell twice and executes it in between to generate a runtime profile.  –verbose  Print debug information like generated .c/.cpp file location and exact gcc/g++ command invoked. 

## Cython cache[¶](#cython-cache "Link to this heading")

The Cython cache is used to store cythonized `.c`/`.cpp` files to avoid running the Cython compiler on the files which were cythonized before.

Note

Only `.c`/`.cpp` files are cached. The C compiler is run every time. To avoid executing C compiler a tool like ccache needs to be used.

The Cython cache is disabled by default but can be enabled by the `cache` parameter of `cythonize()`:

```
from setuptools import setup, Extension
from Cython.Build import cythonize

extensions = [
    Extension("*", ["lib.pyx"]),
]

setup(
    name="hello",
    ext_modules=cythonize(extensions, cache=True)
)
```

The cached files are searched in the following paths by default in the following order:

1. path specified in the `CYTHON_CACHE_DIR` environment variable,
2. `~/Library/Caches/Cython` on MacOS and `$XDG_CACHE_HOME/cython` on POSIX if the `XDG_CACHE_HOME` environment variable is defined,
3. otherwise `~/.cython`.

## Compiler options[¶](#compiler-options "Link to this heading")

Compiler options can be set in the `setup.py`, before calling `cythonize()`,
like this:

```
from setuptools import setup

from Cython.Build import cythonize
from Cython.Compiler import Options

Options.docstrings = False

setup(
    name = "hello",
    ext_modules = cythonize("lib.pyx"),
)
```

Here are the options that are available:

Cython.Compiler.Options.docstrings = True[¶](#Cython.Compiler.Options.docstrings "Link to this definition")

Whether or not to include docstring in the Python extension. If False, the binary size
will be smaller, but the `__doc__` attribute of any class or function will be an
empty string.

Cython.Compiler.Options.embed\_pos\_in\_docstring = False[¶](#Cython.Compiler.Options.embed_pos_in_docstring "Link to this definition")

Embed the source code position in the docstrings of functions and classes.

Cython.Compiler.Options.generate\_cleanup\_code = False[¶](#Cython.Compiler.Options.generate_cleanup_code "Link to this definition")

Decref global variables in each module on exit for garbage collection.
0: None, 1+: interned objects, 2+: cdef globals, 3+: types objects
Mostly for reducing noise in Valgrind as it typically executes at process exit
(when all memory will be reclaimed anyways).
Note that directly or indirectly executed cleanup code that makes use of global
variables or types may no longer be safe when enabling the respective level since
there is no guaranteed order in which the (reference counted) objects will
be cleaned up. The order can change due to live references and reference cycles.

Cython.Compiler.Options.clear\_to\_none = True[¶](#Cython.Compiler.Options.clear_to_none "Link to this definition")

Should tp\_clear() set object fields to None instead of clearing them to NULL?

Cython.Compiler.Options.annotate = False[¶](#Cython.Compiler.Options.annotate "Link to this definition")

Generate an annotated HTML version of the input source files for debugging and optimisation purposes.
This has the same effect as the `annotate` argument in `cythonize()`.

Cython.Compiler.Options.fast\_fail = False[¶](#Cython.Compiler.Options.fast_fail "Link to this definition")

This will abort the compilation on the first error occurred rather than trying
to keep going and printing further error messages.

Cython.Compiler.Options.warning\_errors = False[¶](#Cython.Compiler.Options.warning_errors "Link to this definition")

Turn all warnings into errors.

Cython.Compiler.Options.error\_on\_unknown\_names = True[¶](#Cython.Compiler.Options.error_on_unknown_names "Link to this definition")

Make unknown names an error. Python raises a NameError when
encountering unknown names at runtime, whereas this option makes
them a compile time error. If you want full Python compatibility,
you should disable this option and also ‘cache\_builtins’.

Cython.Compiler.Options.error\_on\_uninitialized = True[¶](#Cython.Compiler.Options.error_on_uninitialized "Link to this definition")

Make uninitialized local variable reference a compile time error.
Python raises UnboundLocalError at runtime, whereas this option makes
them a compile time error. Note that this option affects only variables
of “python object” type.

Cython.Compiler.Options.convert\_range = True[¶](#Cython.Compiler.Options.convert_range "Link to this definition")

This will convert statements of the form `for i in range(...)`
to `for i from ...` when `i` is a C integer type, and the direction
(i.e. sign of step) can be determined.
WARNING: This may change the semantics if the range causes assignment to
i to overflow. Specifically, if this option is set, an error will be
raised before the loop is entered, whereas without this option the loop
will execute until an overflowing value is encountered.

Cython.Compiler.Options.cache\_builtins = True[¶](#Cython.Compiler.Options.cache_builtins "Link to this definition")

Perform lookups on builtin names only once, at module initialisation
time. This will prevent the module from getting imported if a
builtin name that it uses cannot be found during initialisation.
Default is True.
Note that some legacy builtins are automatically remapped
from their Python 2 names to their Python 3 names by Cython
when building in Python 3.x,
so that they do not get in the way even if this option is enabled.

Cython.Compiler.Options.gcc\_branch\_hints = True[¶](#Cython.Compiler.Options.gcc_branch_hints "Link to this definition")

Generate branch prediction hints to speed up error handling etc.

Cython.Compiler.Options.lookup\_module\_cpdef = False[¶](#Cython.Compiler.Options.lookup_module_cpdef "Link to this definition")

Enable this to allow one to write `your_module.foo = ...` to overwrite the
definition of the cpdef function foo, at the cost of an extra dictionary
lookup on every call.
If this is false it generates only the Python wrapper and no override check.

Cython.Compiler.Options.embed = None[¶](#Cython.Compiler.Options.embed "Link to this definition")

Whether or not to embed the Python interpreter, for use in making a
standalone executable or calling from external libraries.
This will provide a C function which initialises the interpreter and
executes the body of this module.
See [this demo](https://github.com/cython/cython/tree/master/Demos/embed "https://github.com/cython/cython/tree/master/Demos/embed")
for a concrete example.
If true, the initialisation function is the C main() function, but
this option can also be set to a non-empty string to provide a function name explicitly.
Default is False.

Cython.Compiler.Options.cimport\_from\_pyx = False[¶](#Cython.Compiler.Options.cimport_from_pyx "Link to this definition")

Allows cimporting from a pyx file without a pxd file.

Cython.Compiler.Options.buffer\_max\_dims = 8[¶](#Cython.Compiler.Options.buffer_max_dims "Link to this definition")

Maximum number of dimensions for buffers – set lower than number of
dimensions in numpy, as
slices are passed by value and involve a lot of copying.

Cython.Compiler.Options.closure\_freelist\_size = 8[¶](#Cython.Compiler.Options.closure_freelist_size "Link to this definition")

Number of function closure instances to keep in a freelist (0: no freelists)

## Compiler directives[¶](#compiler-directives "Link to this heading")

Compiler directives are instructions which affect the behavior of
Cython code. Here is the list of currently supported directives:

`binding` (True / False), default=True

Controls whether free functions behave more like Python’s CFunctions
(e.g. [`len()`](https://docs.python.org/3/library/functions.html#len "(in Python v3.14)")) or, when set to True, more like Python’s functions.
When enabled, functions will bind to an instance when looked up as a
class attribute (hence the name) and will emulate the attributes
of Python functions, including introspections like argument names and
annotations.

Changed in version 3.0.0: Default changed from False to True

`boundscheck` (True / False), default=True

If set to False, Cython is free to assume that indexing operations
([]-operator) in the code will not cause any IndexErrors to be
raised. Lists, tuples, and strings are affected only if the index
can be determined to be non-negative (or if `wraparound` is False).
Conditions which would normally trigger an IndexError may instead cause
segfaults or data corruption if this is set to False.

`wraparound` (True / False), default=True

In Python, arrays and sequences can be indexed relative to the end.
For example, A[-1] indexes the last value of a list.
In C, negative indexing is not supported.
If set to False, Cython is allowed to neither check for nor correctly
handle negative indices, possibly causing segfaults or data corruption.
If bounds checks are enabled (the default, see `boundschecks` above),
negative indexing will usually raise an `IndexError` for indices that
Cython evaluates itself.
However, these cases can be difficult to recognise in user code to
distinguish them from indexing or slicing that is evaluated by the
underlying Python array or sequence object and thus continues to support
wrap-around indices.
It is therefore safest to apply this option only to code that does not
process negative indices at all.

`initializedcheck` (True / False), default=TrueIf set to True, Cython checks that

* a memoryview is initialized whenever its elements are accessed
  or assigned to.
* a C++ class is initialized when it is accessed
  (only when `cpp_locals` is on)

Setting this to False disables these checks.

`nonecheck` (True / False), default=False

If set to False, Cython is free to assume that native field
accesses on variables typed as an extension type, or buffer
accesses on a buffer variable, never occurs when the variable is
set to `None`. Otherwise a check is inserted and the
appropriate exception is raised. This is off by default for
performance reasons.

`freethreading_compatible` (True / False), default=False

If set to True, Cython sets the `Py_mod_gil` slot to
`Py_MOD_GIL_NOT_USED` to signal that the module is safe to run
without an active GIL and prevent the GIL from being enabled
when the module is imported. Otherwise the slot is set to
`Py_MOD_GIL_USED` which will cause the GIL to be automatically
enabled. Setting this to True does not itself make the module safe
to run without the GIL; it merely confirms that you have checked
the logic and consider it safe to run. Since free-threading support
is still experimental itself, this is also an experimental directive that
might be changed or removed in future releases.

`subinterpreters_compatible` (no / shared\_gil / own\_gil), default=no

If set to `shared_gil` or `own_gil`, then Cython sets the
`Py_mod_multiple_interpreters` slot to `Py_MOD_MULTIPLE_INTERPRETERS_SUPPORTED`
or `Py_MOD_PER_INTERPRETER_GIL_SUPPORTED` respectively to signal that
the module is safe to run in isolated subinterpreters. Setting this option
does not itself make the module safe to run in isolated subinterpreters;
it merely confirms that you have checked the logic and consider it safe to run.
Currently `cdef` global variables (especially when the type is a Python object) and
acquiring the GIL (but not re-acquiring the GIL) are known not to work
correctly and will generate warnings at compile time.

`overflowcheck` (True / False), default=False

If set to True, raise errors on overflowing C integer arithmetic
operations. Incurs a modest runtime penalty, but is much faster than
using Python ints.

`overflowcheck.fold` (True / False), default=True

If set to True, and overflowcheck is True, check the overflow bit for
nested, side-effect-free arithmetic expressions once rather than at every
step. Depending on the compiler, architecture, and optimization settings,
this may help or hurt performance. A simple suite of benchmarks can be
found in `Demos/overflow_perf.pyx`.

`embedsignature` (True / False), default=False

If set to True, Cython will embed a textual copy of the call
signature in the docstring of all Python visible functions and
classes. Tools like IPython and epydoc can thus display the
signature, which cannot otherwise be retrieved after
compilation.

`embedsignature.format` (`c` / `python` / `clinic`), default=”c”

If set to `c`, Cython will generate signatures preserving
C type declarations and Python type annotations.
If set to `python`, Cython will do a best attempt to use
pure-Python type annotations in embedded signatures. For arguments
without Python type annotations, the C type is mapped to the
closest Python type equivalent (e.g., C `short` is mapped to
Python `int` type and C `double` is mapped to Python `float`
type). The specific output and type mapping are experimental and
may change over time.
The `clinic` format generates signatures that are compatible
with those understood by CPython’s Argument Clinic tool. The
CPython runtime strips these signatures from docstrings and
translates them into a `__text_signature__` attribute. This is
mainly useful when using `binding=False`, since the Cython
functions generated with `binding=True` do not have (nor need)
a `__text_signature__` attribute.

`cdivision` (True / False), default=False

If set to False, Cython will adjust the remainder and quotient
operators C types to match those of Python ints (which differ when
the operands have opposite signs) and raise a
`ZeroDivisionError` when the right operand is 0. This has up to
a 35% speed penalty. If set to True, no checks are performed. See
[CEP 516](https://github.com/cython/cython/wiki/enhancements-division "https://github.com/cython/cython/wiki/enhancements-division").

`cdivision_warnings` (True / False), default=False

If set to True, Cython will emit a runtime warning whenever
division is performed with negative operands. See [CEP 516](https://github.com/cython/cython/wiki/enhancements-division "https://github.com/cython/cython/wiki/enhancements-division").

`cpow` (True / False), default=False

`cpow` modifies the return type of `a**b`, as shown in the
table below:

cpow behaviour[¶](#id18 "Link to this table")





 Type of `a`  Type of `b`  `cpow==True`  `cpow==False`  C integer  Negative integer compile-time constant  Return type is C double  Return type is C double (special case)  C integer  C integer (known to be >= 0 at compile time)  Return type is integer  Return type is integer  C integer  C integer (may be negative)  Return type is integer  Return type is C double (note that Python would dynamically pick `int` or `float` here, while Cython doesn’t)  C floating point  C integer  Return type is floating point  Return type is floating point  C floating point (or C integer)  C floating point  Return type is floating point, result is NaN if the result would be complex  Either a C real or complex number at cost of some speed

The `cpow==True` behaviour largely keeps the result type the
same as the operand types, while the `cpow==False` behaviour
follows Python and returns a flexible type depending on the
inputs.

Introduced in Cython 3.0 with a default of False;
before that, the behaviour matched the `cpow=True` version.

`always_allow_keywords` (True / False), default=True

When disabled, uses the `METH_NOARGS` and `METH_O` signatures when
constructing functions/methods which take zero or one arguments. Has no
effect on special methods and functions with more than one argument. The
`METH_NOARGS` and `METH_O` signatures provide slightly faster
calling conventions but disallow the use of keywords.

`c_api_binop_methods` (True / False), default=False

When enabled, makes the special binary operator methods (`__add__`, etc.)
behave according to the low-level C-API slot semantics, i.e. only a single
method implements both the normal and reversed operator. This used to be
the default in Cython 0.x and was now replaced by Python semantics, i.e. the
default in Cython 3.x and later is `False`.

`profile` (True / False), default=False

Write hooks for Python profilers into the compiled C code.
Whether the generated module actually uses profiling depends on
the value of the C macro `CYTHON_PROFILE` which is `1` by
default but which you can optionally set to `0` to turn off the
profiling code at C compile-time. Define `CYTHON_USE_SYS_MONITORING`
to either 1 or 0 to control the mechanism used to implement profiling
on Python 3.13 and above. Note that neither `profile`
nor `linetrace` work with any tool that uses `sys.monitoring`
on Python 3.12.

`linetrace` (True / False), default=False

Write line tracing hooks for Python profilers or coverage reporting
into the compiled C code. This also enables profiling.
Note that the generated module will not actually use line
tracing, unless you additionally pass the C macro definition
`CYTHON_TRACE=1` to the C compiler (e.g. using the setuptools option
`define_macros`). Define `CYTHON_TRACE_NOGIL=1` to also include
`nogil` functions and sections. Define `CYTHON_USE_SYS_MONITORING`
to either 1 or 0 to control the mechanism used to implement these
features on Python 3.13 and above. Note that neither `profile`
nor `linetrace` work with any tool that uses `sys.monitoring`
on Python 3.12.

`infer_types` (True / False), default=None

Infer types of untyped variables in function bodies. Default is
None, indicating that only safe (semantically-unchanging) inferences
are allowed.
In particular, inferring integral types for variables used in arithmetic
expressions is considered unsafe (due to possible overflow) and must be
explicitly requested.

`language_level` (2/3/3str), default=None

Globally set the Python language level to be used for module compilation.
Default is None, indicating compatibility with Python 3 in Cython 3.x and with Python 2
in Cython 0.x. To enable Python 3 source code semantics, set this to 3 (or 3str) at the start
of a module or pass the “-3” or “–3str” command line options to the
compiler. For Python 2 semantics, use 2 and “-2” accordingly.
Before Cython 3.1, the `3str` option enabled Python 3 semantics but did
not change the `str` type and unprefixed string literals to
`unicode` when the compiled code runs in Python 2.x.
In Cython 3.1, `3str` is an alias for `3`.
Language level 2 ignores `x: int` type annotations due to the int/long ambiguity.
Note that cimported files inherit this setting from the module
being compiled, unless they explicitly set their own language level.
Included source files always inherit this setting.

`c_string_type` (bytes / str / unicode), default=bytes

Globally set the type of an implicit coercion from char\* or std::string.

`c_string_encoding` (ascii, default, utf-8, etc.), default=””

Globally set the encoding to use when implicitly coercing char\* or std:string
to a unicode object. Coercion from a unicode object to C type is only allowed
when set to `ascii` or `default`, the latter being utf-8 in Python 3 and
nearly-always ascii in Python 2.

`type_version_tag` (True / False), default=True

Enables the attribute cache for extension types in CPython by setting the
type flag `Py_TPFLAGS_HAVE_VERSION_TAG`. Default is True, meaning that
the cache is enabled for Cython implemented types. To disable it
explicitly in the rare cases where a type needs to juggle with its `tp_dict`
internally without paying attention to cache consistency, this option can
be set to False. Note that this no longer applies to Python 3.11 and later.

`unraisable_tracebacks` (True / False), default=False

Whether to print tracebacks when suppressing unraisable exceptions.

`iterable_coroutine` (True / False), default=False

[PEP 492](https://peps.python.org/pep-0492/ "https://peps.python.org/pep-0492/") specifies that async-def
coroutines must not be iterable, in order to prevent accidental misuse in
non-async contexts. However, this makes it difficult and inefficient to write
backwards compatible code that uses async-def coroutines in Cython but needs to
interact with async Python code that uses the older yield-from syntax, such as
asyncio before Python 3.5. This directive can be applied in modules or
selectively as decorator on an async-def coroutine to make the affected
coroutine(s) iterable and thus directly interoperable with yield-from.

`annotation_typing` (True / False), default=True

Uses function argument annotations to determine the type of variables.
Since Python does not enforce types given in
annotations, setting to False gives greater compatibility with Python code.
From Cython 3.0, `annotation_typing` can be set on a per-function or
per-class basis.

`emit_code_comments` (True / False), default=True

Copy the original source code line by line into C code comments in the generated
code file to help with understanding the output.
This is also required for coverage analysis.

`cpp_locals` (True / False), default=False

Make C++ variables behave more like Python variables by allowing them to be
“unbound” instead of always default-constructing them at the start of a
function. See [cpp\_locals directive](wrapping_CPlusPlus.html#cpp-locals-directive "wrapping_CPlusPlus.html#cpp-locals-directive") for more detail.

`legacy_implicit_noexcept` (True / False), default=False

When enabled, `cdef` functions will not propagate raised exceptions by default. Hence,
the function will behave in the same way as if declared with noexcept keyword. See
[Error return values](language_basics.html#error-return-values "language_basics.html#error-return-values") for details. Setting this directive to `True` will
cause Cython 3.0 to have the same semantics as Cython 0.x. This directive was solely added
to help migrate legacy code written before Cython 3. It will be removed in a future release.

### Configurable optimisations[¶](#configurable-optimisations "Link to this heading")

`optimize.use_switch` (True / False), default=True

Whether to expand chained if-else statements (including statements like
`if x == 1 or x == 2:`) into C switch statements. This can have performance
benefits if there are lots of values but cause compiler errors if there are any
duplicate values (which may not be detectable at Cython compile time for all
C constants).

`optimize.unpack_method_calls` (True / False), default=True

Cython can generate code that optimistically checks for Python method objects
at call time and unpacks the underlying function to call it directly. This
can substantially speed up method calls, especially for builtins, but may also
have a slight negative performance impact in some cases where the guess goes
completely wrong.
Disabling this option can also reduce the code size.

### Warnings[¶](#warnings "Link to this heading")

All warning directives take True / False as options
to turn the warning on / off.

`warn.undeclared` (default False)

Warns about any variables that are implicitly declared without a `cdef` declaration

`warn.unreachable` (default True)

Warns about code paths that are statically determined to be unreachable, e.g.
returning twice unconditionally.

`warn.maybe_uninitialized` (default False)

Warns about use of variables that are conditionally uninitialized.

`warn.unused` (default False)

Warns about unused variables and declarations

`warn.unused_arg` (default False)

Warns about unused function arguments

`warn.unused_result` (default False)

Warns about unused assignment to the same name, such as
`r = 2; r = 1 + 2`

`warn.multiple_declarators` (default True)

Warns about multiple variables declared on the same line with at least one pointer type.
For example `cdef double* a, b` - which, as in C, declares `a` as a pointer, `b` as
a value type, but could be mininterpreted as declaring two pointers.

`warn.deprecated.DEF` (default False)

Warns about use of the deprecated `DEF` statement in Cython code, see
[Conditional Compilation](language_basics.html#conditional-compilation "language_basics.html#conditional-compilation") and [Deprecation of DEF / IF](migrating_to_cy30.html#deprecated-def-if "migrating_to_cy30.html#deprecated-def-if").

`warn.deprecated.IF` (default True)

Warns about use of the deprecated `IF` statement in Cython code, see
[Conditional Compilation](language_basics.html#conditional-compilation "language_basics.html#conditional-compilation") and [Deprecation of DEF / IF](migrating_to_cy30.html#deprecated-def-if "migrating_to_cy30.html#deprecated-def-if").

`show_performance_hints` (default True)

Show performance hints during compilation pointing to places in the code which can yield performance degradation.
Note that performance hints are not warnings and hence the directives starting with `warn.` above do not affect them
and they will not trigger a failure when “error on warnings” is enabled.

### How to set directives[¶](#how-to-set-directives "Link to this heading")

#### Globally[¶](#globally "Link to this heading")

One can set compiler directives through a special header comment near the top of the file, like this:

```
# cython: language_level=3, boundscheck=False
```

The comment must appear before any code (but can appear after other
comments or whitespace).

One can also pass a directive on the command line by using the -X switch:

```
$ cython -X boundscheck=True ...
```

Directives passed on the command line will override directives set in
header comments.

#### Locally[¶](#locally "Link to this heading")

For local blocks, you need to cimport the special builtin `cython`
module:

```
#!python
cimport cython
```

Then you can use the directives either as decorators or in a with
statement, like this:

```
#!python
@cython.boundscheck(False) # turn off boundscheck for this function
def f():
    ...
    # turn it temporarily on again for this block
    with cython.boundscheck(True):
        ...
```

Warning

These two methods of setting directives are not
affected by overriding the directive on the command-line using the
-X option.

#### In `setup.py`[¶](#in-setup-py "Link to this heading")

Compiler directives can also be set in the `setup.py` file by passing a keyword
argument to `cythonize`:

```
from setuptools import setup
from Cython.Build import cythonize

setup(
    name="My hello app",
    ext_modules=cythonize('hello.pyx', compiler_directives={'embedsignature': True}),
)
```

This will override the default directives as specified in the `compiler_directives` dictionary.
Note that explicit per-file or local directives as explained above take precedence over the
values passed to `cythonize`.

## C line numbers in tracebacks[¶](#c-line-numbers-in-tracebacks "Link to this heading")

To provide more detailed debug information, Python tracebacks of Cython modules
show the C line where the exception originated (or was propagated). This feature is not
entirely for free and can visibly increase the C compile time as well as adding 0-5% to the
size of the binary extension module. It is therefore disabled in Cython 3.1 and can be controlled using C macros.

* `CYTHON_CLINE_IN_TRACEBACK=1` always shows the C line number in tracebacks,
* `CYTHON_CLINE_IN_TRACEBACK=0` never shows the C line number in tracebacks,

Unless the feature is disabled completely with this macro, there is also support for enabling and disabling
the feature at runtime, at the before mentioned cost of longer C compile times and larger extension modules.
This can be configured with the C macro

`CYTHON_CLINE_IN_TRACEBACK_RUNTIME=1`

To then change the behaviour at runtime, you can import the special module `cython_runtime`
after loading a Cython module and set the attribute `cline_in_traceback` in that module
to either true or false to control the behaviour as your Cython code is being run:

```
import cython_runtime
cython_runtime.cline_in_traceback = True

raise ValueError(5)
```

If both macros are not defined by the build setup or `CFLAGS`, the feature is disabled.

In Cython 3.0 and earlier, the Cython compiler option `c_line_in_traceback` (passed as
an argument to `cythonize` in `setup.py`) or the command
line argument `--no-c-in-traceback` could also be used to disable this feature.
From Cython 3.1, this is still possible, but should be migrated to using the C macros instead.
Before Cython 3.1, the `CYTHON_CLINE_IN_TRACEBACK` macro already works as described
but the Cython option is needed to remove the compile-time cost.

## C macro defines[¶](#c-macro-defines "Link to this heading")

Cython has a number of C macros that can be used to control compilation. Typically, these
would be set using `extra_compile_args` in setup.py (for example
`extra_compile_args=['-DCYTHON_USE_TYPE_SPECS=1']`), however they can also be set in
other ways like using the `CFLAGS` environmental variable.

These macros are set automatically by Cython to sensible default values unless
you chose to explicitly override them, so they are a tool that most users
can happily ignore. Not all combinations of macros are compatible or tested, and
some change the default value of other macros. They are listed below in rough order from
most important to least important:

`Py_LIMITED_API`

Turns on Cython’s Limited API support, meaning that one compiled module
can be used by many Python interpreter versions (at the cost of some performance).
At this stage many features do not work in the Limited API. You should set this
macro to be the version hex for the
minimum Python version you want to support (>=3.8). `0x03080000` will support
Python 3.8 upwards.
Note that this is a [`Python macro`](https://docs.python.org/3/c-api/stable.html#c.Py_LIMITED_API "(in Python v3.14)"),
rather than just a Cython macro, and so it changes what parts of the Python headers
are visible too. See [The Limited API and Stable ABI](limited_api.html#limited-api "limited_api.html#limited-api") for more details about this feature.

`CYTHON_PEP489_MULTI_PHASE_INIT`

Uses multi-phase module initialization as described in [PEP 489](https://peps.python.org/pep-0489/ "https://peps.python.org/pep-0489/"). This improves
Python compatibility, especially when running the initial import of the code when it
makes attributes such as `__file__` available. It is therefore on by default
where supported.

`CYTHON_USE_MODULE_STATE`

Stores module data on a struct associated with the module object rather than as
C global variables. The advantage is that it should be possible to import the
same module more than once (e.g. in different sub-interpreters). At the moment
this is experimental and not all data has been moved. Specifically, `cdef`
globals have not been moved.

`CYTHON_USE_TYPE_SPECS`

Defines `cdef class`es as [Heap Types](https://docs.python.org/3/c-api/typeobj.html#heap-types "(in Python v3.14)") rather than
“static types”. Practically this does not change a lot from a user
point of view, but it is needed to implement Limited API support.

`CYTHON_PROFILE`, `CYTHON_TRACE`, `CYTHON_TRACE_NOGIL`

These control the inclusion of profiling and line tracing calls in the module.
See the `profile` and `linetrace` [Compiler directives](#compiler-directives "#compiler-directives").
`CYTHON_PROFILE` is on by default; the `CYTHON_TRACE` macros are
off by default.

`CYTHON_USE_SYS_MONITORING`

On Python 3.13+ this selects the new [sys.monitoring](https://docs.python.org/3/library/sys.monitoring.html "https://docs.python.org/3/library/sys.monitoring.html")
mechanism for profiling and linetracing. It is on by default, but can be set to 0
to force use of the old mechanism. Some tools still require the old mechanism,
most notably “Coverage” (as of 2025).

`CYTHON_EXTERN_C`

Slightly different to the other macros, this controls how `cdef public`
functions appear to C++ code. See [C++ public declarations](external_C_code.html#cython-extern-c "external_C_code.html#cython-extern-c") for full details.

`CYTHON_CLINE_IN_TRACEBACK`

Controls whether C lines numbers appear in tracebacks.
See [C line numbers in tracebacks](#cline-in-traceback "#cline-in-traceback") for a complete description.

`CYTHON_CCOMPLEX`

Passes complex numbers using the C or C++ language standard library types
instead of an internal type defined by Cython. Turning it on
maximizes compatibility with external libraries. However, MSVC
has poor standards support (especially in C mode) and so struggles to
use the standard library types. It is on by default on platforms
where we think it’s likely to work.

`CYTHON_COMPRESS_STRINGS`

Store Python strings in the binary module as compressed data, decompressing them
at import time. By default, `zlib` compression is used (`CYTHON_COMPRESS_STRINGS=1`).
Set to `0` to disable compression or to `2` to select `bzip2` compression.
Note that the respective standard library decompression module must be available
at module import time, or the import will fail.
`compression.zstd` can be selected with `CYTHON_COMPRESS_STRINGS=3` but is only
available in the standard library in Python 3.14 and later. Cython will then
fall back to `zlib` when compiling in older Python versions.

`CYTHON_IMMORTAL_CONSTANTS`

Makes cached constants (e.g. strings, tuples, ints, floats, slices) immortal,
in Python versions that support immortality. This is most useful when
the constants are used in many different threads because it avoids most writes
to the constants due to reference counting. Disabled by default, but enabled
in free-threaded builds.

There is a further list of macros which turn off various optimizations or language
features. Under normal circumstance Cython enables these automatically based on the
version of Python you are compiling for so there is no need to use them
to try to enable extra optimizations - all supported optimizations are enabled by
default. These are mostly relevant if you’re tying to get Cython working in a
new and unsupported Python interpreter where you will typically want to set
them to 0 to disable optimizations. They are listed below for completeness but
hidden by default since most users will be uninterested in changing them.

HideShow

`CYTHON_USE_TYPE_SLOTS`

If enabled, Cython will directly access members of the `PyTypeObject`
struct.

`CYTHON_USE_PYTYPE_LOOKUP`

Use the internal \_PyType\_Lookup() function for more efficient access
to properties of C classes.

`CYTHON_USE_PYLONG_INTERNALS`/`CYTHON_USE_PYLIST_INTERNALS`/`CYTHON_USE_UNICODE_INTERNALS`

Enable optimizations based on direct access into the internals of Python
`int`/`list`/`unicode` objects respectively.

`CYTHON_USE_UNICODE_WRITER`

Use a faster (but internal) mechanism for building unicode strings, for
example in f-strings.

`CYTHON_AVOID_BORROWED_REFS`

Avoid using “borrowed references” and ensure that Cython always holds
a reference to objects it manipulates. Most useful for
non-reference-counted implementations of Python, like PyPy
(where it is enabled by default).

`CYTHON_AVOID_THREAD_UNSAFE_BORROWED_REFS`

Avoid using APIs that return unsafe “borrowed references” and instead use
the equivalent APIs that return “strong references”. Most useful for
the free-threaded build of CPython, where incrementing the reference
count of borrowed references to items in mutable containers might
introduce thread safety issues. Borrowed references to items in immutable
containers are still allowed with this setting.

`CYTHON_ASSUME_SAFE_MACROS`

Use some C-API macros that increase performance by skipping error checking,
which may not be safe on all Python implementations (e.g. PyPy).

`CYTHON_ASSUME_SAFE_SIZE`

Prefer the `Py*_GET_SIZE()` C-API macros / inline-functions for builtin types
over their `Py*_GetSize()` counterparts if errors are not expected.

`CYTHON_FAST_GIL`

On some Python versions this speeds up getting/releasing the GIL.

`CYTHON_UNPACK_METHODS`

Try to speed up method calls at the cost of code-size. Linked to
the `optimize.unpack_method_calls` compiler directive - this macro
is used to selectively enable the compiler directive only on versions
of Python that support it.

`CYTHON_METH_FASTCALL`/`CYTHON_FAST_PYCALL`

These are used internally to incrementally enable the vectorcall calling
mechanism on older Python versions (<3.8).

`CYTHON_PEP487_INIT_SUBCLASS`

Enable [PEP 487](https://peps.python.org/pep-0487/ "https://peps.python.org/pep-0487/") `__init_subclass__` behaviour.

`CYTHON_USE_TP_FINALIZE`

Use the `tp_finalize` type-slot instead of `tp_dealloc`,
as described in [PEP 442](https://peps.python.org/pep-0442/ "https://peps.python.org/pep-0442/").

`CYTHON_USE_DICT_VERSIONS`

Try to optimize attribute lookup by using versioned dictionaries
where supported.

`CYTHON_USE_EXC_INFO_STACK`

Use an internal structure to track exception state,
used in CPython 3.7 and later.

`CYTHON_UPDATE_DESCRIPTOR_DOC`

Attempt to provide docstrings also for special (double underscore) methods.

`CYTHON_USE_FREELISTS`

Enable the use of freelists on extension types with
[the @cython.freelist decorator](extension_types.html#freelist "extension_types.html#freelist").

`CYTHON_ATOMICS`

Enable the use of atomic reference counting (as opposed to locking then
reference counting) in Cython typed memoryviews.

`CYTHON_DEBUG_VISIT_CONST`

Debug option for including constant (string/integer/code/…) objects in
[`gc.get_referents()`](https://docs.python.org/3/library/gc.html#gc.get_referents "(in Python v3.14)").
By default, Cython avoids GC traversing these objects because they can never participate
in reference cycles, and thus would uselessly waste time during garbage collection runs.

`CYTHON_MODULE_STATE_LOOKUP_THREAD_SAFE`

Makes module state lookup thread-safe (when `CYTHON_USE_MODULE_STATE` and
`CYTHON_PEP489_MULTI_PHASE_INIT` are both enabled). This is on by default
where it would be helpful, however it can be disabled if you are sure that
one interpreter will not be importing your module at the same time as another
is using it. Values greater than 1 can be used to select a specific implementation
for debugging purposes.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Source Files and Compilation](# "#")
  + [Compiling from the command line](#compiling-from-the-command-line "#compiling-from-the-command-line")
    - [Compiling with the cython command](#compiling-with-the-cython-command "#compiling-with-the-cython-command")
    - [Compiling with the cythonize command](#compiling-with-the-cythonize-command "#compiling-with-the-cythonize-command")
  + [Basic `setup.py`](#basic-setup-py "#basic-setup-py")
    - [Configuring the C-Build](#configuring-the-c-build "#configuring-the-c-build")
    - [Cythonize arguments](#cythonize-arguments "#cythonize-arguments")
      * [`cythonize()`](#Cython.Build.cythonize "#Cython.Build.cythonize")
  + [Multiple Cython Files in a Package](#multiple-cython-files-in-a-package "#multiple-cython-files-in-a-package")
    - [Distributing Cython modules](#distributing-cython-modules "#distributing-cython-modules")
  + [Shared utility module](#shared-utility-module "#shared-utility-module")
    - [Compiling shared module using setuptools](#compiling-shared-module-using-setuptools "#compiling-shared-module-using-setuptools")
  + [Integrating multiple modules](#integrating-multiple-modules "#integrating-multiple-modules")
  + [Compiling with `pyximport`](#compiling-with-pyximport "#compiling-with-pyximport")
    - [Arguments](#arguments "#arguments")
      * [`install()`](#pyximport.install "#pyximport.install")
    - [Dependency Handling](#dependency-handling "#dependency-handling")
    - [Limitations](#limitations "#limitations")
  + [Compiling with `cython.inline`](#compiling-with-cython-inline "#compiling-with-cython-inline")
  + [Compiling with `cython.compile`](#compiling-with-cython-compile "#compiling-with-cython-compile")
  + [Compiling with Sage](#compiling-with-sage "#compiling-with-sage")
  + [Compiling with a Jupyter Notebook](#compiling-with-a-jupyter-notebook "#compiling-with-a-jupyter-notebook")
  + [Cython cache](#cython-cache "#cython-cache")
  + [Compiler options](#compiler-options "#compiler-options")
    - [`docstrings`](#Cython.Compiler.Options.docstrings "#Cython.Compiler.Options.docstrings")
    - [`embed_pos_in_docstring`](#Cython.Compiler.Options.embed_pos_in_docstring "#Cython.Compiler.Options.embed_pos_in_docstring")
    - [`generate_cleanup_code`](#Cython.Compiler.Options.generate_cleanup_code "#Cython.Compiler.Options.generate_cleanup_code")
    - [`clear_to_none`](#Cython.Compiler.Options.clear_to_none "#Cython.Compiler.Options.clear_to_none")
    - [`annotate`](#Cython.Compiler.Options.annotate "#Cython.Compiler.Options.annotate")
    - [`fast_fail`](#Cython.Compiler.Options.fast_fail "#Cython.Compiler.Options.fast_fail")
    - [`warning_errors`](#Cython.Compiler.Options.warning_errors "#Cython.Compiler.Options.warning_errors")
    - [`error_on_unknown_names`](#Cython.Compiler.Options.error_on_unknown_names "#Cython.Compiler.Options.error_on_unknown_names")
    - [`error_on_uninitialized`](#Cython.Compiler.Options.error_on_uninitialized "#Cython.Compiler.Options.error_on_uninitialized")
    - [`convert_range`](#Cython.Compiler.Options.convert_range "#Cython.Compiler.Options.convert_range")
    - [`cache_builtins`](#Cython.Compiler.Options.cache_builtins "#Cython.Compiler.Options.cache_builtins")
    - [`gcc_branch_hints`](#Cython.Compiler.Options.gcc_branch_hints "#Cython.Compiler.Options.gcc_branch_hints")
    - [`lookup_module_cpdef`](#Cython.Compiler.Options.lookup_module_cpdef "#Cython.Compiler.Options.lookup_module_cpdef")
    - [`embed`](#Cython.Compiler.Options.embed "#Cython.Compiler.Options.embed")
    - [`cimport_from_pyx`](#Cython.Compiler.Options.cimport_from_pyx "#Cython.Compiler.Options.cimport_from_pyx")
    - [`buffer_max_dims`](#Cython.Compiler.Options.buffer_max_dims "#Cython.Compiler.Options.buffer_max_dims")
    - [`closure_freelist_size`](#Cython.Compiler.Options.closure_freelist_size "#Cython.Compiler.Options.closure_freelist_size")
  + [Compiler directives](#compiler-directives "#compiler-directives")
    - [Configurable optimisations](#configurable-optimisations "#configurable-optimisations")
    - [Warnings](#warnings "#warnings")
    - [How to set directives](#how-to-set-directives "#how-to-set-directives")
      * [Globally](#globally "#globally")
      * [Locally](#locally "#locally")
      * [In `setup.py`](#in-setup-py "#in-setup-py")
  + [C line numbers in tracebacks](#c-line-numbers-in-tracebacks "#c-line-numbers-in-tracebacks")
  + [C macro defines](#c-macro-defines "#c-macro-defines")

#### Previous topic

[Interfacing with External C Code](external_C_code.html "previous chapter")

#### Next topic

[Early Binding for Speed](early_binding_for_speed.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/source_files_and_compilation.rst.txt "../../_sources/src/userguide/source_files_and_compilation.rst.txt")

### Quick search

### Navigation

* [next](early_binding_for_speed.html "Early Binding for Speed")
* [previous](external_C_code.html "Interfacing with External C Code") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Source Files and Compilation

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

