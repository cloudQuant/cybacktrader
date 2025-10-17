




Welcome, and thank you for your interest in contributing! — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/CONTRIBUTING.html "/en/stable/CONTRIBUTING.html").

### Navigation

* [next](src/devguide/bugtracker.html "Bug/Feature Tracking and Project Culture")
* [previous](src/reference/special_methods_table.html "Special Methods Table") |
* [Cython 3.2.0b1 documentation](index.html "index.html") »
* Welcome, and thank you for your interest in contributing!

🤝 Like the tool? Help make it better! [Your donation helps!](src/donating.html "src/donating.html") 🤝

# Welcome, and thank you for your interest in contributing![¶](#welcome-and-thank-you-for-your-interest-in-contributing "Link to this heading")

If you are looking for a good way to contribute to the Cython project, please

* Read these docs,
  especially the section on [Getting started working on Cython](src/devguide/getting_started.html#getting-started "src/devguide/getting_started.html#getting-started").
* look through the [issues that need help](https://github.com/cython/cython/labels/help%20wanted "https://github.com/cython/cython/labels/help%20wanted").
* look through the [issues that are a good entry point for beginners](https://github.com/cython/cython/labels/good%20first%20issue "https://github.com/cython/cython/labels/good%20first%20issue").
* ask on the [core developers mailing list](https://mail.python.org/mailman/listinfo/cython-devel "https://mail.python.org/mailman/listinfo/cython-devel") for guidance.
* a useful introduction is [John Cantor’s Cython notes](https://web.archive.org/web/20170511222231/https://wstein.org/wiki/attachments/2008(2f)sageseminar(2f)kantor/slides.pdf "https://web.archive.org/web/20170511222231/https://wstein.org/wiki/attachments/2008(2f)sageseminar(2f)kantor/slides.pdf").

Note that some (but not all) “good first issue”s also require an understanding of C
and a bit of the CPython C-API - usually those that also have the `Code Generation`
label. We generally consider a ticket a “good first issue” if it has a limited scope
that new contributors will have to learn about, e.g. only needs changes to the parser,
the type analysis or the code generation, but does not require changes all across the
compiler pipeline.

If you have code that you want to contribute, please make sure that it

* includes tests in the `tests/` directory
* comes in form of a pull request

We use [github actions](https://github.com/cython/cython/actions "https://github.com/cython/cython/actions") for cross-platform testing, including pull requests.

* [Bug/Feature Tracking and Project Culture](src/devguide/bugtracker.html "src/devguide/bugtracker.html")
* [Getting started working on Cython](src/devguide/getting_started.html "src/devguide/getting_started.html")
  + [Git](src/devguide/getting_started.html#git "src/devguide/getting_started.html#git")
  + [Running Cython on your PC](src/devguide/getting_started.html#running-cython-on-your-pc "src/devguide/getting_started.html#running-cython-on-your-pc")
* [“Where does that C code come from?”](src/devguide/debugging_the_cython_compiler.html "src/devguide/debugging_the_cython_compiler.html")
* [Cython internals](src/devguide/cython_internals.html "src/devguide/cython_internals.html")
  + [The parse tree (AST)](src/devguide/cython_internals.html#the-parse-tree-ast "src/devguide/cython_internals.html#the-parse-tree-ast")
  + [How to add a new attribute to an AST node](src/devguide/cython_internals.html#how-to-add-a-new-attribute-to-an-ast-node "src/devguide/cython_internals.html#how-to-add-a-new-attribute-to-an-ast-node")
  + [Utility Code](src/devguide/cython_internals.html#utility-code "src/devguide/cython_internals.html#utility-code")
  + [Naming conventions](src/devguide/cython_internals.html#naming-conventions "src/devguide/cython_internals.html#naming-conventions")
* [The Test Suite](src/devguide/tests.html "src/devguide/tests.html")
  + [Tags](src/devguide/tests.html#tags "src/devguide/tests.html#tags")
  + [Tests](src/devguide/tests.html#tests "src/devguide/tests.html#tests")
  + [Parse tree assertions](src/devguide/tests.html#parse-tree-assertions "src/devguide/tests.html#parse-tree-assertions")
  + [Running the CPython test suite](src/devguide/tests.html#running-the-cpython-test-suite "src/devguide/tests.html#running-the-cpython-test-suite")
  + [Tip to create doctest scripts](src/devguide/tests.html#tip-to-create-doctest-scripts "src/devguide/tests.html#tip-to-create-doctest-scripts")
  + [Debugging failures in the Cython test suite](src/devguide/tests.html#debugging-failures-in-the-cython-test-suite "src/devguide/tests.html#debugging-failures-in-the-cython-test-suite")

[![Logo](_static/cythonlogo.png)](index.html "index.html")

#### Previous topic

[Special Methods Table](src/reference/special_methods_table.html "previous chapter")

#### Next topic

[Bug/Feature Tracking and Project Culture](src/devguide/bugtracker.html "next chapter")

### This Page

* [Show Source](_sources/CONTRIBUTING.rst.txt "_sources/CONTRIBUTING.rst.txt")

### Quick search

### Navigation

* [next](src/devguide/bugtracker.html "Bug/Feature Tracking and Project Culture")
* [previous](src/reference/special_methods_table.html "Special Methods Table") |
* [Cython 3.2.0b1 documentation](index.html "index.html") »
* Welcome, and thank you for your interest in contributing!

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

