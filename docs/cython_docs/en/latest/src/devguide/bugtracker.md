




Bug/Feature Tracking and Project Culture — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/devguide/bugtracker.html "/en/stable/src/devguide/bugtracker.html").

### Navigation

* [next](getting_started.html "Getting started working on Cython")
* [previous](../../CONTRIBUTING.html "Welcome, and thank you for your interest in contributing!") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Welcome, and thank you for your interest in contributing!](../../CONTRIBUTING.html "../../CONTRIBUTING.html") »
* Bug/Feature Tracking and Project Culture

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Bug/Feature Tracking and Project Culture[¶](#bug-feature-tracking-and-project-culture "Link to this heading")

The Cython project is strongly driven by interest and has a rather free and open development culture.
There are a couple of main developers and regular committers from various different backgrounds,
but we are very happy to receive input and patches from everyone.

In order try to keep the intervals between releases short, however, there are a couple of restrictions that we impose on ourselves,
especially when working on bug-fix (third digit) releases.

1. Every change that goes into a bug fix release must be backed by a [ticket](https://github.com/cython/cython/issues "https://github.com/cython/cython/issues").
2. Every ticket should have a bug test case associated with it. Fairly often, users who report a problem add an example
   to the ticket description anyway, but it definitely makes the life of the developers easier when they do so in form
   of a readily usable test case. Otherwise, the developers have to write it up themselves, in addition to fixing the bug.
   Please see the section about [The Test Suite](tests.html#the-test-suite "tests.html#the-test-suite") below to find out how to write a good test.

   Either way, before a ticket gets fixed or assigned a milestone, there must be a failing test
   case in the appropriate `tests/` directory (preferably `tests/run`) that is named
   “`nicely_descriptive_name_here_Txyz.pyx`” (where `'xyz'` is the ticket number).
   Please try to do this even for the tricky cases that feel like there isn’t a good test case.
   Reproducing a bug is critical for fixing it, and having a test case is critical for knowing when
   it’s fixed and for not breaking it in the future. Broken examples are listed in the `tests/bugs.txt`
   file, and are skipped during normal testing (this makes it easier to detect regressions when doing other work).
3. A working patch in a pull request, together with a descriptive test, will definitely accelerate the
   mainline bug fixing. If you are unsure where to get started, it’s usually best to ask on the mailing list before getting lost.
4. Pull requests will usually be handled with priority and should at least receive a timely review.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

#### Previous topic

[Welcome, and thank you for your interest in contributing!](../../CONTRIBUTING.html "previous chapter")

#### Next topic

[Getting started working on Cython](getting_started.html "next chapter")

### This Page

* [Show Source](../../_sources/src/devguide/bugtracker.rst.txt "../../_sources/src/devguide/bugtracker.rst.txt")

### Quick search

### Navigation

* [next](getting_started.html "Getting started working on Cython")
* [previous](../../CONTRIBUTING.html "Welcome, and thank you for your interest in contributing!") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Welcome, and thank you for your interest in contributing!](../../CONTRIBUTING.html "../../CONTRIBUTING.html") »
* Bug/Feature Tracking and Project Culture

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

