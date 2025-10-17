




Compilation — Cython 3.1.4 documentation

### Navigation

* [next](special_methods_table.html "Special Methods Table")
* [previous](index.html "Reference Guide") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Reference Guide](index.html "index.html") »
* Compilation

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Compilation[¶](#compilation "Link to this heading")

Note

The sections in this page were moved to the [Source Files and Compilation](../userguide/source_files_and_compilation.html#compilation "../userguide/source_files_and_compilation.html#compilation") in the userguide.

## Compiling from the command line[¶](#compiling-from-the-command-line "Link to this heading")

This section was moved to [Compiling from the command line](../userguide/source_files_and_compilation.html#compiling-command-line "../userguide/source_files_and_compilation.html#compiling-command-line").

## Compiling with `distutils`[¶](#compiling-with-distutils "Link to this heading")

This section was moved to [Basic setup.py](../userguide/source_files_and_compilation.html#basic-setup-py "../userguide/source_files_and_compilation.html#basic-setup-py").

### Configuring the C-Build[¶](#configuring-the-c-build "Link to this heading")

This section was moved to [Basic setup.py](../userguide/source_files_and_compilation.html#basic-setup-py "../userguide/source_files_and_compilation.html#basic-setup-py").

### Cythonize arguments[¶](#cythonize-arguments "Link to this heading")

This section was moved to [Cythonize arguments](../userguide/source_files_and_compilation.html#cythonize-arguments "../userguide/source_files_and_compilation.html#cythonize-arguments").

### Compiler options[¶](#compiler-options "Link to this heading")

This section was moved to [Compiler options](../userguide/source_files_and_compilation.html#compiler-options "../userguide/source_files_and_compilation.html#compiler-options").

### Distributing Cython modules[¶](#distributing-cython-modules "Link to this heading")

This section was moved to [Distributing Cython modules](../userguide/source_files_and_compilation.html#distributing-cython-modules "../userguide/source_files_and_compilation.html#distributing-cython-modules").

## Integrating multiple modules[¶](#integrating-multiple-modules "Link to this heading")

This section was moved to [Integrating multiple modules](../userguide/source_files_and_compilation.html#integrating-multiple-modules "../userguide/source_files_and_compilation.html#integrating-multiple-modules").

## Compiling with `pyximport`[¶](#compiling-with-pyximport "Link to this heading")

This section was moved to [Compiling with pyximport](../userguide/source_files_and_compilation.html#pyximport "../userguide/source_files_and_compilation.html#pyximport").

### Arguments[¶](#arguments "Link to this heading")

### Dependency Handling[¶](#dependency-handling "Link to this heading")

### Limitations[¶](#limitations "Link to this heading")

## Compiling with `cython.inline`[¶](#compiling-with-cython-inline "Link to this heading")

This section was moved to [Compiling with cython.inline](../userguide/source_files_and_compilation.html#compiling-with-cython-inline "../userguide/source_files_and_compilation.html#compiling-with-cython-inline").

## Compiling with Sage[¶](#compiling-with-sage "Link to this heading")

This section was moved to [Compiling with Sage](../userguide/source_files_and_compilation.html#compiling-with-sage "../userguide/source_files_and_compilation.html#compiling-with-sage").

## Compiling with a Jupyter Notebook[¶](#compiling-with-a-jupyter-notebook "Link to this heading")

This section was moved to [Compiling with a Jupyter Notebook](../userguide/source_files_and_compilation.html#compiling-notebook "../userguide/source_files_and_compilation.html#compiling-notebook").

## Compiler directives[¶](#compiler-directives "Link to this heading")

This section was moved to [Compiler directives](../userguide/source_files_and_compilation.html#compiler-directives "../userguide/source_files_and_compilation.html#compiler-directives").

### Configurable optimisations[¶](#configurable-optimisations "Link to this heading")

This section was moved to [Configurable optimisations](../userguide/source_files_and_compilation.html#configurable-optimisations "../userguide/source_files_and_compilation.html#configurable-optimisations").

### Warnings[¶](#warnings "Link to this heading")

This section was moved to [Warnings](../userguide/source_files_and_compilation.html#warnings "../userguide/source_files_and_compilation.html#warnings").

### How to set directives[¶](#how-to-set-directives "Link to this heading")

This section was moved to [How to set directives](../userguide/source_files_and_compilation.html#how-to-set-directives "../userguide/source_files_and_compilation.html#how-to-set-directives").

#### Globally[¶](#globally "Link to this heading")

#### Locally[¶](#locally "Link to this heading")

#### In `setup.py`[¶](#in-setup-py "Link to this heading")

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Compilation](# "#")
  + [Compiling from the command line](#compiling-from-the-command-line "#compiling-from-the-command-line")
  + [Compiling with `distutils`](#compiling-with-distutils "#compiling-with-distutils")
    - [Configuring the C-Build](#configuring-the-c-build "#configuring-the-c-build")
    - [Cythonize arguments](#cythonize-arguments "#cythonize-arguments")
    - [Compiler options](#compiler-options "#compiler-options")
    - [Distributing Cython modules](#distributing-cython-modules "#distributing-cython-modules")
  + [Integrating multiple modules](#integrating-multiple-modules "#integrating-multiple-modules")
  + [Compiling with `pyximport`](#compiling-with-pyximport "#compiling-with-pyximport")
    - [Arguments](#arguments "#arguments")
    - [Dependency Handling](#dependency-handling "#dependency-handling")
    - [Limitations](#limitations "#limitations")
  + [Compiling with `cython.inline`](#compiling-with-cython-inline "#compiling-with-cython-inline")
  + [Compiling with Sage](#compiling-with-sage "#compiling-with-sage")
  + [Compiling with a Jupyter Notebook](#compiling-with-a-jupyter-notebook "#compiling-with-a-jupyter-notebook")
  + [Compiler directives](#compiler-directives "#compiler-directives")
    - [Configurable optimisations](#configurable-optimisations "#configurable-optimisations")
    - [Warnings](#warnings "#warnings")
    - [How to set directives](#how-to-set-directives "#how-to-set-directives")
      * [Globally](#globally "#globally")
      * [Locally](#locally "#locally")
      * [In `setup.py`](#in-setup-py "#in-setup-py")

#### Previous topic

[Reference Guide](index.html "previous chapter")

#### Next topic

[Special Methods Table](special_methods_table.html "next chapter")

### This Page

* [Show Source](../../_sources/src/reference/compilation.rst.txt "../../_sources/src/reference/compilation.rst.txt")

### Quick search

### Navigation

* [next](special_methods_table.html "Special Methods Table")
* [previous](index.html "Reference Guide") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Reference Guide](index.html "index.html") »
* Compilation

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

