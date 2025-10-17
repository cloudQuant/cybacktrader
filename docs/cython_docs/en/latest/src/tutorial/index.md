




Tutorials — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/tutorial/index.html "/en/stable/src/tutorial/index.html").

### Navigation

* [next](cython_tutorial.html "Basic Tutorial")
* [previous](../quickstart/cythonize.html "Faster code via static typing") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* Tutorials

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Tutorials[¶](#tutorials "Link to this heading")

* [Basic Tutorial](cython_tutorial.html "cython_tutorial.html")
  + [The Basics of Cython](cython_tutorial.html#the-basics-of-cython "cython_tutorial.html#the-basics-of-cython")
  + [Cython Hello World](cython_tutorial.html#cython-hello-world "cython_tutorial.html#cython-hello-world")
  + [Fibonacci Fun](cython_tutorial.html#fibonacci-fun "cython_tutorial.html#fibonacci-fun")
  + [Primes](cython_tutorial.html#primes "cython_tutorial.html#primes")
  + [Primes with C++](cython_tutorial.html#primes-with-c "cython_tutorial.html#primes-with-c")
  + [Language Details](cython_tutorial.html#language-details "cython_tutorial.html#language-details")
* [Calling C functions](external.html "external.html")
  + [Dynamic linking](external.html#dynamic-linking "external.html#dynamic-linking")
  + [External declarations](external.html#external-declarations "external.html#external-declarations")
  + [Naming parameters](external.html#naming-parameters "external.html#naming-parameters")
* [Using C libraries](clibraries.html "clibraries.html")
  + [Defining external declarations](clibraries.html#defining-external-declarations "clibraries.html#defining-external-declarations")
  + [Writing a wrapper class](clibraries.html#writing-a-wrapper-class "clibraries.html#writing-a-wrapper-class")
  + [Memory management](clibraries.html#memory-management "clibraries.html#memory-management")
  + [Compiling and linking](clibraries.html#compiling-and-linking "clibraries.html#compiling-and-linking")
* [Extension types (aka. cdef classes)](cdef_classes.html "cdef_classes.html")
* [pxd files](pxd_files.html "pxd_files.html")
  + [\_\_init\_\_.pxd](pxd_files.html#init-pxd "pxd_files.html#init-pxd")
* [Caveats](caveats.html "caveats.html")
* [Profiling](profiling_tutorial.html "profiling_tutorial.html")
  + [Cython Profiling Basics](profiling_tutorial.html#cython-profiling-basics "profiling_tutorial.html#cython-profiling-basics")
  + [Profiling Tutorial](profiling_tutorial.html#profiling-tutorial "profiling_tutorial.html#profiling-tutorial")
* [Unicode and passing strings](strings.html "strings.html")
  + [Python string types in Cython code](strings.html#python-string-types-in-cython-code "strings.html#python-string-types-in-cython-code")
  + [String literals](strings.html#string-literals "strings.html#string-literals")
  + [General notes about C strings](strings.html#general-notes-about-c-strings "strings.html#general-notes-about-c-strings")
  + [Passing byte strings](strings.html#passing-byte-strings "strings.html#passing-byte-strings")
  + [Accepting strings from Python code](strings.html#accepting-strings-from-python-code "strings.html#accepting-strings-from-python-code")
  + [Dealing with “const”](strings.html#dealing-with-const "strings.html#dealing-with-const")
  + [Decoding bytes to text](strings.html#decoding-bytes-to-text "strings.html#decoding-bytes-to-text")
  + [Encoding text to bytes](strings.html#encoding-text-to-bytes "strings.html#encoding-text-to-bytes")
  + [C++ strings](strings.html#c-strings "strings.html#c-strings")
  + [Auto encoding and decoding](strings.html#auto-encoding-and-decoding "strings.html#auto-encoding-and-decoding")
  + [Source code encoding](strings.html#source-code-encoding "strings.html#source-code-encoding")
  + [Single bytes and characters](strings.html#single-bytes-and-characters "strings.html#single-bytes-and-characters")
  + [Narrow Unicode builds](strings.html#narrow-unicode-builds "strings.html#narrow-unicode-builds")
  + [Iteration](strings.html#iteration "strings.html#iteration")
  + [Windows and wide character APIs](strings.html#windows-and-wide-character-apis "strings.html#windows-and-wide-character-apis")
* [Memory Allocation](memory_allocation.html "memory_allocation.html")
* [Embedding Cython modules in C/C++ applications](embedding.html "embedding.html")
  + [Initialising your main module](embedding.html#initialising-your-main-module "embedding.html#initialising-your-main-module")
  + [Embedding example code](embedding.html#embedding-example-code "embedding.html#embedding-example-code")
  + [Troubleshooting](embedding.html#troubleshooting "embedding.html#troubleshooting")
* [Pure Python Mode](pure.html "pure.html")
  + [Augmenting .pxd](pure.html#augmenting-pxd "pure.html#augmenting-pxd")
  + [Magic Attributes](pure.html#magic-attributes "pure.html#magic-attributes")
  + [PEP-484 type annotations](pure.html#pep-484-type-annotations "pure.html#pep-484-type-annotations")
  + [Tips and Tricks](pure.html#tips-and-tricks "pure.html#tips-and-tricks")
* [Working with NumPy](numpy.html "numpy.html")
  + [Adding types](numpy.html#adding-types "numpy.html#adding-types")
  + [Efficient indexing](numpy.html#efficient-indexing "numpy.html#efficient-indexing")
  + [Tuning indexing further](numpy.html#tuning-indexing-further "numpy.html#tuning-indexing-further")
  + [What typing does not do](numpy.html#what-typing-does-not-do "numpy.html#what-typing-does-not-do")
  + [More generic code](numpy.html#more-generic-code "numpy.html#more-generic-code")
  + [Buffer options](numpy.html#buffer-options "numpy.html#buffer-options")
* [Working with Python arrays](array.html "array.html")
  + [Safe usage with memory views](array.html#safe-usage-with-memory-views "array.html#safe-usage-with-memory-views")
  + [Zero-overhead, unsafe access to raw C pointer](array.html#zero-overhead-unsafe-access-to-raw-c-pointer "array.html#zero-overhead-unsafe-access-to-raw-c-pointer")
  + [Cloning, extending arrays](array.html#cloning-extending-arrays "array.html#cloning-extending-arrays")
  + [API reference](array.html#api-reference "array.html#api-reference")
* [Writing parallel code with Cython](parallelization.html "parallelization.html")
  + [Compilation](parallelization.html#compilation "parallelization.html#compilation")
  + [Element-wise parallel operations](parallelization.html#element-wise-parallel-operations "parallelization.html#element-wise-parallel-operations")
  + [Reductions](parallelization.html#reductions "parallelization.html#reductions")
  + [`parallel` blocks](parallelization.html#parallel-blocks "parallelization.html#parallel-blocks")
* [Further reading](readings.html "readings.html")
* [Related work](related_work.html "related_work.html")
* [Appendix: Installing MinGW on Windows](appendix.html "appendix.html")
  + [Python 3.8+](appendix.html#python-3-8 "appendix.html#python-3-8")

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Faster code via static typing](../quickstart/cythonize.html "previous chapter")

#### Next topic

[Basic Tutorial](cython_tutorial.html "next chapter")

### This Page

* [Show Source](../../_sources/src/tutorial/index.rst.txt "../../_sources/src/tutorial/index.rst.txt")

### Quick search

### Navigation

* [next](cython_tutorial.html "Basic Tutorial")
* [previous](../quickstart/cythonize.html "Faster code via static typing") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* Tutorials

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

