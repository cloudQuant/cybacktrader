




Cython Changelog — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/changes.html "/en/stable/src/changes.html").

### Navigation

* [previous](devguide/tests.html "The Test Suite")
* [Cython 3.2.0b1 documentation](../index.html "../index.html") »
* Cython Changelog

🤝 Like the tool? Help make it better! [Your donation helps!](donating.html "donating.html") 🤝

# Cython Changelog[¶](#cython-changelog "Link to this heading")

## 3.2.0b1 (2025-10-??)[¶](#b1-2025-10 "Link to this heading")

### Features added[¶](#features-added "Link to this heading")

* Builtin exception types are now inferred.
  (Github issue [#6908](https://github.com/cython/cython/issues/6908 "https://github.com/cython/cython/issues/6908"))
* The list of known, inferred and optimised Python builtins was updated.
  range is now considered a type. ascii, bin, format, hex, oct were added as functions.
  (Github issue [#6931](https://github.com/cython/cython/issues/6931 "https://github.com/cython/cython/issues/6931"))
* The f-string syntax was extended according to PEP-701.
  (Github issue [#5452](https://github.com/cython/cython/issues/5452 "https://github.com/cython/cython/issues/5452"))
* t-strings are implemented according to PEP-750. The implementation backports the template classes
  but prefers existing backports if installed separately.
  (Github issue [#6811](https://github.com/cython/cython/issues/6811 "https://github.com/cython/cython/issues/6811"))
* Unknown return type annotations with -> are no longer rejected but produce warnings.
  This allows better integration with Python type hints that are not always usable for Cython.
  `-> None` is also allowed now.
  Patch by jpe. (Github issue [#6946](https://github.com/cython/cython/issues/6946 "https://github.com/cython/cython/issues/6946"))
* The runtime Python dispatch for fused functions is substantially faster.
  (Github issues [#1385](https://github.com/cython/cython/issues/1385 "https://github.com/cython/cython/issues/1385"), [#6996](https://github.com/cython/cython/issues/6996 "https://github.com/cython/cython/issues/6996"))
* Freelists (via cdef class decorator and for internally used types such as `async`)
  are now also used in the Limited API and with extension type specs enabled.
  (Github issue [#7151](https://github.com/cython/cython/issues/7151 "https://github.com/cython/cython/issues/7151"))
* Module imports now quickly check for an already imported module to speed up reimports.
  Patch by Lysandros Nikolaou. (Github issue [#7035](https://github.com/cython/cython/issues/7035 "https://github.com/cython/cython/issues/7035"))
* Type checks on PEP-604 union types (int | None) are optimised into separate checks.
  (Github issue [#6935](https://github.com/cython/cython/issues/6935 "https://github.com/cython/cython/issues/6935"))
* Assignments to the PEP-604 union type float | None allow any suitable Python number as input
  and convert it to a Python float automatically.
  (Github issue [#5750](https://github.com/cython/cython/issues/5750 "https://github.com/cython/cython/issues/5750"))
* Item type inference was improved for looping over literals.
  (Github issue [#6912](https://github.com/cython/cython/issues/6912 "https://github.com/cython/cython/issues/6912"))
* Looping over literal sequences and strings now uses efficient C array looping if possible.
  (Github issue [#6926](https://github.com/cython/cython/issues/6926 "https://github.com/cython/cython/issues/6926"))
* Releasing the GIL from an unknown lock state is more efficient.
  (Github issue [#6847](https://github.com/cython/cython/issues/6847 "https://github.com/cython/cython/issues/6847"))
* `cython.critical_section(PyMutex)` now works, as with Python objects.
  (Github issue [#6847](https://github.com/cython/cython/issues/6847 "https://github.com/cython/cython/issues/6847"))
* `bool(c_int/float/ptr)` avoid passing through Python objects.
  (Github issue [#7015](https://github.com/cython/cython/issues/7015 "https://github.com/cython/cython/issues/7015"))
* Variables assigned inside of `prange` loops can now be initialised outside of the loop.
  (Github issue [#7178](https://github.com/cython/cython/issues/7178 "https://github.com/cython/cython/issues/7178"))
* Unused exceptions in `except` clauses are detected in some more cases to avoid their normalisation.
  (Github issue [#7021](https://github.com/cython/cython/issues/7021 "https://github.com/cython/cython/issues/7021"))
* Some object constants are now marked as `immortal` to speed up their reference counting
  in recent CPython versions. This can be configured with the `CYTHON_IMMORTAL_CONSTANTS` C macro.
  (Github issue [#7118](https://github.com/cython/cython/issues/7118 "https://github.com/cython/cython/issues/7118"))
* Further improvements were made to reduce the size of the resulting extension modules.
  (Github issue [#6983](https://github.com/cython/cython/issues/6983 "https://github.com/cython/cython/issues/6983"), [#7199](https://github.com/cython/cython/issues/7199 "https://github.com/cython/cython/issues/7199"), [#7220](https://github.com/cython/cython/issues/7220 "https://github.com/cython/cython/issues/7220"))
* Several improvements were made in freethreaded Python code.
  (Github issues [#6936](https://github.com/cython/cython/issues/6936 "https://github.com/cython/cython/issues/6936"), [#6939](https://github.com/cython/cython/issues/6939 "https://github.com/cython/cython/issues/6939"), [#6949](https://github.com/cython/cython/issues/6949 "https://github.com/cython/cython/issues/6949"), [#6984](https://github.com/cython/cython/issues/6984 "https://github.com/cython/cython/issues/6984"),

  [#7011](https://github.com/cython/cython/issues/7011 "https://github.com/cython/cython/issues/7011"), [#7066](https://github.com/cython/cython/issues/7066 "https://github.com/cython/cython/issues/7066"), [#7114](https://github.com/cython/cython/issues/7114 "https://github.com/cython/cython/issues/7114"), [#7200](https://github.com/cython/cython/issues/7200 "https://github.com/cython/cython/issues/7200"))
* Several improvements were made for the Limited API.
  (Github issues [#6959](https://github.com/cython/cython/issues/6959 "https://github.com/cython/cython/issues/6959"), [#6991](https://github.com/cython/cython/issues/6991 "https://github.com/cython/cython/issues/6991"))
* Several improvements were made for the GraalPython support.
  Patch by Michael Šimáček. (Github issue [#7074](https://github.com/cython/cython/issues/7074 "https://github.com/cython/cython/issues/7074"))
* Some GIL-safe C-API wrappers were added to the libc/libcpp declarations.
  (Github issue [#6829](https://github.com/cython/cython/issues/6829 "https://github.com/cython/cython/issues/6829"), [#6993](https://github.com/cython/cython/issues/6993 "https://github.com/cython/cython/issues/6993"))
* String and number constants use less storage space in the module.
  (Github issues [#6971](https://github.com/cython/cython/issues/6971 "https://github.com/cython/cython/issues/6971"), [#6978](https://github.com/cython/cython/issues/6978 "https://github.com/cython/cython/issues/6978"), [#6986](https://github.com/cython/cython/issues/6986 "https://github.com/cython/cython/issues/6986"))
* The managed dict/weakref support in CPython 3.12+ is used for internal types
  to benefit from future CPython optimisations here.
  (Github issue [#6891](https://github.com/cython/cython/issues/6891 "https://github.com/cython/cython/issues/6891"))
* Using `NaN` as exception return value is supported.
  (Github issues [#6900](https://github.com/cython/cython/issues/6900 "https://github.com/cython/cython/issues/6900"), [#6903](https://github.com/cython/cython/issues/6903 "https://github.com/cython/cython/issues/6903"))
* Declarations for C++ condition variables were added.
  (Github issue [#6836](https://github.com/cython/cython/issues/6836 "https://github.com/cython/cython/issues/6836"))
* `cython --embed` gained a new option `--embed-modules=…` to list further extension modules
  that will be statically linked into the generated extension module, to get them initialised
  on application start.
  (Github issue [#2849](https://github.com/cython/cython/issues/2849 "https://github.com/cython/cython/issues/2849"))
* The annotated source HTML page shows alternating +/− markers to open/close lines.
  Patch by Kamil Monicz. (Github issue [#7099](https://github.com/cython/cython/issues/7099 "https://github.com/cython/cython/issues/7099"))
* Unicode 16.0.0 is used to parse identifiers.
  (Github issue [#6836](https://github.com/cython/cython/issues/6836 "https://github.com/cython/cython/issues/6836"))

### Bugs fixed[¶](#bugs-fixed "Link to this heading")

* Special float exception values could generate invalid C code.
  (Github issues [#6900](https://github.com/cython/cython/issues/6900 "https://github.com/cython/cython/issues/6900"), [#6903](https://github.com/cython/cython/issues/6903 "https://github.com/cython/cython/issues/6903"))
* References to the Python `bool` type could generate invalid C code.
  (Github issue [#6902](https://github.com/cython/cython/issues/6902 "https://github.com/cython/cython/issues/6902"))
* Vectorcalls could use needless temp assignments for `self`.
  (Github issue [#6909](https://github.com/cython/cython/issues/6909 "https://github.com/cython/cython/issues/6909"))
* Iterating over temporary memoryviews could crash Cython.
  (Github issue [#7005](https://github.com/cython/cython/issues/7005 "https://github.com/cython/cython/issues/7005"))
* Type casts on constants as part of numeric expressions could crash Cython.
  (Github issue [#6779](https://github.com/cython/cython/issues/6779 "https://github.com/cython/cython/issues/6779"))
* Long code bodies in `with` statements could crash Cython.
  (Github issue [#7122](https://github.com/cython/cython/issues/7122 "https://github.com/cython/cython/issues/7122"))
* Indexing `bytes` failed to optimise in some cases.
  (Github issue [#6997](https://github.com/cython/cython/issues/6997 "https://github.com/cython/cython/issues/6997"))
* Optimised C integer formatting in f-strings failed to apply to typedef types.
  (Github issue [#7170](https://github.com/cython/cython/issues/7170 "https://github.com/cython/cython/issues/7170"))
* Conversion from C++ strings longer than `PY_SSIZE_T_MAX` did not validate the length.
* Some non-Limited API code was incorrectly used in generated header files.
  (Github issue [#7157](https://github.com/cython/cython/issues/7157 "https://github.com/cython/cython/issues/7157"))
* Optimised unpacking of Python integers in expressions uses a slightly safer scheme.
  (Github issue [#7134](https://github.com/cython/cython/issues/7134 "https://github.com/cython/cython/issues/7134"))
* In auto-pickling, trying to unpickle an object that has no `__dict__` from object pickle data
  that includes instance dict state is now an error.
  (Github issue [#7222](https://github.com/cython/cython/issues/7222 "https://github.com/cython/cython/issues/7222"))
* The type objects of heap types were not always correctly decrefed on deallocation.
  (Github issue [#7145](https://github.com/cython/cython/issues/7145 "https://github.com/cython/cython/issues/7145"))
* Pure mode type aliases like `p_int` or `ulong` leaked into some C type contexts,
  risking to conflict with user declarations.
  (Github issues [#6922](https://github.com/cython/cython/issues/6922 "https://github.com/cython/cython/issues/6922"), [#6339](https://github.com/cython/cython/issues/6339 "https://github.com/cython/cython/issues/6339"))
* Boolean (emptyness) tests on builtin containers could fail to handle (unlikely) errors.
  (Github issue [#7090](https://github.com/cython/cython/issues/7090 "https://github.com/cython/cython/issues/7090"))
* The return type of `bytes.join()` was sometimes inferred as plain `object`.
  (Github issue [#6987](https://github.com/cython/cython/issues/6987 "https://github.com/cython/cython/issues/6987"))
* Type inference could fail to understand `prange()` arguments.
  (Github issue [#6974](https://github.com/cython/cython/issues/6974 "https://github.com/cython/cython/issues/6974"))
* Empty return statements were not always reported when tracing.
  (Github issue [#7022](https://github.com/cython/cython/issues/7022 "https://github.com/cython/cython/issues/7022"))
* Value conversion errors when tracing C return statements no longer fail the trace
  but fall back to reporting `None` returns instead.
  (Github issue [#7022](https://github.com/cython/cython/issues/7022 "https://github.com/cython/cython/issues/7022"))
* `embedsignatures` failed if `lambda` was used in function default arguments.
  (Github issue [#6880](https://github.com/cython/cython/issues/6880 "https://github.com/cython/cython/issues/6880"))
* An internal C function was not marked as `static` and leaked a linker symbol.
  (Github issue [#6957](https://github.com/cython/cython/issues/6957 "https://github.com/cython/cython/issues/6957"))
* Conversion code for memoryview dtypes from and to Python objects generated C warnings about
  incorrect `const` / non-`const` casting code.
  (Github issue [#7219](https://github.com/cython/cython/issues/7219 "https://github.com/cython/cython/issues/7219"))
* Cython’s tools and frontend scripts now use `python3` instead of just `python`
  in their shebang line.
  Patch by Matti Picus. (Github issue [#7053](https://github.com/cython/cython/issues/7053 "https://github.com/cython/cython/issues/7053"))
* Includes all fixes as of Cython 3.1.4.

### Other changes[¶](#other-changes "Link to this heading")

* Usages of Py\_TPFLAGS\_HAVE\_FINALIZE were removed. The constant remains available as cimport from
  `cpython.object` for legacy reasons.
  (Github issue [#6423](https://github.com/cython/cython/issues/6423 "https://github.com/cython/cython/issues/6423"))

## 3.1.5 (2025-??-??)[¶](#id1 "Link to this heading")

### Bugs fixed[¶](#id2 "Link to this heading")

* Conversion from C++ strings longer than `PY_SSIZE_T_MAX` did not validate the length.
* Some non-Limited API code was incorrectly used in generated header files.
  (Github issue [#7157](https://github.com/cython/cython/issues/7157 "https://github.com/cython/cython/issues/7157"))
* Optimised unpacking of Python integers in expressions uses a slightly safer scheme.
  (Github issue [#7134](https://github.com/cython/cython/issues/7134 "https://github.com/cython/cython/issues/7134"))

## 3.1.4 (2025-09-16)[¶](#id3 "Link to this heading")

### Features added[¶](#id4 "Link to this heading")

* Declarations for the new `PyUnstable_*()` refcounting C-API functions in Py3.14 were added.
  (Github issue [#6836](https://github.com/cython/cython/issues/6836 "https://github.com/cython/cython/issues/6836"))

### Bugs fixed[¶](#id5 "Link to this heading")

* The monitoring code could crash on tracing.
  (Github issue [#7050](https://github.com/cython/cython/issues/7050 "https://github.com/cython/cython/issues/7050"))
* Initialising the monitoring code could fail with a CPython exception.
  See [https://github.com/nedbat/coveragepy/issues/1790#issuecomment-3257410149](https://github.com/nedbat/coveragepy/issues/1790#issuecomment-3257410149 "https://github.com/nedbat/coveragepy/issues/1790#issuecomment-3257410149")
* Optimised integer shifting triggered undefined behaviour in C.
  (Github issue [#7089](https://github.com/cython/cython/issues/7089 "https://github.com/cython/cython/issues/7089"))
* Deallocating objects that inherit from external types defined in pxd files
  could run into an infinite loop.
  (Github issue [#7143](https://github.com/cython/cython/issues/7143 "https://github.com/cython/cython/issues/7143"))
* A reference to metaclasses could be leaked on instantiation.
  (Github issue [#7130](https://github.com/cython/cython/issues/7130 "https://github.com/cython/cython/issues/7130"))
* (Unlikely) error handling during empty builtin container tests was ineffective.
  (Github issue [#7190](https://github.com/cython/cython/issues/7190 "https://github.com/cython/cython/issues/7190"))
* Generated `*_api.h` files used potentially unknown Cython configuration macros.
  (Github issue [#7108](https://github.com/cython/cython/issues/7108 "https://github.com/cython/cython/issues/7108"))
* `cythonize()` avoids parallel compiler runs on systems using `spawn()` in multiprocessing.
  Patch by Marcel Bargull. (Github issue [#3262](https://github.com/cython/cython/issues/3262 "https://github.com/cython/cython/issues/3262"))
* The `@cython.ufunc` decorator was missing in type checker stubs.
  Patch by jayClean. (Github issue [#7109](https://github.com/cython/cython/issues/7109 "https://github.com/cython/cython/issues/7109"))

## 3.1.3 (2025-08-13)[¶](#id6 "Link to this heading")

### Bugs fixed[¶](#id7 "Link to this heading")

* Some method calls with 0 or 1 argument failed to use `PyObject_VectorCallMethod()`.
* Walrus assignments of literal Python integers could generate invalid C code.
  (Github issue [#6989](https://github.com/cython/cython/issues/6989 "https://github.com/cython/cython/issues/6989"))
* `cython.pythread_type_lock` (also used as fallback for `cython.pymutex`)
  could stall on heavily contended locks.
  (Github issue [#6999](https://github.com/cython/cython/issues/6999 "https://github.com/cython/cython/issues/6999"))
* C string arrays (not pointers) always coerced to the Python default string type,
  even on explicit casts to other string types.
  (Github issue [#7020](https://github.com/cython/cython/issues/7020 "https://github.com/cython/cython/issues/7020"))
* Unterminated `\N{}` character escapes in strings could unrail the parser.
  (Github issue [#7056](https://github.com/cython/cython/issues/7056 "https://github.com/cython/cython/issues/7056"))
* An internal C function was not marked as `static` and leaked a linker symbol.
  (Github issue [#6957](https://github.com/cython/cython/issues/6957 "https://github.com/cython/cython/issues/6957"))
* Some Unicode letters were not recognised as lexically valid name parts.
  (Github issue [#7059](https://github.com/cython/cython/issues/7059 "https://github.com/cython/cython/issues/7059"))
* Compatibility with PyPy3.8 was lost by accident.
* The Linux binary wheels of 3.1.2 used SSSE3 CPU instructions which are not available on some CPUs.
  (Github issue [#7038](https://github.com/cython/cython/issues/7038 "https://github.com/cython/cython/issues/7038"))

## 3.1.2 (2025-06-09)[¶](#id8 "Link to this heading")

### Bugs fixed[¶](#id9 "Link to this heading")

* Attribute lookups failed on the `bool` builtin type.
  (Github issue [#6905](https://github.com/cython/cython/issues/6905 "https://github.com/cython/cython/issues/6905"))
* Type checks on or-ed union types could incorrectly return false.
  (Github issue [#6420](https://github.com/cython/cython/issues/6420 "https://github.com/cython/cython/issues/6420"))
* Negative list indexing could accidentally wrap around twice in PyPy and the Limited API.
* Iterating over literal sequences with starred (unpacked) items could infer a wrong
  type for the loop variable and fail to assign the values.
  (Github issue [#6924](https://github.com/cython/cython/issues/6924 "https://github.com/cython/cython/issues/6924"))
* Calls to C functions taking exception types failed to check for a None argument.
  (Github issue [#6420](https://github.com/cython/cython/issues/6420 "https://github.com/cython/cython/issues/6420"))
* Fused functions had an incorrect `__module__` attribute.
  (Github issue [#6897](https://github.com/cython/cython/issues/6897 "https://github.com/cython/cython/issues/6897"))
* The type of Cython implemented functions had an incorrect `__module__` attribute.
  (Github issue [#6841](https://github.com/cython/cython/issues/6841 "https://github.com/cython/cython/issues/6841"))
* Errors while indexing into `bytearray` or `str` in `nogil` sections could crash.
  (Github issue [#6947](https://github.com/cython/cython/issues/6947 "https://github.com/cython/cython/issues/6947"))
* `bytearray.append()` could silently accept some invalid character numbers.
* The C++11 `<type_traits>` header was included regardless of the C++ version.
  (Github issue [#6896](https://github.com/cython/cython/issues/6896 "https://github.com/cython/cython/issues/6896"))
* `PyDict_GetItemStringRef()` was accidentally used in older Limited API versions.
  (Github issue [#6914](https://github.com/cython/cython/issues/6914 "https://github.com/cython/cython/issues/6914"))
* `abort()` was used but not always available in the Limited API.
  (Github issue [#6918](https://github.com/cython/cython/issues/6918 "https://github.com/cython/cython/issues/6918"))
* Some dependencies were missing from the `depfile`.
  (Github issue [#6938](https://github.com/cython/cython/issues/6938 "https://github.com/cython/cython/issues/6938"))
* Embedded function signatures were not always separated from the existing docstring.
  (Github issue [#6904](https://github.com/cython/cython/issues/6904 "https://github.com/cython/cython/issues/6904"))
* `numpy.math` was missing from `Cython/Includes/` and could not be cimported.
  (Github issue [#6859](https://github.com/cython/cython/issues/6859 "https://github.com/cython/cython/issues/6859"))
* Some tests were adapted for NumPy 2.x.
  (Github issue [#6898](https://github.com/cython/cython/issues/6898 "https://github.com/cython/cython/issues/6898"))
* Some C compiler warnings were fixed.
  (Github issue [#6870](https://github.com/cython/cython/issues/6870 "https://github.com/cython/cython/issues/6870"))
* `Cython.Build` was not officially exposing the `cythonize` function.
  (Github issue [#6934](https://github.com/cython/cython/issues/6934 "https://github.com/cython/cython/issues/6934"))

## 3.1.1 (2025-05-19)[¶](#id10 "Link to this heading")

### Bugs fixed[¶](#id11 "Link to this heading")

* A reference leak in the async delegation code was fixed.
  (Github issues [#6850](https://github.com/cython/cython/issues/6850 "https://github.com/cython/cython/issues/6850"), [#6878](https://github.com/cython/cython/issues/6878 "https://github.com/cython/cython/issues/6878"))
* Conditional if-else expressions mixing Python and C (numeric) types could end up
  inferring an overly tight result type, thus leading to unexpected type conversions,
  runtime exceptions on assignment, or incorrect “temporary assignment” compile errors.
  (Github issue [#6854](https://github.com/cython/cython/issues/6854 "https://github.com/cython/cython/issues/6854"))
* Some Limited API issues were resolved.
  (Github issue [#6862](https://github.com/cython/cython/issues/6862 "https://github.com/cython/cython/issues/6862"))
* Large C `long long` values could be truncated when passed into PyPy.
  (Github issue [#6890](https://github.com/cython/cython/issues/6890 "https://github.com/cython/cython/issues/6890"))
* `callable()` incorrectly reported `False` in PyPy for classes with metaclasses.
  Patch by Anatolii Aniskovych. (Github issue [#6892](https://github.com/cython/cython/issues/6892 "https://github.com/cython/cython/issues/6892"))
* The signature of fused functions was no longer introspectable in Cython 3.1.0.
  (Github issue [#6855](https://github.com/cython/cython/issues/6855 "https://github.com/cython/cython/issues/6855"))
* Coroutines could generate invalid C with line tracing enabled.
  (Github issue [#6865](https://github.com/cython/cython/issues/6865 "https://github.com/cython/cython/issues/6865"))
* Code using `complex()` could generate invalid C code missing type declarations.
  (Github issue [#6860](https://github.com/cython/cython/issues/6860 "https://github.com/cython/cython/issues/6860"))
* Code using e.g. `list[int | None]` outside of variable/argument annotations failed to compile.
  (Github issue [#6856](https://github.com/cython/cython/issues/6856 "https://github.com/cython/cython/issues/6856"))
* Code using ctuples in a `const` context could generate invalid C.
  (Github issue [#6864](https://github.com/cython/cython/issues/6864 "https://github.com/cython/cython/issues/6864"))
* Accessing special methods on cpdef enums failed to compile.
* Some C compiler warnings were resolved.
  Patches by Daniel Larraz. (Github issues [#6876](https://github.com/cython/cython/issues/6876 "https://github.com/cython/cython/issues/6876"), [#3172](https://github.com/cython/cython/issues/3172 "https://github.com/cython/cython/issues/3172"), [#6873](https://github.com/cython/cython/issues/6873 "https://github.com/cython/cython/issues/6873"), [#6877](https://github.com/cython/cython/issues/6877 "https://github.com/cython/cython/issues/6877"))
* Re-establish support for PyPy 3.8.
  (Github issue [#6867](https://github.com/cython/cython/issues/6867 "https://github.com/cython/cython/issues/6867"))

## 3.1.0 (2025-05-08)[¶](#id12 "Link to this heading")

### Other changes[¶](#id13 "Link to this heading")

* No functional changes since 3.1.0 rc 2.

## 3.1.0 rc 2 (2025-05-07)[¶](#rc-2-2025-05-07 "Link to this heading")

### Features added[¶](#id14 "Link to this heading")

* Declarations for C++ `std::stop_token` were added as `libcpp.stop_token` to provide
  additional low-level synchronisation primitives also in the light of free-threading Python.
  (Github issue [#6820](https://github.com/cython/cython/issues/6820 "https://github.com/cython/cython/issues/6820"))
* The generation of the shared module now happens automatically from `cythonize()` in a
  `setuptools` build if a corresponding `Extension` has been configured.
  This avoids an additional step outside of the `setup.py` or `pip wheel` run.
  (Github issue [#6842](https://github.com/cython/cython/issues/6842 "https://github.com/cython/cython/issues/6842"))

### Bugs fixed[¶](#id15 "Link to this heading")

* Variables typed as builtin Python exception types now accept subtypes instead of rejecting them.
  This specifically impacted types like `BaseException`, `Exception` or `OSError`,
  which almost always intend to reference subtypes.
  (Github issue [#6828](https://github.com/cython/cython/issues/6828 "https://github.com/cython/cython/issues/6828"))
* Functions with more than 10 constant default argument values could generate invalid C code.
  (Github issue [#6843](https://github.com/cython/cython/issues/6843 "https://github.com/cython/cython/issues/6843"))
* The `call_once()` function argument in `libc.threads` (new in 3.1) was changed to require
  a `nogil` declaration, as semantically implied. Code that used it with a callback function
  expecting to hold the GIL must change the callback code to use `with gil`.
* Calling cimported C functions with their fully qualified package name could crash Cython.
  (Github issue [#6551](https://github.com/cython/cython/issues/6551 "https://github.com/cython/cython/issues/6551"))
* Naming a variable after its inferred type (e.g. `str += ""`) could trigger an infinite loop in Cython.
  (Github issue [#6835](https://github.com/cython/cython/issues/6835 "https://github.com/cython/cython/issues/6835"))
* Cython is more relaxed about the exact C++ constructor name when it calls `new()` on ctypedefs.
  (Github issue [#6821](https://github.com/cython/cython/issues/6821 "https://github.com/cython/cython/issues/6821"))
* Using `cpp_locals` in nogil sections could crash.
  (Github issue [#6838](https://github.com/cython/cython/issues/6838 "https://github.com/cython/cython/issues/6838"))
* `const struct` declarations could lead to invalid assignments to `const` temp variables.
  (Github issue [#6804](https://github.com/cython/cython/issues/6804 "https://github.com/cython/cython/issues/6804"))
* A refcounting error was fixed in the method class cell support code.
  (Github issue [#6839](https://github.com/cython/cython/issues/6839 "https://github.com/cython/cython/issues/6839"))

## 3.1.0 rc 1 (2025-05-01)[¶](#rc-1-2025-05-01 "Link to this heading")

### Features added[¶](#id16 "Link to this heading")

* `cython.pymutex` provides a fast mutex by wrapping the new `PyMutex` feature of recent
  CPython versions (including free-threading) and falls back to `PyThread` locks in older Pythons.
  (Github issue [#6579](https://github.com/cython/cython/issues/6579 "https://github.com/cython/cython/issues/6579"))
* A new directive `subinterpreters_compatible=shared_gil/own_gil` was added to allow modules
  to declare support for subinterpreters.
  (Github issue [#6513](https://github.com/cython/cython/issues/6513 "https://github.com/cython/cython/issues/6513"))
* `divmod()` is also optimised for C floating point types and can be called on C number types
  without holding the GIL.
  (Github issue [#6801](https://github.com/cython/cython/issues/6801 "https://github.com/cython/cython/issues/6801"))
* New C++ declarations were added.
  (Github issues [#6625](https://github.com/cython/cython/issues/6625 "https://github.com/cython/cython/issues/6625"), [#6731](https://github.com/cython/cython/issues/6731 "https://github.com/cython/cython/issues/6731"))
* `embedsignature` now works for special methods (if they have a docstring).
  (Github issue [#1577](https://github.com/cython/cython/issues/1577 "https://github.com/cython/cython/issues/1577"))

### Bugs fixed[¶](#id17 "Link to this heading")

* Iterating over literal sequences in generator expressions could generate invalid C code.
  (Github issue [#6725](https://github.com/cython/cython/issues/6725 "https://github.com/cython/cython/issues/6725"))
* Tracing could generate invalid C code.
  (Github issue [#6781](https://github.com/cython/cython/issues/6781 "https://github.com/cython/cython/issues/6781"))
* Non-ASCII function argument names could generate invalid C code.
  (Github issue [#6813](https://github.com/cython/cython/issues/6813 "https://github.com/cython/cython/issues/6813"))
* Optimised `divmod()` calls could produce incorrect results in beta-1 due to incorrect C type usage.
  (Github issue [#6786](https://github.com/cython/cython/issues/6786 "https://github.com/cython/cython/issues/6786"))
* Raising `UnboundLocalError` could fail for non-ascii variable names.
  (Github issue [#6800](https://github.com/cython/cython/issues/6800 "https://github.com/cython/cython/issues/6800"))
* The signature of `PyByteArray_Resize()` in `cpython.bytearray` failed to propagate exceptions.
  Patch by Kirill Smelkov. (Github issue [#6787](https://github.com/cython/cython/issues/6787 "https://github.com/cython/cython/issues/6787"))
* Some more issues with the Limited C-API and free-threading Python were resolved.

  [https://github.com/cython/cython/issues?q=label%3A%22limited+api%22](https://github.com/cython/cython/issues?q=label%3A%22limited+api%22 "https://github.com/cython/cython/issues?q=label%3A%22limited+api%22")

  [https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22](https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22 "https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22")
* The signature of `cythonize_one()` accidentally changed in 3.1.0b1.
  (Github issue [#6815](https://github.com/cython/cython/issues/6815 "https://github.com/cython/cython/issues/6815"))

### Other changes[¶](#id18 "Link to this heading")

* Named `cpdef enums` no longer copy their item names into the global module namespace.
  This was considered unhelpful for named enums which already live in their own class namespace.
  In cases where the old behaviour was desired, users can add the following backwards compatible
  command after their enum class definition: `globals().update(getattr(TheUserEnumClass, '__members__'))`.
  Anonymous enums still produce global item names, as before.
  (Github issue [#4571](https://github.com/cython/cython/issues/4571 "https://github.com/cython/cython/issues/4571"))

## 3.1.0 beta 1 (2025-04-03)[¶](#beta-1-2025-04-03 "Link to this heading")

### Features added[¶](#id19 "Link to this heading")

* Global `cdef const …` variables are supported.
  (Github issue [#6542](https://github.com/cython/cython/issues/6542 "https://github.com/cython/cython/issues/6542"))
* A new context manager / function decorator `cython.critical_section` was added
  wrapping Python’s critical section C-API feature.
  (Github issues [#6516](https://github.com/cython/cython/issues/6516 "https://github.com/cython/cython/issues/6516"), [#6577](https://github.com/cython/cython/issues/6577 "https://github.com/cython/cython/issues/6577"))
* Some common Cython-internal code (currently only memoryview related) can now be extracted
  into a shared extension module to reduce the installed overall size of a package with many
  Cython compiled modules.
  (Github issue [#2356](https://github.com/cython/cython/issues/2356 "https://github.com/cython/cython/issues/2356"))
* The type of `prange` loop targets is now inferred.
  (Github issue [#6585](https://github.com/cython/cython/issues/6585 "https://github.com/cython/cython/issues/6585"))
* Extracting keyword arguments is faster in some cases.
  (Github issue [#6683](https://github.com/cython/cython/issues/6683 "https://github.com/cython/cython/issues/6683"))
* Calling `divmod()` on any C integer types is efficient.
  (Github issue [#6717](https://github.com/cython/cython/issues/6717 "https://github.com/cython/cython/issues/6717"))
* Some async/coroutine/vectorcall code has improved fast-paths.
  (Github issues [#6732](https://github.com/cython/cython/issues/6732 "https://github.com/cython/cython/issues/6732"), [#6735](https://github.com/cython/cython/issues/6735 "https://github.com/cython/cython/issues/6735"), [#6736](https://github.com/cython/cython/issues/6736 "https://github.com/cython/cython/issues/6736"), [#6738](https://github.com/cython/cython/issues/6738 "https://github.com/cython/cython/issues/6738"), [#6742](https://github.com/cython/cython/issues/6742 "https://github.com/cython/cython/issues/6742"), [#6771](https://github.com/cython/cython/issues/6771 "https://github.com/cython/cython/issues/6771"))
* Calls to Python builtins and extension types use the vectorcall protocol.
  (Github issue [#6744](https://github.com/cython/cython/issues/6744 "https://github.com/cython/cython/issues/6744"))
* Method calls use `PyObject_VectorcallMethod()` where possible.
  (Github issue [#6747](https://github.com/cython/cython/issues/6747 "https://github.com/cython/cython/issues/6747"))
* Some C-API shortcuts were (re-)added.
  (Github issue [#6761](https://github.com/cython/cython/issues/6761 "https://github.com/cython/cython/issues/6761"))
* Cython can avoid normalising exceptions in an except clause if it knows that they are unused.
  (Github issue [#6601](https://github.com/cython/cython/issues/6601 "https://github.com/cython/cython/issues/6601"))
* The `cython` command has a new option `--cache` to cache generated files.
  (Github issue [#6091](https://github.com/cython/cython/issues/6091 "https://github.com/cython/cython/issues/6091"))
* The `cythonize` command has a new option `--timeit` to benchmark Cython code snippets.
  (Github issue [#6697](https://github.com/cython/cython/issues/6697 "https://github.com/cython/cython/issues/6697"))
* The argument parsing `cygdb` command was improved based on `argparse`.
  Patch by William Ayd. (Github issue [#5499](https://github.com/cython/cython/issues/5499 "https://github.com/cython/cython/issues/5499"))
* The `PyWeakref_GetRef` declaration was added to `cpython.weakref` and backported.
  Patch by Lysandros Nikolaou. (Github issue [#6478](https://github.com/cython/cython/issues/6478 "https://github.com/cython/cython/issues/6478"))
* `std::span` declarations were added to `libcpp`.
  Patch by Alexander Condello. (Github issue [#6539](https://github.com/cython/cython/issues/6539 "https://github.com/cython/cython/issues/6539"))
* `std::string_view` declarations were added to `libcpp`.
  Patch by Antoine Pitrou. (Github issue [#6539](https://github.com/cython/cython/issues/6539 "https://github.com/cython/cython/issues/6539"))
* Mutex declarations for `libc` and `libcpp` were added.
  (Github issue [#6610](https://github.com/cython/cython/issues/6610 "https://github.com/cython/cython/issues/6610"))
* Several C++ declarations were improved and extended.
  Patches by Yury V. Zaytsev. (Github issues [#488](https://github.com/cython/cython/issues/488 "https://github.com/cython/cython/issues/488"), [#489](https://github.com/cython/cython/issues/489 "https://github.com/cython/cython/issues/489"))
* Bazel build rules were updated for better interoperability.
  Patch by maleo. (Github issue [#6478](https://github.com/cython/cython/issues/6478 "https://github.com/cython/cython/issues/6478"))
* The `Demos/benchmarks/` directory include a new benchmark runner that can run selected
  benchmarks against different Cython git revisions.

### Bugs fixed[¶](#id20 "Link to this heading")

* Many issues with the Limited C-API and free-threading Python were resolved.
  This includes better thread-safety of Cython-internal types like functions and generators.

  [https://github.com/cython/cython/issues?q=label%3A%22limited+api%22](https://github.com/cython/cython/issues?q=label%3A%22limited+api%22 "https://github.com/cython/cython/issues?q=label%3A%22limited+api%22")

  [https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22](https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22 "https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22")
* `for-in` loops could generate invalid code for C++ containers.
  Patch by Taras Kozlov. (Github issue [#6578](https://github.com/cython/cython/issues/6578 "https://github.com/cython/cython/issues/6578"))
* `PyDict_GetItemRef()` and `PyList_GetItemRef()` were not always used correctly.
  Patch by Lisandro Dalcin. (Github issue [#6647](https://github.com/cython/cython/issues/6647 "https://github.com/cython/cython/issues/6647"))
* Inlined calls to local functions could crash with `binding=False`.
  (Github issue [#6556](https://github.com/cython/cython/issues/6556 "https://github.com/cython/cython/issues/6556"))
* Calling `sorted()` could crash in 3.1.0a1.
  (Github issue [#6496](https://github.com/cython/cython/issues/6496 "https://github.com/cython/cython/issues/6496"))
* Calling 0-arg methods was unnecessarily slow in 3.1.0a1.
  (Github issue [#6730](https://github.com/cython/cython/issues/6730 "https://github.com/cython/cython/issues/6730"))
* A crash when reading the interpreter ID was fixed.
* Crashes while tracing C function returns were resolved.
  (Github issue [#6503](https://github.com/cython/cython/issues/6503 "https://github.com/cython/cython/issues/6503"))
* A compiler crash on `complex/complex` was resolved.
  (Github issue [#6552](https://github.com/cython/cython/issues/6552 "https://github.com/cython/cython/issues/6552"))
* A compiler crash when using the `cpp_locals` directive was resolved.
  (Github issue [#6370](https://github.com/cython/cython/issues/6370 "https://github.com/cython/cython/issues/6370"))
* Name mangling did not work correctly for attributes of extension types that have reserved C names.
  (Github issue [#6678](https://github.com/cython/cython/issues/6678 "https://github.com/cython/cython/issues/6678"))
* Declaring a `@staticmethod` in a pxd file and overriding it in a subclass could
  trigger incorrect “declared but not defined” errors.
  Patch by Aditya Pillai. (Github issue [#6714](https://github.com/cython/cython/issues/6714 "https://github.com/cython/cython/issues/6714"))
* Cython’s fake code objects are now compatible with GraalPython.
  (Github issue [#6409](https://github.com/cython/cython/issues/6409 "https://github.com/cython/cython/issues/6409"))
* Stepping through foreign code with `cygdb` could fail with an `IndexError`.
  Patch by clayote. (Github issue [#6552](https://github.com/cython/cython/issues/6552 "https://github.com/cython/cython/issues/6552"))
* Some PyPy incompatibilities were resolved.
  Patches by Matti Picus. (Github issue [#6592](https://github.com/cython/cython/issues/6592 "https://github.com/cython/cython/issues/6592"), [#6640](https://github.com/cython/cython/issues/6640 "https://github.com/cython/cython/issues/6640"))
* Interoperability with recent Pythran releases was fixed.
  (Github issue [#6494](https://github.com/cython/cython/issues/6494 "https://github.com/cython/cython/issues/6494"))
* The `gdb` compatibility of `cygdb` was improved.
  Patch by Kent Slaney. (Github issue [#6681](https://github.com/cython/cython/issues/6681 "https://github.com/cython/cython/issues/6681"))
* Some redundant exception normalisation work was removed in Python 3.12+.
  (Github issue [#6599](https://github.com/cython/cython/issues/6599 "https://github.com/cython/cython/issues/6599"))
* A compiler hang introduced in 3.1a1 when overriding methods was resolved.
  Patch by Aditya Pillai. (Github issue [#6704](https://github.com/cython/cython/issues/6704 "https://github.com/cython/cython/issues/6704"))
* A compiler crash was resolved when trying to issue a warning.
  Patch by Gabriele N. Tornetta. (Github issue [#6711](https://github.com/cython/cython/issues/6711 "https://github.com/cython/cython/issues/6711"))
* Some incomplete import time “safety checks” from 3.1.0a1 were removed again.
  (Github issue [#6671](https://github.com/cython/cython/issues/6671 "https://github.com/cython/cython/issues/6671"))
* Using the `common_utility_include_dir` option in parallel builds on Windows could fail.
* Some “unused” warnings from the C compiler were resolved.
  Patches by Lisandro Dalcin. (Github issue [#6726](https://github.com/cython/cython/issues/6726 "https://github.com/cython/cython/issues/6726"))

### Other changes[¶](#id21 "Link to this heading")

* All Cython-internal types (functions, coroutines, …) are now heap types and use type specs.
  (Github issue [#6633](https://github.com/cython/cython/issues/6633 "https://github.com/cython/cython/issues/6633"))
* Tracing/monitoring is now disabled in parallel/prange sections.
  (Github issue [#6709](https://github.com/cython/cython/issues/6709 "https://github.com/cython/cython/issues/6709"))
* The `numpy.math` cimport module has been deprecated.
  Usages should be replaced by `libc.math`.
  (Github issue [#6743](https://github.com/cython/cython/issues/6743 "https://github.com/cython/cython/issues/6743"))
* Includes all fixes as of Cython 3.0.12.

## 3.1.0 alpha 1 (2024-11-08)[¶](#alpha-1-2024-11-08 "Link to this heading")

### Features added[¶](#id22 "Link to this heading")

* Support for freethreading builds of CPython 3.13 was added.
  It comes with a new directive `freethreading_compatible=True` to mark modules as
  free-threading compatible (`Py_mod_gil`).

  [https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22](https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22 "https://github.com/cython/cython/issues?q=label%3A%22nogil+CPython%22")

  Patches by Lysandros Nikolaou and Nathan Goldbaum. (Github issue [#6162](https://github.com/cython/cython/issues/6162 "https://github.com/cython/cython/issues/6162"))
* Support for monitoring Cython modules via sys.monitoring in CPython 3.13+ was added.
  For coverage reporting, this needs to be disabled with -DCYTHON\_USE\_SYS\_MONITORING=0
  as long as coverage.py does not support sys.monitoring for coverage plugins.
  (Github issue [#6144](https://github.com/cython/cython/issues/6144 "https://github.com/cython/cython/issues/6144"))
* Many issues with the Limited C-API were resolved.
  It is now sufficient to define the macro `Py_LIMITED_API` to activate the support.

  [https://github.com/cython/cython/issues?q=label%3A%22limited+api%22](https://github.com/cython/cython/issues?q=label%3A%22limited+api%22 "https://github.com/cython/cython/issues?q=label%3A%22limited+api%22")
* Support for GraalPython was improved (but is still incomplete).
* Several issues with the gdb support were resolved.
  Patches by Kent Slaney. (Github issues [#5955](https://github.com/cython/cython/issues/5955 "https://github.com/cython/cython/issues/5955"), [#5948](https://github.com/cython/cython/issues/5948 "https://github.com/cython/cython/issues/5948"))
* `typing.Union[SomeType, None]` and `SomeType | None` are now understood and mean
  the same as `typing.Optional[SomeType]`, allowing `None` in type checks.
  (Github issue [#6254](https://github.com/cython/cython/issues/6254 "https://github.com/cython/cython/issues/6254"))
* `cython.const[]` and `cython.volatile[]` are now available as type modifiers in Python code.
  (Github issue [#5728](https://github.com/cython/cython/issues/5728 "https://github.com/cython/cython/issues/5728"))
* `cython.pointer[SomeCType]` can now be used to define pointer types in Python type annotations.
  (Github issue [#5071](https://github.com/cython/cython/issues/5071 "https://github.com/cython/cython/issues/5071"))
* Several improvements were made to reduce the size of the resulting extension modules.
  (Github issue [#4425](https://github.com/cython/cython/issues/4425 "https://github.com/cython/cython/issues/4425"))
* Function calls now use the PEP-590 Vectorcall protocol, even when passing keyword arguments.
  (Github issues [#5804](https://github.com/cython/cython/issues/5804 "https://github.com/cython/cython/issues/5804"))
* Coroutines now use the `am_send` slot function instead of going through a Python `.send()` call.
  This has been backported for Python 3.7 - 3.9.
  (Github issues [#4585](https://github.com/cython/cython/issues/4585 "https://github.com/cython/cython/issues/4585"))
* `__set_name__` is called when assigning to class attributes.
  (Github issue [#6179](https://github.com/cython/cython/issues/6179 "https://github.com/cython/cython/issues/6179"))
* Most builtin methods now provide their return type for type inference.
  (Github issues [#4829](https://github.com/cython/cython/issues/4829 "https://github.com/cython/cython/issues/4829"), [#5865](https://github.com/cython/cython/issues/5865 "https://github.com/cython/cython/issues/5865"), [#6412](https://github.com/cython/cython/issues/6412 "https://github.com/cython/cython/issues/6412"))
* Method calls on builtin literal values are evaluated at compile time, if applicable.
  (Github issue [#6383](https://github.com/cython/cython/issues/6383 "https://github.com/cython/cython/issues/6383"))
* The Python `int` type now maps directly to `PyLong` and is inferred accordingly.
  (Github issue [#4237](https://github.com/cython/cython/issues/4237 "https://github.com/cython/cython/issues/4237"))
* Integer operations on known `int` types are faster.
  (Github issue [#5785](https://github.com/cython/cython/issues/5785 "https://github.com/cython/cython/issues/5785"))
* f-strings are faster in some cases.
  (Github issues [#5866](https://github.com/cython/cython/issues/5866 "https://github.com/cython/cython/issues/5866"), [#6342](https://github.com/cython/cython/issues/6342 "https://github.com/cython/cython/issues/6342"), [#6383](https://github.com/cython/cython/issues/6383 "https://github.com/cython/cython/issues/6383"))
* `divmod()` is faster on C `int`.
  Patch by Tong He. (Github issue [#6073](https://github.com/cython/cython/issues/6073 "https://github.com/cython/cython/issues/6073"))
* `dict.pop()` is faster in some cases.
  (Github issue [#5911](https://github.com/cython/cython/issues/5911 "https://github.com/cython/cython/issues/5911"))
* `.isprintable()` is optimised for Unicode characters.
  (Github issue [#3277](https://github.com/cython/cython/issues/3277 "https://github.com/cython/cython/issues/3277"))
* `x in ()` and similar tests against empty constant sequences (e.g. in generated code)
  are now discarded if they have no side-effects.
  (Github issue [#6288](https://github.com/cython/cython/issues/6288 "https://github.com/cython/cython/issues/6288"))
* Constant (non-GC) Python objects are no longer traversed with `Py_VISIT()` during GC runs.
  (Github issue [#6277](https://github.com/cython/cython/issues/6277 "https://github.com/cython/cython/issues/6277"))
* C++ classes implemented in Cython can now use method overloading.
  Patch by samaingw. (Github issue [#3235](https://github.com/cython/cython/issues/3235 "https://github.com/cython/cython/issues/3235"))
* Assigning a Python container to a C++ vector now makes use of `__length_hint__`
  to avoid reallocations.
  Patch by Denis Lukianov. (Github issue [#6077](https://github.com/cython/cython/issues/6077 "https://github.com/cython/cython/issues/6077"))
* The C++11 `emplace*` methods were added to `libcpp.deque`.
  Patch by Somin An. (Github issue [#6159](https://github.com/cython/cython/issues/6159 "https://github.com/cython/cython/issues/6159"))
* `cpython.time` was updated and extended for Python 3.13.
  (Github issue [#6187](https://github.com/cython/cython/issues/6187 "https://github.com/cython/cython/issues/6187"))
* Dataclasses support the `match_args` option.
  (Github issue [#5381](https://github.com/cython/cython/issues/5381 "https://github.com/cython/cython/issues/5381"))
* Threading in parallel sections can now be disabled with a new `use_threads_if` condition.
  (Github issue [#5919](https://github.com/cython/cython/issues/5919 "https://github.com/cython/cython/issues/5919"))
* New options `warn.deprecated.DEF` and `warn.deprecated.IF` can silence the deprecation warnings.
  Patch by Eric Larson. (Github issue [#6243](https://github.com/cython/cython/issues/6243 "https://github.com/cython/cython/issues/6243"))
* `cygdb` shows more helpful output for some objects.
  Patch by Kent Slaney. (Github issue [#5958](https://github.com/cython/cython/issues/5958 "https://github.com/cython/cython/issues/5958"))
* Bazel build support for improved.
  Patch by mering. (Github issue [#6452](https://github.com/cython/cython/issues/6452 "https://github.com/cython/cython/issues/6452"))
* The parser was updated for Unicode 15.1 (as provided by CPython 3.13b4).

### Bugs fixed[¶](#id23 "Link to this heading")

* C functions used different start lines and columns for error reporting and tracing
  than Python functions. They now use the line and column of their first decorator
  or (if none) their definition line, as in Python.
  (Github issue [#6366](https://github.com/cython/cython/issues/6366 "https://github.com/cython/cython/issues/6366"))
* Dataclasses did not handle default fields without init value correctly.
  (Github issue [#5858](https://github.com/cython/cython/issues/5858 "https://github.com/cython/cython/issues/5858"))
* Implementing a special method based on another could lead to infinite recursion.
  (Github issue [#5863](https://github.com/cython/cython/issues/5863 "https://github.com/cython/cython/issues/5863"))
* The `__class__` cell variable in methods was not always working as in Python.
  Initial patch by Tom Keefe. (Github issue [#2912](https://github.com/cython/cython/issues/2912 "https://github.com/cython/cython/issues/2912"))
* Lambda functions had no code objects. Their signature can now be introspected.
  (Github issue [#2983](https://github.com/cython/cython/issues/2983 "https://github.com/cython/cython/issues/2983"))
* Subtyping complex as extension type could fail.
  (Github issue [#6346](https://github.com/cython/cython/issues/6346 "https://github.com/cython/cython/issues/6346"))
* `hasattr()` now propagates exceptions that occur during lookup.
  (Github issue [#6269](https://github.com/cython/cython/issues/6269 "https://github.com/cython/cython/issues/6269"))
* The base type of extension heap types is now traversed during GC runs in Py3.9+.
  (Github issue [#4193](https://github.com/cython/cython/issues/4193 "https://github.com/cython/cython/issues/4193"))
* The Python `&` operator could touch invalid memory with certain `0` values in Python <= 3.10.
  Patch by Michael J. Sullivan. (Github issue [#4193](https://github.com/cython/cython/issues/4193 "https://github.com/cython/cython/issues/4193"))
* Exception values were not always recognised as equal at compile time.
  (Github issue [#5709](https://github.com/cython/cython/issues/5709 "https://github.com/cython/cython/issues/5709"))
* Running Cython in different Python versions could generate slightly different C code
  due to differences in the builtins.
  (Github issue [#5591](https://github.com/cython/cython/issues/5591 "https://github.com/cython/cython/issues/5591"))
* The common\_include\_dir feature used different file paths in the C code on Windows and Posix.
  It now uses forward slashes as directory separator consistently.
  (Github issue [#6355](https://github.com/cython/cython/issues/6355 "https://github.com/cython/cython/issues/6355"))
* File paths in the C code are now relative to the build directory.
  Patch by Oscar Benjamin. (Github issue [#6341](https://github.com/cython/cython/issues/6341 "https://github.com/cython/cython/issues/6341"))
* depfiles now use relative paths whenever possible.
  Patch by Loïc Estève. (Github issue [#6345](https://github.com/cython/cython/issues/6345 "https://github.com/cython/cython/issues/6345"))
* The `-a` option in the IPython magic no longer copies the complete HTML document
  into the notebook but only a more reasonable content snippet.
  Patch by Min RK. (Github issue [#5760](https://github.com/cython/cython/issues/5760 "https://github.com/cython/cython/issues/5760"))
* Uselessly referring to C enums (not enum values) as Python objects is now rejected.
  Patch by Vyas Ramasubramani. (Github issue [#5638](https://github.com/cython/cython/issues/5638 "https://github.com/cython/cython/issues/5638"))
* Cython no longer acquires the GIL during in-place assignments to C attributes in nogil sections.
  Patch by Mads Ynddal. (Github issue [#6407](https://github.com/cython/cython/issues/6407 "https://github.com/cython/cython/issues/6407"))
* Several C++ warnings about `char*` casts were resolved.
  (Github issues [#5515](https://github.com/cython/cython/issues/5515 "https://github.com/cython/cython/issues/5515"), [#5847](https://github.com/cython/cython/issues/5847 "https://github.com/cython/cython/issues/5847"))
* C++ undefined behaviour was fixed in an error handling case.
  (Github issue [#5278](https://github.com/cython/cython/issues/5278 "https://github.com/cython/cython/issues/5278"))
* Dict assignments to struct members with reserved C/C++ names could generate invalid C code.
* The PEP-479 implementation could raise a visible `RuntimeError` without
  a trace of the original `StopIteration`.
  (Github issue [#5953](https://github.com/cython/cython/issues/5953 "https://github.com/cython/cython/issues/5953"))
* A crash was fixed when assigning a zero-length slice to a memoryview.
  Patch by Michael Man. (Github issue [#6227](https://github.com/cython/cython/issues/6227 "https://github.com/cython/cython/issues/6227"))
* Conditionally assigning to variables with the walrus operator could crash.
  (Github issue [#6094](https://github.com/cython/cython/issues/6094 "https://github.com/cython/cython/issues/6094"))
* Unterminated string literals could lock up the build in an infinite loop.
  (Github issue [#5977](https://github.com/cython/cython/issues/5977 "https://github.com/cython/cython/issues/5977"))
* Exporting C functions uses better platform compatible code.
  (Github issue [#4683](https://github.com/cython/cython/issues/4683 "https://github.com/cython/cython/issues/4683"))
* The shebang in `libpython.py` was incorrect.
  Patch by Luke Hamburg. (Github issue [#6439](https://github.com/cython/cython/issues/6439 "https://github.com/cython/cython/issues/6439"))
* Cython now uses SHA-256 instead of SHA-1 for caching etc. as the latter may not be
  available on all Python installations.
  (Github issue [#6354](https://github.com/cython/cython/issues/6354 "https://github.com/cython/cython/issues/6354"))

### Other changes[¶](#id24 "Link to this heading")

* Support for Python 2.7 - 3.7 was removed, along with large chunks of legacy code.
  (Github issue [#2800](https://github.com/cython/cython/issues/2800 "https://github.com/cython/cython/issues/2800"))
* The pxd files `cpython.int`, `cpython.cobject`, `cpython.oldbuffer` and `cpython.string`
  were removed as they refer to C-API declarations that are only in Python 2.x.
  (Github issue [#5870](https://github.com/cython/cython/issues/5870 "https://github.com/cython/cython/issues/5870"))
* The generated C code now requires a C99 compatible C compiler.
* `language_level=3` is now the default.
  `language_level=3str` has become a legacy alias.
  (Github issue [#5827](https://github.com/cython/cython/issues/5827 "https://github.com/cython/cython/issues/5827"))
* The Py2 types `unicode` and `basestring` are now deprecated and have become aliases
  of the `str` type.
  (Github issue [#6374](https://github.com/cython/cython/issues/6374 "https://github.com/cython/cython/issues/6374"))
* Docstrings now strip their leading whitespace according to PEP-257.
  Patch by Lawrence Mitchell. (Github issue [#6241](https://github.com/cython/cython/issues/6241 "https://github.com/cython/cython/issues/6241"))
* Type checkers should have it easier to find and validate Cython types in .py files.
  (Github issue [#4327](https://github.com/cython/cython/issues/4327 "https://github.com/cython/cython/issues/4327"))
* The previously shipped NumPy C-API declarations (`cimport numpy`) were removed.
  NumPy has been providing version specific declarations for several versions now.
  (Github issue [#5842](https://github.com/cython/cython/issues/5842 "https://github.com/cython/cython/issues/5842"))
* Usages of the outdated `WITH_THREAD` macro guard were removed.
  (Github issue [#5812](https://github.com/cython/cython/issues/5812 "https://github.com/cython/cython/issues/5812"))
* The options for showing the C code line in Python exception stack traces were cleaned up.
  Previously, disabling the option with the `CYTHON_CLINE_IN_TRACEBACK` macro did not
  reduce the code overhead of the feature, and the `c_line_in_traceback` compile option
  was partly redundant with the C macro switches and lead to warnings about unused code.
  Since this is considered mostly a debug feature, the new default is that it is \_disabled\_
  to avoid code and runtime overhead. It can be enabled by setting the C macro to 1, and
  a new macro `CYTHON_CLINE_IN_TRACEBACK_RUNTIME` was added that controls the runtime
  configurable setting if the feature is enabled, which was previously only available
  through the compile option. The compile option is now deprecated (but still available),
  and users should migrate to using the two C macros only.
  (Github issue [#6036](https://github.com/cython/cython/issues/6036 "https://github.com/cython/cython/issues/6036"))
* Includes all fixes as of Cython 3.0.11 (but generates C99 code in some places).

## 3.0.12 (2025-02-11)[¶](#id25 "Link to this heading")

### Bugs fixed[¶](#id26 "Link to this heading")

* Release 3.0.11 introduced some incorrect `noexcept` warnings.
  (Github issue [#6335](https://github.com/cython/cython/issues/6335 "https://github.com/cython/cython/issues/6335"))
* Conditional assignments to variables using the walrus operator could crash.
  (Github issue [#6094](https://github.com/cython/cython/issues/6094 "https://github.com/cython/cython/issues/6094"))
* Dict assignments to struct members with reserved C names could generate invalid C code.
* Fused ctuples with the same entry types but different sizes could fail to compile.
  (Github issue [#6328](https://github.com/cython/cython/issues/6328 "https://github.com/cython/cython/issues/6328"))
* In Py3, pyximport was not searching sys.path when looking for importable source files.
  (Github issue [#5615](https://github.com/cython/cython/issues/5615 "https://github.com/cython/cython/issues/5615"))
* Using & 0 on integers produced with int.from\_bytes() could read invalid memory on Python 3.10.
  (Github issue [#6480](https://github.com/cython/cython/issues/6480 "https://github.com/cython/cython/issues/6480"))
* Modules could fail to compile in PyPy 3.11 due to missing CPython specific header files.
  Patch by Matti Picus. (Github issue [#6482](https://github.com/cython/cython/issues/6482 "https://github.com/cython/cython/issues/6482"))
* Minor fix in C++ `partial_sum()` declaration.

## 3.0.11 (2024-08-05)[¶](#id27 "Link to this heading")

### Features added[¶](#id28 "Link to this heading")

* The C++11 `emplace*` methods were added to `libcpp.deque`.
  Patch by Somin An. (Github issue [#6159](https://github.com/cython/cython/issues/6159 "https://github.com/cython/cython/issues/6159"))

### Bugs fixed[¶](#id29 "Link to this heading")

* The exception check value of functions declared in pxd files was not always applied in 3.0.10.
  (Github issue [#6122](https://github.com/cython/cython/issues/6122 "https://github.com/cython/cython/issues/6122"))
* A crash on exception deallocations was fixed.
  (Github issue [#6022](https://github.com/cython/cython/issues/6022 "https://github.com/cython/cython/issues/6022"))
* A crash was fixed when assigning a zero-length slice to a memoryview.
  Patch by Michael Man. (Github issue [#6227](https://github.com/cython/cython/issues/6227 "https://github.com/cython/cython/issues/6227"))
* `libcpp.optional.value()` could crash if it raised a C++ exception.
  Patch by Alexander Condello. (Github issue [#6190](https://github.com/cython/cython/issues/6190 "https://github.com/cython/cython/issues/6190"))
* The return type of `str()` was mishandled, leading to crashes with `language_level=3`.
  (Github issue [#6166](https://github.com/cython/cython/issues/6166 "https://github.com/cython/cython/issues/6166"))
* `bytes.startswith/endswith()` failed for non-bytes substrings (e.g. `bytearray`).
  (Github issue [#6168](https://github.com/cython/cython/issues/6168 "https://github.com/cython/cython/issues/6168"))
* Fused ctuples crashed Cython.
  (Github issue [#6068](https://github.com/cython/cython/issues/6068 "https://github.com/cython/cython/issues/6068"))
* A compiler crash was fixed when using extension types in fused types.
  (Github issue [#6204](https://github.com/cython/cython/issues/6204 "https://github.com/cython/cython/issues/6204"))
* The module cleanup code was incorrect for globally defined memory view slices.
  (Github issue [#6276](https://github.com/cython/cython/issues/6276 "https://github.com/cython/cython/issues/6276"))
* Some adaptations were made to enable compilation in Python 3.13.
  (Github issues [#5997](https://github.com/cython/cython/issues/5997 "https://github.com/cython/cython/issues/5997"), [#6182](https://github.com/cython/cython/issues/6182 "https://github.com/cython/cython/issues/6182"), [#6251](https://github.com/cython/cython/issues/6251 "https://github.com/cython/cython/issues/6251"))

## 3.0.10 (2024-03-30)[¶](#id30 "Link to this heading")

### Bugs fixed[¶](#id31 "Link to this heading")

* Cython generated incorrect self-casts when directly calling final methods of subtypes.
  Patch by Lisandro Dalcin. (Github issue [#2747](https://github.com/cython/cython/issues/2747 "https://github.com/cython/cython/issues/2747"))
* Internal C names generated from C function signatures could become too long for MSVC.
  (Github issue [#6052](https://github.com/cython/cython/issues/6052 "https://github.com/cython/cython/issues/6052"))
* The `noexcept` warnings could be misleading in some cases.
  Patch by Gonzalo Tornaría. (Github issue [#6087](https://github.com/cython/cython/issues/6087 "https://github.com/cython/cython/issues/6087"))
* The `@cython.ufunc` implementation could generate incomplete C code.
  (Github issue [#6064](https://github.com/cython/cython/issues/6064 "https://github.com/cython/cython/issues/6064"))
* The `libcpp.complex` declarations could result in incorrect C++ code.
  Patch by Raffi Enficiaud. (Github issue [#6037](https://github.com/cython/cython/issues/6037 "https://github.com/cython/cython/issues/6037"))
* Several tests were adapted to work with both NumPy 1.x and 2.0.
  Patch by Matti Picus. (Github issues [#6076](https://github.com/cython/cython/issues/6076 "https://github.com/cython/cython/issues/6076"), [#6100](https://github.com/cython/cython/issues/6100 "https://github.com/cython/cython/issues/6100"))
* C compiler warnings when the freelist implementation is disabled (e.g. on PyPy) were fixed.
  It can now be disabled explicitly with the C macro guard `CYTHON_USE_FREELISTS=0`.
  (Github issue [#6099](https://github.com/cython/cython/issues/6099 "https://github.com/cython/cython/issues/6099"))
* Some C macro guards for feature flags were missing from the NOGIL Python configuration.
* Some recently added builtins were unconditionally looked up at module import time
  (if used by user code) that weren’t available on all Python versions and could thus
  fail the import.
* A performance hint regarding exported pxd declarations was improved.
  (Github issue [#6001](https://github.com/cython/cython/issues/6001 "https://github.com/cython/cython/issues/6001"))

## 3.0.9 (2024-03-05)[¶](#id32 "Link to this heading")

### Features added[¶](#id33 "Link to this heading")

* Assigning `const` values to non-const variables now issues a warning.
  (Github issue [#5639](https://github.com/cython/cython/issues/5639 "https://github.com/cython/cython/issues/5639"))
* Using `noexcept` on a function returning Python objects now issues a warning.
  (Github issue [#5661](https://github.com/cython/cython/issues/5661 "https://github.com/cython/cython/issues/5661"))
* Some C-API usage was updated for the upcoming CPython 3.13.
  Patches by Victor Stinner et al. (Github issues [#6003](https://github.com/cython/cython/issues/6003 "https://github.com/cython/cython/issues/6003"), [#6020](https://github.com/cython/cython/issues/6020 "https://github.com/cython/cython/issues/6020"))
* The deprecated `Py_UNICODE` type is no longer used, unless required by user code.
  (Github issue [#5982](https://github.com/cython/cython/issues/5982 "https://github.com/cython/cython/issues/5982"))
* `std::string.replace()` declarations were added to libcpp.string.
  Patch by Kieran Geary. (Github issue [#6037](https://github.com/cython/cython/issues/6037 "https://github.com/cython/cython/issues/6037"))

### Bugs fixed[¶](#id34 "Link to this heading")

* Cython generates incorrect (but harmless) self-casts when directly calling
  final methods of subtypes. Lacking a better solution, the errors that recent
  gcc versions produce have been silenced for the time being.
  Original patch by Michał Górny. (Github issue [#2747](https://github.com/cython/cython/issues/2747 "https://github.com/cython/cython/issues/2747"))
* Unused variable warnings about clineno were fixed when C lines in tracebacks are disabled.
  (Github issue [#6035](https://github.com/cython/cython/issues/6035 "https://github.com/cython/cython/issues/6035"))
* Subclass deallocation of extern classes could crash if the base class uses GC.
  Original patch by Jason Fried. (Github issue [#5971](https://github.com/cython/cython/issues/5971 "https://github.com/cython/cython/issues/5971"))
* Type checks for Python `memoryview` could use an invalid C function.
  Patch by Xenia Lu. (Github issue [#5988](https://github.com/cython/cython/issues/5988 "https://github.com/cython/cython/issues/5988"))
* Calling final fused functions could generate invalid C code.
  (Github issue [#5989](https://github.com/cython/cython/issues/5989 "https://github.com/cython/cython/issues/5989"))
* Declaring extern enums multiple times could generate invalid C code.
  (Github issue [#5905](https://github.com/cython/cython/issues/5905 "https://github.com/cython/cython/issues/5905"))
* `pyximport` used relative paths incorrectly.
  Patch by Stefano Rivera. (Github issue [#5957](https://github.com/cython/cython/issues/5957 "https://github.com/cython/cython/issues/5957"))
* Running Cython with globbing characters (`[]*?`) in the module search path could fail.
  Patch by eewanco. (Github issue [#5942](https://github.com/cython/cython/issues/5942 "https://github.com/cython/cython/issues/5942"))
* Literal strings that include braces could change the C code indentation.

### Other changes[¶](#id35 "Link to this heading")

* The “enum class not importable” warning is now only issued once per enum type.
  (Github issue [#5941](https://github.com/cython/cython/issues/5941 "https://github.com/cython/cython/issues/5941"))

## 3.0.8 (2024-01-10)[¶](#id36 "Link to this heading")

### Bugs fixed[¶](#id37 "Link to this heading")

* Using `const` together with defined fused types could fail to compile.
  (Github issue [#5230](https://github.com/cython/cython/issues/5230 "https://github.com/cython/cython/issues/5230"))
* A “use after free” bug was fixed in parallel sections.
  (Github issue [#5922](https://github.com/cython/cython/issues/5922 "https://github.com/cython/cython/issues/5922"))
* Several types were not available as `cython.*` types in pure Python code.
* The generated code is now correct C89 again, removing some C++ style `//` comments
  and C99-style declaration-after-code code ordering. This is still relevant for some
  ols C compilers, specifically ones that match old Python 2.7 installations.

## 3.0.7 (2023-12-19)[¶](#id38 "Link to this heading")

### Bugs fixed[¶](#id39 "Link to this heading")

* In the iterator of generator expressions, `await` and `yield` were not correctly analysed.
  (Github issue [#5851](https://github.com/cython/cython/issues/5851 "https://github.com/cython/cython/issues/5851"))
* `cpdef` enums with the same name cimported from different modules could lead to
  invalid C code.
  (Github issue [#5887](https://github.com/cython/cython/issues/5887 "https://github.com/cython/cython/issues/5887"))
* Some declarations in `cpython.unicode` were fixed and extended.
  (Github issue [#5902](https://github.com/cython/cython/issues/5902 "https://github.com/cython/cython/issues/5902"))
* Compiling fused types used in pxd files could crash Cython in Python 3.11+.
  (Github issues [#5894](https://github.com/cython/cython/issues/5894 "https://github.com/cython/cython/issues/5894"), [#5588](https://github.com/cython/cython/issues/5588 "https://github.com/cython/cython/issues/5588"))
* Source files with non-ASCII file names could crash Cython.
  (Github issue [#5873](https://github.com/cython/cython/issues/5873 "https://github.com/cython/cython/issues/5873"))
* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the [0.29.37 (2023-12-18)](#id124 "#id124") release.

## 3.0.6 (2023-11-26)[¶](#id40 "Link to this heading")

### Features added[¶](#id41 "Link to this heading")

* Fused def function dispatch is a bit faster.
* Declarations for the `wchar` PyUnicode API were added.
  (Github issue [#5836](https://github.com/cython/cython/issues/5836 "https://github.com/cython/cython/issues/5836"))
* The Python “nogil” fork is now also detected with the new `Py_GIL_DISABLED` macro.
  Patch by Hugo van Kemenade. (Github issue [#5852](https://github.com/cython/cython/issues/5852 "https://github.com/cython/cython/issues/5852"))

### Bugs fixed[¶](#id42 "Link to this heading")

* Comparing dataclasses could give different results than Python.
  (Github issue [#5857](https://github.com/cython/cython/issues/5857 "https://github.com/cython/cython/issues/5857"))
* `float(std::string)` generated invalid C code.
  (Github issue [#5818](https://github.com/cython/cython/issues/5818 "https://github.com/cython/cython/issues/5818"))
* Using `cpdef` functions with `cimport_from_pyx` failed.
  (Github issue [#5795](https://github.com/cython/cython/issues/5795 "https://github.com/cython/cython/issues/5795"))
* A crash was fixed when string-formatting a Python value fails.
  (Github issue [#5787](https://github.com/cython/cython/issues/5787 "https://github.com/cython/cython/issues/5787"))
* On item access, Cython could try the sequence protocol before the mapping protocol
  in some cases if an object supports both.
  (Github issue [#5776](https://github.com/cython/cython/issues/5776 "https://github.com/cython/cython/issues/5776"))
* A C compiler warning was resolved.
  (Github issue [#5794](https://github.com/cython/cython/issues/5794 "https://github.com/cython/cython/issues/5794"))
* Complex numbers failed to compile in MSVC with C11.
  Patch by Lysandros Nikolaou. (Github issue [#5809](https://github.com/cython/cython/issues/5809 "https://github.com/cython/cython/issues/5809"))
* Some issues with the Limited API and with PyPy were resolved.
  (Github issues [#5695](https://github.com/cython/cython/issues/5695 "https://github.com/cython/cython/issues/5695"), [#5696](https://github.com/cython/cython/issues/5696 "https://github.com/cython/cython/issues/5696"))
* A C++ issue in Python 3.13 was resolved.
  (Github issue [#5790](https://github.com/cython/cython/issues/5790 "https://github.com/cython/cython/issues/5790"))
* Several directives are now also available (as no-ops) in Python code.
  (Github issue [#5803](https://github.com/cython/cython/issues/5803 "https://github.com/cython/cython/issues/5803"))
* An error message was corrected.
  Patch by Mads Ynddal. (Github issue [#5805](https://github.com/cython/cython/issues/5805 "https://github.com/cython/cython/issues/5805"))

## 3.0.5 (2023-10-31)[¶](#id43 "Link to this heading")

### Features added[¶](#id44 "Link to this heading")

* Preliminary support for CPython 3.13a1 was added to allow early testing.
  (Github issue [#5767](https://github.com/cython/cython/issues/5767 "https://github.com/cython/cython/issues/5767"))

### Bugs fixed[¶](#id45 "Link to this heading")

* A compiler crash was fixed.
  (Github issue [#5771](https://github.com/cython/cython/issues/5771 "https://github.com/cython/cython/issues/5771"))
* A typo in the `always_allow_keywords` directive for Python code was fixed.
  Patch by lk-1984. (Github issue [#5772](https://github.com/cython/cython/issues/5772 "https://github.com/cython/cython/issues/5772"))
* Some C compiler warnings were resolved.
  Patch by Pierre Jolivet. (Github issue [#5780](https://github.com/cython/cython/issues/5780 "https://github.com/cython/cython/issues/5780"))

## 3.0.4 (2023-10-17)[¶](#id46 "Link to this heading")

### Features added[¶](#id47 "Link to this heading")

* A new compiler directive `show_performance_hints` was added to disable the
  newly added performance hint output.
  (Github issue [#5748](https://github.com/cython/cython/issues/5748 "https://github.com/cython/cython/issues/5748"))

### Bugs fixed[¶](#id48 "Link to this heading")

* ``` `cythonize` required ``distutils ``` even for operations that did not build binaries.
  (Github issue [#5751](https://github.com/cython/cython/issues/5751 "https://github.com/cython/cython/issues/5751"))
* A regression in 3.0.3 was fixed that prevented calling inline functions
  from another inline function in `.pxd` files.
  (Github issue [#5748](https://github.com/cython/cython/issues/5748 "https://github.com/cython/cython/issues/5748"))
* Some C compiler warnings were resolved.
  Patch by Pierre Jolivet. (Github issue [#5756](https://github.com/cython/cython/issues/5756 "https://github.com/cython/cython/issues/5756"))

## 3.0.3 (2023-10-05)[¶](#id49 "Link to this heading")

### Features added[¶](#id50 "Link to this heading")

* More warnings were added to help users migrate and avoid bugs.
  (Github issue [#5650](https://github.com/cython/cython/issues/5650 "https://github.com/cython/cython/issues/5650"))
* A warning-like category for performance hints was added that bypasses `-Werror`.
  (Github issue [#5673](https://github.com/cython/cython/issues/5673 "https://github.com/cython/cython/issues/5673"))
* FastGIL now uses standard `thread_local` in C++.
  (Github issue [#5640](https://github.com/cython/cython/issues/5640 "https://github.com/cython/cython/issues/5640"))
* `reference_wrapper` was added to `libcpp.functional`.
  Patch by Vyas Ramasubramani. (Github issue [#5671](https://github.com/cython/cython/issues/5671 "https://github.com/cython/cython/issues/5671"))
* The `cythonize` command now supports the `--cplus` option known from the `cython` command.
  (Github issue [#5736](https://github.com/cython/cython/issues/5736 "https://github.com/cython/cython/issues/5736"))

### Bugs fixed[¶](#id51 "Link to this heading")

* Performance regressions where the GIL was needlessly acquired were fixed.
  (Github issues [#5670](https://github.com/cython/cython/issues/5670 "https://github.com/cython/cython/issues/5670"), [#5700](https://github.com/cython/cython/issues/5700 "https://github.com/cython/cython/issues/5700"))
* A reference leak for exceptions in Python 3.12 was resolved.
  Patch by Eric Johnson. (Github issue [#5724](https://github.com/cython/cython/issues/5724 "https://github.com/cython/cython/issues/5724"))
* `fastcall` calls with keyword arguments generated incorrect C code.
  (Github issue [#5665](https://github.com/cython/cython/issues/5665 "https://github.com/cython/cython/issues/5665"))
* Assigning the type converted result of a conditional (if-else) expression
  to `int` or `bool` variables could lead to incorrect C code.
  (Github issue [#5731](https://github.com/cython/cython/issues/5731 "https://github.com/cython/cython/issues/5731"))
* Early (unlikely) failures in Python function wrappers no longer set a
  traceback in order to simplify the C code flow. Being mostly memory
  allocation errors, they probably would never have created a traceback anyway.
  (Github issue [#5681](https://github.com/cython/cython/issues/5681 "https://github.com/cython/cython/issues/5681"))
* Relative cimports from packages with `__init__.py` files could fail.
  (Github issue [#5715](https://github.com/cython/cython/issues/5715 "https://github.com/cython/cython/issues/5715"))
* Several issues with the Limited API support were resolved.
  (Github issues [#5641](https://github.com/cython/cython/issues/5641 "https://github.com/cython/cython/issues/5641"), [#5648](https://github.com/cython/cython/issues/5648 "https://github.com/cython/cython/issues/5648"), [#5689](https://github.com/cython/cython/issues/5689 "https://github.com/cython/cython/issues/5689"))
* The code generated for special-casing both Cython functions and PyCFunctions was cleaned up
  to avoid calling C-API functions that were not meant for the other type respectively.
  This could previously trigger assertions in CPython debug builds and now also plays better
  with the Limited API.
  (Github issues [#4804](https://github.com/cython/cython/issues/4804 "https://github.com/cython/cython/issues/4804"), [#5739](https://github.com/cython/cython/issues/5739 "https://github.com/cython/cython/issues/5739"))
* Fix some C compiler warnings.
  Patches by Ralf Gommers, Oleksandr Pavlyk, Sebastian Koslowski et al.
  (Github issues [#5651](https://github.com/cython/cython/issues/5651 "https://github.com/cython/cython/issues/5651"), [#5663](https://github.com/cython/cython/issues/5663 "https://github.com/cython/cython/issues/5663"), [#5668](https://github.com/cython/cython/issues/5668 "https://github.com/cython/cython/issues/5668"), [#5717](https://github.com/cython/cython/issues/5717 "https://github.com/cython/cython/issues/5717"), [#5726](https://github.com/cython/cython/issues/5726 "https://github.com/cython/cython/issues/5726"), [#5734](https://github.com/cython/cython/issues/5734 "https://github.com/cython/cython/issues/5734"))
* Generating gdb debugging information failed when using generator expressions.
  Patch by Oleksandr Pavlyk. (Github issue [#5552](https://github.com/cython/cython/issues/5552 "https://github.com/cython/cython/issues/5552"))
* Passing a `setuptools.Extension` into `cythonize()` instead of a
  `distutils.Extension` could make it miss the matching extensions.
* `cython -M` needlessly required `distutils`, which made it fail in Python 3.12.
  (Github issue [#5681](https://github.com/cython/cython/issues/5681 "https://github.com/cython/cython/issues/5681"))

### Other changes[¶](#id52 "Link to this heading")

* The visible deprecation warning for `DEF` was removed again since it proved
  difficult for some users to migrate away from it. The statement is still
  meant to be removed at some point (and thus, like `IF`, should not be
  used in new code), but the time for sunset is probably not around the corner.
  (Github issue [#4310](https://github.com/cython/cython/issues/4310 "https://github.com/cython/cython/issues/4310"))
* The `np_pythran` option raise a `DeprecationWarning` if it receives other values
  than `True` and `False`. This will eventually be disallowed (in line with all
  other boolean options).

## 3.0.2 (2023-08-27)[¶](#id53 "Link to this heading")

### Bugs fixed[¶](#id54 "Link to this heading")

* Using `None` as default value for arguments annotated as `int` could crash Cython.
  (Github issue [#5643](https://github.com/cython/cython/issues/5643 "https://github.com/cython/cython/issues/5643"))
* Default values of fused types that include `complex` could generate invalid C code
  with `-DCYTHON_CCOMPLEX=0`.
  (Github issue [#5644](https://github.com/cython/cython/issues/5644 "https://github.com/cython/cython/issues/5644"))
* Using C++ enum class types in extension type method signatures could generate invalid C code.
  (Github issue [#5637](https://github.com/cython/cython/issues/5637 "https://github.com/cython/cython/issues/5637"))

## 3.0.1 (2023-08-25)[¶](#id55 "Link to this heading")

### Features added[¶](#id56 "Link to this heading")

* The error messages regarding exception declarations were improved in order to give
  better help about possible reasons and fixes.
  (Github issue [#5547](https://github.com/cython/cython/issues/5547 "https://github.com/cython/cython/issues/5547"))

### Bugs fixed[¶](#id57 "Link to this heading")

* Memory view types in Python argument annotations no longer accept `None`. They now
  require an explicit `Optional[]` or a `None` default value in order to allow `None`
  to be passed. This was an oversight in the 3.0.0 release and is a BACKWARDS INCOMPATIBLE
  change. However, since it only applies to code using Python syntax, it probably only
  applies to newly written code that was written for Cython 3.0 and can easily be adapted.
  In most cases, we expect that this change will avoid bugs in user code rather than
  produce problems.
  (Github issue [#5612](https://github.com/cython/cython/issues/5612 "https://github.com/cython/cython/issues/5612"))
* `nogil` functions using parallel code could freeze when called with the GIL held.
  (Github issues [#5564](https://github.com/cython/cython/issues/5564 "https://github.com/cython/cython/issues/5564"), [#5573](https://github.com/cython/cython/issues/5573 "https://github.com/cython/cython/issues/5573"))
* Relative cimports could end up searching globally and find the same package installed
  elsewhere, potentially in another version.
  (Github issue [#5511](https://github.com/cython/cython/issues/5511 "https://github.com/cython/cython/issues/5511"))
* Attribute lookups on known standard library modules could accidentally search
  in the module namespace instead.
  (Github issue [#5536](https://github.com/cython/cython/issues/5536 "https://github.com/cython/cython/issues/5536"))
* Using constructed C++ default arguments could generate invalid C++ code.
  (Github issue [#5553](https://github.com/cython/cython/issues/5553 "https://github.com/cython/cython/issues/5553"))
* `libcpp.memory.make_unique()` was lacking C++ exception handling.
  (Github issue [#5560](https://github.com/cython/cython/issues/5560 "https://github.com/cython/cython/issues/5560"))
* Some non-public and deprecated CAPI usages were replaced by public
  (and thus more future proof) API code.
* Many issues with the Limited API support were resolved.
  Patches by Lisandro Dalcin et al.
  (Github issues [#5549](https://github.com/cython/cython/issues/5549 "https://github.com/cython/cython/issues/5549"), [#5550](https://github.com/cython/cython/issues/5550 "https://github.com/cython/cython/issues/5550"), [#5556](https://github.com/cython/cython/issues/5556 "https://github.com/cython/cython/issues/5556"), [#5605](https://github.com/cython/cython/issues/5605 "https://github.com/cython/cython/issues/5605"), [#5617](https://github.com/cython/cython/issues/5617 "https://github.com/cython/cython/issues/5617"))
* Some C compiler warnings were resolved.
  Patches by Matti Picus et al. (Github issues [#5557](https://github.com/cython/cython/issues/5557 "https://github.com/cython/cython/issues/5557"), [#5555](https://github.com/cython/cython/issues/5555 "https://github.com/cython/cython/issues/5555"))
* Large Python integers are now stored in hex instead of decimal strings to work around
  security limits in Python and generally speed up their Python object creation.
* `NULL` could not be used as default for fused type pointer arguments.
  (Github issue [#5554](https://github.com/cython/cython/issues/5554 "https://github.com/cython/cython/issues/5554"))
* C functions that return pointer types now return `NULL` as default exception value.
  Previously, calling code wasn’t aware of this and always tested for raised exceptions.
  (Github issue [#5554](https://github.com/cython/cython/issues/5554 "https://github.com/cython/cython/issues/5554"))
* Untyped literal default arguments in fused functions could generate invalid C code.
  (Github issue [#5614](https://github.com/cython/cython/issues/5614 "https://github.com/cython/cython/issues/5614"))
* C variables declared as `const` could generate invalid C code when used in closures,
  generator expressions, ctuples, etc.
  (Github issues [#5558](https://github.com/cython/cython/issues/5558 "https://github.com/cython/cython/issues/5558"), [#5333](https://github.com/cython/cython/issues/5333 "https://github.com/cython/cython/issues/5333"))
* Enums could not refer to previously defined enums in their definition.
  (Github issue [#5602](https://github.com/cython/cython/issues/5602 "https://github.com/cython/cython/issues/5602"))
* The Python conversion code for anonymous C enums conflicted with regular int conversion.
  (Github issue [#5623](https://github.com/cython/cython/issues/5623 "https://github.com/cython/cython/issues/5623"))
* Using memory views for property methods (and other special methods) could lead to
  refcounting problems.
  (Github issue [#5571](https://github.com/cython/cython/issues/5571 "https://github.com/cython/cython/issues/5571"))
* Star-imports could generate code that tried to assign to constant C macros like
  `PY_SSIZE_T_MAX` and `PY_SSIZE_T_MIN`.
  Patch by Philipp Wagner. (Github issue [#5562](https://github.com/cython/cython/issues/5562 "https://github.com/cython/cython/issues/5562"))
* `CYTHON_USE_TYPE_SPECS` can now be (explicitly) enabled in PyPy.
* The template parameter “delimeters” in the Tempita `Template` class was corrected
  to “delimiters”. The old spelling is still available in the main template API but
  now issues a `DeprecationWarning`.
  (Github issue [#5608](https://github.com/cython/cython/issues/5608 "https://github.com/cython/cython/issues/5608"))
* The `cython --version` output is now less likely to reach both stdout and stderr.
  Patch by Eli Schwartz. (Github issue [#5504](https://github.com/cython/cython/issues/5504 "https://github.com/cython/cython/issues/5504"))
* The sdist was missing the Shadow.pyi stub file.

## 3.0.0 unified release notes[¶](#unified-release-notes "Link to this heading")

Cython 3.0.0 has been a very large effort that cleaned up many old warts,
introduced many new features, and introduces a couple of intentional
behaviour changes, even though the goal remained to stay compatible as
much as possible with Cython 0.29.x. For details, see the [migration guide](https://cython.readthedocs.io/en/latest/src/userguide/migrating_to_cy30.html "https://cython.readthedocs.io/en/latest/src/userguide/migrating_to_cy30.html").

As the development was spread out over several years, a lot of things have
happened in the meantime. Many crucial bugfixes and some features were
backported to 0.29.x and are not strictly speaking “new” in Cython 3.0.0.

## Major themes in 3.0.0[¶](#major-themes-in-3-0-0 "Link to this heading")

### Compatibility with CPython and the Python C API[¶](#compatibility-with-cpython-and-the-python-c-api "Link to this heading")

Since Cython 3.0.0 started development, CPython 3.8-3.11 were released.
All these are supported in Cython, including experimental support for the
in-development CPython 3.12. On the other end of the spectrum, support for
Python 2.6 was dropped.

Cython interacts very closely with the C-API of Python, which is where most
of the adaptation work happens.

#### Related changes[¶](#related-changes "Link to this heading")

* The long deprecated include files `python_*`, `stdio`, `stdlib` and
  `stl` in `Cython/Includes/Deprecated/` were removed. Use the `libc.*`
  and `cpython.*` pxd modules instead.
  Patch by Jeroen Demeyer. (Github issue [#2904](https://github.com/cython/cython/issues/2904 "https://github.com/cython/cython/issues/2904"))
* The `Py_hash_t` type failed to accept arbitrary “index” values.
  (Github issue [#2752](https://github.com/cython/cython/issues/2752 "https://github.com/cython/cython/issues/2752"))
* `@cython.trashcan(True)` can be used on an extension type to enable the
  CPython [Enabling the deallocation trashcan](userguide/extension_types.html#trashcan "userguide/extension_types.html#trashcan"). This allows deallocating deeply recursive objects
  without overflowing the stack. Patch by Jeroen Demeyer. (Github issue [#2842](https://github.com/cython/cython/issues/2842 "https://github.com/cython/cython/issues/2842"))
* `PyEval_InitThreads()` is no longer used in Py3.7+ where it is a no-op.
* A low-level inline function `total_seconds(timedelta)` was added to
  `cpython.datetime` to bypass the Python method call. Note that this function
  is not guaranteed to give exactly the same results for very large time intervals.
  Patch by Brock Mendel. (Github issue [#3616](https://github.com/cython/cython/issues/3616 "https://github.com/cython/cython/issues/3616"))
* The internal CPython macro `Py_ISSPACE()` is no longer used.
  Original patch by Andrew Jones. (Github issue [#4111](https://github.com/cython/cython/issues/4111 "https://github.com/cython/cython/issues/4111"))
* The value `PyBUF_MAX_NDIM` was added to the `cpython.buffer` module.
  Patch by John Kirkham. (Github issue [#3811](https://github.com/cython/cython/issues/3811 "https://github.com/cython/cython/issues/3811"))
* A new module `cpython.time` was added with some low-level alternatives to
  Python’s `time` module.
  Patch by Brock Mendel. (Github issue [#3767](https://github.com/cython/cython/issues/3767 "https://github.com/cython/cython/issues/3767"))
* More C-API declarations for `cpython.datetime` were added.
  Patch by Bluenix2. (Github issue [#4128](https://github.com/cython/cython/issues/4128 "https://github.com/cython/cython/issues/4128"))
* C-API declarations for context variables in Python 3.7 were added.
  Original patch by Zolisa Bleki. (Github issue [#2281](https://github.com/cython/cython/issues/2281 "https://github.com/cython/cython/issues/2281"))
* C-API declarations for `cpython.fileobject` were added.
  Patch by Zackery Spytz. (Github issue [#3906](https://github.com/cython/cython/issues/3906 "https://github.com/cython/cython/issues/3906"))
* The signature of `PyFloat_FromString()` in `cpython.float` was changed
  to match the signature in Py3. It still has an automatic fallback for Py2.
  (Github issue [#3909](https://github.com/cython/cython/issues/3909 "https://github.com/cython/cython/issues/3909"))
* `PyMem_[Raw]Calloc()` was added to the `cpython.mem` declarations.
  Note that the `Raw` versions are no longer #defined by Cython. The previous
  macros were not considered safe.
  Patch by William Schwartz and David Woods. (Github issue [#3047](https://github.com/cython/cython/issues/3047 "https://github.com/cython/cython/issues/3047"))
* The runtime size check for imported `PyVarObject` types was improved
  to reduce false positives and adapt to Python 3.11.
  Patch by David Woods. (Github issues [#4827](https://github.com/cython/cython/issues/4827 "https://github.com/cython/cython/issues/4827"), [#4894](https://github.com/cython/cython/issues/4894 "https://github.com/cython/cython/issues/4894"))
* The generated C code failed to compile in CPython 3.11a4 and later.
  (Github issue [#4500](https://github.com/cython/cython/issues/4500 "https://github.com/cython/cython/issues/4500"))
* `pyximport` no longer uses the deprecated `imp` module.
  Patch by Matúš Valo. (Github issue [#4560](https://github.com/cython/cython/issues/4560 "https://github.com/cython/cython/issues/4560"))
* Improvements to `PyTypeObject` definitions in pxd wrapping of libpython.
  Patch by John Kirkham. (Github issue [#4699](https://github.com/cython/cython/issues/4699 "https://github.com/cython/cython/issues/4699"))
* Some old usages of the deprecated Python `imp` module were replaced with `importlib`.
  Patch by Matúš Valo. (Github issue [#4640](https://github.com/cython/cython/issues/4640 "https://github.com/cython/cython/issues/4640"))
* `cpdef` enums no longer use `OrderedDict` but `dict` in Python 3.6 and later.
  Patch by GalaxySnail. (Github issue [#5180](https://github.com/cython/cython/issues/5180 "https://github.com/cython/cython/issues/5180"))
* Several problems with CPython 3.12 were resolved.
  (Github issue [#5238](https://github.com/cython/cython/issues/5238 "https://github.com/cython/cython/issues/5238"))
* The exception handling code was adapted to CPython 3.12.
  (Github issue [#5442](https://github.com/cython/cython/issues/5442 "https://github.com/cython/cython/issues/5442"))
* The Python `int` handling code was adapted to make use of the new `PyLong`
  internals in CPython 3.12.
  (Github issue [#5353](https://github.com/cython/cython/issues/5353 "https://github.com/cython/cython/issues/5353"))
* A compile error when using `__debug__` was resolved.
* The deprecated `_PyGC_FINALIZED()` C-API macro is no longer used.
  Patch by Thomas Caswell and Matúš Valo. (Github issue [#5481](https://github.com/cython/cython/issues/5481 "https://github.com/cython/cython/issues/5481"))
* A crash in Python 2.7 was fixed when cleaning up extension type instances
  at program end.

### Compatibility with other Python implementations[¶](#compatibility-with-other-python-implementations "Link to this heading")

Cython tries to support other Python implementations, largely on a best-effort
basis. The most advanced support exists for PyPy, which is tested in our CI
and considered supported.

#### Related changes[¶](#id58 "Link to this heading")

* An unsupported C-API call in PyPy was fixed.
  Patch by Max Bachmann. (Github issue [#4055](https://github.com/cython/cython/issues/4055 "https://github.com/cython/cython/issues/4055"))
* Support for the now unsupported Pyston V1 was removed in favour of Pyston V2.
  Patch by Marius Wachtler. (Github issue [#4211](https://github.com/cython/cython/issues/4211 "https://github.com/cython/cython/issues/4211"))
* A C compiler warning in PyPy3 regarding `PyEval_EvalCode()` was resolved.
* Some compatibility issues with PyPy were resolved.
  Patches by Max Bachmann, Matti Picus.
  (Github issues [#4454](https://github.com/cython/cython/issues/4454 "https://github.com/cython/cython/issues/4454"), [#4477](https://github.com/cython/cython/issues/4477 "https://github.com/cython/cython/issues/4477"), [#4478](https://github.com/cython/cython/issues/4478 "https://github.com/cython/cython/issues/4478"), [#4509](https://github.com/cython/cython/issues/4509 "https://github.com/cython/cython/issues/4509"), [#4517](https://github.com/cython/cython/issues/4517 "https://github.com/cython/cython/issues/4517"))
* An initial set of adaptations for GraalVM Python was implemented. Note that
  this does not imply any general support for this target or that your code
  will work at all in this environment. But testing should be possible now.
  Patch by David Woods. (Github issue [#4328](https://github.com/cython/cython/issues/4328 "https://github.com/cython/cython/issues/4328"))
* A work-around for StacklessPython < 3.8 was disabled in Py3.8 and later.
  (Github issue [#4329](https://github.com/cython/cython/issues/4329 "https://github.com/cython/cython/issues/4329"))

### Initial support for Limited API[¶](#initial-support-for-limited-api "Link to this heading")

CPython provides a stable, limited subset of its C-API as the so-called Limited API.
This C-API comes with the guarantee of a stable ABI, meaning that extensions modules
that were compiled for one version of CPython can also be imported in later versions
without recompilation.

There is initial support for this in Cython. By defining the `CYTHON_LIMITED_API`
macro, Cython cuts down its C-API usage and tries to adhere to the Limited C-API,
probably at the cost of a bit of performance.
In order to get full benefit from the limited API you will also need to define the
CPython macro `Py_LIMITED_API` to a specific CPython compatibility version,
which additionally restricts the C-API during the C compilation,
thus enforcing the forward compatibility of the extension module.

Note that “initial support” in Cython really means that setting the `Py_LIMITED_API`
macro will almost certainly not yet work for your specific code.
There are limitations in the Limited C-API
that are difficult for Cython to generate C code for, so some advanced Python features
(like async code) may not lead to C code that cannot adhere to the Limited C-API, or
where Cython simply does not know yet how to adhere to it. Basically, if you get your
code to compile with both macros set, and it passes your test suite, then it should be
possible to import the extension module also in later CPython versions.

The experimental feature flags `CYTHON_USE_MODULE_STATE` and
`CYTHON_USE_TYPE_SPECS` enable some individual aspects of the Limited API
implementation independently.

#### Related changes[¶](#id59 "Link to this heading")

* Preliminary support for the CPython’s `Py_LIMITED_API` (stable ABI) is
  available by setting the `CYTHON_LIMITED_API` C macro. Note that the
  support is currently in an early stage and many features do not yet work.
  You currently still have to define `Py_LIMITED_API` externally in order
  to restrict the API usage. This will change when the feature stabilises.
  Patches by Eddie Elizondo and David Woods. (Github issues [#3223](https://github.com/cython/cython/issues/3223 "https://github.com/cython/cython/issues/3223"),
  [#3311](https://github.com/cython/cython/issues/3311 "https://github.com/cython/cython/issues/3311"), [#3501](https://github.com/cython/cython/issues/3501 "https://github.com/cython/cython/issues/3501"))
* Limited API support was improved.
  Patches by Matthias Braun. (Github issues [#3693](https://github.com/cython/cython/issues/3693 "https://github.com/cython/cython/issues/3693"), [#3707](https://github.com/cython/cython/issues/3707 "https://github.com/cython/cython/issues/3707"))
* New C feature flags: `CYTHON_USE_MODULE_STATE`, `CYTHON_USE_TYPE_SPECS`
  Both are currently considered experimental.
  (Github issue [#3611](https://github.com/cython/cython/issues/3611 "https://github.com/cython/cython/issues/3611"))
* `_Py_TPFLAGS_HAVE_VECTORCALL` was always set on extension types when using the limited API.
  Patch by David Woods. (Github issue [#4453](https://github.com/cython/cython/issues/4453 "https://github.com/cython/cython/issues/4453"))
* Limited API C preprocessor warning is compatible with MSVC. Patch by
  Victor Molina Garcia. (Github issue [#4826](https://github.com/cython/cython/issues/4826 "https://github.com/cython/cython/issues/4826"))
* The embedding code no longer calls deprecated C-API functions but uses the new `PyConfig`
  API instead on CPython versions that support it (3.8+).
  Patch by Alexander Shadchin. (Github issue [#4895](https://github.com/cython/cython/issues/4895 "https://github.com/cython/cython/issues/4895"))
* Some C code issue were resolved for the Limited API target.
  (Github issues [#5264](https://github.com/cython/cython/issues/5264 "https://github.com/cython/cython/issues/5264"), [#5265](https://github.com/cython/cython/issues/5265 "https://github.com/cython/cython/issues/5265"), [#5266](https://github.com/cython/cython/issues/5266 "https://github.com/cython/cython/issues/5266"))
* Conversion of Python ints to C `int128` is now always supported, although slow
  if dedicated C-API support is missing (`_PyLong_AsByteArray()`), specifically in
  the Limited C-API.
  (Github issue [#5419](https://github.com/cython/cython/issues/5419 "https://github.com/cython/cython/issues/5419"))
* Custom buffer slot methods are now supported in the Limited C-API of Python 3.9+.
  Patch by Lisandro Dalcin. (Github issue [#5422](https://github.com/cython/cython/issues/5422 "https://github.com/cython/cython/issues/5422"))

### Improved fidelity to Python semantics[¶](#improved-fidelity-to-python-semantics "Link to this heading")

#### Implemented PEPs[¶](#implemented-peps "Link to this heading")

* [PEP-3131](https://www.python.org/dev/peps/pep-3131 "https://www.python.org/dev/peps/pep-3131"): Supporting Non-ASCII Identifiers (Github issue [#2601](https://github.com/cython/cython/issues/2601 "https://github.com/cython/cython/issues/2601"))
* [PEP-479](https://www.python.org/dev/peps/pep-0479 "https://www.python.org/dev/peps/pep-0479"): generator\_stop (enabled by default for language\_level=3) (Github issue [#2580](https://github.com/cython/cython/issues/2580 "https://github.com/cython/cython/issues/2580"))
* [PEP-487](https://www.python.org/dev/peps/pep-0487 "https://www.python.org/dev/peps/pep-0487"): Simpler customisation of class creation (Github issue [#2781](https://github.com/cython/cython/issues/2781 "https://github.com/cython/cython/issues/2781"))
* [PEP-563](https://www.python.org/dev/peps/pep-0563 "https://www.python.org/dev/peps/pep-0563"): Postponed Evaluation of Annotations (Github issue [#3285](https://github.com/cython/cython/issues/3285 "https://github.com/cython/cython/issues/3285"))
* [PEP-570](https://www.python.org/dev/peps/pep-0570 "https://www.python.org/dev/peps/pep-0570"): Positional-Only Parameters (Github issue [#2915](https://github.com/cython/cython/issues/2915 "https://github.com/cython/cython/issues/2915"))
* [PEP-572](https://www.python.org/dev/peps/pep-0572 "https://www.python.org/dev/peps/pep-0572"): Assignment Expressions (a.k.a. the walrus operator :=) (Github issue [#2636](https://github.com/cython/cython/issues/2636 "https://github.com/cython/cython/issues/2636"))
* [PEP-590](https://www.python.org/dev/peps/pep-0590 "https://www.python.org/dev/peps/pep-0590"): Vectorcall protocol (Github issue [#2263](https://github.com/cython/cython/issues/2263 "https://github.com/cython/cython/issues/2263"))
* [PEP-614](https://www.python.org/dev/peps/pep-0614 "https://www.python.org/dev/peps/pep-0614"): Relaxing Grammar Restrictions On Decorators (Github issue [#4570](https://github.com/cython/cython/issues/4570 "https://github.com/cython/cython/issues/4570"))

Typing support in the sense of [PEP-484](https://www.python.org/dev/peps/pep-0484 "https://www.python.org/dev/peps/pep-0484") (Github issues [#3949](https://github.com/cython/cython/issues/3949 "https://github.com/cython/cython/issues/3949"), [#4243](https://github.com/cython/cython/issues/4243 "https://github.com/cython/cython/issues/4243"))
and [PEP-560](https://www.python.org/dev/peps/pep-0560 "https://www.python.org/dev/peps/pep-0560") (Github issues [#2753](https://github.com/cython/cython/issues/2753 "https://github.com/cython/cython/issues/2753"), [#3537](https://github.com/cython/cython/issues/3537 "https://github.com/cython/cython/issues/3537"), [#3764](https://github.com/cython/cython/issues/3764 "https://github.com/cython/cython/issues/3764")) was also improved.

The default language level was changed to `3str`, i.e. Python 3 semantics,
but with `str` literals (also in Python 2.7). This is a backwards incompatible
change from the previous default of Python 2 semantics. The previous behaviour
is available through the directive `language_level=2`.
(Github issue [#2565](https://github.com/cython/cython/issues/2565 "https://github.com/cython/cython/issues/2565")). This covers changes such as using the
`print`-function instead of the `print`-statement, and integer-integer
division giving a floating point answer. Most of these changes were available
in earlier versions of Cython but are now the default.

Cython 3.0.0 also aligns its own language semantics more closely with Python, in particular:

* the power operator has changed to give a result matching what Python does rather than
  keeping the same types as the input (as in C),
* operator overloading of `cdef classes` behaves much more like Python classes,
* Cython’s behaviour when using type annotations aligns more closely with their
  standard use in Python.

#### Related changes[¶](#id60 "Link to this heading")

* Cython no longer generates `__qualname__` attributes for classes in Python
  2.x since they are problematic there and not correctly maintained for subclasses.
  Patch by Jeroen Demeyer. (Github issue [#2772](https://github.com/cython/cython/issues/2772 "https://github.com/cython/cython/issues/2772"))
* Binding staticmethods of Cython functions were not behaving like Python methods.
  Patch by Jeroen Demeyer. (Github issue [#3106](https://github.com/cython/cython/issues/3106 "https://github.com/cython/cython/issues/3106"), [#3102](https://github.com/cython/cython/issues/3102 "https://github.com/cython/cython/issues/3102"))
* Compiling package `__init__` files could fail under Windows due to an
  undefined export symbol. (Github issue [#2968](https://github.com/cython/cython/issues/2968 "https://github.com/cython/cython/issues/2968"))
* `__init__.pyx` files were not always considered as package indicators.
  (Github issue [#2665](https://github.com/cython/cython/issues/2665 "https://github.com/cython/cython/issues/2665"))
* Setting `language_level=2` in a file did not work if `language_level=3`
  was enabled globally before.
  Patch by Jeroen Demeyer. (Github issue [#2791](https://github.com/cython/cython/issues/2791 "https://github.com/cython/cython/issues/2791"))
* `__doc__` was not available inside of the class body during class creation.
  (Github issue [#1635](https://github.com/cython/cython/issues/1635 "https://github.com/cython/cython/issues/1635"))
* The first function line number of functions with decorators pointed to the
  signature line and not the first decorator line, as in Python.
  Patch by Felix Kohlgrüber. (Github issue [#2536](https://github.com/cython/cython/issues/2536 "https://github.com/cython/cython/issues/2536"))
* Pickling unbound methods of Python classes failed.
  Patch by Pierre Glaser. (Github issue [#2972](https://github.com/cython/cython/issues/2972 "https://github.com/cython/cython/issues/2972"))
* Item access (subscripting) with integer indices/keys always tried the
  Sequence protocol before the Mapping protocol, which diverged from Python
  semantics. It now passes through the Mapping protocol first when supported.
  (Github issue [#1807](https://github.com/cython/cython/issues/1807 "https://github.com/cython/cython/issues/1807"))
* Nested dict literals in function call kwargs could incorrectly raise an
  error about duplicate keyword arguments, which are allowed when passing
  them from dict literals.
  (Github issue [#2963](https://github.com/cython/cython/issues/2963 "https://github.com/cython/cython/issues/2963"))
* Diverging from the usual behaviour, `len(memoryview)`, `len(char*)`
  and `len(Py_UNICODE*)` returned an unsigned `size_t` value. They now
  return a signed `Py_ssize_t`, like other usages of `len()`.
* The unicode methods `.upper()`, `.lower()` and `.title()` were
  incorrectly optimised for single character input values and only returned
  the first character if multiple characters should have been returned.
  They now use the original Python methods again.
* The `cython.view.array` type supports inheritance.
  Patch by David Woods. (Github issue [#3413](https://github.com/cython/cython/issues/3413 "https://github.com/cython/cython/issues/3413"))
* The builtin `abs()` function can now be used on C numbers in nogil code.
  Patch by Elliott Sales de Andrade. (Github issue [#2748](https://github.com/cython/cython/issues/2748 "https://github.com/cython/cython/issues/2748"))
* The attributes `gen.gi_frame` and `coro.cr_frame` of Cython compiled
  generators and coroutines now return an actual frame object for introspection.
  (Github issue [#2306](https://github.com/cython/cython/issues/2306 "https://github.com/cython/cython/issues/2306"))
* Inlined properties can be defined for external extension types.
  Patch by Matti Picus. (Github issue [#2640](https://github.com/cython/cython/issues/2640 "https://github.com/cython/cython/issues/2640"), redone later in [#3571](https://github.com/cython/cython/issues/3571 "https://github.com/cython/cython/issues/3571"))
* Unicode module names and imports are supported.
  Patch by David Woods. (Github issue [#3119](https://github.com/cython/cython/issues/3119 "https://github.com/cython/cython/issues/3119"))
* `__arg` argument names in methods were not mangled with the class name.
  Patch by David Woods. (Github issue [#1382](https://github.com/cython/cython/issues/1382 "https://github.com/cython/cython/issues/1382"))
* With `language_level=3/3str`, Python classes without explicit base class
  are now new-style (type) classes also in Py2. Previously, they were created
  as old-style (non-type) classes.
  (Github issue [#3530](https://github.com/cython/cython/issues/3530 "https://github.com/cython/cython/issues/3530"))
* Conditional blocks in Python code that depend on `cython.compiled` are
  eliminated at an earlier stage, which gives more freedom in writing
  replacement Python code.
  Patch by David Woods. (Github issue [#3507](https://github.com/cython/cython/issues/3507 "https://github.com/cython/cython/issues/3507"))
* Python private name mangling now falls back to unmangled names for non-Python
  globals, since double-underscore names are not uncommon in C. Unmangled Python
  names are also still found as a legacy fallback but produce a warning.
  Patch by David Woods. (Github issue [#3548](https://github.com/cython/cython/issues/3548 "https://github.com/cython/cython/issues/3548"))
* The `print` statement (not the `print()` function) is allowed in
  `nogil` code without an explicit `with gil` section.
* `repr()` was assumed to return `str` instead of `unicode` with `language_level=3`.
  (Github issue [#3736](https://github.com/cython/cython/issues/3736 "https://github.com/cython/cython/issues/3736"))
* Type inference now understands that `a, *b = x` assigns a list to `b`.
* No/single argument functions now accept keyword arguments by default in order
  to comply with Python semantics. The marginally faster calling conventions
  `METH_NOARGS` and `METH_O` that reject keyword arguments are still available
  with the directive `@cython.always_allow_keywords(False)`.
  (Github issue [#3090](https://github.com/cython/cython/issues/3090 "https://github.com/cython/cython/issues/3090"))
* Special methods for binary operators now follow Python semantics.
  Rather than e.g. a single `__add__` method for cdef classes, where
  “self” can be either the first or second argument, one can now define
  both `__add__` and `__radd__` as for standard Python classes.
  This behavior can be disabled with the `c_api_binop_methods` directive
  to return to the previous semantics in Cython code (available from Cython
  0.29.20), or the reversed method (`__radd__`) can be implemented in
  addition to an existing two-sided operator method (`__add__`) to get a
  backwards compatible implementation.
  (Github issue [#2056](https://github.com/cython/cython/issues/2056 "https://github.com/cython/cython/issues/2056"))
* Generator expressions in pxd-overridden `cdef` functions could
  fail to compile.
  Patch by Matúš Valo. (Github issue [#3477](https://github.com/cython/cython/issues/3477 "https://github.com/cython/cython/issues/3477"))
* Calls to `.__class__()` of a known extension type failed.
  Patch by David Woods. (Github issue [#3954](https://github.com/cython/cython/issues/3954 "https://github.com/cython/cython/issues/3954"))
* Structs could not be instantiated with positional arguments in
  pure Python mode.
* Annotations were not exposed on annotated (data-)classes.
  Patch by matsjoyce. (Github issue [#4151](https://github.com/cython/cython/issues/4151 "https://github.com/cython/cython/issues/4151"))
* Docstrings of `cpdef` enums are now copied to the enum class.
  Patch by matham. (Github issue [#3805](https://github.com/cython/cython/issues/3805 "https://github.com/cython/cython/issues/3805"))
* `asyncio.iscoroutinefunction()` now recognises coroutine functions
  also when compiled by Cython.
  Patch by Pedro Marques da Luz. (Github issue [#2273](https://github.com/cython/cython/issues/2273 "https://github.com/cython/cython/issues/2273"))
* Self-documenting f-strings (`=`) were implemented.
  Patch by davfsa. (Github issue [#3796](https://github.com/cython/cython/issues/3796 "https://github.com/cython/cython/issues/3796"))
* `cython.array` supports simple, non-strided views.
  (Github issue [#3775](https://github.com/cython/cython/issues/3775 "https://github.com/cython/cython/issues/3775"))
* Attribute annotations in Python classes are now ignored, because they are
  just Python objects in a dict (as opposed to the fields of extension types).
  Patch by David Woods. (Github issues [#4196](https://github.com/cython/cython/issues/4196 "https://github.com/cython/cython/issues/4196"), [#4198](https://github.com/cython/cython/issues/4198 "https://github.com/cython/cython/issues/4198"))
* A warning was added when `__defaults__` or `__kwdefaults__` of Cython compiled
  functions were re-assigned, since this does not current have an effect.
  Patch by David Woods. (Github issue [#2650](https://github.com/cython/cython/issues/2650 "https://github.com/cython/cython/issues/2650"))
* The `self` argument of static methods in .pxd files was incorrectly typed.
  Patch by David Woods. (Github issue [#3174](https://github.com/cython/cython/issues/3174 "https://github.com/cython/cython/issues/3174"))
* Default values for memory views arguments were not properly supported.
  Patch by Corentin Cadiou. (Github issue [#4313](https://github.com/cython/cython/issues/4313 "https://github.com/cython/cython/issues/4313"))
* Python object types were not allowed as `->` return type annotations.
  Patch by Matúš Valo. (Github issue [#4433](https://github.com/cython/cython/issues/4433 "https://github.com/cython/cython/issues/4433"))
* The excess arguments in a for-in-range loop with more than 3 arguments to range()
  were silently ignored.
  Original patch by Max Bachmann. (Github issue [#4550](https://github.com/cython/cython/issues/4550 "https://github.com/cython/cython/issues/4550"))
* Unsupported decorators on cdef functions were not rejected in recent releases.
  Patch by David Woods. (Github issue [#4322](https://github.com/cython/cython/issues/4322 "https://github.com/cython/cython/issues/4322"))
* Fused functions were binding unnecessarily, which prevented them from being pickled.
  Patch by David Woods. (Github issue [#4370](https://github.com/cython/cython/issues/4370 "https://github.com/cython/cython/issues/4370"))
* Decorators on inner functions were not evaluated in the right scope.
  Patch by David Woods. (Github issue [#4367](https://github.com/cython/cython/issues/4367 "https://github.com/cython/cython/issues/4367"))
* Cython did not type the `self` argument in special binary methods.
  Patch by David Woods. (Github issue [#4434](https://github.com/cython/cython/issues/4434 "https://github.com/cython/cython/issues/4434"))
* Circular imports of compiled modules could fail needlessly even when the import
  could already be resolved from `sys.modules`.
  Patch by Syam Gadde. (Github issue [#4390](https://github.com/cython/cython/issues/4390 "https://github.com/cython/cython/issues/4390"))
* `__del__(self)` on extension types now maps to `tp_finalize` in Python 3.
  Original patch by ax487. (Github issue [#3612](https://github.com/cython/cython/issues/3612 "https://github.com/cython/cython/issues/3612"))
* Reusing an extension type attribute name as a method name is now an error.
  Patch by 0dminnimda. (Github issue [#4661](https://github.com/cython/cython/issues/4661 "https://github.com/cython/cython/issues/4661"))
* When using type annotations, `func(x: list)` or `func(x: ExtType)` (and other
  Python builtin or extension types) no longer allow `None` as input argument to `x`.
  This is consistent with the normal typing semantics in Python, and was a common gotcha
  for users who did not expect `None` to be allowed as input. To allow `None`, use
  `typing.Optional` as in `func(x: Optional[list])`. `None` is also automatically
  allowed when it is used as default argument, i.e. `func(x: list = None)`.
  `int` and `float` are now also recognised in type annotations and restrict the
  value type at runtime. They were previously ignored.
  Note that, for backwards compatibility reasons, the new behaviour does not apply when using
  Cython’s C notation, as in `func(list x)`. Here, `None` is still allowed, as always.
  Also, the `annotation_typing` directive can now be enabled and disabled more finely
  within the module.
  (Github issues [#2696](https://github.com/cython/cython/issues/2696 "https://github.com/cython/cython/issues/2696"), [#3883](https://github.com/cython/cython/issues/3883 "https://github.com/cython/cython/issues/3883"), [#4606](https://github.com/cython/cython/issues/4606 "https://github.com/cython/cython/issues/4606"), [#4669](https://github.com/cython/cython/issues/4669 "https://github.com/cython/cython/issues/4669"), [#4886](https://github.com/cython/cython/issues/4886 "https://github.com/cython/cython/issues/4886"))
* The parser allowed some invalid spellings of `...`.
  Patch by 0dminnimda. (Github issue [#4868](https://github.com/cython/cython/issues/4868 "https://github.com/cython/cython/issues/4868"))
* The `__self__` attribute of fused functions reports its availability correctly
  with `hasattr()`. Patch by David Woods.
  (Github issue [#4808](https://github.com/cython/cython/issues/4808 "https://github.com/cython/cython/issues/4808"))
* Several optimised string methods failed to accept `None` as arguments to their options.
  Test patch by Kirill Smelkov. (Github issue [#4737](https://github.com/cython/cython/issues/4737 "https://github.com/cython/cython/issues/4737"))
* Cython generators and coroutines now identify as `CO_ASYNC_GENERATOR`,
  `CO_COROUTINE` and `CO_GENERATOR` accordingly.
  (Github issue [#4902](https://github.com/cython/cython/issues/4902 "https://github.com/cython/cython/issues/4902"))
* Memory views and the internal Cython array type now identify as `collections.abc.Sequence`.
  Patch by David Woods. (Github issue [#4817](https://github.com/cython/cython/issues/4817 "https://github.com/cython/cython/issues/4817"))
* Context managers can be written in parentheses.
  Patch by David Woods. (Github issue [#4814](https://github.com/cython/cython/issues/4814 "https://github.com/cython/cython/issues/4814"))
* Some parser issues were resolved.
  (Github issue [#4992](https://github.com/cython/cython/issues/4992 "https://github.com/cython/cython/issues/4992"))
* Unused `**kwargs` arguments did not show up in `locals()`.
  (Github issue [#4899](https://github.com/cython/cython/issues/4899 "https://github.com/cython/cython/issues/4899"))
* Relative imports failed in compiled `__init__.py` package modules.
  Patch by Matúš Valo. (Github issue [#3442](https://github.com/cython/cython/issues/3442 "https://github.com/cython/cython/issues/3442"))
* Extension types are now explicitly marked as immutable types to prevent them from
  being considered mutable.
  Patch by Max Bachmann. (Github issue [#5023](https://github.com/cython/cython/issues/5023 "https://github.com/cython/cython/issues/5023"))
* `int(Py_UCS4)` returned the code point instead of the parsed digit value.
  (Github issue [#5216](https://github.com/cython/cython/issues/5216 "https://github.com/cython/cython/issues/5216"))
* Calling bound classmethods of builtin types could fail trying to call the unbound method.
  (Github issue [#5051](https://github.com/cython/cython/issues/5051 "https://github.com/cython/cython/issues/5051"))
* Generator expressions and comprehensions now look up their outer-most iterable
  on creation, as Python does, and not later on start, as they did previously.
  (Github issue [#1159](https://github.com/cython/cython/issues/1159 "https://github.com/cython/cython/issues/1159"))
* Bound C methods can now coerce to Python objects.
  (Github issues [#4890](https://github.com/cython/cython/issues/4890 "https://github.com/cython/cython/issues/4890"), [#5062](https://github.com/cython/cython/issues/5062 "https://github.com/cython/cython/issues/5062"))
* `cpdef` enums can now be pickled.
  (Github issue [#5120](https://github.com/cython/cython/issues/5120 "https://github.com/cython/cython/issues/5120"))
* The Python Enum of a `cpdef enum` now inherits from `IntFlag` to better match
  both Python and C semantics of enums.
  (Github issue [#2732](https://github.com/cython/cython/issues/2732 "https://github.com/cython/cython/issues/2732"))
* The special `__*pow__` methods now support the 2- and 3-argument variants.
  (Github issue [#5160](https://github.com/cython/cython/issues/5160 "https://github.com/cython/cython/issues/5160"))
* The `**` power operator now behaves more like in Python by returning the correct complex
  result if required by math. A new `cpow` directive was added to turn on the previous
  C-like behaviour.
  (Github issue [#4936](https://github.com/cython/cython/issues/4936 "https://github.com/cython/cython/issues/4936"))
* With `language_level=2`, imports of modules in packages could return the wrong module in Python 3.
  (Github issue [#5308](https://github.com/cython/cython/issues/5308 "https://github.com/cython/cython/issues/5308"))
* Function signatures containing a type like tuple[()] could not be printed.
  Patch by Lisandro Dalcin. (Github issue [#5355](https://github.com/cython/cython/issues/5355 "https://github.com/cython/cython/issues/5355"))
* `__qualname__` and `__module__` were not available inside of class bodies.
  (Github issue [#4447](https://github.com/cython/cython/issues/4447 "https://github.com/cython/cython/issues/4447"))
* A new directive `embedsignature.format` was added to select the format of the
  docstring embedded signatures between `python`, `c` and argument `clinic`.
  Patch by Lisandro Dalcin. (Github issue [#5415](https://github.com/cython/cython/issues/5415 "https://github.com/cython/cython/issues/5415"))
* ctuples can now be assigned from arbitrary sequences, not just Python tuples.

### Improvements in Pure Python mode[¶](#improvements-in-pure-python-mode "Link to this heading")

Cython strives to be able to
parse newer Python constructs for use with its [pure python](https://cython.readthedocs.io/en/latest/src/tutorial/pure.html "https://cython.readthedocs.io/en/latest/src/tutorial/pure.html") mode, which
has been a focus. In short, this allows to compile a wider range of Python
code into optimized C code.

Pure python mode gained many new features and was generally overhauled to make
it as capable as the Cython syntax. Except for using external C/C++ libraries,
it should now be possible to express all Cython code and use all features in
regular Python syntax. The very few remaining exceptions or bugs are noted in
the documentation.

Additionally, the documentation has been substantially updated
(primarily by Matúš Valo and 0dminnimda) to show both the older Cython syntax
and pure Python syntax.

#### Related changes[¶](#id61 "Link to this heading")

* The `cython.declare()` and `cython.cast()` functions could fail in pure mode.
  Patch by Dmitry Shesterkin. (Github issue [#3244](https://github.com/cython/cython/issues/3244 "https://github.com/cython/cython/issues/3244"))
* Fused argument types were not correctly handled in type annotations and
  `cython.locals()`.
  Patch by David Woods. (Github issues [#3391](https://github.com/cython/cython/issues/3391 "https://github.com/cython/cython/issues/3391"), [#3142](https://github.com/cython/cython/issues/3142 "https://github.com/cython/cython/issues/3142"))
* `nogil` functions now avoid acquiring the GIL on function exit if possible
  even if they contain `with gil` blocks.
  (Github issue [#3554](https://github.com/cython/cython/issues/3554 "https://github.com/cython/cython/issues/3554"))
* The `@returns()` decorator propagates exceptions by default for suitable C
  return types when no `@exceptval()` is defined.
  (Github issues [#3625](https://github.com/cython/cython/issues/3625 "https://github.com/cython/cython/issues/3625"), [#3664](https://github.com/cython/cython/issues/3664 "https://github.com/cython/cython/issues/3664"))
* Extension types inheriting from Python classes could not safely
  be exposed in `.pxd` files.
  (Github issue [#4106](https://github.com/cython/cython/issues/4106 "https://github.com/cython/cython/issues/4106"))
* Default arguments of methods were not exposed for introspection.
  Patch by Vladimir Matveev. (Github issue [#4061](https://github.com/cython/cython/issues/4061 "https://github.com/cython/cython/issues/4061"))
* Literal list assignments to pointer variables declared in PEP-526
  notation failed to compile.
* The type `cython.Py_hash_t` is available in Python mode.
* A `cimport` is now supported in pure Python code by prefixing the
  imported module name with `cython.cimports.`, e.g.
  `from cython.cimports.libc.math import sin`.
  (GIthub issue [#4190](https://github.com/cython/cython/issues/4190 "https://github.com/cython/cython/issues/4190"))
* Directives starting with `optimization.*` in pure Python mode were incorrectly named.
  It should have been `optimize.*`.
  Patch by David Woods. (Github issue [#4258](https://github.com/cython/cython/issues/4258 "https://github.com/cython/cython/issues/4258"))
* Invalid and misspelled `cython.*` module names were not reported as errors.
  (Github issue [#4947](https://github.com/cython/cython/issues/4947 "https://github.com/cython/cython/issues/4947"))
* The `annotation_typing` directive was missing in pure Python mode.
  Patch by 0dminnimda. (Github issue [#5194](https://github.com/cython/cython/issues/5194 "https://github.com/cython/cython/issues/5194"))
* Memoryviews with `object` item type were not supported in Python type declarations.
  (Github issue [#4907](https://github.com/cython/cython/issues/4907 "https://github.com/cython/cython/issues/4907"))
* Subscripted builtin types in type declarations (like `list[float]`) are now
  better supported.
  (Github issue [#5058](https://github.com/cython/cython/issues/5058 "https://github.com/cython/cython/issues/5058"))
* Unknown type annotations (e.g. because of typos) now emit a warning at compile time.
  Patch by Matúš Valo. (Github issue [#5070](https://github.com/cython/cython/issues/5070 "https://github.com/cython/cython/issues/5070"))
* `typing.Optional` could fail on tuple types.
  (Github issue [#5263](https://github.com/cython/cython/issues/5263 "https://github.com/cython/cython/issues/5263"))
* `from cython cimport … as …` could lead to imported names not being found in annotations.
  Patch by Chia-Hsiang Cheng. (Github issue [#5235](https://github.com/cython/cython/issues/5235 "https://github.com/cython/cython/issues/5235"))
* Simple tuple types like `(int, int)` are no longer accepted in Python annotations
  and require the Python notation instead (e.g. `tuple[cython.int, cython.int]`).
  (Github issue [#5397](https://github.com/cython/cython/issues/5397 "https://github.com/cython/cython/issues/5397"))
* The Python implementation of `cimport cython.cimports…` could raise an `ImportError`
  instead of an `AttributeError` when looking up package variable names.
  Patch by Matti Picus. (Github issue [#5411](https://github.com/cython/cython/issues/5411 "https://github.com/cython/cython/issues/5411"))
* A new decorator `@cython.with_gil` is available in Python code to match the `with gil`
  function declaration in Cython syntax.
* `with gil` and `with nogil(flag)` now accept their flag argument also in Python code.
  Patch by Matúš Valo. (Github issue [#5113](https://github.com/cython/cython/issues/5113 "https://github.com/cython/cython/issues/5113"))

### Code generation changes[¶](#code-generation-changes "Link to this heading")

Cython has gained several major new features that speed up both the development
and the code. Dataclasses have gained an extension type equivalent that implements
the dataclass features in C code. Similarly, the `@functools.total_ordering`
decorator to an extension type will implement the comparison functions in C.

Finally, NumPy ufuncs can be generated from simple computation functions with the
new `@cython.ufunc` decorator.

#### Related changes[¶](#id62 "Link to this heading")

* `with gil/nogil` statements can be conditional based on compile-time
  constants, e.g. fused type checks.
  Patch by Noam Hershtig. (Github issue [#2579](https://github.com/cython/cython/issues/2579 "https://github.com/cython/cython/issues/2579"))
* The names of Cython’s internal types (functions, generator, coroutine, etc.)
  are now qualified with the module name of the internal Cython module that is
  used for sharing them across Cython implemented modules, for example
  `_cython_3_0a5.coroutine`. This was done to avoid making them look like
  homeless builtins, to help with debugging, and in order to avoid a CPython
  warning according to [https://bugs.python.org/issue20204](https://bugs.python.org/issue20204 "https://bugs.python.org/issue20204")
* A `@cython.total_ordering` decorator has been added to automatically
  implement all comparison operators, similar to `functools.total_ordering`.
  Patch by Spencer Brown. (Github issue [#2090](https://github.com/cython/cython/issues/2090 "https://github.com/cython/cython/issues/2090"))
* A new decorator `@cython.dataclasses.dataclass` was implemented that provides
  compile time dataclass generation capabilities to `cdef` classes (extension types).
  Patch by David Woods. (Github issue [#2903](https://github.com/cython/cython/issues/2903 "https://github.com/cython/cython/issues/2903")). `kw_only` dataclasses
  added by Yury Sokov. (Github issue [#4794](https://github.com/cython/cython/issues/4794 "https://github.com/cython/cython/issues/4794"))
* A new function decorator `@cython.ufunc` automatically generates a (NumPy) ufunc that
  applies the calculation function to an entire memoryview.
  (Github issue [#4758](https://github.com/cython/cython/issues/4758 "https://github.com/cython/cython/issues/4758"))
* Generated NumPy ufuncs could crash for large arrays due to incorrect GIL handling.
  (Github issue [#5328](https://github.com/cython/cython/issues/5328 "https://github.com/cython/cython/issues/5328"))
* Some invalid directive usages are now detected and rejected, e.g. using `@ccall`
  together with `@cfunc`, and applying `@cfunc` to a `@ufunc`. Cython also
  warns now when a directive is applied needlessly.
  (Github issue [#5399](https://github.com/cython/cython/issues/5399 "https://github.com/cython/cython/issues/5399") et al.)
* The normal `@dataclasses.dataclass` and `@functools.total_ordering` decorators
  can now be used on extension types. Using the corresponding `@cython.*` decorator
  will automatically turn a Python class into an extension type (no need for `@cclass`).
  (Github issue [#5292](https://github.com/cython/cython/issues/5292 "https://github.com/cython/cython/issues/5292"))

### Interaction with numpy[¶](#interaction-with-numpy "Link to this heading")

The NumPy declarations (`cimport numpy`) were moved over to the NumPy project in order
to allow version specific changes on their side.

One effect is that Cython does not use deprecated NumPy C-APIs any more. Thus, you
can define the respective NumPy C macro to get rid of the compatibility warning at
C compile time.

#### Related changes[¶](#id63 "Link to this heading")

* `cython.inline()` now sets the `NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION`
  C macro automatically when `numpy` is imported in the code, to avoid C compiler
  warnings about deprecated NumPy C-API usage.
* Deprecated NumPy API usages were removed from `numpy.pxd`.
  Patch by Matti Picus. (Github issue [#3365](https://github.com/cython/cython/issues/3365 "https://github.com/cython/cython/issues/3365"))
* `numpy.import_array()` is automatically called if `numpy` has been cimported
  and it has not been called in the module code. This is intended as a hidden
  fail-safe so user code should continue to call `numpy.import_array`.
  Patch by David Woods. (Github issue [#3524](https://github.com/cython/cython/issues/3524 "https://github.com/cython/cython/issues/3524"))
* The outdated getbuffer/releasebuffer implementations in the NumPy
  declarations were removed so that buffers declared as `ndarray`
  now use the normal implementation in NumPy.
* Several macros/functions declared in the NumPy API are now usable without
  holding the GIL.
* The `numpy` declarations were updated.
  Patch by Brock Mendel. (Github issue [#3630](https://github.com/cython/cython/issues/3630 "https://github.com/cython/cython/issues/3630"))
* `ndarray.shape` failed to compile with Pythran and recent NumPy.
  Patch by Serge Guelton. (Github issue [#3762](https://github.com/cython/cython/issues/3762 "https://github.com/cython/cython/issues/3762"))
* A C-level compatibility issue with recent NumPy versions was resolved.
  Patch by David Woods. (Github issue [#4396](https://github.com/cython/cython/issues/4396 "https://github.com/cython/cython/issues/4396"))
* The generated modules no longer import NumPy internally when using
  fused types but no memoryviews.
  Patch by David Woods. (Github issue [#4935](https://github.com/cython/cython/issues/4935 "https://github.com/cython/cython/issues/4935"))
* `np.long_t` and `np.ulong_t` were removed from the NumPy declarations,
  syncing Cython with upstream NumPy v1.25.0. The aliases were confusing
  since they could mean different things on different platforms.

### Exception handling[¶](#exception-handling "Link to this heading")

Cython-implemented C functions now propagate exceptions by default, rather than
swallowing them in non-object returning function if the user forgot to add an
`except` declaration to the signature. This was a long-standing source of bugs,
but can require adding the `noexcept` declaration to existing functions if
exception propagation is really undesired.
(Github issue [#4280](https://github.com/cython/cython/issues/4280 "https://github.com/cython/cython/issues/4280"))

To ease the transition for this break in behaviour, it is possible to set
`legacy_implicit_noexcept=True`.

#### Related changes[¶](#id64 "Link to this heading")

* The `assert` statement is allowed in `nogil` sections. Here, the GIL is
  only acquired if the `AssertionError` is really raised, which means that the
  evaluation of the asserted condition only allows C expressions.
* The exception handling annotation `except +*` was broken.
  Patch by David Woods. (Github issues [#3065](https://github.com/cython/cython/issues/3065 "https://github.com/cython/cython/issues/3065"), [#3066](https://github.com/cython/cython/issues/3066 "https://github.com/cython/cython/issues/3066"))
* Improve conversion between function pointers with non-identical but
  compatible exception specifications. Patches by David Woods.
  (Github issues [#4770](https://github.com/cython/cython/issues/4770 "https://github.com/cython/cython/issues/4770"), [#4689](https://github.com/cython/cython/issues/4689 "https://github.com/cython/cython/issues/4689"))
* Exceptions within for-loops that run over memoryviews could lead to a ref-counting error.
  Patch by David Woods. (Github issue [#4662](https://github.com/cython/cython/issues/4662 "https://github.com/cython/cython/issues/4662"))
* To opt out of the new, safer exception handling behaviour, legacy code can set the new
  directive `legacy_implicit_noexcept=True` for a transition period to keep the
  previous, unsafe behaviour. This directive will eventually be removed in a later release.
  Patch by Matúš Valo. (Github issue [#5094](https://github.com/cython/cython/issues/5094 "https://github.com/cython/cython/issues/5094"))
* Cython implemented C functions now propagate exceptions by default, rather than
  swallowing them in non-object returning function if the user forgot to add an
  `except` declaration to the signature. This was a long-standing source of bugs,
  but can require adding the `noexcept` declaration to existing functions if
  exception propagation is really undesired.
  (Github issue [#4280](https://github.com/cython/cython/issues/4280 "https://github.com/cython/cython/issues/4280"))
* The code `except +nogil` (declaring a C++ exception handler function called `nogil`)
  is now rejected because it is almost certainly a typo from `except + nogil`.
  (Github issue [#5430](https://github.com/cython/cython/issues/5430 "https://github.com/cython/cython/issues/5430"))
* Handling freshly raised exceptions that didn’t have a traceback yet could crash.
  (Github issue [#5495](https://github.com/cython/cython/issues/5495 "https://github.com/cython/cython/issues/5495"))

### Optimizations[¶](#optimizations "Link to this heading")

Generating efficient code has long been a goal of Cython, and 3.0 continues that.
Probably the most significant change is that Cython functions use the PEP-590 vectorcall
protocol on Python 3.7 and higher.

#### Related changes[¶](#id65 "Link to this heading")

* Name lookups in class bodies no longer go through an attribute lookup.
  Patch by Jeroen Demeyer. (Github issue [#3100](https://github.com/cython/cython/issues/3100 "https://github.com/cython/cython/issues/3100"))
* Extension types that do not need their own `tp_new` implementation (because
  they have no object attributes etc.) directly inherit the implementation of
  their parent type if possible.
  (Github issue [#1555](https://github.com/cython/cython/issues/1555 "https://github.com/cython/cython/issues/1555"))
* Some list copying is avoided internally when a new list needs to be created
  but we already have a fresh one.
  (Github issue [#3494](https://github.com/cython/cython/issues/3494 "https://github.com/cython/cython/issues/3494"))
* Multiplication of Python numbers with small constant integers is faster.
  (Github issue [#2808](https://github.com/cython/cython/issues/2808 "https://github.com/cython/cython/issues/2808"))
* String concatenation can now happen in place if possible, by extending the
  existing string rather than always creating a new one.
  Patch by David Woods. (Github issue [#3453](https://github.com/cython/cython/issues/3453 "https://github.com/cython/cython/issues/3453"))
* The `str()` builtin now calls `PyObject_Str()` instead of going
  through a Python call.
  Patch by William Ayd. (Github issue [#3279](https://github.com/cython/cython/issues/3279 "https://github.com/cython/cython/issues/3279"))
* Reimports of already imported modules are substantially faster.
  (Github issue [#2854](https://github.com/cython/cython/issues/2854 "https://github.com/cython/cython/issues/2854"))
* The dispatch to fused functions is now linear in the number of arguments,
  which makes it much faster, often 2x or more, and several times faster for
  larger fused types with many specialisations.
  Patch by will-ca. (Github issue [#1385](https://github.com/cython/cython/issues/1385 "https://github.com/cython/cython/issues/1385"))
* The fastcall/vectorcall protocols are used for several internal Python calls.
  (Github issue [#3540](https://github.com/cython/cython/issues/3540 "https://github.com/cython/cython/issues/3540"))
* `nogil` functions now avoid acquiring the GIL on function exit if possible
  even if they contain `with gil` blocks.
  (Github issue [#3554](https://github.com/cython/cython/issues/3554 "https://github.com/cython/cython/issues/3554"))
* Type inference now works for memory views and slices.
  Patch by David Woods. (Github issue [#2227](https://github.com/cython/cython/issues/2227 "https://github.com/cython/cython/issues/2227"))
* For-in-loop iteration over `bytearray` and memory views is optimised.
  Patch by David Woods. (Github issue [#2227](https://github.com/cython/cython/issues/2227 "https://github.com/cython/cython/issues/2227"))
* For-in-loop iteration over `bytearray` and memory views is optimised.
  Patch by David Woods. (Github issue [#2227](https://github.com/cython/cython/issues/2227 "https://github.com/cython/cython/issues/2227"))
* `float(…)` is optimised for string arguments (str/bytes/bytearray).
* `[...] * N` is optimised for C integer multipliers `N`.
  (Github issue [#3922](https://github.com/cython/cython/issues/3922 "https://github.com/cython/cython/issues/3922"))
* Some constant tuples containing strings were not deduplicated.
  Patch by David Woods. (Github issue [#4353](https://github.com/cython/cython/issues/4353 "https://github.com/cython/cython/issues/4353"))
* Memory views can use atomic CPU instructions instead of locks in more cases.
  Patch by Sam Gross. (Github issue [#4912](https://github.com/cython/cython/issues/4912 "https://github.com/cython/cython/issues/4912"))
* Cython avoids raising `StopIteration` in `__next__` methods when possible.
  Patch by David Woods. (Github issue [#3447](https://github.com/cython/cython/issues/3447 "https://github.com/cython/cython/issues/3447"))
* Larger numbers of extension types with multiple subclasses could take very long to compile.
  Patch by Scott Wolchok. (Github issue [#5139](https://github.com/cython/cython/issues/5139 "https://github.com/cython/cython/issues/5139"))
* Integer comparisons avoid Python coercions if possible.
  (Github issue [#4821](https://github.com/cython/cython/issues/4821 "https://github.com/cython/cython/issues/4821"))
* The call-time dispatch for fused memoryview types is less slow.
  (Github issue [#5073](https://github.com/cython/cython/issues/5073 "https://github.com/cython/cython/issues/5073"))
* Python’s `memoryview` is now a known builtin type with optimised properties.
  (Github issue [#3798](https://github.com/cython/cython/issues/3798 "https://github.com/cython/cython/issues/3798"))
* Multiplying a sequence by a C integer avoids creating and intermediate Python integer.
* The reference counting of memory views involved useless overhead.
  (Github issue [#5510](https://github.com/cython/cython/issues/5510 "https://github.com/cython/cython/issues/5510"))

### Compatibility with C[¶](#compatibility-with-c "Link to this heading")

The support for C features like `const` or `volatile` was substantially improved.

The generated code has been cleared up to reduce the number of C compiler warnings emitted.

#### Related changes[¶](#id66 "Link to this heading")

* A C compiler cast warning was resolved.
  Patch by Michael Buesch. (Github issue [#2775](https://github.com/cython/cython/issues/2775 "https://github.com/cython/cython/issues/2775"))
* Constant integer expressions that used a negative exponent were evaluated
  as integer 0 instead of the expected float value.
  Patch by Kryštof Pilnáček. (Github issue [#2133](https://github.com/cython/cython/issues/2133 "https://github.com/cython/cython/issues/2133"))
* Several declarations in `cpython.*`, `libc.*` and `libcpp.*` were added.
  Patches by Jeroen Demeyer, Matthew Edwards, Chris Gyurgyik, Jerome Kieffer
  and Zackery Spytz.
  (Github issues [#3468](https://github.com/cython/cython/issues/3468 "https://github.com/cython/cython/issues/3468"), [#3332](https://github.com/cython/cython/issues/3332 "https://github.com/cython/cython/issues/3332"), [#3202](https://github.com/cython/cython/issues/3202 "https://github.com/cython/cython/issues/3202"), [#3188](https://github.com/cython/cython/issues/3188 "https://github.com/cython/cython/issues/3188"),
  [#3179](https://github.com/cython/cython/issues/3179 "https://github.com/cython/cython/issues/3179"), [#2891](https://github.com/cython/cython/issues/2891 "https://github.com/cython/cython/issues/2891"), [#2826](https://github.com/cython/cython/issues/2826 "https://github.com/cython/cython/issues/2826"), [#2713](https://github.com/cython/cython/issues/2713 "https://github.com/cython/cython/issues/2713"))
* The `volatile` C modifier is supported in Cython code.
  Patch by Jeroen Demeyer. (Github issue [#1667](https://github.com/cython/cython/issues/1667 "https://github.com/cython/cython/issues/1667"))
* `const` can be used together with fused types.
  Patch by Thomas Vincent. (Github issue [#1772](https://github.com/cython/cython/issues/1772 "https://github.com/cython/cython/issues/1772"))
* Temporary buffer indexing variables were not released and could show up in
  C compiler warnings, e.g. in generators.
  Patch by David Woods. (Github issues [#3430](https://github.com/cython/cython/issues/3430 "https://github.com/cython/cython/issues/3430"), [#3522](https://github.com/cython/cython/issues/3522 "https://github.com/cython/cython/issues/3522"))
* The C property feature has been rewritten and now requires C property methods
  to be declared `inline` ([#3571](https://github.com/cython/cython/issues/3571 "https://github.com/cython/cython/issues/3571")).
* Cython generates C compiler branch hints for unlikely user defined if-clauses
  in more cases, when they end up raising exceptions unconditionally. This now
  includes exceptions being raised in `nogil`/`with gil` sections.
* Several issues with arithmetic overflow handling were resolved, including
  undefined behaviour in C.
  Patch by Sam Sneddon. (Github issue [#3588](https://github.com/cython/cython/issues/3588 "https://github.com/cython/cython/issues/3588"))
* libc.math was extended to include all C99 function declarations.
  Patch by Dean Scarff. (Github issue [#3570](https://github.com/cython/cython/issues/3570 "https://github.com/cython/cython/issues/3570"))
* Some C compiler warninge were resolved.
  Patches by Max Bachmann. (Github issue [#4053](https://github.com/cython/cython/issues/4053 "https://github.com/cython/cython/issues/4053"), [#4059](https://github.com/cython/cython/issues/4059 "https://github.com/cython/cython/issues/4059"), [#4054](https://github.com/cython/cython/issues/4054 "https://github.com/cython/cython/issues/4054"), [#4148](https://github.com/cython/cython/issues/4148 "https://github.com/cython/cython/issues/4148"), [#4162](https://github.com/cython/cython/issues/4162 "https://github.com/cython/cython/issues/4162"))
* A C compiler warning about enum value casting was resolved in GCC.
  (Github issue [#2749](https://github.com/cython/cython/issues/2749 "https://github.com/cython/cython/issues/2749"))
* A C compiler warning about unused code was resolved.
  (Github issue [#3763](https://github.com/cython/cython/issues/3763 "https://github.com/cython/cython/issues/3763"))
* Some compiler problems and warnings were resolved.
  Patches by David Woods, 0dminnimda, Nicolas Pauss and others.
  (Github issues [#4317](https://github.com/cython/cython/issues/4317 "https://github.com/cython/cython/issues/4317"), [#4324](https://github.com/cython/cython/issues/4324 "https://github.com/cython/cython/issues/4324"), [#4361](https://github.com/cython/cython/issues/4361 "https://github.com/cython/cython/issues/4361"), [#4357](https://github.com/cython/cython/issues/4357 "https://github.com/cython/cython/issues/4357"))
* Some C compiler warnings were fixed.
  Patch by mwtian. (Github issue [#4831](https://github.com/cython/cython/issues/4831 "https://github.com/cython/cython/issues/4831"))
* A case of undefined C behaviour was resolved in the list slicing code.
  Patch by Richard Barnes. (Github issue [#4734](https://github.com/cython/cython/issues/4734 "https://github.com/cython/cython/issues/4734"))
* Typedefs for the `bint` type did not always behave like `bint`.
  Patch by Nathan Manville and 0dminnimda. (Github issue [#4660](https://github.com/cython/cython/issues/4660 "https://github.com/cython/cython/issues/4660"))
* Intel C compilers could complain about unsupported gcc pragmas.
  Patch by Ralf Gommers. (Github issue [#5052](https://github.com/cython/cython/issues/5052 "https://github.com/cython/cython/issues/5052"))
* Structs that contained an array field resulted in incorrect C code. Their initialisation
  now uses `memcpy()`.
  Patch by Chia-Hsiang Cheng. (Github issue [#5178](https://github.com/cython/cython/issues/5178 "https://github.com/cython/cython/issues/5178"))
* The module state struct was not initialised in correct C (before C23), leading to
  compile errors on Windows.
  Patch by yudonglin. (Github issue [#5169](https://github.com/cython/cython/issues/5169 "https://github.com/cython/cython/issues/5169"))
* `cdef public` functions declared in .pxd files could use an incorrectly mangled C name.
  Patch by EpigeneMax. (Github issue [#2940](https://github.com/cython/cython/issues/2940 "https://github.com/cython/cython/issues/2940"))
* `const` types could not be returned from functions.
  Patch by Mike Graham. (Github issue [#5135](https://github.com/cython/cython/issues/5135 "https://github.com/cython/cython/issues/5135"))
* C11 `complex.h` is now properly detected.
  (Github issue [#2513](https://github.com/cython/cython/issues/2513 "https://github.com/cython/cython/issues/2513"))
* Standard C/C++ atomic operations are now used for memory views, if available.
  (Github issue [#4925](https://github.com/cython/cython/issues/4925 "https://github.com/cython/cython/issues/4925"))
* C arrays can be initialised inside of nogil functions.
  Patch by Matúš Valo. (Github issue [#1662](https://github.com/cython/cython/issues/1662 "https://github.com/cython/cython/issues/1662"))
* Very long Python integer constants could exceed the maximum C name length of MSVC.
  Patch by 0dminnimda. (Github issue [#5290](https://github.com/cython/cython/issues/5290 "https://github.com/cython/cython/issues/5290"))
* Some C compiler warnings were resolved.
  Patches by Matt Tyson, Lisandro Dalcin, Philipp Wagner, Matti Picus et al.
  (Github issues [#5417](https://github.com/cython/cython/issues/5417 "https://github.com/cython/cython/issues/5417"), [#5418](https://github.com/cython/cython/issues/5418 "https://github.com/cython/cython/issues/5418"), [#5421](https://github.com/cython/cython/issues/5421 "https://github.com/cython/cython/issues/5421"), [#5437](https://github.com/cython/cython/issues/5437 "https://github.com/cython/cython/issues/5437"), [#5438](https://github.com/cython/cython/issues/5438 "https://github.com/cython/cython/issues/5438"), [#5443](https://github.com/cython/cython/issues/5443 "https://github.com/cython/cython/issues/5443"))
* Some typedef declarations for libc function types were fixed.
  (Github issue [#5498](https://github.com/cython/cython/issues/5498 "https://github.com/cython/cython/issues/5498"))
* With MSVC, Cython no longer enables C-Complex support by accident (which is not supported there).
  (Github issue [#5512](https://github.com/cython/cython/issues/5512 "https://github.com/cython/cython/issues/5512"))

### Compatibility with C++[¶](#id67 "Link to this heading")

Many C++ features like forwarding references or `std::move` are now supported or even used
internally, if possible.

Cython’s wrapping of the C++ standard library has been extended.

A new cpp\_locals` directive enables C++ local variables to initialized when assigned to
rather than at the start of the function, making them behave more like Python variables,
and also removing the requirement for them to be default constructible.

#### Related changes[¶](#id68 "Link to this heading")

* C++ `typeid()` failed for fused types.
  Patch by David Woods. (Github issue [#3203](https://github.com/cython/cython/issues/3203 "https://github.com/cython/cython/issues/3203"))
* `std::move()` is now used in C++ mode for internal temp variables to
  make them work without copying values.
  Patch by David Woods. (Github issues [#3253](https://github.com/cython/cython/issues/3253 "https://github.com/cython/cython/issues/3253"), [#1612](https://github.com/cython/cython/issues/1612 "https://github.com/cython/cython/issues/1612"))
* The C++ `typeid()` function was allowed in C mode.
  Patch by Celelibi. (Github issue [#3637](https://github.com/cython/cython/issues/3637 "https://github.com/cython/cython/issues/3637"))
* C++ references failed to compile when used as Python object indexes.
  Patch by David Woods. (Github issue [#3754](https://github.com/cython/cython/issues/3754 "https://github.com/cython/cython/issues/3754"))
* The construct `for x in cpp_function_call()` failed to compile.
  Patch by David Woods. (Github issue [#3663](https://github.com/cython/cython/issues/3663 "https://github.com/cython/cython/issues/3663"))
* Some C++ STL methods did not propagate exceptions.
  Patch by Max Bachmann. (Github issue [#4079](https://github.com/cython/cython/issues/4079 "https://github.com/cython/cython/issues/4079"))
* A compile failure for C++ enums in Py3.4 / MSVC was resolved.
  Patch by Ashwin Srinath. (Github issue [#3782](https://github.com/cython/cython/issues/3782 "https://github.com/cython/cython/issues/3782"))
* Cython compiled functions always provided a `__self__` attribute,
  regardless of being used as a method or not.
  Patch by David Woods. (Github issue [#4036](https://github.com/cython/cython/issues/4036 "https://github.com/cython/cython/issues/4036"))
* Overloaded C++ static methods were lost.
  Patch by Ashwin Srinath. (Github [#1851](https://github.com/cython/cython/issues/1851 "https://github.com/cython/cython/issues/1851"))
* Nested C++ types were not usable through ctypedefs.
  Patch by Vadim Pushtaev. (Github issue [#4039](https://github.com/cython/cython/issues/4039 "https://github.com/cython/cython/issues/4039"))
* More declarations for C++ string methods were added.
* Converting C++ containers to Python lists uses less memory allocations.
  Patch by Max Bachmann. (Github issue [#4081](https://github.com/cython/cython/issues/4081 "https://github.com/cython/cython/issues/4081"))
* `std::move()` is now also called for temps during `yield`.
  Patch by Yu Feng. (Github issue [#4154](https://github.com/cython/cython/issues/4154 "https://github.com/cython/cython/issues/4154"))
* The destructor is now called for fields in C++ structs.
  Patch by David Woods. (Github issue [#3226](https://github.com/cython/cython/issues/3226 "https://github.com/cython/cython/issues/3226"))
* Conversion from Python dicts to `std::map` was broken.
  Patch by David Woods and Mikkel Skofelt. (Github issues [#4228](https://github.com/cython/cython/issues/4228 "https://github.com/cython/cython/issues/4228"), [#4231](https://github.com/cython/cython/issues/4231 "https://github.com/cython/cython/issues/4231"))
* Code optimisations were not applied to methods of Cython implemented C++ classes.
  Patch by David Woods. (Github issue [#4212](https://github.com/cython/cython/issues/4212 "https://github.com/cython/cython/issues/4212"))
* C++17 execution policies are supported in `libcpp.algorithm`.
  Patch by Ashwin Srinath. (Github issue [#3790](https://github.com/cython/cython/issues/3790 "https://github.com/cython/cython/issues/3790"))
* A new directive `cpp_locals` was added that allows local C++ variables to
  be lazily initialised (without default constructor), thus making them behave
  more like Python variables.
  Patch by David Woods. (Github issue [#4160](https://github.com/cython/cython/issues/4160 "https://github.com/cython/cython/issues/4160"))
* Generated utility code for C++ conversions no longer depends on several user
  definable directives that may make it behave incorrectly.
  Patch by David Woods. (Github issue [#4206](https://github.com/cython/cython/issues/4206 "https://github.com/cython/cython/issues/4206"))
* Several issues with the new `cpp_locals` directive were resolved and
  its test coverage improved.
  Patch by David Woods. (Github issues [#4265](https://github.com/cython/cython/issues/4265 "https://github.com/cython/cython/issues/4265"), [#4266](https://github.com/cython/cython/issues/4266 "https://github.com/cython/cython/issues/4266"))
* Declarations for `libcpp.algorithms`, `libcpp.set` and `libcpp.unordered_set`
  were extended.
  Patch by David Woods. (Github issues [#4271](https://github.com/cython/cython/issues/4271 "https://github.com/cython/cython/issues/4271"), [#4273](https://github.com/cython/cython/issues/4273 "https://github.com/cython/cython/issues/4273"))
* Several C++ library declarations were added and fixed.
  Patches by Dobatymo, account-login, Jonathan Helgert, Evgeny Yakimov, GalaxySnail, Max Bachmann.
  (Github issues [#4408](https://github.com/cython/cython/issues/4408 "https://github.com/cython/cython/issues/4408"), [#4419](https://github.com/cython/cython/issues/4419 "https://github.com/cython/cython/issues/4419"), [#4410](https://github.com/cython/cython/issues/4410 "https://github.com/cython/cython/issues/4410"), [#4395](https://github.com/cython/cython/issues/4395 "https://github.com/cython/cython/issues/4395"),
  [#4423](https://github.com/cython/cython/issues/4423 "https://github.com/cython/cython/issues/4423"), [#4448](https://github.com/cython/cython/issues/4448 "https://github.com/cython/cython/issues/4448"), [#4462](https://github.com/cython/cython/issues/4462 "https://github.com/cython/cython/issues/4462"), [#3293](https://github.com/cython/cython/issues/3293 "https://github.com/cython/cython/issues/3293"), [#4522](https://github.com/cython/cython/issues/4522 "https://github.com/cython/cython/issues/4522"),
  [#2171](https://github.com/cython/cython/issues/2171 "https://github.com/cython/cython/issues/2171"), [#4531](https://github.com/cython/cython/issues/4531 "https://github.com/cython/cython/issues/4531"))
* Templating C++ classes with memory view types lead to buggy code and is now rejected.
  Patch by David Woods. (Github issue [#3085](https://github.com/cython/cython/issues/3085 "https://github.com/cython/cython/issues/3085"))
* `prange` loops generated incorrect code when `cpp_locals` is enabled.
  Patch by David Woods. (Github issue [#4354](https://github.com/cython/cython/issues/4354 "https://github.com/cython/cython/issues/4354"))
* Direct assignments to C++ references are now allowed.
  Patch by David Woods. (Github issue [#1863](https://github.com/cython/cython/issues/1863 "https://github.com/cython/cython/issues/1863"))
* Conversion from Python dict to C++ map now supports arbitrary Python mappings,
  not just dicts.
* Some C++ and CPython library declarations were extended and fixed.
  Patches by Max Bachmann, Till Hoffmann, Julien Jerphanion, Wenjun Si.
  (Github issues [#4530](https://github.com/cython/cython/issues/4530 "https://github.com/cython/cython/issues/4530"), [#4528](https://github.com/cython/cython/issues/4528 "https://github.com/cython/cython/issues/4528"), [#4710](https://github.com/cython/cython/issues/4710 "https://github.com/cython/cython/issues/4710"), [#4746](https://github.com/cython/cython/issues/4746 "https://github.com/cython/cython/issues/4746"),
  [#4751](https://github.com/cython/cython/issues/4751 "https://github.com/cython/cython/issues/4751"), [#4818](https://github.com/cython/cython/issues/4818 "https://github.com/cython/cython/issues/4818"), [#4762](https://github.com/cython/cython/issues/4762 "https://github.com/cython/cython/issues/4762"), [#4910](https://github.com/cython/cython/issues/4910 "https://github.com/cython/cython/issues/4910"))
* Some C/C++ warnings were resolved.
  Patches by Max Bachmann, Alexander Shadchin, at al.
  (Github issues [#5004](https://github.com/cython/cython/issues/5004 "https://github.com/cython/cython/issues/5004"), [#5005](https://github.com/cython/cython/issues/5005 "https://github.com/cython/cython/issues/5005"), [#5019](https://github.com/cython/cython/issues/5019 "https://github.com/cython/cython/issues/5019"), [#5029](https://github.com/cython/cython/issues/5029 "https://github.com/cython/cython/issues/5029"), [#5096](https://github.com/cython/cython/issues/5096 "https://github.com/cython/cython/issues/5096"))
* C++ references did not work on fused types.
  (Github issue [#4717](https://github.com/cython/cython/issues/4717 "https://github.com/cython/cython/issues/4717"))
* C++ iteration more safely stores the iterable in temporary variables.
  Patch by Xavier. (Github issue [#3828](https://github.com/cython/cython/issues/3828 "https://github.com/cython/cython/issues/3828"))
* C++ post-increment/-decrement operators were not correctly looked up on declared C++
  classes, thus allowing Cython declarations to be missing for them and incorrect C++
  code to be generated.
  Patch by Max Bachmann. (Github issue [#4536](https://github.com/cython/cython/issues/4536 "https://github.com/cython/cython/issues/4536"))
* `cdef public` functions used an incorrect linkage declaration in C++.
  Patch by Maximilien Colange. (Github issue [#1839](https://github.com/cython/cython/issues/1839 "https://github.com/cython/cython/issues/1839"))
* Declarations were added for the C++ bit operations, some other parts of C++20 and CPython APIs.
  Patches by Jonathan Helgert, Dobatymo, William Ayd and Max Bachmann.
  (Github issues [#4962](https://github.com/cython/cython/issues/4962 "https://github.com/cython/cython/issues/4962"), [#5101](https://github.com/cython/cython/issues/5101 "https://github.com/cython/cython/issues/5101"), [#5157](https://github.com/cython/cython/issues/5157 "https://github.com/cython/cython/issues/5157"), [#5163](https://github.com/cython/cython/issues/5163 "https://github.com/cython/cython/issues/5163"), [#5257](https://github.com/cython/cython/issues/5257 "https://github.com/cython/cython/issues/5257"))
* `cpp_locals` no longer have to be “assignable”.
  (Github issue [#4558](https://github.com/cython/cython/issues/4558 "https://github.com/cython/cython/issues/4558"))
* Nested `cppclass` definitions are supported.
  Patch by samaingw. (Github issue [#1218](https://github.com/cython/cython/issues/1218 "https://github.com/cython/cython/issues/1218"))
* `reversed()` can now be used together with C++ iteration.
  Patch by Chia-Hsiang Cheng. (Github issue [#5002](https://github.com/cython/cython/issues/5002 "https://github.com/cython/cython/issues/5002"))
* Some C++ warnings regarding `const` usage in internally generated utility code were resolved.
  Patch by Max Bachmann. (Github issue [#5301](https://github.com/cython/cython/issues/5301 "https://github.com/cython/cython/issues/5301"))
* Cython generated C++ code accidentally used C++11 features in some cases.
  (Github issue [#5316](https://github.com/cython/cython/issues/5316 "https://github.com/cython/cython/issues/5316"))
* Fully qualified C++ names prefixed by a cimported module name could fail to compile.
  Patch by Chia-Hsiang Cheng. (Github issue [#5229](https://github.com/cython/cython/issues/5229 "https://github.com/cython/cython/issues/5229"))
* C++ declarations for `<cmath>`, `<numbers>` and `std::any` were added.
  Patches by Jonathan Helgert and Maximilien Colange.
  (Github issues [#5262](https://github.com/cython/cython/issues/5262 "https://github.com/cython/cython/issues/5262"), [#5309](https://github.com/cython/cython/issues/5309 "https://github.com/cython/cython/issues/5309"), [#5314](https://github.com/cython/cython/issues/5314 "https://github.com/cython/cython/issues/5314"))
* The `extern "C"` and `extern "C++"` markers that Cython generates for
  `public` functions can now be controlled by setting the C macro `CYTHON_EXTERN_C`.
* C++ containers of item type `bint` could conflict with those of item type `int`.
  (Github issue [#5516](https://github.com/cython/cython/issues/5516 "https://github.com/cython/cython/issues/5516"))
* Reverse iteration in C++ no longer removes the `const` qualifier from the item type.
  Patch by Isuru Fernando. (Github issue [#5478](https://github.com/cython/cython/issues/5478 "https://github.com/cython/cython/issues/5478"))

### Commandline Interface[¶](#commandline-interface "Link to this heading")

A number of new options were added to the `cython` and `cythonize`
commands.

#### Related changes[¶](#id69 "Link to this heading")

* The command line parser was rewritten and modernised using `argparse`.
  Patch by Egor Dranischnikow. (Github issue [#2952](https://github.com/cython/cython/issues/2952 "https://github.com/cython/cython/issues/2952"), [#3001](https://github.com/cython/cython/issues/3001 "https://github.com/cython/cython/issues/3001"))
* `cygdb` gives better error messages when it fails to initialise the
  Python runtime support in gdb.
  Patch by Volker Weissmann. (Github issue [#3489](https://github.com/cython/cython/issues/3489 "https://github.com/cython/cython/issues/3489"))
* `--no-docstrings` option added to `cythonize` script.
  Original patch by mo-han. (Github issue [#2889](https://github.com/cython/cython/issues/2889 "https://github.com/cython/cython/issues/2889"))
* Code annotation accepts a new debugging argument `--annotate-fullc` that
  will include the complete syntax highlighted C file in the HTML output.
  (Github issue [#2855](https://github.com/cython/cython/issues/2855 "https://github.com/cython/cython/issues/2855"))
* `cygdb` has a new option `--skip-interpreter` that allows using a different
  Python runtime than the one used to generate the debugging information.
  Patch by Alessandro Molina. (Github issue [#4186](https://github.com/cython/cython/issues/4186 "https://github.com/cython/cython/issues/4186"))
* `cythonize()` and the corresponding CLI command now regenerate the output files
  also when they already exist but were generated by a different Cython version.
* The `cython` and `cythonize` commands ignored non-existing input files without error.
  Patch by Matúš Valo. (Github issue [#4629](https://github.com/cython/cython/issues/4629 "https://github.com/cython/cython/issues/4629"))
* `cythonize --help` now also prints information about the supported environment variables.
  Patch by Matúš Valo. (Github issue [#1711](https://github.com/cython/cython/issues/1711 "https://github.com/cython/cython/issues/1711"))
* Using the `--working` option could lead to sources not being found.
  Patch by Lisandro Dalcin. (Github issue [#5365](https://github.com/cython/cython/issues/5365 "https://github.com/cython/cython/issues/5365"))
* Passing a language level and directives on the command line lost the language level setting.
  Patch by Matúš Valo. (Github issue [#5484](https://github.com/cython/cython/issues/5484 "https://github.com/cython/cython/issues/5484"))
* `cython --version` now prints the version to both stdout and stderr (unless that is a TTY).
  (Github issue [#5504](https://github.com/cython/cython/issues/5504 "https://github.com/cython/cython/issues/5504"))

### Build integration[¶](#build-integration "Link to this heading")

Cython has made a number of improvements both to how it compiles itself
and how it integrates with external build tools. Most notably Cython
has been moving to use `setuptools` instead of the deprecated/removed
`distutils` where possible.

The new `--depfile` option generates dependency files to help integrate
Cython with other build tools.

#### Related changes[¶](#id70 "Link to this heading")

* Binary Linux wheels now follow the manylinux2010 standard.
  Patch by Alexey Stepanov. (Github issue [#3355](https://github.com/cython/cython/issues/3355 "https://github.com/cython/cython/issues/3355"))
* The search order for include files was changed. Previously it was
  `include_directories`, `Cython/Includes`, `sys.path`. Now it is
  `include_directories`, `sys.path`, `Cython/Includes`. This was done to
  allow third-party `*.pxd` files to override the ones in Cython.
  Patch by Matti Picus. (Github issue [#2905](https://github.com/cython/cython/issues/2905 "https://github.com/cython/cython/issues/2905"))
* Source file fingerprinting now uses SHA-1 instead of MD5 since the latter
  tends to be slower and less widely supported these days.
  (Github issue [#2790](https://github.com/cython/cython/issues/2790 "https://github.com/cython/cython/issues/2790"))
* The Cython AST code serialiser class `CodeWriter` in `Cython.CodeWriter`
  supports more syntax nodes.
* Parallel builds of Cython itself (`setup.py build_ext -j N`) failed on Windows.
* When importing the old Cython `build_ext` integration with distutils, the
  additional command line arguments leaked into the regular command.
  Patch by Kamekameha. (Github issue [#2209](https://github.com/cython/cython/issues/2209 "https://github.com/cython/cython/issues/2209"))
* `.pxd` files can now be [versioned](userguide/sharing_declarations.html#versioning "userguide/sharing_declarations.html#versioning") by adding an
  extension like “`.cython-30.pxd`” to prevent older Cython versions (than
  3.0 in this case) from picking them up. (Github issue [#3577](https://github.com/cython/cython/issues/3577 "https://github.com/cython/cython/issues/3577"))
* The Cython `CodeWriter` can now handle more syntax constructs.
  Patch by Tao He. (Github issue [#3514](https://github.com/cython/cython/issues/3514 "https://github.com/cython/cython/issues/3514"))
* The Cython `CodeWriter` mishandled no-argument `return` statements.
  Patch by Tao He. (Github issue [#3795](https://github.com/cython/cython/issues/3795 "https://github.com/cython/cython/issues/3795"))
* Cython now detects when existing output files were not previously generated
  by itself and refuses to overwrite them. It is a common mistake to name
  the module file of a wrapper after the library (source file) that it wraps,
  which can lead to surprising errors when the file gets overwritten.
* The `Cython.Build.BuildExecutable` tool no longer executes the program automatically.
  Use `cythonrun` for that.
* Python modules were not automatically recompiled when only their `.pxd` file changed.
  Patch by Golden Rockefeller. (Github issue [#1428](https://github.com/cython/cython/issues/1428 "https://github.com/cython/cython/issues/1428"))
* An unnecessary slow-down at import time was removed from `Cython.Distutils`.
  Original patch by Anthony Sottile. (Github issue [#4224](https://github.com/cython/cython/issues/4224 "https://github.com/cython/cython/issues/4224"))
* A compiler crash when running Cython thread-parallel from distutils was resolved.
  (Github issue [#4503](https://github.com/cython/cython/issues/4503 "https://github.com/cython/cython/issues/4503"))
* An incompatibility with recent coverage.py versions was resolved.
  Patch by David Woods. (Github issue [#4440](https://github.com/cython/cython/issues/4440 "https://github.com/cython/cython/issues/4440"))
* `pyximport` now uses `cythonize()` internally.
  Patch by Matúš Valo. (Github issue [#2304](https://github.com/cython/cython/issues/2304 "https://github.com/cython/cython/issues/2304"))
* `Cython.Distutils.build_ext` now uses `cythonize()` internally (previously
  known as `new_build_ext`), while still supporting the options that were
  available in the old implementation (`old_build_ext`).
  Patch by Matúš Valo. (Github issue [#3541](https://github.com/cython/cython/issues/3541 "https://github.com/cython/cython/issues/3541"))
* Improve compatibility between classes pickled in Cython 3.0 and 0.29.x
  by accepting MD5, SHA-1 and SHA-256 checksums.
  (Github issue [#4680](https://github.com/cython/cython/issues/4680 "https://github.com/cython/cython/issues/4680"))
* `pyximport` failed for long filenames on Windows.
  Patch by Matti Picus. (Github issue [#4630](https://github.com/cython/cython/issues/4630 "https://github.com/cython/cython/issues/4630"))
* A new Cython build option `--cython-compile-minimal` was added to compile only a
  smaller set of Cython’s own modules, which can be used to reduce the package
  and install size.
* The environment variable `CYTHON_FORCE_REGEN=1` can be used to force `cythonize`
  to regenerate the output files regardless of modification times and changes.
* The `cythonize` and `cython` commands have a new option `-M` / `--depfile`
  to generate `.dep` dependency files for the compilation unit. This can be used
  by external build tools to track these dependencies.
  The `cythonize` option was already available in Cython [0.29.27 (2022-01-28)](#id158 "#id158").
  Patches by Evgeni Burovski and Eli Schwartz. (Github issue [#1214](https://github.com/cython/cython/issues/1214 "https://github.com/cython/cython/issues/1214"))
* Wheels now include a compiled parser again, which increases their size a little
  but gives about a 10% speed-up when running Cython.
* The wheel building process was migrated to use the `cibuildwheel` tool.
  Patch by Thomas Li. (Github issue [#4736](https://github.com/cython/cython/issues/4736 "https://github.com/cython/cython/issues/4736"))
* `setup.cfg` was missing from the source distribution.
  (Github issue [#5199](https://github.com/cython/cython/issues/5199 "https://github.com/cython/cython/issues/5199"))
* Extended glob paths with `/**/` and `\**\` for finding source files failed on Windows.
* Coverage analysis failed in projects with a separate source subdirectory.
  Patch by Sviatoslav Sydorenko and Ruben Vorderman. (Github issue [#3636](https://github.com/cython/cython/issues/3636 "https://github.com/cython/cython/issues/3636"))
* Cython could crash when finding import files with dots in their names.
  Patch by Matúš Valo. (Github issue [#5396](https://github.com/cython/cython/issues/5396 "https://github.com/cython/cython/issues/5396"))
* A module loading problem with `cython.inline()` on Windows was resolved.

### Deprecations[¶](#deprecations "Link to this heading")

Some older features of Cython have been deprecated. Most notable are the
compile time `DEF` and `IF` statements, although we emphasise that
they will remain until a good alternative exists for all their use-cases.

#### Related changes[¶](#id71 "Link to this heading")

* Dotted filenames for qualified module names (`pkg.mod.pyx`) are deprecated.
  Use the normal Python package directory layout instead.
  (Github issue [#2686](https://github.com/cython/cython/issues/2686 "https://github.com/cython/cython/issues/2686"))
* “Declaration after use” is now an error for variables.
  Patch by David Woods. (Github issue [#3976](https://github.com/cython/cython/issues/3976 "https://github.com/cython/cython/issues/3976"))
* Variables can no longer be declared with `cpdef`.
  Patch by David Woods. (Github issue [#887](https://github.com/cython/cython/issues/887 "https://github.com/cython/cython/issues/887"))
* The compile-time `DEF` and `IF` statements are deprecated and generate a warning.
  They should be replaced with normal constants, code generation or C macros.
  (Github issue [#4310](https://github.com/cython/cython/issues/4310 "https://github.com/cython/cython/issues/4310"))
* C-style array declarations (`cdef int a[4]`) are now (silently) deprecated in
  favour of the Java-style `cdef int[4] a` form. The latter was always available
  and the Python type declaration syntax already used it exclusively (`a: int[4]`).
  Patch by Matúš Valo. (Github issue [#5248](https://github.com/cython/cython/issues/5248 "https://github.com/cython/cython/issues/5248"))
* The undocumented, untested and apparently useless syntax
  `from somemodule cimport class/struct/union somename` was removed. The type
  modifier is not needed here and a plain `cimport` of the name will do.
  (Github issue [#4904](https://github.com/cython/cython/issues/4904 "https://github.com/cython/cython/issues/4904"))

### Editor support[¶](#editor-support "Link to this heading")

#### Related changes[¶](#id72 "Link to this heading")

* C compiler warnings and errors are now shown in Jupyter notebooks.
  Patch by Egor Dranischnikow. (Github issue [#3751](https://github.com/cython/cython/issues/3751 "https://github.com/cython/cython/issues/3751"))
* An endless loop in `cython-mode.el` was resolved.
  Patch by Johannes Mueller. (Github issue [#3218](https://github.com/cython/cython/issues/3218 "https://github.com/cython/cython/issues/3218"))
* The Emacs Cython mode file `cython-mode.el` is now maintained in a separate repo:
  [https://github.com/cython/emacs-cython-mode](https://github.com/cython/emacs-cython-mode "https://github.com/cython/emacs-cython-mode")
* The C code shown in the annotated HTML output could lack the last C code line(s).

### Other changes[¶](#id73 "Link to this heading")

* Memoryviews failed to compile when the `cache_builtins` feature was disabled.
  Patch by David Woods. (Github issue [#3406](https://github.com/cython/cython/issues/3406 "https://github.com/cython/cython/issues/3406"))
* Broadcast assignments to a multi-dimensional memory view slice could end
  up in the wrong places when the underlying memory view is known to be
  contiguous but the slice is not.
  (Github issue [#2941](https://github.com/cython/cython/issues/2941 "https://github.com/cython/cython/issues/2941"))
* The Pythran `shape` attribute is supported.
  Patch by Serge Guelton. (Github issue [#3307](https://github.com/cython/cython/issues/3307 "https://github.com/cython/cython/issues/3307"))
* `--no-capture` added to `runtests.py` to prevent stdout/stderr capturing
  during srctree tests.
  Patch by Matti Picus. (Github issue [#2701](https://github.com/cython/cython/issues/2701 "https://github.com/cython/cython/issues/2701"))
* Decoding an empty bytes/char\* slice with large bounds could crash.
  Patch by Sam Sneddon. (Github issue [#3534](https://github.com/cython/cython/issues/3534 "https://github.com/cython/cython/issues/3534"))
* Creating an empty unicode slice with large bounds could crash.
  Patch by Sam Sneddon. (Github issue [#3531](https://github.com/cython/cython/issues/3531 "https://github.com/cython/cython/issues/3531"))
* Complex buffer item types of structs of arrays could fail to validate.
  Patch by Leo and smutch. (Github issue [#1407](https://github.com/cython/cython/issues/1407 "https://github.com/cython/cython/issues/1407"))
* Error handling in `cython.array` creation was improved to avoid calling
  C-API functions with an error held.
* Error handling early in the module init code could lead to a crash.
* Exception position reporting could run into race conditions on threaded code.
  It now uses function-local variables again.
* A reference leak on import failures was resolved.
  Patch by Max Bachmann. (Github issue [#4056](https://github.com/cython/cython/issues/4056 "https://github.com/cython/cython/issues/4056"))
* Casting to ctuples is now allowed.
  Patch by David Woods. (Github issue [#3808](https://github.com/cython/cython/issues/3808 "https://github.com/cython/cython/issues/3808"))
* Some issues were resolved that could lead to duplicated C names.
  Patch by David Woods. (Github issue [#3716](https://github.com/cython/cython/issues/3716 "https://github.com/cython/cython/issues/3716"), [#3741](https://github.com/cython/cython/issues/3741 "https://github.com/cython/cython/issues/3741"), [#3734](https://github.com/cython/cython/issues/3734 "https://github.com/cython/cython/issues/3734"))
* Inline functions and other code in `.pxd` files could accidentally
  inherit the compiler directives of the `.pyx` file that imported them.
  Patch by David Woods. (Github issue [#1071](https://github.com/cython/cython/issues/1071 "https://github.com/cython/cython/issues/1071"))
* Parts of the documentation were (and are being) rewritten to show the
  Cython language syntax next to the equivalent Python syntax.
  Patches by 0dminnimda and Matúš Valo. (Github issue [#4187](https://github.com/cython/cython/issues/4187 "https://github.com/cython/cython/issues/4187"))
* A name collision when including multiple generated API header files was resolved.
  Patch by David Woods. (Github issue [#4308](https://github.com/cython/cython/issues/4308 "https://github.com/cython/cython/issues/4308"))
* Very early errors during module initialisation could lead to crashes.
  Patch by David Woods. (Github issue [#4377](https://github.com/cython/cython/issues/4377 "https://github.com/cython/cython/issues/4377"))
* Type errors when passing memory view arguments could leak buffer references.
  Patch by David Woods. (Github issue [#4296](https://github.com/cython/cython/issues/4296 "https://github.com/cython/cython/issues/4296"))
* The GIL can now safely be released inside of `nogil` functions (which may actually
  be called with the GIL held at runtime).
  Patch by David Woods. (Github issue [#4137](https://github.com/cython/cython/issues/4137 "https://github.com/cython/cython/issues/4137"))
* The return type of a fused function is no longer ignored for function pointers,
  since it is relevant when passing them e.g. as argument into other fused functions.
  Patch by David Woods. (Github issue [#4644](https://github.com/cython/cython/issues/4644 "https://github.com/cython/cython/issues/4644"))
* Using memoryview arguments in closures of inner functions could lead to ref-counting errors.
  Patch by David Woods. (Github issue [#4798](https://github.com/cython/cython/issues/4798 "https://github.com/cython/cython/issues/4798"))
* Decorators like `@cfunc` and `@ccall` could leak into nested functions and classes.
  Patch by David Woods. (Github issue [#4092](https://github.com/cython/cython/issues/4092 "https://github.com/cython/cython/issues/4092"))
* Cython now uses a `.dev0` version suffix for unreleased source installations.
* The `Tempita` module no longer contains HTML processing capabilities, which
  were found to be broken in Python 3.8 and later.
  Patch by Marcel Stimberg. (Github issue [#3309](https://github.com/cython/cython/issues/3309 "https://github.com/cython/cython/issues/3309"))
* Nesting fused types in other fused types could fail to specialise the inner type.
  (Github issue [#4725](https://github.com/cython/cython/issues/4725 "https://github.com/cython/cython/issues/4725"))
* Iterating over memoryviews in generator expressions could leak a buffer reference.
  (Github issue [#4968](https://github.com/cython/cython/issues/4968 "https://github.com/cython/cython/issues/4968"))
* The C `float` type was not inferred on assignments.
  (Github issue [#5234](https://github.com/cython/cython/issues/5234 "https://github.com/cython/cython/issues/5234"))
* Type checks for Python’s `memoryview` type generated incorrect C code.
  (Github issues [#5268](https://github.com/cython/cython/issues/5268 "https://github.com/cython/cython/issues/5268"), [#5270](https://github.com/cython/cython/issues/5270 "https://github.com/cython/cython/issues/5270"))
* Auto-generated utility code didn’t always have all required user defined types available.
  (Github issue [#5269](https://github.com/cython/cython/issues/5269 "https://github.com/cython/cython/issues/5269"))
* `cimport_from_pyx` could miss some declarations.
  Patch by Chia-Hsiang Cheng. (Github issue [#5318](https://github.com/cython/cython/issues/5318 "https://github.com/cython/cython/issues/5318"))
* For-loops now release the internal reference to their list/tuple iterable before
  instead of after the `else:` clause. This probably has no practical impact.
  (Github issue [#5347](https://github.com/cython/cython/issues/5347 "https://github.com/cython/cython/issues/5347"))
* Extension type hierarchies were generated in the wrong order, thus leading to compile issues.
  Patch by Lisandro Dalcin. (Github issue [#5395](https://github.com/cython/cython/issues/5395 "https://github.com/cython/cython/issues/5395"))
* The FAQ page was moved from the GitHub Wiki to the regular documentation
  to make it more visible.

## 3.0.0 (2023-07-17)[¶](#id74 "Link to this heading")

### Bugs fixed[¶](#id75 "Link to this heading")

* A crash in Python 2.7 was fixed when cleaning up extension type instances
  at program end.

## 3.0.0 rc 2 (2023-07-13)[¶](#rc-2-2023-07-13 "Link to this heading")

### Bugs fixed[¶](#id76 "Link to this heading")

* Parser crash on hex/oct enum values.
  (Github issue [#5524](https://github.com/cython/cython/issues/5524 "https://github.com/cython/cython/issues/5524"))
* `cython --version` now prints the version to both stdout and stderr (unless that is a TTY).
  (Github issue [#5504](https://github.com/cython/cython/issues/5504 "https://github.com/cython/cython/issues/5504"))

## 3.0.0 rc 1 (2023-07-12)[¶](#rc-1-2023-07-12 "Link to this heading")

### Features added[¶](#id77 "Link to this heading")

* `with gil` and `with nogil(flag)` now accept their flag argument also in Python code.
  Patch by Matúš Valo. (Github issue [#5113](https://github.com/cython/cython/issues/5113 "https://github.com/cython/cython/issues/5113"))
* A new decorator `@cython.with_gil` is available in Python code to match the `with gil`
  function declaration in Cython syntax.
* Assigning a list to a ctuple is slightly faster.

### Bugs fixed[¶](#id78 "Link to this heading")

* The reference counting of memory views involved useless overhead.
  (Github issue [#5510](https://github.com/cython/cython/issues/5510 "https://github.com/cython/cython/issues/5510"))
* Duplicate values in a `cpdef` enum could lead to invalid switch statements.
  (Github issue [#5400](https://github.com/cython/cython/issues/5400 "https://github.com/cython/cython/issues/5400"))
* Handling freshly raised exceptions that didn’t have a traceback yet could crash.
  (Github issue [#5495](https://github.com/cython/cython/issues/5495 "https://github.com/cython/cython/issues/5495"))
* Reverse iteration in C++ no longer removes the `const` qualifier from the item type.
  Patch by Isuru Fernando. (Github issue [#5478](https://github.com/cython/cython/issues/5478 "https://github.com/cython/cython/issues/5478"))
* C++ containers of item type `bint` could conflict with those of item type `int`.
  (Github issue [#5516](https://github.com/cython/cython/issues/5516 "https://github.com/cython/cython/issues/5516"))
* With MSVC, Cython no longer enables C-Complex support by accident (which is not supported there).
  (Github issue [#5512](https://github.com/cython/cython/issues/5512 "https://github.com/cython/cython/issues/5512"))
* The Python implementation of `cimport cython.cimports…` could raise an `ImportError`
  instead of an `AttributeError` when looking up package variable names.
  Patch by Matti Picus. (Github issue [#5411](https://github.com/cython/cython/issues/5411 "https://github.com/cython/cython/issues/5411"))
* Passing a language level and directives on the command line lost the language level setting.
  Patch by Matúš Valo. (Github issue [#5484](https://github.com/cython/cython/issues/5484 "https://github.com/cython/cython/issues/5484"))
* Some typedef declarations for libc function types were fixed.
  (Github issue [#5498](https://github.com/cython/cython/issues/5498 "https://github.com/cython/cython/issues/5498"))
* Some C compiler warnings and errors in CPython 3.12 were resolved.
* The deprecated `_PyGC_FINALIZED()` C-API macro is no longer used.
  Patch by Thomas Caswell and Matúš Valo. (Github issue [#5481](https://github.com/cython/cython/issues/5481 "https://github.com/cython/cython/issues/5481"))
* A compile error when using `__debug__` was resolved.
* A module loading problem with `cython.inline()` on Windows was resolved.
* `cython --version` now prints the version to stdout instead of stderr.
  (Github issue [#5504](https://github.com/cython/cython/issues/5504 "https://github.com/cython/cython/issues/5504"))
* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the [0.29.36 (2023-07-04)](#id127 "#id127") release.

### Other changes[¶](#id79 "Link to this heading")

* The FAQ page was moved from the GitHub Wiki to the regular documentation
  to make it more visible.
* `np.long_t` and `np.ulong_t` were removed from the NumPy declarations,
  syncing Cython with upstream NumPy v1.25.0. The aliases were confusing
  since they could mean different things on different platforms.

## 3.0.0 beta 3 (2023-05-24)[¶](#beta-3-2023-05-24 "Link to this heading")

### Features added[¶](#id80 "Link to this heading")

* Custom buffer slot methods are now supported in the Limited C-API of Python 3.9+.
  Patch by Lisandro Dalcin. (Github issue [#5422](https://github.com/cython/cython/issues/5422 "https://github.com/cython/cython/issues/5422"))
* The `extern "C"` and `extern "C++"` markers that Cython generates for
  `public` functions can now be controlled by setting the C macro `CYTHON_EXTERN_C`.
* The Python `int` handling code was adapted to make use of the new `PyLong`
  internals in CPython 3.12.
  (Github issue [#5353](https://github.com/cython/cython/issues/5353 "https://github.com/cython/cython/issues/5353"))
* Conversion of Python ints to C `int128` is now always supported, although slow
  if dedicated C-API support is missing (`_PyLong_AsByteArray()`), specifically in
  the Limited C-API.
  (Github issue [#5419](https://github.com/cython/cython/issues/5419 "https://github.com/cython/cython/issues/5419"))
* The exception handling code was adapted to CPython 3.12.
  (Github issue [#5442](https://github.com/cython/cython/issues/5442 "https://github.com/cython/cython/issues/5442"))
* The dataclass implementation was adapted to support Python 3.12.
  (Github issue [#5346](https://github.com/cython/cython/issues/5346 "https://github.com/cython/cython/issues/5346"))
* The normal `@dataclasses.dataclass` and `@functools.total_ordering` decorators
  can now be used on extension types. Using the corresponding `@cython.*` decorator
  will automatically turn a Python class into an extension type (no need for `@cclass`).
  (Github issue [#5292](https://github.com/cython/cython/issues/5292 "https://github.com/cython/cython/issues/5292"))
* Multiplying a sequence by a C integer avoids creating and intermediate Python integer.
* ctuples can now be assigned from arbitrary sequences, not just Python tuples.
* A new directive `embedsignature.format` was added to select the format of the
  docstring embedded signatures between `python`, `c` and argument `clinic`.
  Patch by Lisandro Dalcin. (Github issue [#5415](https://github.com/cython/cython/issues/5415 "https://github.com/cython/cython/issues/5415"))
* Some invalid directive usages are now detected and rejected, e.g. using `@ccall`
  together with `@cfunc`, and applying `@cfunc` to a `@ufunc`. Cython also
  warns now when a directive is applied needlessly.
  (Github issue [#5399](https://github.com/cython/cython/issues/5399 "https://github.com/cython/cython/issues/5399") et al.)
* Unicode identifier names now allow all letters defined in CPython 3.12.

### Bugs fixed[¶](#id81 "Link to this heading")

* Some C compile failures in CPython 3.12.0a6/a7 were resolved.
* Cascaded comparisons between integer constants and Python types could fail to compile.
  (Github issue [#5354](https://github.com/cython/cython/issues/5354 "https://github.com/cython/cython/issues/5354"))
* The internal macro `__PYX_IS_UNSIGNED` was accidentally duplicated in beta 2
  which lead to C compile errors.
  Patch by 0dminnimda. (Github issue [#5356](https://github.com/cython/cython/issues/5356 "https://github.com/cython/cython/issues/5356"))
* Memoryviews with typedef item types could fail to match the non-typedef item types.
  Patch by Yue Yang. (Github issue [#5373](https://github.com/cython/cython/issues/5373 "https://github.com/cython/cython/issues/5373"))
* Fused memory views could raise a `TypeError` instead of a `ValueError` on creation.
  Patch by Matúš Valo. (Github issue [#5401](https://github.com/cython/cython/issues/5401 "https://github.com/cython/cython/issues/5401"))
* Cython could crash when finding import files with dots in their names.
  Patch by Matúš Valo. (Github issue [#5396](https://github.com/cython/cython/issues/5396 "https://github.com/cython/cython/issues/5396"))
* Selecting a context manager in parentheses and then calling it directly failed to parse.
  (Github issue [#5403](https://github.com/cython/cython/issues/5403 "https://github.com/cython/cython/issues/5403"))
* `__qualname__` and `__module__` were not available inside of class bodies.
  (Github issue [#4447](https://github.com/cython/cython/issues/4447 "https://github.com/cython/cython/issues/4447"))
* `noexcept` was not automatically applied to function pointer attributes in extern structs.
  Patch by Matúš Valo. (Github issue [#5359](https://github.com/cython/cython/issues/5359 "https://github.com/cython/cython/issues/5359"))
* Function signatures containing a type like tuple[()] could not be printed.
  Patch by Lisandro Dalcin. (Github issue [#5355](https://github.com/cython/cython/issues/5355 "https://github.com/cython/cython/issues/5355"))
* Extension type hierarchies were generated in the wrong order, thus leading to compile issues.
  Patch by Lisandro Dalcin. (Github issue [#5395](https://github.com/cython/cython/issues/5395 "https://github.com/cython/cython/issues/5395"))
* Using the `--working` option could lead to sources not being found.
  Patch by Lisandro Dalcin. (Github issue [#5365](https://github.com/cython/cython/issues/5365 "https://github.com/cython/cython/issues/5365"))
* Some C compiler warnings were resolved.
  Patches by Matt Tyson, Lisandro Dalcin, Philipp Wagner, Matti Picus et al.
  (Github issues [#5417](https://github.com/cython/cython/issues/5417 "https://github.com/cython/cython/issues/5417"), [#5418](https://github.com/cython/cython/issues/5418 "https://github.com/cython/cython/issues/5418"), [#5421](https://github.com/cython/cython/issues/5421 "https://github.com/cython/cython/issues/5421"), [#5437](https://github.com/cython/cython/issues/5437 "https://github.com/cython/cython/issues/5437"), [#5438](https://github.com/cython/cython/issues/5438 "https://github.com/cython/cython/issues/5438"), [#5443](https://github.com/cython/cython/issues/5443 "https://github.com/cython/cython/issues/5443"))
* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the [0.29.35 (2023-05-24)](#id130 "#id130") release.

### Other changes[¶](#id82 "Link to this heading")

* For-loops now release the internal reference to their list/tuple iterable before
  instead of after the `else:` clause. This probably has no practical impact.
  (Github issue [#5347](https://github.com/cython/cython/issues/5347 "https://github.com/cython/cython/issues/5347"))
* Simple tuple types like `(int, int)` are no longer accepted in Python annotations
  and require the Python notation instead (e.g. `tuple[cython.int, cython.int]`).
  (Github issue [#5397](https://github.com/cython/cython/issues/5397 "https://github.com/cython/cython/issues/5397"))
* The code `except +nogil` (declaring a C++ exception handler function called `nogil`)
  is now rejected because it is almost certainly a typo from `except + nogil`.
  (Github issue [#5430](https://github.com/cython/cython/issues/5430 "https://github.com/cython/cython/issues/5430"))

## 3.0.0 beta 2 (2023-03-27)[¶](#beta-2-2023-03-27 "Link to this heading")

### Features added[¶](#id83 "Link to this heading")

* C++ declarations for `<cmath>`, `<numbers>` and `std::any` were added.
  Patches by Jonathan Helgert and Maximilien Colange.
  (Github issues [#5262](https://github.com/cython/cython/issues/5262 "https://github.com/cython/cython/issues/5262"), [#5309](https://github.com/cython/cython/issues/5309 "https://github.com/cython/cython/issues/5309"), [#5314](https://github.com/cython/cython/issues/5314 "https://github.com/cython/cython/issues/5314"))

### Bugs fixed[¶](#id84 "Link to this heading")

* Unintended internal exception handling lead to a visible performance regression
  for `nogil` memoryview code in 3.0.0b1.
  (Github issue [#5324](https://github.com/cython/cython/issues/5324 "https://github.com/cython/cython/issues/5324"))
* `None` default arguments for arguments with fused memoryview types could select a different
  implementation in 3.0 than in 0.29.x. The selection behaviour is generally considered
  suboptimal but was at least reverted to the old behaviour for now.
  (Github issue [#5297](https://github.com/cython/cython/issues/5297 "https://github.com/cython/cython/issues/5297"))
* The new complex vs. floating point behaviour of the `**` power operator accidentally
  added a dependency on the GIL, which was really only required on failures.
  (Github issue [#5287](https://github.com/cython/cython/issues/5287 "https://github.com/cython/cython/issues/5287"))
* `from cython cimport … as …` could lead to imported names not being found in annotations.
  Patch by Chia-Hsiang Cheng. (Github issue [#5235](https://github.com/cython/cython/issues/5235 "https://github.com/cython/cython/issues/5235"))
* Generated NumPy ufuncs could crash for large arrays due to incorrect GIL handling.
  (Github issue [#5328](https://github.com/cython/cython/issues/5328 "https://github.com/cython/cython/issues/5328"))
* Very long Python integer constants could exceed the maximum C name length of MSVC.
  Patch by 0dminnimda. (Github issue [#5290](https://github.com/cython/cython/issues/5290 "https://github.com/cython/cython/issues/5290"))
* `cimport_from_pyx` could miss some declarations.
  Patch by Chia-Hsiang Cheng. (Github issue [#5318](https://github.com/cython/cython/issues/5318 "https://github.com/cython/cython/issues/5318"))
* Fully qualified C++ names prefixed by a cimported module name could fail to compile.
  Patch by Chia-Hsiang Cheng. (Github issue [#5229](https://github.com/cython/cython/issues/5229 "https://github.com/cython/cython/issues/5229"))
* Cython generated C++ code accidentally used C++11 features in some cases.
  (Github issue [#5316](https://github.com/cython/cython/issues/5316 "https://github.com/cython/cython/issues/5316"))
* Some C++ warnings regarding `const` usage in internally generated utility code were resolved.
  Patch by Max Bachmann. (Github issue [#5301](https://github.com/cython/cython/issues/5301 "https://github.com/cython/cython/issues/5301"))
* With `language_level=2`, imports of modules in packages could return the wrong module in Python 3.
  (Github issue [#5308](https://github.com/cython/cython/issues/5308 "https://github.com/cython/cython/issues/5308"))
* `typing.Optional` could fail on tuple types.
  (Github issue [#5263](https://github.com/cython/cython/issues/5263 "https://github.com/cython/cython/issues/5263"))
* Auto-generated utility code didn’t always have all required user defined types available.
  (Github issue [#5269](https://github.com/cython/cython/issues/5269 "https://github.com/cython/cython/issues/5269"))
* Type checks for Python’s `memoryview` type generated incorrect C code.
  (Github issues [#5268](https://github.com/cython/cython/issues/5268 "https://github.com/cython/cython/issues/5268"), [#5270](https://github.com/cython/cython/issues/5270 "https://github.com/cython/cython/issues/5270"))
* Some issues with `depfile` generation were resolved.
  Patches by Eli Schwartz. (Github issues [#5279](https://github.com/cython/cython/issues/5279 "https://github.com/cython/cython/issues/5279"), [#5291](https://github.com/cython/cython/issues/5291 "https://github.com/cython/cython/issues/5291"))
* Some C code issue were resolved for the Limited API target.
  (Github issues [#5264](https://github.com/cython/cython/issues/5264 "https://github.com/cython/cython/issues/5264"), [#5265](https://github.com/cython/cython/issues/5265 "https://github.com/cython/cython/issues/5265"), [#5266](https://github.com/cython/cython/issues/5266 "https://github.com/cython/cython/issues/5266"))
* The C code shown in the annotated HTML output could lack the last C code line(s).

## 3.0.0 beta 1 (2023-02-25)[¶](#beta-1-2023-02-25 "Link to this heading")

### Features added[¶](#id85 "Link to this heading")

* Cython implemented C functions now propagate exceptions by default, rather than
  swallowing them in non-object returning function if the user forgot to add an
  `except` declaration to the signature. This was a long-standing source of bugs,
  but can require adding the `noexcept` declaration to existing functions if
  exception propagation is really undesired.
  (Github issue [#4280](https://github.com/cython/cython/issues/4280 "https://github.com/cython/cython/issues/4280"))
* To opt out of the new, safer exception handling behaviour, legacy code can set the new
  directive `legacy_implicit_noexcept=True` for a transition period to keep the
  previous, unsafe behaviour. This directive will eventually be removed in a later release.
  Patch by Matúš Valo. (Github issue [#5094](https://github.com/cython/cython/issues/5094 "https://github.com/cython/cython/issues/5094"))
* A new function decorator `@cython.ufunc` automatically generates a (NumPy) ufunc that
  applies the calculation function to an entire memoryview.
  (Github issue [#4758](https://github.com/cython/cython/issues/4758 "https://github.com/cython/cython/issues/4758"))
* The `**` power operator now behaves more like in Python by returning the correct complex
  result if required by math. A new `cpow` directive was added to turn on the previous
  C-like behaviour.
  (Github issue [#4936](https://github.com/cython/cython/issues/4936 "https://github.com/cython/cython/issues/4936"))
* The special `__*pow__` methods now support the 2- and 3-argument variants.
  (Github issue [#5160](https://github.com/cython/cython/issues/5160 "https://github.com/cython/cython/issues/5160"))
* Unknown type annotations (e.g. because of typos) now emit a warning at compile time.
  Patch by Matúš Valo. (Github issue [#5070](https://github.com/cython/cython/issues/5070 "https://github.com/cython/cython/issues/5070"))
* Subscripted builtin types in type declarations (like `list[float]`) are now
  better supported.
  (Github issue [#5058](https://github.com/cython/cython/issues/5058 "https://github.com/cython/cython/issues/5058"))
* Python’s `memoryview` is now a known builtin type with optimised properties.
  (Github issue [#3798](https://github.com/cython/cython/issues/3798 "https://github.com/cython/cython/issues/3798"))
* The call-time dispatch for fused memoryview types is less slow.
  (Github issue [#5073](https://github.com/cython/cython/issues/5073 "https://github.com/cython/cython/issues/5073"))
* Integer comparisons avoid Python coercions if possible.
  (Github issue [#4821](https://github.com/cython/cython/issues/4821 "https://github.com/cython/cython/issues/4821"))
* The Python Enum of a `cpdef enum` now inherits from `IntFlag` to better match
  both Python and C semantics of enums.
  (Github issue [#2732](https://github.com/cython/cython/issues/2732 "https://github.com/cython/cython/issues/2732"))
* [PEP-614](https://www.python.org/dev/peps/pep-0614 "https://www.python.org/dev/peps/pep-0614"):
  decorators can now be arbitrary Python expressions.
  (Github issue [#4570](https://github.com/cython/cython/issues/4570 "https://github.com/cython/cython/issues/4570"))
* `cpdef` enums can now be pickled.
  (Github issue [#5120](https://github.com/cython/cython/issues/5120 "https://github.com/cython/cython/issues/5120"))
* Bound C methods can now coerce to Python objects.
  (Github issues [#4890](https://github.com/cython/cython/issues/4890 "https://github.com/cython/cython/issues/4890"), [#5062](https://github.com/cython/cython/issues/5062 "https://github.com/cython/cython/issues/5062"))
* C arrays can be initialised inside of nogil functions.
  Patch by Matúš Valo. (Github issue [#1662](https://github.com/cython/cython/issues/1662 "https://github.com/cython/cython/issues/1662"))
* `reversed()` can now be used together with C++ iteration.
  Patch by Chia-Hsiang Cheng. (Github issue [#5002](https://github.com/cython/cython/issues/5002 "https://github.com/cython/cython/issues/5002"))
* Standard C/C++ atomic operations are now used for memory views, if available.
  (Github issue [#4925](https://github.com/cython/cython/issues/4925 "https://github.com/cython/cython/issues/4925"))
* C11 `complex.h` is now properly detected.
  (Github issue [#2513](https://github.com/cython/cython/issues/2513 "https://github.com/cython/cython/issues/2513"))
* Nested `cppclass` definitions are supported.
  Patch by samaingw. (Github issue [#1218](https://github.com/cython/cython/issues/1218 "https://github.com/cython/cython/issues/1218"))
* `cpp_locals` no longer have to be “assignable”.
  (Github issue [#4558](https://github.com/cython/cython/issues/4558 "https://github.com/cython/cython/issues/4558"))
* `cythonize --help` now also prints information about the supported environment variables.
  Patch by Matúš Valo. (Github issue [#1711](https://github.com/cython/cython/issues/1711 "https://github.com/cython/cython/issues/1711"))
* Declarations were added for the C++ bit operations, some other parts of C++20 and CPython APIs.
  Patches by Jonathan Helgert, Dobatymo, William Ayd and Max Bachmann.
  (Github issues [#4962](https://github.com/cython/cython/issues/4962 "https://github.com/cython/cython/issues/4962"), [#5101](https://github.com/cython/cython/issues/5101 "https://github.com/cython/cython/issues/5101"), [#5157](https://github.com/cython/cython/issues/5157 "https://github.com/cython/cython/issues/5157"), [#5163](https://github.com/cython/cython/issues/5163 "https://github.com/cython/cython/issues/5163"), [#5257](https://github.com/cython/cython/issues/5257 "https://github.com/cython/cython/issues/5257"))

### Bugs fixed[¶](#id86 "Link to this heading")

* Generator expressions and comprehensions now look up their outer-most iterable
  on creation, as Python does, and not later on start, as they did previously.
  (Github issue [#1159](https://github.com/cython/cython/issues/1159 "https://github.com/cython/cython/issues/1159"))
* Type annotations for Python `int` rejected `long` under Py2 in the alpha-11 release.
  They are now ignored again (as always before) when `language_level=2`, and accept
  both `int` and `long` in Py2 (and only `int` in Py3) otherwise.
  (Github issue [#4944](https://github.com/cython/cython/issues/4944 "https://github.com/cython/cython/issues/4944"))
* Calling bound classmethods of builtin types could fail trying to call the unbound method.
  (Github issue [#5051](https://github.com/cython/cython/issues/5051 "https://github.com/cython/cython/issues/5051"))
* `int(Py_UCS4)` returned the code point instead of the parsed digit value.
  (Github issue [#5216](https://github.com/cython/cython/issues/5216 "https://github.com/cython/cython/issues/5216"))
* Several problems with CPython 3.12 were resolved.
  (Github issue [#5238](https://github.com/cython/cython/issues/5238 "https://github.com/cython/cython/issues/5238"))
* The C `float` type was not inferred on assignments.
  (Github issue [#5234](https://github.com/cython/cython/issues/5234 "https://github.com/cython/cython/issues/5234"))
* Memoryviews with `object` item type were not supported in Python type declarations.
  (Github issue [#4907](https://github.com/cython/cython/issues/4907 "https://github.com/cython/cython/issues/4907"))
* Iterating over memoryviews in generator expressions could leak a buffer reference.
  (Github issue [#4968](https://github.com/cython/cython/issues/4968 "https://github.com/cython/cython/issues/4968"))
* Memory views and the internal Cython array type now identify as `collections.abc.Sequence`
  by setting the `Py_TPFLAGS_SEQUENCE` type flag directly.
  (Github issue [#5187](https://github.com/cython/cython/issues/5187 "https://github.com/cython/cython/issues/5187"))
* `__del__` finaliser methods were not always called if they were only inherited.
  (Github issue [#4995](https://github.com/cython/cython/issues/4995 "https://github.com/cython/cython/issues/4995"))
* Extension types are now explicitly marked as immutable types to prevent them from
  being considered mutable.
  Patch by Max Bachmann. (Github issue [#5023](https://github.com/cython/cython/issues/5023 "https://github.com/cython/cython/issues/5023"))
* `const` types could not be returned from functions.
  Patch by Mike Graham. (Github issue [#5135](https://github.com/cython/cython/issues/5135 "https://github.com/cython/cython/issues/5135"))
* `cdef public` functions declared in .pxd files could use an incorrectly mangled C name.
  Patch by EpigeneMax. (Github issue [#2940](https://github.com/cython/cython/issues/2940 "https://github.com/cython/cython/issues/2940"))
* `cdef public` functions used an incorrect linkage declaration in C++.
  Patch by Maximilien Colange. (Github issue [#1839](https://github.com/cython/cython/issues/1839 "https://github.com/cython/cython/issues/1839"))
* C++ post-increment/-decrement operators were not correctly looked up on declared C++
  classes, thus allowing Cython declarations to be missing for them and incorrect C++
  code to be generated.
  Patch by Max Bachmann. (Github issue [#4536](https://github.com/cython/cython/issues/4536 "https://github.com/cython/cython/issues/4536"))
* C++ iteration more safely stores the iterable in temporary variables.
  Patch by Xavier. (Github issue [#3828](https://github.com/cython/cython/issues/3828 "https://github.com/cython/cython/issues/3828"))
* C++ references did not work on fused types.
  (Github issue [#4717](https://github.com/cython/cython/issues/4717 "https://github.com/cython/cython/issues/4717"))
* The module state struct was not initialised in correct C (before C23), leading to
  compile errors on Windows.
  Patch by yudonglin. (Github issue [#5169](https://github.com/cython/cython/issues/5169 "https://github.com/cython/cython/issues/5169"))
* Structs that contained an array field resulted in incorrect C code. Their initialisation
  now uses `memcpy()`.
  Patch by Chia-Hsiang Cheng. (Github issue [#5178](https://github.com/cython/cython/issues/5178 "https://github.com/cython/cython/issues/5178"))
* Nesting fused types in other fused types could fail to specialise the inner type.
  (Github issue [#4725](https://github.com/cython/cython/issues/4725 "https://github.com/cython/cython/issues/4725"))
* The special methods `__matmul__`, `__truediv__`, `__floordiv__` failed to type
  their `self` argument.
  (Github issue [#5067](https://github.com/cython/cython/issues/5067 "https://github.com/cython/cython/issues/5067"))
* Coverage analysis failed in projects with a separate source subdirectory.
  Patch by Sviatoslav Sydorenko and Ruben Vorderman. (Github issue [#3636](https://github.com/cython/cython/issues/3636 "https://github.com/cython/cython/issues/3636"))
* The `annotation_typing` directive was missing in pure Python mode.
  Patch by 0dminnimda. (Github issue [#5194](https://github.com/cython/cython/issues/5194 "https://github.com/cython/cython/issues/5194"))
* The `@dataclass` directive was accidentally inherited by methods and subclasses.
  (Github issue [#4953](https://github.com/cython/cython/issues/4953 "https://github.com/cython/cython/issues/4953"))
* Some issues with Cython `@dataclass` arguments, hashing, inheritance and `repr()`
  were resolved. (Github issues [#4956](https://github.com/cython/cython/issues/4956 "https://github.com/cython/cython/issues/4956"), [#5046](https://github.com/cython/cython/issues/5046 "https://github.com/cython/cython/issues/5046"))
* `cpdef` enums no longer use `OrderedDict` but `dict` in Python 3.6 and later.
  Patch by GalaxySnail. (Github issue [#5180](https://github.com/cython/cython/issues/5180 "https://github.com/cython/cython/issues/5180"))
* Larger numbers of extension types with multiple subclasses could take very long to compile.
  Patch by Scott Wolchok. (Github issue [#5139](https://github.com/cython/cython/issues/5139 "https://github.com/cython/cython/issues/5139"))
* Relative imports failed in compiled `__init__.py` package modules.
  Patch by Matúš Valo. (Github issue [#3442](https://github.com/cython/cython/issues/3442 "https://github.com/cython/cython/issues/3442"))
* Some old usages of the deprecated Python `imp` module were replaced with `importlib`.
  Patch by Matúš Valo. (Github issue [#4640](https://github.com/cython/cython/issues/4640 "https://github.com/cython/cython/issues/4640"))
* The `cython` and `cythonize` commands ignored non-existing input files without error.
  Patch by Matúš Valo. (Github issue [#4629](https://github.com/cython/cython/issues/4629 "https://github.com/cython/cython/issues/4629"))
* Invalid and misspelled `cython.*` module names were not reported as errors.
  (Github issue [#4947](https://github.com/cython/cython/issues/4947 "https://github.com/cython/cython/issues/4947"))
* Unused `**kwargs` arguments did not show up in `locals()`.
  (Github issue [#4899](https://github.com/cython/cython/issues/4899 "https://github.com/cython/cython/issues/4899"))
* Extended glob paths with `/**/` and `\**\` for finding source files failed on Windows.
* Annotated HTML generation was missing newlines in 3.0.0a11.
  (Github issue [#4945](https://github.com/cython/cython/issues/4945 "https://github.com/cython/cython/issues/4945"))
* Some parser issues were resolved.
  (Github issue [#4992](https://github.com/cython/cython/issues/4992 "https://github.com/cython/cython/issues/4992"))
* `setup.cfg` was missing from the source distribution.
  (Github issue [#5199](https://github.com/cython/cython/issues/5199 "https://github.com/cython/cython/issues/5199"))
* Some C/C++ warnings were resolved.
  Patches by Max Bachmann, Alexander Shadchin, at al.
  (Github issues [#5004](https://github.com/cython/cython/issues/5004 "https://github.com/cython/cython/issues/5004"), [#5005](https://github.com/cython/cython/issues/5005 "https://github.com/cython/cython/issues/5005"), [#5019](https://github.com/cython/cython/issues/5019 "https://github.com/cython/cython/issues/5019"), [#5029](https://github.com/cython/cython/issues/5029 "https://github.com/cython/cython/issues/5029"), [#5096](https://github.com/cython/cython/issues/5096 "https://github.com/cython/cython/issues/5096"))
* The embedding code no longer calls deprecated C-API functions but uses the new `PyConfig`
  API instead on CPython versions that support it (3.8+).
  Patch by Alexander Shadchin. (Github issue [#4895](https://github.com/cython/cython/issues/4895 "https://github.com/cython/cython/issues/4895"))
* Intel C compilers could complain about unsupported gcc pragmas.
  Patch by Ralf Gommers. (Github issue [#5052](https://github.com/cython/cython/issues/5052 "https://github.com/cython/cython/issues/5052"))
* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the [0.29.33 (2023-01-06)](#id136 "#id136") release.

### Other changes[¶](#id87 "Link to this heading")

* The undocumented, untested and apparently useless syntax
  `from somemodule cimport class/struct/union somename` was removed. The type
  modifier is not needed here and a plain `cimport` of the name will do.
  (Github issue [#4904](https://github.com/cython/cython/issues/4904 "https://github.com/cython/cython/issues/4904"))
* C-style array declarations (`cdef int a[4]`) are now (silently) deprecated in
  favour of the Java-style `cdef int[4] a` form. The latter was always available
  and the Python type declaration syntax already used it exclusively (`a: int[4]`).
  Patch by Matúš Valo. (Github issue [#5248](https://github.com/cython/cython/issues/5248 "https://github.com/cython/cython/issues/5248"))
* The wheel building process was migrated to use the `cibuildwheel` tool.
  Patch by Thomas Li. (Github issue [#4736](https://github.com/cython/cython/issues/4736 "https://github.com/cython/cython/issues/4736"))
* Wheels now include a compiled parser again, which increases their size a little
  but gives about a 10% speed-up when running Cython.
* The `Tempita` module no longer contains HTML processing capabilities, which
  were found to be broken in Python 3.8 and later.
  Patch by Marcel Stimberg. (Github issue [#3309](https://github.com/cython/cython/issues/3309 "https://github.com/cython/cython/issues/3309"))
* The Emacs Cython mode file `cython-mode.el` is now maintained in a separate repo:
  [https://github.com/cython/emacs-cython-mode](https://github.com/cython/emacs-cython-mode "https://github.com/cython/emacs-cython-mode")
* Cython now uses a `.dev0` version suffix for unreleased source installations.

## 3.0.0 alpha 11 (2022-07-31)[¶](#alpha-11-2022-07-31 "Link to this heading")

### Features added[¶](#id88 "Link to this heading")

* A new decorator `@cython.dataclasses.dataclass` was implemented that provides
  compile time dataclass generation capabilities to `cdef` classes (extension types).
  Patch by David Woods. (Github issue [#2903](https://github.com/cython/cython/issues/2903 "https://github.com/cython/cython/issues/2903")). `kw_only` dataclasses
  added by Yury Sokov. (Github issue [#4794](https://github.com/cython/cython/issues/4794 "https://github.com/cython/cython/issues/4794"))
* Named expressions (PEP 572) aka. assignment expressions (aka. the walrus operator
  `:=`) were implemented.
  Patch by David Woods. (Github issue [#2636](https://github.com/cython/cython/issues/2636 "https://github.com/cython/cython/issues/2636"))
* Context managers can be written in parentheses.
  Patch by David Woods. (Github issue [#4814](https://github.com/cython/cython/issues/4814 "https://github.com/cython/cython/issues/4814"))
* Cython avoids raising `StopIteration` in `__next__` methods when possible.
  Patch by David Woods. (Github issue [#3447](https://github.com/cython/cython/issues/3447 "https://github.com/cython/cython/issues/3447"))
* Some C++ and CPython library declarations were extended and fixed.
  Patches by Max Bachmann, Till Hoffmann, Julien Jerphanion, Wenjun Si.
  (Github issues [#4530](https://github.com/cython/cython/issues/4530 "https://github.com/cython/cython/issues/4530"), [#4528](https://github.com/cython/cython/issues/4528 "https://github.com/cython/cython/issues/4528"), [#4710](https://github.com/cython/cython/issues/4710 "https://github.com/cython/cython/issues/4710"), [#4746](https://github.com/cython/cython/issues/4746 "https://github.com/cython/cython/issues/4746"),
  [#4751](https://github.com/cython/cython/issues/4751 "https://github.com/cython/cython/issues/4751"), [#4818](https://github.com/cython/cython/issues/4818 "https://github.com/cython/cython/issues/4818"), [#4762](https://github.com/cython/cython/issues/4762 "https://github.com/cython/cython/issues/4762"), [#4910](https://github.com/cython/cython/issues/4910 "https://github.com/cython/cython/issues/4910"))
* The `cythonize` and `cython` commands have a new option `-M` / `--depfile`
  to generate `.dep` dependency files for the compilation unit. This can be used
  by external build tools to track these dependencies.
  The `cythonize` option was already available in Cython [0.29.27 (2022-01-28)](#id158 "#id158").
  Patches by Evgeni Burovski and Eli Schwartz. (Github issue [#1214](https://github.com/cython/cython/issues/1214 "https://github.com/cython/cython/issues/1214"))
* `cythonize()` and the corresponding CLI command now regenerate the output files
  also when they already exist but were generated by a different Cython version.
* Memory views and the internal Cython array type now identify as `collections.abc.Sequence`.
  Patch by David Woods. (Github issue [#4817](https://github.com/cython/cython/issues/4817 "https://github.com/cython/cython/issues/4817"))
* Cython generators and coroutines now identify as `CO_ASYNC_GENERATOR`,
  `CO_COROUTINE` and `CO_GENERATOR` accordingly.
  (Github issue [#4902](https://github.com/cython/cython/issues/4902 "https://github.com/cython/cython/issues/4902"))
* Memory views can use atomic CPU instructions instead of locks in more cases.
  Patch by Sam Gross. (Github issue [#4912](https://github.com/cython/cython/issues/4912 "https://github.com/cython/cython/issues/4912"))
* The environment variable `CYTHON_FORCE_REGEN=1` can be used to force `cythonize`
  to regenerate the output files regardless of modification times and changes.
* A new Cython build option `--cython-compile-minimal` was added to compile only a
  smaller set of Cython’s own modules, which can be used to reduce the package
  and install size.
* Improvements to `PyTypeObject` definitions in pxd wrapping of libpython.
  Patch by John Kirkham. (Github issue [#4699](https://github.com/cython/cython/issues/4699 "https://github.com/cython/cython/issues/4699"))

### Bugs fixed[¶](#id89 "Link to this heading")

* Decorators like `@cfunc` and `@ccall` could leak into nested functions and classes.
  Patch by David Woods. (Github issue [#4092](https://github.com/cython/cython/issues/4092 "https://github.com/cython/cython/issues/4092"))
* Exceptions within for-loops that run over memoryviews could lead to a ref-counting error.
  Patch by David Woods. (Github issue [#4662](https://github.com/cython/cython/issues/4662 "https://github.com/cython/cython/issues/4662"))
* Using memoryview arguments in closures of inner functions could lead to ref-counting errors.
  Patch by David Woods. (Github issue [#4798](https://github.com/cython/cython/issues/4798 "https://github.com/cython/cython/issues/4798"))
* Several optimised string methods failed to accept `None` as arguments to their options.
  Test patch by Kirill Smelkov. (Github issue [#4737](https://github.com/cython/cython/issues/4737 "https://github.com/cython/cython/issues/4737"))
* A regression in 3.0.0a10 was resolved that prevented property setter methods from
  having the same name as their value argument.
  Patch by David Woods. (Github issue [#4836](https://github.com/cython/cython/issues/4836 "https://github.com/cython/cython/issues/4836"))
* Typedefs for the `bint` type did not always behave like `bint`.
  Patch by Nathan Manville and 0dminnimda. (Github issue [#4660](https://github.com/cython/cython/issues/4660 "https://github.com/cython/cython/issues/4660"))
* The return type of a fused function is no longer ignored for function pointers,
  since it is relevant when passing them e.g. as argument into other fused functions.
  Patch by David Woods. (Github issue [#4644](https://github.com/cython/cython/issues/4644 "https://github.com/cython/cython/issues/4644"))
* The `__self__` attribute of fused functions reports its availability correctly
  with `hasattr()`. Patch by David Woods.
  (Github issue [#4808](https://github.com/cython/cython/issues/4808 "https://github.com/cython/cython/issues/4808"))
* `pyximport` no longer uses the deprecated `imp` module.
  Patch by Matúš Valo. (Github issue [#4560](https://github.com/cython/cython/issues/4560 "https://github.com/cython/cython/issues/4560"))
* `pyximport` failed for long filenames on Windows.
  Patch by Matti Picus. (Github issue [#4630](https://github.com/cython/cython/issues/4630 "https://github.com/cython/cython/issues/4630"))
* The generated C code failed to compile in CPython 3.11a4 and later.
  (Github issue [#4500](https://github.com/cython/cython/issues/4500 "https://github.com/cython/cython/issues/4500"))
* A case of undefined C behaviour was resolved in the list slicing code.
  Patch by Richard Barnes. (Github issue [#4734](https://github.com/cython/cython/issues/4734 "https://github.com/cython/cython/issues/4734"))
* Using the Limited API could report incorrect line numbers in tracebacks.
* A work-around for StacklessPython < 3.8 was disabled in Py3.8 and later.
  (Github issue [#4329](https://github.com/cython/cython/issues/4329 "https://github.com/cython/cython/issues/4329"))
* Improve conversion between function pointers with non-identical but
  compatible exception specifications. Patches by David Woods.
  (Github issues [#4770](https://github.com/cython/cython/issues/4770 "https://github.com/cython/cython/issues/4770"), [#4689](https://github.com/cython/cython/issues/4689 "https://github.com/cython/cython/issues/4689"))
* The runtime size check for imported `PyVarObject` types was improved
  to reduce false positives and adapt to Python 3.11.
  Patch by David Woods. (Github issues [#4827](https://github.com/cython/cython/issues/4827 "https://github.com/cython/cython/issues/4827"), [#4894](https://github.com/cython/cython/issues/4894 "https://github.com/cython/cython/issues/4894"))
* The generated modules no longer import NumPy internally when using
  fused types but no memoryviews.
  Patch by David Woods. (Github issue [#4935](https://github.com/cython/cython/issues/4935 "https://github.com/cython/cython/issues/4935"))
* Improve compatibility with forthcoming CPython 3.12 release.
* Limited API C preprocessor warning is compatible with MSVC. Patch by
  Victor Molina Garcia. (Github issue [#4826](https://github.com/cython/cython/issues/4826 "https://github.com/cython/cython/issues/4826"))
* Some C compiler warnings were fixed.
  Patch by mwtian. (Github issue [#4831](https://github.com/cython/cython/issues/4831 "https://github.com/cython/cython/issues/4831"))
* The parser allowed some invalid spellings of `...`.
  Patch by 0dminnimda. (Github issue [#4868](https://github.com/cython/cython/issues/4868 "https://github.com/cython/cython/issues/4868"))
* Includes all bug-fixes and features from the 0.29 maintenance branch
  up to the [0.29.32 (2022-07-29)](#id141 "#id141") release.

### Other changes[¶](#id90 "Link to this heading")

* When using type annotations, `func(x: list)` or `func(x: ExtType)` (and other
  Python builtin or extension types) no longer allow `None` as input argument to `x`.
  This is consistent with the normal typing semantics in Python, and was a common gotcha
  for users who did not expect `None` to be allowed as input. To allow `None`, use
  `typing.Optional` as in `func(x: Optional[list])`. `None` is also automatically
  allowed when it is used as default argument, i.e. `func(x: list = None)`.
  `int` and `float` are now also recognised in type annotations and restrict the
  value type at runtime. They were previously ignored.
  Note that, for backwards compatibility reasons, the new behaviour does not apply when using
  Cython’s C notation, as in `func(list x)`. Here, `None` is still allowed, as always.
  Also, the `annotation_typing` directive can now be enabled and disabled more finely
  within the module.
  (Github issues [#3883](https://github.com/cython/cython/issues/3883 "https://github.com/cython/cython/issues/3883"), [#2696](https://github.com/cython/cython/issues/2696 "https://github.com/cython/cython/issues/2696"), [#4669](https://github.com/cython/cython/issues/4669 "https://github.com/cython/cython/issues/4669"), [#4606](https://github.com/cython/cython/issues/4606 "https://github.com/cython/cython/issues/4606"), [#4886](https://github.com/cython/cython/issues/4886 "https://github.com/cython/cython/issues/4886"))
* The compile-time `DEF` and `IF` statements are deprecated and generate a warning.
  They should be replaced with normal constants, code generation or C macros.
  (Github issue [#4310](https://github.com/cython/cython/issues/4310 "https://github.com/cython/cython/issues/4310"))
* Reusing an extension type attribute name as a method name is now an error.
  Patch by 0dminnimda. (Github issue [#4661](https://github.com/cython/cython/issues/4661 "https://github.com/cython/cython/issues/4661"))
* Improve compatibility between classes pickled in Cython 3.0 and 0.29.x
  by accepting MD5, SHA-1 and SHA-256 checksums.
  (Github issue [#4680](https://github.com/cython/cython/issues/4680 "https://github.com/cython/cython/issues/4680"))

## 3.0.0 alpha 10 (2022-01-06)[¶](#alpha-10-2022-01-06 "Link to this heading")

### Features added[¶](#id91 "Link to this heading")

* `Cython.Distutils.build_ext` now uses `cythonize()` internally (previously
  known as `new_build_ext`), while still supporting the options that were
  available in the old implementation (`old_build_ext`).
  Patch by Matúš Valo. (Github issue [#3541](https://github.com/cython/cython/issues/3541 "https://github.com/cython/cython/issues/3541"))
* `pyximport` now uses `cythonize()` internally.
  Patch by Matúš Valo. (Github issue [#2304](https://github.com/cython/cython/issues/2304 "https://github.com/cython/cython/issues/2304"))
* `__del__(self)` on extension types now maps to `tp_finalize` in Python 3.
  Original patch by ax487. (Github issue [#3612](https://github.com/cython/cython/issues/3612 "https://github.com/cython/cython/issues/3612"))
* Conversion from Python dict to C++ map now supports arbitrary Python mappings,
  not just dicts.
* Direct assignments to C++ references are now allowed.
  Patch by David Woods. (Github issue [#1863](https://github.com/cython/cython/issues/1863 "https://github.com/cython/cython/issues/1863"))
* An initial set of adaptations for GraalVM Python was implemented. Note that
  this does not imply any general support for this target or that your code
  will work at all in this environment. But testing should be possible now.
  Patch by David Woods. (Github issue [#4328](https://github.com/cython/cython/issues/4328 "https://github.com/cython/cython/issues/4328"))
* `PyMem_[Raw]Calloc()` was added to the `cpython.mem` declarations.
  Note that the `Raw` versions are no longer #defined by Cython. The previous
  macros were not considered safe.
  Patch by William Schwartz and David Woods. (Github issue [#3047](https://github.com/cython/cython/issues/3047 "https://github.com/cython/cython/issues/3047"))

### Bugs fixed[¶](#id92 "Link to this heading")

* Circular imports of compiled modules could fail needlessly even when the import
  could already be resolved from `sys.modules`.
  Patch by Syam Gadde. (Github issue [#4390](https://github.com/cython/cython/issues/4390 "https://github.com/cython/cython/issues/4390"))
* The GIL can now safely be released inside of `nogil` functions (which may actually
  be called with the GIL held at runtime).
  Patch by David Woods. (Github issue [#4137](https://github.com/cython/cython/issues/4137 "https://github.com/cython/cython/issues/4137"))
* Type errors when passing memory view arguments could leak buffer references.
  Patch by David Woods. (Github issue [#4296](https://github.com/cython/cython/issues/4296 "https://github.com/cython/cython/issues/4296"))
* Cython did not type the `self` argument in special binary methods.
  Patch by David Woods. (Github issue [#4434](https://github.com/cython/cython/issues/4434 "https://github.com/cython/cython/issues/4434"))
* An incompatibility with recent coverage.py versions was resolved.
  Patch by David Woods. (Github issue [#4440](https://github.com/cython/cython/issues/4440 "https://github.com/cython/cython/issues/4440"))
* Fused typed default arguments generated incorrect code.
  Patch by David Woods. (Github issue [#4413](https://github.com/cython/cython/issues/4413 "https://github.com/cython/cython/issues/4413"))
* `prange` loops generated incorrect code when `cpp_locals` is enabled.
  Patch by David Woods. (Github issue [#4354](https://github.com/cython/cython/issues/4354 "https://github.com/cython/cython/issues/4354"))
* A C-level compatibility issue with recent NumPy versions was resolved.
  Patch by David Woods. (Github issue [#4396](https://github.com/cython/cython/issues/4396 "https://github.com/cython/cython/issues/4396"))
* Decorators on inner functions were not evaluated in the right scope.
  Patch by David Woods. (Github issue [#4367](https://github.com/cython/cython/issues/4367 "https://github.com/cython/cython/issues/4367"))
* Very early errors during module initialisation could lead to crashes.
  Patch by David Woods. (Github issue [#4377](https://github.com/cython/cython/issues/4377 "https://github.com/cython/cython/issues/4377"))
* Fused functions were binding unnecessarily, which prevented them from being pickled.
  Patch by David Woods. (Github issue [#4370](https://github.com/cython/cython/issues/4370 "https://github.com/cython/cython/issues/4370"))
* Some constant tuples containing strings were not deduplicated.
  Patch by David Woods. (Github issue [#4353](https://github.com/cython/cython/issues/4353 "https://github.com/cython/cython/issues/4353"))
* Unsupported decorators on cdef functions were not rejected in recent releases.
  Patch by David Woods. (Github issue [#4322](https://github.com/cython/cython/issues/4322 "https://github.com/cython/cython/issues/4322"))
* The excess arguments in a for-in-range loop with more than 3 arguments to range()
  were silently ignored.
  Original patch by Max Bachmann. (Github issue [#4550](https://github.com/cython/cython/issues/4550 "https://github.com/cython/cython/issues/4550"))
* Python object types were not allowed as `->` return type annotations.
  Patch by Matúš Valo. (Github issue [#4433](https://github.com/cython/cython/issues/4433 "https://github.com/cython/cython/issues/4433"))
* Default values for memory views arguments were not properly supported.
  Patch by Corentin Cadiou. (Github issue [#4313](https://github.com/cython/cython/issues/4313 "https://github.com/cython/cython/issues/4313"))
* Templating C++ classes with memory view types lead to buggy code and is now rejected.
  Patch by David Woods. (Github issue [#3085](https://github.com/cython/cython/issues/3085 "https://github.com/cython/cython/issues/3085"))
* Several C++ library declarations were added and fixed.
  Patches by Dobatymo, account-login, Jonathan Helgert, Evgeny Yakimov, GalaxySnail, Max Bachmann.
  (Github issues [#4408](https://github.com/cython/cython/issues/4408 "https://github.com/cython/cython/issues/4408"), [#4419](https://github.com/cython/cython/issues/4419 "https://github.com/cython/cython/issues/4419"), [#4410](https://github.com/cython/cython/issues/4410 "https://github.com/cython/cython/issues/4410"), [#4395](https://github.com/cython/cython/issues/4395 "https://github.com/cython/cython/issues/4395"),
  [#4423](https://github.com/cython/cython/issues/4423 "https://github.com/cython/cython/issues/4423"), [#4448](https://github.com/cython/cython/issues/4448 "https://github.com/cython/cython/issues/4448"), [#4462](https://github.com/cython/cython/issues/4462 "https://github.com/cython/cython/issues/4462"), [#3293](https://github.com/cython/cython/issues/3293 "https://github.com/cython/cython/issues/3293"), [#4522](https://github.com/cython/cython/issues/4522 "https://github.com/cython/cython/issues/4522"),
  [#2171](https://github.com/cython/cython/issues/2171 "https://github.com/cython/cython/issues/2171"), [#4531](https://github.com/cython/cython/issues/4531 "https://github.com/cython/cython/issues/4531"))
* Some compiler problems and warnings were resolved.
  Patches by David Woods, 0dminnimda, Nicolas Pauss and others.
  (Github issues [#4317](https://github.com/cython/cython/issues/4317 "https://github.com/cython/cython/issues/4317"), [#4324](https://github.com/cython/cython/issues/4324 "https://github.com/cython/cython/issues/4324"), [#4361](https://github.com/cython/cython/issues/4361 "https://github.com/cython/cython/issues/4361"), [#4357](https://github.com/cython/cython/issues/4357 "https://github.com/cython/cython/issues/4357"))
* The `self` argument of static methods in .pxd files was incorrectly typed.
  Patch by David Woods. (Github issue [#3174](https://github.com/cython/cython/issues/3174 "https://github.com/cython/cython/issues/3174"))
* A name collision when including multiple generated API header files was resolved.
  Patch by David Woods. (Github issue [#4308](https://github.com/cython/cython/issues/4308 "https://github.com/cython/cython/issues/4308"))
* An endless loop in `cython-mode.el` was resolved.
  Patch by Johannes Mueller. (Github issue [#3218](https://github.com/cython/cython/issues/3218 "https://github.com/cython/cython/issues/3218"))
* `_Py_TPFLAGS_HAVE_VECTORCALL` was always set on extension types when using the limited API.
  Patch by David Woods. (Github issue [#4453](https://github.com/cython/cython/issues/4453 "https://github.com/cython/cython/issues/4453"))
* Some compatibility issues with PyPy were resolved.
  Patches by Max Bachmann, Matti Picus.
  (Github issues [#4454](https://github.com/cython/cython/issues/4454 "https://github.com/cython/cython/issues/4454"), [#4477](https://github.com/cython/cython/issues/4477 "https://github.com/cython/cython/issues/4477"), [#4478](https://github.com/cython/cython/issues/4478 "https://github.com/cython/cython/issues/4478"), [#4509](https://github.com/cython/cython/issues/4509 "https://github.com/cython/cython/issues/4509"), [#4517](https://github.com/cython/cython/issues/4517 "https://github.com/cython/cython/issues/4517"))
* A compiler crash when running Cython thread-parallel from distutils was resolved.
  (Github issue [#4503](https://github.com/cython/cython/issues/4503 "https://github.com/cython/cython/issues/4503"))
* Includes all bug-fixes from the [0.29.26 (2021-12-16)](#id162 "#id162") release.

### Other changes[¶](#id93 "Link to this heading")

* A warning was added when `__defaults__` or `__kwdefaults__` of Cython compiled
  functions were re-assigned, since this does not current have an effect.
  Patch by David Woods. (Github issue [#2650](https://github.com/cython/cython/issues/2650 "https://github.com/cython/cython/issues/2650"))

## 3.0.0 alpha 9 (2021-07-21)[¶](#alpha-9-2021-07-21 "Link to this heading")

### Features added[¶](#id94 "Link to this heading")

* Declarations for `libcpp.algorithms`, `libcpp.set` and `libcpp.unordered_set`
  were extended.
  Patch by David Woods. (Github issues [#4271](https://github.com/cython/cython/issues/4271 "https://github.com/cython/cython/issues/4271"), [#4273](https://github.com/cython/cython/issues/4273 "https://github.com/cython/cython/issues/4273"))
* `cygdb` has a new option `--skip-interpreter` that allows using a different
  Python runtime than the one used to generate the debugging information.
  Patch by Alessandro Molina. (Github issue [#4186](https://github.com/cython/cython/issues/4186 "https://github.com/cython/cython/issues/4186"))

### Bugs fixed[¶](#id95 "Link to this heading")

* Several issues with the new `cpp_locals` directive were resolved and
  its test coverage improved.
  Patch by David Woods. (Github issues [#4266](https://github.com/cython/cython/issues/4266 "https://github.com/cython/cython/issues/4266"), [#4265](https://github.com/cython/cython/issues/4265 "https://github.com/cython/cython/issues/4265"))
* Generated utility code for C++ conversions no longer depends on several user
  definable directives that may make it behave incorrectly.
  Patch by David Woods. (Github issue [#4206](https://github.com/cython/cython/issues/4206 "https://github.com/cython/cython/issues/4206"))
* A reference counting bug in the new `@cython.total_ordering` decorator was fixed.
* Includes all bug-fixes from the [0.29.24 (2021-07-14)](#id168 "#id168") release.

### Other changes[¶](#id96 "Link to this heading")

* Parts of the documentation were (and are being) rewritten to show the
  Cython language syntax next to the equivalent Python syntax.
  Patches by 0dminnimda and Matúš Valo. (Github issue [#4187](https://github.com/cython/cython/issues/4187 "https://github.com/cython/cython/issues/4187"))

## 3.0.0 alpha 8 (2021-07-02)[¶](#alpha-8-2021-07-02 "Link to this heading")

### Features added[¶](#id97 "Link to this heading")

* A `@cython.total_ordering` decorator has been added to automatically
  implement all comparison operators, similar to `functools.total_ordering`.
  Patch by Spencer Brown. (Github issue [#2090](https://github.com/cython/cython/issues/2090 "https://github.com/cython/cython/issues/2090"))
* A new directive `cpp_locals` was added that allows local C++ variables to
  be lazily initialised (without default constructor), thus making them behave
  more like Python variables.
  Patch by David Woods. (Github issue [#4160](https://github.com/cython/cython/issues/4160 "https://github.com/cython/cython/issues/4160"))
* C++17 execution policies are supported in `libcpp.algorithm`.
  Patch by Ashwin Srinath. (Github issue [#3790](https://github.com/cython/cython/issues/3790 "https://github.com/cython/cython/issues/3790"))
* New C feature flags: `CYTHON_USE_MODULE_STATE`, `CYTHON_USE_TYPE_SPECS`
  Both are currently considered experimental.
  (Github issue [#3611](https://github.com/cython/cython/issues/3611 "https://github.com/cython/cython/issues/3611"))
* `[...] * N` is optimised for C integer multipliers `N`.
  (Github issue [#3922](https://github.com/cython/cython/issues/3922 "https://github.com/cython/cython/issues/3922"))

### Bugs fixed[¶](#id98 "Link to this heading")

* The dispatch code for binary operators to special methods could run into infinite recursion.
  Patch by David Woods. (Github issue [#4172](https://github.com/cython/cython/issues/4172 "https://github.com/cython/cython/issues/4172"))
* Code optimisations were not applied to methods of Cython implemented C++ classes.
  Patch by David Woods. (Github issue [#4212](https://github.com/cython/cython/issues/4212 "https://github.com/cython/cython/issues/4212"))
* The special `cython` module was not always detected in PEP-484 type annotations.
  Patch by David Woods. (Github issue [#4243](https://github.com/cython/cython/issues/4243 "https://github.com/cython/cython/issues/4243"))
* Conversion from Python dicts to `std::map` was broken.
  Patch by David Woods and Mikkel Skofelt. (Github issues [#4231](https://github.com/cython/cython/issues/4231 "https://github.com/cython/cython/issues/4231"), [#4228](https://github.com/cython/cython/issues/4228 "https://github.com/cython/cython/issues/4228"))
* The exception handling annotation `except +*` was broken.
  Patch by David Woods. (Github issues [#3065](https://github.com/cython/cython/issues/3065 "https://github.com/cython/cython/issues/3065"), [#3066](https://github.com/cython/cython/issues/3066 "https://github.com/cython/cython/issues/3066"))
* Attribute annotations in Python classes are now ignored, because they are
  just Python objects in a dict (as opposed to the fields of extension types).
  Patch by David Woods. (Github issues [#4196](https://github.com/cython/cython/issues/4196 "https://github.com/cython/cython/issues/4196"), [#4198](https://github.com/cython/cython/issues/4198 "https://github.com/cython/cython/issues/4198"))
* An unnecessary slow-down at import time was removed from `Cython.Distutils`.
  Original patch by Anthony Sottile. (Github issue [#4224](https://github.com/cython/cython/issues/4224 "https://github.com/cython/cython/issues/4224"))
* Python modules were not automatically recompiled when only their `.pxd` file changed.
  Patch by Golden Rockefeller. (Github issue [#1428](https://github.com/cython/cython/issues/1428 "https://github.com/cython/cython/issues/1428"))
* The signature of `PyFloat_FromString()` in `cpython.float` was changed
  to match the signature in Py3. It still has an automatic fallback for Py2.
  (Github issue [#3909](https://github.com/cython/cython/issues/3909 "https://github.com/cython/cython/issues/3909"))
* A compile error on MSVC was resolved.
  Patch by David Woods. (Github issue [#4202](https://github.com/cython/cython/issues/4202 "https://github.com/cython/cython/issues/4202"))
* A C compiler warning in PyPy3 regarding `PyEval_EvalCode()` was resolved.
* Directives starting with `optimization.*` in pure Python mode were incorrectly named.
  It should have been `optimize.*`.
  Patch by David Woods. (Github issue [#4258](https://github.com/cython/cython/issues/4258 "https://github.com/cython/cython/issues/4258"))

### Other changes[¶](#id99 "Link to this heading")

* Variables can no longer be declared with `cpdef`.
  Patch by David Woods. (Github issue [#887](https://github.com/cython/cython/issues/887 "https://github.com/cython/cython/issues/887"))
* Support for the now unsupported Pyston V1 was removed in favour of Pyston V2.
  Patch by Marius Wachtler. (Github issue [#4211](https://github.com/cython/cython/issues/4211 "https://github.com/cython/cython/issues/4211"))
* The `Cython.Build.BuildExecutable` tool no longer executes the program automatically.
  Use `cythonrun` for that.

## 3.0.0 alpha 7 (2021-05-24)[¶](#alpha-7-2021-05-24 "Link to this heading")

### Features added[¶](#id100 "Link to this heading")

* A `cimport` is now supported in pure Python code by prefixing the
  imported module name with `cython.cimports.`, e.g.
  `from cython.cimports.libc.math import sin`.
  (GIthub issue [#4190](https://github.com/cython/cython/issues/4190 "https://github.com/cython/cython/issues/4190"))
* `__class_getitem__` ([PEP-560](https://www.python.org/dev/peps/pep-0560 "https://www.python.org/dev/peps/pep-0560")) is supported for cdef classes.
  Patch by Kmol Yuan. (Github issue [#3764](https://github.com/cython/cython/issues/3764 "https://github.com/cython/cython/issues/3764"))
* `__mro_entries__` ([PEP-560](https://www.python.org/dev/peps/pep-0560 "https://www.python.org/dev/peps/pep-0560")) is supported for Python classes.
  Patch by David Woods. (Github issue [#3537](https://github.com/cython/cython/issues/3537 "https://github.com/cython/cython/issues/3537"))
* `cython.array` supports simple, non-strided views.
  (Github issue [#3775](https://github.com/cython/cython/issues/3775 "https://github.com/cython/cython/issues/3775"))
* Self-documenting f-strings (`=`) were implemented.
  Patch by davfsa. (Github issue [#3796](https://github.com/cython/cython/issues/3796 "https://github.com/cython/cython/issues/3796"))
* The destructor is now called for fields in C++ structs.
  Patch by David Woods. (Github issue [#3226](https://github.com/cython/cython/issues/3226 "https://github.com/cython/cython/issues/3226"))
* `std::move()` is now also called for temps during `yield`.
  Patch by Yu Feng. (Github issue [#4154](https://github.com/cython/cython/issues/4154 "https://github.com/cython/cython/issues/4154"))
* `asyncio.iscoroutinefunction()` now recognises coroutine functions
  also when compiled by Cython.
  Patch by Pedro Marques da Luz. (Github issue [#2273](https://github.com/cython/cython/issues/2273 "https://github.com/cython/cython/issues/2273"))
* C compiler warnings and errors are now shown in Jupyter notebooks.
  Patch by Egor Dranischnikow. (Github issue [#3751](https://github.com/cython/cython/issues/3751 "https://github.com/cython/cython/issues/3751"))
* `float(…)` is optimised for string arguments (str/bytes/bytearray).
* Converting C++ containers to Python lists uses less memory allocations.
  Patch by Max Bachmann. (Github issue [#4081](https://github.com/cython/cython/issues/4081 "https://github.com/cython/cython/issues/4081"))
* Docstrings of `cpdef` enums are now copied to the enum class.
  Patch by matham. (Github issue [#3805](https://github.com/cython/cython/issues/3805 "https://github.com/cython/cython/issues/3805"))
* The type `cython.Py_hash_t` is available in Python mode.
* C-API declarations for `cpython.fileobject` were added.
  Patch by Zackery Spytz. (Github issue [#3906](https://github.com/cython/cython/issues/3906 "https://github.com/cython/cython/issues/3906"))
* C-API declarations for context variables in Python 3.7 were added.
  Original patch by Zolisa Bleki. (Github issue [#2281](https://github.com/cython/cython/issues/2281 "https://github.com/cython/cython/issues/2281"))
* More C-API declarations for `cpython.datetime` were added.
  Patch by Bluenix2. (Github issue [#4128](https://github.com/cython/cython/issues/4128 "https://github.com/cython/cython/issues/4128"))
* A new module `cpython.time` was added with some low-level alternatives to
  Python’s `time` module.
  Patch by Brock Mendel. (Github issue [#3767](https://github.com/cython/cython/issues/3767 "https://github.com/cython/cython/issues/3767"))
* The value `PyBUF_MAX_NDIM` was added to the `cpython.buffer` module.
  Patch by John Kirkham. (Github issue [#3811](https://github.com/cython/cython/issues/3811 "https://github.com/cython/cython/issues/3811"))
* “Declaration after use” is now an error for variables.
  Patch by David Woods. (Github issue [#3976](https://github.com/cython/cython/issues/3976 "https://github.com/cython/cython/issues/3976"))
* More declarations for C++ string methods were added.
* Cython now detects when existing output files were not previously generated
  by itself and refuses to overwrite them. It is a common mistake to name
  the module file of a wrapper after the library (source file) that it wraps,
  which can lead to surprising errors when the file gets overwritten.

### Bugs fixed[¶](#id101 "Link to this heading")

* Annotations were not exposed on annotated (data-)classes.
  Patch by matsjoyce. (Github issue [#4151](https://github.com/cython/cython/issues/4151 "https://github.com/cython/cython/issues/4151"))
* Inline functions and other code in `.pxd` files could accidentally
  inherit the compiler directives of the `.pyx` file that imported them.
  Patch by David Woods. (Github issue [#1071](https://github.com/cython/cython/issues/1071 "https://github.com/cython/cython/issues/1071"))
* Some issues were resolved that could lead to duplicated C names.
  Patch by David Woods. (Github issue [#3716](https://github.com/cython/cython/issues/3716 "https://github.com/cython/cython/issues/3716"), [#3741](https://github.com/cython/cython/issues/3741 "https://github.com/cython/cython/issues/3741"), [#3734](https://github.com/cython/cython/issues/3734 "https://github.com/cython/cython/issues/3734"))
* Modules with unicode names failed to build on Windows.
  Patch by David Woods. (Github issue [#4125](https://github.com/cython/cython/issues/4125 "https://github.com/cython/cython/issues/4125"))
* `ndarray.shape` failed to compile with Pythran and recent NumPy.
  Patch by Serge Guelton. (Github issue [#3762](https://github.com/cython/cython/issues/3762 "https://github.com/cython/cython/issues/3762"))
* Casting to ctuples is now allowed.
  Patch by David Woods. (Github issue [#3808](https://github.com/cython/cython/issues/3808 "https://github.com/cython/cython/issues/3808"))
* Structs could not be instantiated with positional arguments in
  pure Python mode.
* Literal list assignments to pointer variables declared in PEP-526
  notation failed to compile.
* Nested C++ types were not usable through ctypedefs.
  Patch by Vadim Pushtaev. (Github issue [#4039](https://github.com/cython/cython/issues/4039 "https://github.com/cython/cython/issues/4039"))
* Overloaded C++ static methods were lost.
  Patch by Ashwin Srinath. (Github [#1851](https://github.com/cython/cython/issues/1851 "https://github.com/cython/cython/issues/1851"))
* Cython compiled functions always provided a `__self__` attribute,
  regardless of being used as a method or not.
  Patch by David Woods. (Github issue [#4036](https://github.com/cython/cython/issues/4036 "https://github.com/cython/cython/issues/4036"))
* Calls to `.__class__()` of a known extension type failed.
  Patch by David Woods. (Github issue [#3954](https://github.com/cython/cython/issues/3954 "https://github.com/cython/cython/issues/3954"))
* Generator expressions in pxd-overridden `cdef` functions could
  fail to compile.
  Patch by Matúš Valo. (Github issue [#3477](https://github.com/cython/cython/issues/3477 "https://github.com/cython/cython/issues/3477"))
* A reference leak on import failures was resolved.
  Patch by Max Bachmann. (Github issue [#4056](https://github.com/cython/cython/issues/4056 "https://github.com/cython/cython/issues/4056"))
* A C compiler warning about unused code was resolved.
  (Github issue [#3763](https://github.com/cython/cython/issues/3763 "https://github.com/cython/cython/issues/3763"))
* A C compiler warning about enum value casting was resolved in GCC.
  (Github issue [#2749](https://github.com/cython/cython/issues/2749 "https://github.com/cython/cython/issues/2749"))
* Some C compiler warninge were resolved.
  Patches by Max Bachmann. (Github issue [#4053](https://github.com/cython/cython/issues/4053 "https://github.com/cython/cython/issues/4053"), [#4059](https://github.com/cython/cython/issues/4059 "https://github.com/cython/cython/issues/4059"), [#4054](https://github.com/cython/cython/issues/4054 "https://github.com/cython/cython/issues/4054"), [#4148](https://github.com/cython/cython/issues/4148 "https://github.com/cython/cython/issues/4148"), [#4162](https://github.com/cython/cython/issues/4162 "https://github.com/cython/cython/issues/4162"))
* A compile failure for C++ enums in Py3.4 / MSVC was resolved.
  Patch by Ashwin Srinath. (Github issue [#3782](https://github.com/cython/cython/issues/3782 "https://github.com/cython/cython/issues/3782"))
* Some C++ STL methods did not propagate exceptions.
  Patch by Max Bachmann. (Github issue [#4079](https://github.com/cython/cython/issues/4079 "https://github.com/cython/cython/issues/4079"))
* An unsupported C-API call in PyPy was fixed.
  Patch by Max Bachmann. (Github issue [#4055](https://github.com/cython/cython/issues/4055 "https://github.com/cython/cython/issues/4055"))
* The Cython `CodeWriter` mishandled no-argument `return` statements.
  Patch by Tao He. (Github issue [#3795](https://github.com/cython/cython/issues/3795 "https://github.com/cython/cython/issues/3795"))
* `complex` wasn’t supported in PEP-484 type annotations.
  Patch by David Woods. (Github issue [#3949](https://github.com/cython/cython/issues/3949 "https://github.com/cython/cython/issues/3949"))
* Default arguments of methods were not exposed for introspection.
  Patch by Vladimir Matveev. (Github issue [#4061](https://github.com/cython/cython/issues/4061 "https://github.com/cython/cython/issues/4061"))
* Extension types inheriting from Python classes could not safely
  be exposed in `.pxd` files.
  (Github issue [#4106](https://github.com/cython/cython/issues/4106 "https://github.com/cython/cython/issues/4106"))
* The profiling/tracing code was adapted to work with Python 3.10b1.
* The internal CPython macro `Py_ISSPACE()` is no longer used.
  Original patch by Andrew Jones. (Github issue [#4111](https://github.com/cython/cython/issues/4111 "https://github.com/cython/cython/issues/4111"))
* Includes all bug-fixes from the [0.29.23 (2021-04-14)](#id171 "#id171") release.

## 3.0.0 alpha 6 (2020-07-31)[¶](#alpha-6-2020-07-31 "Link to this heading")

### Features added[¶](#id102 "Link to this heading")

* Special methods for binary operators now follow Python semantics.
  Rather than e.g. a single `__add__` method for cdef classes, where
  “self” can be either the first or second argument, one can now define
  both `__add__` and `__radd__` as for standard Python classes.
  This behavior can be disabled with the `c_api_binop_methods` directive
  to return to the previous semantics in Cython code (available from Cython
  0.29.20), or the reversed method (`__radd__`) can be implemented in
  addition to an existing two-sided operator method (`__add__`) to get a
  backwards compatible implementation.
  (Github issue [#2056](https://github.com/cython/cython/issues/2056 "https://github.com/cython/cython/issues/2056"))
* No/single argument functions now accept keyword arguments by default in order
  to comply with Python semantics. The marginally faster calling conventions
  `METH_NOARGS` and `METH_O` that reject keyword arguments are still available
  with the directive `@cython.always_allow_keywords(False)`.
  (Github issue [#3090](https://github.com/cython/cython/issues/3090 "https://github.com/cython/cython/issues/3090"))
* For-in-loop iteration over `bytearray` and memory views is optimised.
  Patch by David Woods. (Github issue [#2227](https://github.com/cython/cython/issues/2227 "https://github.com/cython/cython/issues/2227"))
* Type inference now works for memory views and slices.
  Patch by David Woods. (Github issue [#2227](https://github.com/cython/cython/issues/2227 "https://github.com/cython/cython/issues/2227"))
* The `@returns()` decorator propagates exceptions by default for suitable C
  return types when no `@exceptval()` is defined.
  (Github issues [#3625](https://github.com/cython/cython/issues/3625 "https://github.com/cython/cython/issues/3625"), [#3664](https://github.com/cython/cython/issues/3664 "https://github.com/cython/cython/issues/3664"))
* A low-level inline function `total_seconds(timedelta)` was added to
  `cpython.datetime` to bypass the Python method call. Note that this function
  is not guaranteed to give exactly the same results for very large time intervals.
  Patch by Brock Mendel. (Github issue [#3616](https://github.com/cython/cython/issues/3616 "https://github.com/cython/cython/issues/3616"))
* Type inference now understands that `a, *b = x` assigns a list to `b`.
* Limited API support was improved.
  Patches by Matthias Braun. (Github issues [#3693](https://github.com/cython/cython/issues/3693 "https://github.com/cython/cython/issues/3693"), [#3707](https://github.com/cython/cython/issues/3707 "https://github.com/cython/cython/issues/3707"))
* The Cython `CodeWriter` can now handle more syntax constructs.
  Patch by Tao He. (Github issue [#3514](https://github.com/cython/cython/issues/3514 "https://github.com/cython/cython/issues/3514"))

### Bugs fixed[¶](#id103 "Link to this heading")

* The construct `for x in cpp_function_call()` failed to compile.
  Patch by David Woods. (Github issue [#3663](https://github.com/cython/cython/issues/3663 "https://github.com/cython/cython/issues/3663"))
* C++ references failed to compile when used as Python object indexes.
  Patch by David Woods. (Github issue [#3754](https://github.com/cython/cython/issues/3754 "https://github.com/cython/cython/issues/3754"))
* The C++ `typeid()` function was allowed in C mode.
  Patch by Celelibi. (Github issue [#3637](https://github.com/cython/cython/issues/3637 "https://github.com/cython/cython/issues/3637"))
* `repr()` was assumed to return `str` instead of `unicode` with `language_level=3`.
  (Github issue [#3736](https://github.com/cython/cython/issues/3736 "https://github.com/cython/cython/issues/3736"))
* Includes all bug-fixes from the [0.29.21 (2020-07-09)](#id179 "#id179") release.

### Other changes[¶](#id104 "Link to this heading")

* The `numpy` declarations were updated.
  Patch by Brock Mendel. (Github issue [#3630](https://github.com/cython/cython/issues/3630 "https://github.com/cython/cython/issues/3630"))
* The names of Cython’s internal types (functions, generator, coroutine, etc.)
  are now qualified with the module name of the internal Cython module that is
  used for sharing them across Cython implemented modules, for example
  `_cython_3_0a5.coroutine`. This was done to avoid making them look like
  homeless builtins, to help with debugging, and in order to avoid a CPython
  warning according to [https://bugs.python.org/issue20204](https://bugs.python.org/issue20204 "https://bugs.python.org/issue20204")

## 3.0.0 alpha 5 (2020-05-19)[¶](#alpha-5-2020-05-19 "Link to this heading")

### Features added[¶](#id105 "Link to this heading")

* `.pxd` files can now be [versioned](userguide/sharing_declarations.html#versioning "userguide/sharing_declarations.html#versioning") by adding an
  extension like “`.cython-30.pxd`” to prevent older Cython versions (than
  3.0 in this case) from picking them up. (Github issue [#3577](https://github.com/cython/cython/issues/3577 "https://github.com/cython/cython/issues/3577"))
* Several macros/functions declared in the NumPy API are now usable without
  holding the GIL.
* libc.math was extended to include all C99 function declarations.
  Patch by Dean Scarff. (Github issue [#3570](https://github.com/cython/cython/issues/3570 "https://github.com/cython/cython/issues/3570"))

### Bugs fixed[¶](#id106 "Link to this heading")

* Several issues with arithmetic overflow handling were resolved, including
  undefined behaviour in C.
  Patch by Sam Sneddon. (Github issue [#3588](https://github.com/cython/cython/issues/3588 "https://github.com/cython/cython/issues/3588"))
* The improved GIL handling in `nogil` functions introduced in 3.0a3
  could fail to acquire the GIL in some cases on function exit.
  (Github issue [#3590](https://github.com/cython/cython/issues/3590 "https://github.com/cython/cython/issues/3590") etc.)
* A reference leak when processing keyword arguments in Py2 was resolved,
  that appeared in 3.0a1.
  (Github issue [#3578](https://github.com/cython/cython/issues/3578 "https://github.com/cython/cython/issues/3578"))
* The outdated getbuffer/releasebuffer implementations in the NumPy
  declarations were removed so that buffers declared as `ndarray`
  now use the normal implementation in NumPy.
* Includes all bug-fixes from the [0.29.18 (2020-05-18)](#id188 "#id188") release.

## 3.0.0 alpha 4 (2020-05-05)[¶](#alpha-4-2020-05-05 "Link to this heading")

### Features added[¶](#id107 "Link to this heading")

* The `print` statement (not the `print()` function) is allowed in
  `nogil` code without an explicit `with gil` section.
* The `assert` statement is allowed in `nogil` sections. Here, the GIL is
  only acquired if the `AssertionError` is really raised, which means that the
  evaluation of the asserted condition only allows C expressions.
* Cython generates C compiler branch hints for unlikely user defined if-clauses
  in more cases, when they end up raising exceptions unconditionally. This now
  includes exceptions being raised in `nogil`/`with gil` sections.
* Some internal memoryview functions were tuned to reduce object overhead.

### Bugs fixed[¶](#id108 "Link to this heading")

* Exception position reporting could run into race conditions on threaded code.
  It now uses function-local variables again.
* Error handling early in the module init code could lead to a crash.
* Error handling in `cython.array` creation was improved to avoid calling
  C-API functions with an error held.
* Complex buffer item types of structs of arrays could fail to validate.
  Patch by Leo and smutch. (Github issue [#1407](https://github.com/cython/cython/issues/1407 "https://github.com/cython/cython/issues/1407"))
* When importing the old Cython `build_ext` integration with distutils, the
  additional command line arguments leaked into the regular command.
  Patch by Kamekameha. (Github issue [#2209](https://github.com/cython/cython/issues/2209 "https://github.com/cython/cython/issues/2209"))
* The improved GIL handling in `nogil` functions introduced in 3.0a3
  could generate invalid C code.
  (Github issue [#3558](https://github.com/cython/cython/issues/3558 "https://github.com/cython/cython/issues/3558"))
* `PyEval_InitThreads()` is no longer used in Py3.7+ where it is a no-op.
* Parallel builds of Cython itself (`setup.py build_ext -j N`) failed on Windows.

### Other changes[¶](#id109 "Link to this heading")

* The C property feature has been rewritten and now requires C property methods
  to be declared `inline` ([#3571](https://github.com/cython/cython/issues/3571 "https://github.com/cython/cython/issues/3571")).

## 3.0.0 alpha 3 (2020-04-27)[¶](#alpha-3-2020-04-27 "Link to this heading")

### Features added[¶](#id110 "Link to this heading")

* `nogil` functions now avoid acquiring the GIL on function exit if possible
  even if they contain `with gil` blocks.
  (Github issue [#3554](https://github.com/cython/cython/issues/3554 "https://github.com/cython/cython/issues/3554"))
* Python private name mangling now falls back to unmangled names for non-Python
  globals, since double-underscore names are not uncommon in C. Unmangled Python
  names are also still found as a legacy fallback but produce a warning.
  Patch by David Woods. (Github issue [#3548](https://github.com/cython/cython/issues/3548 "https://github.com/cython/cython/issues/3548"))

### Bugs fixed[¶](#id111 "Link to this heading")

* Includes all bug-fixes from the [0.29.17 (2020-04-26)](#id191 "#id191") release.

## 3.0.0 alpha 2 (2020-04-23)[¶](#alpha-2-2020-04-23 "Link to this heading")

### Features added[¶](#id112 "Link to this heading")

* `std::move()` is now used in C++ mode for internal temp variables to
  make them work without copying values.
  Patch by David Woods. (Github issues [#3253](https://github.com/cython/cython/issues/3253 "https://github.com/cython/cython/issues/3253"), [#1612](https://github.com/cython/cython/issues/1612 "https://github.com/cython/cython/issues/1612"))
* `__class_getitem__` is supported for types on item access ([PEP-560](https://www.python.org/dev/peps/pep-0560 "https://www.python.org/dev/peps/pep-0560")).
  Patch by msg555. (Github issue [#2753](https://github.com/cython/cython/issues/2753 "https://github.com/cython/cython/issues/2753"))
* The simplified Py3.6 customisation of class creation is implemented ([PEP-487](https://www.python.org/dev/peps/pep-0487 "https://www.python.org/dev/peps/pep-0487")).
  (Github issue [#2781](https://github.com/cython/cython/issues/2781 "https://github.com/cython/cython/issues/2781"))
* Conditional blocks in Python code that depend on `cython.compiled` are
  eliminated at an earlier stage, which gives more freedom in writing
  replacement Python code.
  Patch by David Woods. (Github issue [#3507](https://github.com/cython/cython/issues/3507 "https://github.com/cython/cython/issues/3507"))
* `numpy.import_array()` is automatically called if `numpy` has been cimported
  and it has not been called in the module code. This is intended as a hidden
  fail-safe so user code should continue to call `numpy.import_array`.
  Patch by David Woods. (Github issue [#3524](https://github.com/cython/cython/issues/3524 "https://github.com/cython/cython/issues/3524"))
* The Cython AST code serialiser class `CodeWriter` in `Cython.CodeWriter`
  supports more syntax nodes.
* The fastcall/vectorcall protocols are used for several internal Python calls.
  (Github issue [#3540](https://github.com/cython/cython/issues/3540 "https://github.com/cython/cython/issues/3540"))

### Bugs fixed[¶](#id113 "Link to this heading")

* With `language_level=3/3str`, Python classes without explicit base class
  are now new-style (type) classes also in Py2. Previously, they were created
  as old-style (non-type) classes.
  (Github issue [#3530](https://github.com/cython/cython/issues/3530 "https://github.com/cython/cython/issues/3530"))
* C++ `typeid()` failed for fused types.
  Patch by David Woods. (Github issue [#3203](https://github.com/cython/cython/issues/3203 "https://github.com/cython/cython/issues/3203"))
* `__arg` argument names in methods were not mangled with the class name.
  Patch by David Woods. (Github issue [#1382](https://github.com/cython/cython/issues/1382 "https://github.com/cython/cython/issues/1382"))
* Creating an empty unicode slice with large bounds could crash.
  Patch by Sam Sneddon. (Github issue [#3531](https://github.com/cython/cython/issues/3531 "https://github.com/cython/cython/issues/3531"))
* Decoding an empty bytes/char\* slice with large bounds could crash.
  Patch by Sam Sneddon. (Github issue [#3534](https://github.com/cython/cython/issues/3534 "https://github.com/cython/cython/issues/3534"))
* Temporary buffer indexing variables were not released and could show up in
  C compiler warnings, e.g. in generators.
  Patch by David Woods. (Github issues [#3430](https://github.com/cython/cython/issues/3430 "https://github.com/cython/cython/issues/3430"), [#3522](https://github.com/cython/cython/issues/3522 "https://github.com/cython/cython/issues/3522"))
* Several C compiler warnings were fixed.

## 3.0.0 alpha 1 (2020-04-12)[¶](#alpha-1-2020-04-12 "Link to this heading")

### Features added[¶](#id114 "Link to this heading")

* Cython functions now use the [PEP-590](https://www.python.org/dev/peps/pep-0590 "https://www.python.org/dev/peps/pep-0590") vectorcall protocol in Py3.7+.
  Patch by Jeroen Demeyer. (Github issue [#2263](https://github.com/cython/cython/issues/2263 "https://github.com/cython/cython/issues/2263"))
* Unicode identifiers are supported in Cython code ([PEP-3131](https://www.python.org/dev/peps/pep-3131 "https://www.python.org/dev/peps/pep-3131")).
  Patch by David Woods. (Github issue [#2601](https://github.com/cython/cython/issues/2601 "https://github.com/cython/cython/issues/2601"))
* Unicode module names and imports are supported.
  Patch by David Woods. (Github issue [#3119](https://github.com/cython/cython/issues/3119 "https://github.com/cython/cython/issues/3119"))
* Annotations are no longer parsed, keeping them as strings following [PEP-563](https://www.python.org/dev/peps/pep-0563 "https://www.python.org/dev/peps/pep-0563").
  Patch by David Woods. (Github issue [#3285](https://github.com/cython/cython/issues/3285 "https://github.com/cython/cython/issues/3285"))
* Preliminary support for the CPython’s `Py_LIMITED_API` (stable ABI) is
  available by setting the `CYTHON_LIMITED_API` C macro. Note that the
  support is currently in an early stage and many features do not yet work.
  You currently still have to define `Py_LIMITED_API` externally in order
  to restrict the API usage. This will change when the feature stabilises.
  Patches by Eddie Elizondo and David Woods. (Github issues [#3223](https://github.com/cython/cython/issues/3223 "https://github.com/cython/cython/issues/3223"),
  [#3311](https://github.com/cython/cython/issues/3311 "https://github.com/cython/cython/issues/3311"), [#3501](https://github.com/cython/cython/issues/3501 "https://github.com/cython/cython/issues/3501"))
* The dispatch to fused functions is now linear in the number of arguments,
  which makes it much faster, often 2x or more, and several times faster for
  larger fused types with many specialisations.
  Patch by will-ca. (Github issue [#1385](https://github.com/cython/cython/issues/1385 "https://github.com/cython/cython/issues/1385"))
* `with gil/nogil` statements can be conditional based on compile-time
  constants, e.g. fused type checks.
  Patch by Noam Hershtig. (Github issue [#2579](https://github.com/cython/cython/issues/2579 "https://github.com/cython/cython/issues/2579"))
* `const` can be used together with fused types.
  Patch by Thomas Vincent. (Github issue [#1772](https://github.com/cython/cython/issues/1772 "https://github.com/cython/cython/issues/1772"))
* Reimports of already imported modules are substantially faster.
  (Github issue [#2854](https://github.com/cython/cython/issues/2854 "https://github.com/cython/cython/issues/2854"))
* Positional-only arguments are supported in Python functions ([PEP-570](https://www.python.org/dev/peps/pep-0570 "https://www.python.org/dev/peps/pep-0570")).
  Patch by Josh Tobin. (Github issue [#2915](https://github.com/cython/cython/issues/2915 "https://github.com/cython/cython/issues/2915"))
* The `volatile` C modifier is supported in Cython code.
  Patch by Jeroen Demeyer. (Github issue [#1667](https://github.com/cython/cython/issues/1667 "https://github.com/cython/cython/issues/1667"))
* `@cython.trashcan(True)` can be used on an extension type to enable the
  CPython [Enabling the deallocation trashcan](userguide/extension_types.html#trashcan "userguide/extension_types.html#trashcan"). This allows deallocating deeply recursive objects
  without overflowing the stack. Patch by Jeroen Demeyer. (Github issue [#2842](https://github.com/cython/cython/issues/2842 "https://github.com/cython/cython/issues/2842"))
* Inlined properties can be defined for external extension types.
  Patch by Matti Picus. (Github issue [#2640](https://github.com/cython/cython/issues/2640 "https://github.com/cython/cython/issues/2640"), redone later in [#3571](https://github.com/cython/cython/issues/3571 "https://github.com/cython/cython/issues/3571"))
* The `str()` builtin now calls `PyObject_Str()` instead of going
  through a Python call.
  Patch by William Ayd. (Github issue [#3279](https://github.com/cython/cython/issues/3279 "https://github.com/cython/cython/issues/3279"))
* String concatenation can now happen in place if possible, by extending the
  existing string rather than always creating a new one.
  Patch by David Woods. (Github issue [#3453](https://github.com/cython/cython/issues/3453 "https://github.com/cython/cython/issues/3453"))
* Multiplication of Python numbers with small constant integers is faster.
  (Github issue [#2808](https://github.com/cython/cython/issues/2808 "https://github.com/cython/cython/issues/2808"))
* Some list copying is avoided internally when a new list needs to be created
  but we already have a fresh one.
  (Github issue [#3494](https://github.com/cython/cython/issues/3494 "https://github.com/cython/cython/issues/3494"))
* Extension types that do not need their own `tp_new` implementation (because
  they have no object attributes etc.) directly inherit the implementation of
  their parent type if possible.
  (Github issue [#1555](https://github.com/cython/cython/issues/1555 "https://github.com/cython/cython/issues/1555"))
* The attributes `gen.gi_frame` and `coro.cr_frame` of Cython compiled
  generators and coroutines now return an actual frame object for introspection.
  (Github issue [#2306](https://github.com/cython/cython/issues/2306 "https://github.com/cython/cython/issues/2306"))
* Several declarations in `cpython.*`, `libc.*` and `libcpp.*` were added.
  Patches by Jeroen Demeyer, Matthew Edwards, Chris Gyurgyik, Jerome Kieffer
  and Zackery Spytz.
  (Github issues [#3468](https://github.com/cython/cython/issues/3468 "https://github.com/cython/cython/issues/3468"), [#3332](https://github.com/cython/cython/issues/3332 "https://github.com/cython/cython/issues/3332"), [#3202](https://github.com/cython/cython/issues/3202 "https://github.com/cython/cython/issues/3202"), [#3188](https://github.com/cython/cython/issues/3188 "https://github.com/cython/cython/issues/3188"),
  [#3179](https://github.com/cython/cython/issues/3179 "https://github.com/cython/cython/issues/3179"), [#2891](https://github.com/cython/cython/issues/2891 "https://github.com/cython/cython/issues/2891"), [#2826](https://github.com/cython/cython/issues/2826 "https://github.com/cython/cython/issues/2826"), [#2713](https://github.com/cython/cython/issues/2713 "https://github.com/cython/cython/issues/2713"))
* Deprecated NumPy API usages were removed from `numpy.pxd`.
  Patch by Matti Picus. (Github issue [#3365](https://github.com/cython/cython/issues/3365 "https://github.com/cython/cython/issues/3365"))
* `cython.inline()` now sets the `NPY_NO_DEPRECATED_API=NPY_1_7_API_VERSION`
  C macro automatically when `numpy` is imported in the code, to avoid C compiler
  warnings about deprecated NumPy C-API usage.
* The builtin `abs()` function can now be used on C numbers in nogil code.
  Patch by Elliott Sales de Andrade. (Github issue [#2748](https://github.com/cython/cython/issues/2748 "https://github.com/cython/cython/issues/2748"))
* [PEP-479](https://www.python.org/dev/peps/pep-0479 "https://www.python.org/dev/peps/pep-0479") (`generator_stop`) is now enabled by default with language level 3.
  (Github issue [#2580](https://github.com/cython/cython/issues/2580 "https://github.com/cython/cython/issues/2580"))
* The `cython.view.array` type supports inheritance.
  Patch by David Woods. (Github issue [#3413](https://github.com/cython/cython/issues/3413 "https://github.com/cython/cython/issues/3413"))
* Code annotation accepts a new debugging argument `--annotate-fullc` that
  will include the complete syntax highlighted C file in the HTML output.
  (Github issue [#2855](https://github.com/cython/cython/issues/2855 "https://github.com/cython/cython/issues/2855"))
* `--no-capture` added to `runtests.py` to prevent stdout/stderr capturing
  during srctree tests.
  Patch by Matti Picus. (Github issue [#2701](https://github.com/cython/cython/issues/2701 "https://github.com/cython/cython/issues/2701"))
* `--no-docstrings` option added to `cythonize` script.
  Original patch by mo-han. (Github issue [#2889](https://github.com/cython/cython/issues/2889 "https://github.com/cython/cython/issues/2889"))
* `cygdb` gives better error messages when it fails to initialise the
  Python runtime support in gdb.
  Patch by Volker Weissmann. (Github issue [#3489](https://github.com/cython/cython/issues/3489 "https://github.com/cython/cython/issues/3489"))
* The Pythran `shape` attribute is supported.
  Patch by Serge Guelton. (Github issue [#3307](https://github.com/cython/cython/issues/3307 "https://github.com/cython/cython/issues/3307"))

### Bugs fixed[¶](#id115 "Link to this heading")

* The unicode methods `.upper()`, `.lower()` and `.title()` were
  incorrectly optimised for single character input values and only returned
  the first character if multiple characters should have been returned.
  They now use the original Python methods again.
* Fused argument types were not correctly handled in type annotations and
  `cython.locals()`.
  Patch by David Woods. (Github issues [#3391](https://github.com/cython/cython/issues/3391 "https://github.com/cython/cython/issues/3391"), [#3142](https://github.com/cython/cython/issues/3142 "https://github.com/cython/cython/issues/3142"))
* Diverging from the usual behaviour, `len(memoryview)`, `len(char*)`
  and `len(Py_UNICODE*)` returned an unsigned `size_t` value. They now
  return a signed `Py_ssize_t`, like other usages of `len()`.
* Nested dict literals in function call kwargs could incorrectly raise an
  error about duplicate keyword arguments, which are allowed when passing
  them from dict literals.
  (Github issue [#2963](https://github.com/cython/cython/issues/2963 "https://github.com/cython/cython/issues/2963"))
* Item access (subscripting) with integer indices/keys always tried the
  Sequence protocol before the Mapping protocol, which diverged from Python
  semantics. It now passes through the Mapping protocol first when supported.
  (Github issue [#1807](https://github.com/cython/cython/issues/1807 "https://github.com/cython/cython/issues/1807"))
* Name lookups in class bodies no longer go through an attribute lookup.
  Patch by Jeroen Demeyer. (Github issue [#3100](https://github.com/cython/cython/issues/3100 "https://github.com/cython/cython/issues/3100"))
* Broadcast assignments to a multi-dimensional memory view slice could end
  up in the wrong places when the underlying memory view is known to be
  contiguous but the slice is not.
  (Github issue [#2941](https://github.com/cython/cython/issues/2941 "https://github.com/cython/cython/issues/2941"))
* Pickling unbound methods of Python classes failed.
  Patch by Pierre Glaser. (Github issue [#2972](https://github.com/cython/cython/issues/2972 "https://github.com/cython/cython/issues/2972"))
* The `Py_hash_t` type failed to accept arbitrary “index” values.
  (Github issue [#2752](https://github.com/cython/cython/issues/2752 "https://github.com/cython/cython/issues/2752"))
* The first function line number of functions with decorators pointed to the
  signature line and not the first decorator line, as in Python.
  Patch by Felix Kohlgrüber. (Github issue [#2536](https://github.com/cython/cython/issues/2536 "https://github.com/cython/cython/issues/2536"))
* Constant integer expressions that used a negative exponent were evaluated
  as integer 0 instead of the expected float value.
  Patch by Kryštof Pilnáček. (Github issue [#2133](https://github.com/cython/cython/issues/2133 "https://github.com/cython/cython/issues/2133"))
* The `cython.declare()` and `cython.cast()` functions could fail in pure mode.
  Patch by Dmitry Shesterkin. (Github issue [#3244](https://github.com/cython/cython/issues/3244 "https://github.com/cython/cython/issues/3244"))
* `__doc__` was not available inside of the class body during class creation.
  (Github issue [#1635](https://github.com/cython/cython/issues/1635 "https://github.com/cython/cython/issues/1635"))
* Setting `language_level=2` in a file did not work if `language_level=3`
  was enabled globally before.
  Patch by Jeroen Demeyer. (Github issue [#2791](https://github.com/cython/cython/issues/2791 "https://github.com/cython/cython/issues/2791"))
* `__init__.pyx` files were not always considered as package indicators.
  (Github issue [#2665](https://github.com/cython/cython/issues/2665 "https://github.com/cython/cython/issues/2665"))
* Compiling package `__init__` files could fail under Windows due to an
  undefined export symbol. (Github issue [#2968](https://github.com/cython/cython/issues/2968 "https://github.com/cython/cython/issues/2968"))
* A C compiler cast warning was resolved.
  Patch by Michael Buesch. (Github issue [#2775](https://github.com/cython/cython/issues/2775 "https://github.com/cython/cython/issues/2775"))
* Binding staticmethods of Cython functions were not behaving like Python methods.
  Patch by Jeroen Demeyer. (Github issue [#3106](https://github.com/cython/cython/issues/3106 "https://github.com/cython/cython/issues/3106"), [#3102](https://github.com/cython/cython/issues/3102 "https://github.com/cython/cython/issues/3102"))
* Memoryviews failed to compile when the `cache_builtins` feature was disabled.
  Patch by David Woods. (Github issue [#3406](https://github.com/cython/cython/issues/3406 "https://github.com/cython/cython/issues/3406"))

### Other changes[¶](#id116 "Link to this heading")

* The default language level was changed to `3str`, i.e. Python 3 semantics,
  but with `str` literals (also in Python 2.7). This is a backwards incompatible
  change from the previous default of Python 2 semantics. The previous behaviour
  is available through the directive `language_level=2`.
  (Github issue [#2565](https://github.com/cython/cython/issues/2565 "https://github.com/cython/cython/issues/2565"))
* Cython no longer generates `__qualname__` attributes for classes in Python
  2.x since they are problematic there and not correctly maintained for subclasses.
  Patch by Jeroen Demeyer. (Github issue [#2772](https://github.com/cython/cython/issues/2772 "https://github.com/cython/cython/issues/2772"))
* Source file fingerprinting now uses SHA-1 instead of MD5 since the latter
  tends to be slower and less widely supported these days.
  (Github issue [#2790](https://github.com/cython/cython/issues/2790 "https://github.com/cython/cython/issues/2790"))
* The long deprecated include files `python_*`, `stdio`, `stdlib` and
  `stl` in `Cython/Includes/Deprecated/` were removed. Use the `libc.*`
  and `cpython.*` pxd modules instead.
  Patch by Jeroen Demeyer. (Github issue [#2904](https://github.com/cython/cython/issues/2904 "https://github.com/cython/cython/issues/2904"))
* The search order for include files was changed. Previously it was
  `include_directories`, `Cython/Includes`, `sys.path`. Now it is
  `include_directories`, `sys.path`, `Cython/Includes`. This was done to
  allow third-party `*.pxd` files to override the ones in Cython.
  Patch by Matti Picus. (Github issue [#2905](https://github.com/cython/cython/issues/2905 "https://github.com/cython/cython/issues/2905"))
* The command line parser was rewritten and modernised using `argparse`.
  Patch by Egor Dranischnikow. (Github issue [#2952](https://github.com/cython/cython/issues/2952 "https://github.com/cython/cython/issues/2952"), [#3001](https://github.com/cython/cython/issues/3001 "https://github.com/cython/cython/issues/3001"))
* Dotted filenames for qualified module names (`pkg.mod.pyx`) are deprecated.
  Use the normal Python package directory layout instead.
  (Github issue [#2686](https://github.com/cython/cython/issues/2686 "https://github.com/cython/cython/issues/2686"))
* Binary Linux wheels now follow the manylinux2010 standard.
  Patch by Alexey Stepanov. (Github issue [#3355](https://github.com/cython/cython/issues/3355 "https://github.com/cython/cython/issues/3355"))
* Support for Python 2.6 was removed.

## 0.29.37 (2023-12-18)[¶](#id124 "Link to this heading")

### Bugs fixed[¶](#id126 "Link to this heading")

* Fix a potential crash while cleaning up subtypes of externally imported extension
  types when terminating Python. This was introduced in Cython 0.29.35.
* Fix a `complex` related compile error on Windows.
  (Github issue [#5512](https://github.com/cython/cython/issues/5512 "https://github.com/cython/cython/issues/5512"))
* Compiling fused types used in pxd files could crash Cython in Python 3.11+.
  (Github issues [#5894](https://github.com/cython/cython/issues/5894 "https://github.com/cython/cython/issues/5894"), [#5588](https://github.com/cython/cython/issues/5588 "https://github.com/cython/cython/issues/5588"))
* `cythonize` failed to consider the `CYTHON_FORCE_REGEN` env variable.
  Patch by Harmen Stoppels. (Github issue [#5712](https://github.com/cython/cython/issues/5712 "https://github.com/cython/cython/issues/5712"))

## 0.29.36 (2023-07-04)[¶](#id127 "Link to this heading")

### Bugs fixed[¶](#id129 "Link to this heading")

* Async generators lost their return value in PyPy.
  (Github issue [#5465](https://github.com/cython/cython/issues/5465 "https://github.com/cython/cython/issues/5465"))
* The outdated C macro `_PyGC_FINALIZED()` is no longer used in Py3.9+.
* The deprecated `Py_OptimizeFlag` is no longer used in Python 3.9+.
  (Github issue [#5343](https://github.com/cython/cython/issues/5343 "https://github.com/cython/cython/issues/5343"))
* Using the global `__debug__` variable but not assertions could lead to compile errors.
* The broken HTML template support was removed from Tempita.
  (Github issue [#3309](https://github.com/cython/cython/issues/3309 "https://github.com/cython/cython/issues/3309"))

## 0.29.35 (2023-05-24)[¶](#id130 "Link to this heading")

### Bugs fixed[¶](#id132 "Link to this heading")

* A garbage collection enabled subtype of a non-GC extension type could call into the
  deallocation function of the super type with GC tracking enabled. This could lead
  to crashes during deallocation if GC was triggered on the type at the same time.
  (Github issue [#5432](https://github.com/cython/cython/issues/5432 "https://github.com/cython/cython/issues/5432"))
* Some C compile failures and crashes in CPython 3.12 were resolved.
* `except + nogil` was syntactically not allowed.
  `except +nogil` (i.e. defining a C++ exception handling function called `nogil`)
  is now disallowed to prevent typos.
  (Github issue [#5430](https://github.com/cython/cython/issues/5430 "https://github.com/cython/cython/issues/5430"))
* A C compile failure in PyPy 3.10 was resolved.
  Patch by Matti Picus. (Github issue [#5408](https://github.com/cython/cython/issues/5408 "https://github.com/cython/cython/issues/5408"))
* Cython modules now use PEP-489 multi-phase init by default in PyPy 3.9 and later.
  Original patch by Matti Picus. (Github issue [#5413](https://github.com/cython/cython/issues/5413 "https://github.com/cython/cython/issues/5413"))
* API header files generated by different Cython versions can now be included in the
  same C file.
  (Github issue [#5383](https://github.com/cython/cython/issues/5383 "https://github.com/cython/cython/issues/5383"))
* Function signatures containing a type like tuple[()] could not be printed.
  Patch by Lisandro Dalcin. (Github issue [#5355](https://github.com/cython/cython/issues/5355 "https://github.com/cython/cython/issues/5355"))

## 0.29.34 (2023-04-02)[¶](#id133 "Link to this heading")

### Bugs fixed[¶](#id135 "Link to this heading")

* A reference leak of the for-loop list/tuple iterable was resolved if the for-loop’s
  `else:` branch executes a `break` for an outer loop.
  (Github issue [#5347](https://github.com/cython/cython/issues/5347 "https://github.com/cython/cython/issues/5347"))
* Some C compile failures in CPython 3.12 were resolved.
* Some old usages of the deprecated Python `imp` module were replaced with `importlib`.
  Patch by Matúš Valo. (Github issue [#5300](https://github.com/cython/cython/issues/5300 "https://github.com/cython/cython/issues/5300"))
* Some issues with `depfile` generation were resolved.
  Patches by Eli Schwartz. (Github issues [#5279](https://github.com/cython/cython/issues/5279 "https://github.com/cython/cython/issues/5279"), [#5291](https://github.com/cython/cython/issues/5291 "https://github.com/cython/cython/issues/5291"))

## 0.29.33 (2023-01-06)[¶](#id136 "Link to this heading")

### Features added[¶](#id138 "Link to this heading")

* The `cythonize` and `cython` commands have a new option `-M` / `--depfile`
  to generate `.dep` dependency files for the compilation unit. This can be used
  by external build tools to track these dependencies.
  The `cythonize` option was already available in Cython [0.29.27 (2022-01-28)](#id158 "#id158").
  Patches by Evgeni Burovski and Eli Schwartz. (Github issue [#1214](https://github.com/cython/cython/issues/1214 "https://github.com/cython/cython/issues/1214"))

### Bugs fixed[¶](#id139 "Link to this heading")

* `const` fused types could not be used with memory views.
  Patch by Thomas Vincent. (Github issue [#1772](https://github.com/cython/cython/issues/1772 "https://github.com/cython/cython/issues/1772"))
* `wstr` usage was removed in Python 3.12 and later (PEP-623).
  (Github issue [#5145](https://github.com/cython/cython/issues/5145 "https://github.com/cython/cython/issues/5145"))
* A type check assertion for Cython functions failed in debug Python builds.
  (Github issue [#5031](https://github.com/cython/cython/issues/5031 "https://github.com/cython/cython/issues/5031"))
* Fixed various compiler warnings.
  Patches by Lisandro Dalcin et al. (Github issues [#4948](https://github.com/cython/cython/issues/4948 "https://github.com/cython/cython/issues/4948"), [#5086](https://github.com/cython/cython/issues/5086 "https://github.com/cython/cython/issues/5086"))
* Fixed error when calculating complex powers of negative numbers.
  (Github issue [#5014](https://github.com/cython/cython/issues/5014 "https://github.com/cython/cython/issues/5014"))
* Corrected a small mis-formatting of exception messages on Python 2.
  (Github issue [#5018](https://github.com/cython/cython/issues/5018 "https://github.com/cython/cython/issues/5018"))
* The `PyUnicode_AsUTF8AndSize()` C-API function was missing from the CPython declarations.
  (Github issue [#5163](https://github.com/cython/cython/issues/5163 "https://github.com/cython/cython/issues/5163"))
* A performance problem in the compiler was resolved when nesting conditional expressions.
  (Github issue [#5197](https://github.com/cython/cython/issues/5197 "https://github.com/cython/cython/issues/5197"))
* Test suite problems with recent NumPy and CPython versions were resolved.
  (Github issues [#5183](https://github.com/cython/cython/issues/5183 "https://github.com/cython/cython/issues/5183"), [#5190](https://github.com/cython/cython/issues/5190 "https://github.com/cython/cython/issues/5190"))

### Other changes[¶](#id140 "Link to this heading")

* The undocumented, untested and apparently useless syntax
  `from somemodule cimport class/struct/union somename` was deprecated
  in anticipation of its removal in Cython 3. The type
  modifier is not needed here and a plain `cimport` of the name will do.
  (Github issue [#4905](https://github.com/cython/cython/issues/4905 "https://github.com/cython/cython/issues/4905"))
* Properly disable generation of descriptor docstrings on PyPy since they cause crashes.
  It was previously disabled, but only accidentally via a typo.
  Patch by Matti Picus. (Github issue [#5083](https://github.com/cython/cython/issues/5083 "https://github.com/cython/cython/issues/5083"))
* The `cpow` directive of Cython 3.0 is available as a no-op.
  (Github issue [#5016](https://github.com/cython/cython/issues/5016 "https://github.com/cython/cython/issues/5016"))

## 0.29.32 (2022-07-29)[¶](#id141 "Link to this heading")

### Bugs fixed[¶](#id143 "Link to this heading")

* Revert “Using memoryview typed arguments in inner functions is now rejected as unsupported.”
  Patch by David Woods. (Github issue [#4798](https://github.com/cython/cython/issues/4798 "https://github.com/cython/cython/issues/4798"))
* `from module import *` failed in 0.29.31 when using memoryviews.
  Patch by David Woods. (Github issue [#4927](https://github.com/cython/cython/issues/4927 "https://github.com/cython/cython/issues/4927"))

## 0.29.31 (2022-07-27)[¶](#id144 "Link to this heading")

### Features added[¶](#id146 "Link to this heading")

* A new argument `--module-name` was added to the `cython` command to
  provide the (one) exact target module name from the command line.
  Patch by Matthew Brett and h-vetinari. (Github issue [#4906](https://github.com/cython/cython/issues/4906 "https://github.com/cython/cython/issues/4906"))
* A new keyword `noexcept` was added for forward compatibility with Cython 3.
  Patch by David Woods. (Github issue [#4903](https://github.com/cython/cython/issues/4903 "https://github.com/cython/cython/issues/4903"))

### Bugs fixed[¶](#id147 "Link to this heading")

* Use `importlib.util.find_spec()` instead of the deprecated `importlib.find_loader()`
  function when setting up the package path at import-time.
  Patch by Matti Picus. (Github issue [#4764](https://github.com/cython/cython/issues/4764 "https://github.com/cython/cython/issues/4764"))
* Require the C compiler to support the two-arg form of `va_start`
  on Python 3.10 and higher.
  Patch by Thomas Caswell. (Github issue [#4820](https://github.com/cython/cython/issues/4820 "https://github.com/cython/cython/issues/4820"))
* Make `fused_type` subscriptable in Shadow.py.
  Patch by Pfebrer. (Github issue [#4842](https://github.com/cython/cython/issues/4842 "https://github.com/cython/cython/issues/4842"))
* Fix the incorrect code generation of the target type in `bytearray` loops.
  Patch by Kenrick Everett. (Github issue [#4108](https://github.com/cython/cython/issues/4108 "https://github.com/cython/cython/issues/4108"))
* Atomic refcounts for memoryviews were not used on some GCC versions by accident.
  Patch by Sam Gross. (Github issue [#4915](https://github.com/cython/cython/issues/4915 "https://github.com/cython/cython/issues/4915"))
* Silence some GCC `-Wconversion` warnings in C utility code.
  Patch by Lisandro Dalcin. (Github issue [#4854](https://github.com/cython/cython/issues/4854 "https://github.com/cython/cython/issues/4854"))
* Tuple multiplication was ignored in expressions such as `[*(1,) * 2]`.
  Patch by David Woods. (Github issue [#4864](https://github.com/cython/cython/issues/4864 "https://github.com/cython/cython/issues/4864"))
* Calling `append` methods on extension types could fail to find the method
  in some cases.
  Patch by David Woods. (Github issue [#4828](https://github.com/cython/cython/issues/4828 "https://github.com/cython/cython/issues/4828"))
* Ensure that object buffers (e.g. `ndarray[object, ndim=1]`) containing
  `NULL` pointers are safe to use, returning `None` instead of the `NULL`
  pointer.
  Patch by Sebastian Berg. (Github issue [#4859](https://github.com/cython/cython/issues/4859 "https://github.com/cython/cython/issues/4859"))
* Using memoryview typed arguments in inner functions is now rejected as unsupported.
  Patch by David Woods. (Github issue [#4798](https://github.com/cython/cython/issues/4798 "https://github.com/cython/cython/issues/4798"))
* Compilation could fail on systems (e.g. FIPS) that block MD5 checksums at runtime.
  (Github issue [#4909](https://github.com/cython/cython/issues/4909 "https://github.com/cython/cython/issues/4909"))
* Experimental adaptations for the CPython “nogil” fork was added.
  Note that there is no official support for this in Cython 0.x.
  Patch by Sam Gross. (Github issue [#4912](https://github.com/cython/cython/issues/4912 "https://github.com/cython/cython/issues/4912"))

## 0.29.30 (2022-05-16)[¶](#id148 "Link to this heading")

### Bugs fixed[¶](#id150 "Link to this heading")

* The GIL handling changes in 0.29.29 introduced a regression where
  objects could be deallocated without holding the GIL.
  (Github issue [#4796](https://github.com/cython/cython/issues/4796 "https://github.com/cython/cython/issues/4796"))

## 0.29.29 (2022-05-16)[¶](#id151 "Link to this heading")

### Features added[¶](#id153 "Link to this heading")

* Avoid acquiring the GIL at the end of nogil functions.
  This change was backported in order to avoid generating wrong C code
  that would trigger C compiler warnings with tracing support enabled.
  Backport by Oleksandr Pavlyk. (Github issue [#4637](https://github.com/cython/cython/issues/4637 "https://github.com/cython/cython/issues/4637"))

### Bugs fixed[¶](#id154 "Link to this heading")

* Function definitions in `finally:` clauses were not correctly generated.
  Patch by David Woods. (Github issue [#4651](https://github.com/cython/cython/issues/4651 "https://github.com/cython/cython/issues/4651"))
* A case where C-API functions could be called with a live exception set was fixed.
  Patch by Jakub Kulík. (Github issue [#4722](https://github.com/cython/cython/issues/4722 "https://github.com/cython/cython/issues/4722"))
* Pickles can now be exchanged again with those generated from Cython 3.0 modules.
  (Github issue [#4680](https://github.com/cython/cython/issues/4680 "https://github.com/cython/cython/issues/4680"))
* Cython now correctly generates Python methods for both the provided regular and
  reversed special numeric methods of extension types.
  Patch by David Woods. (Github issue [#4750](https://github.com/cython/cython/issues/4750 "https://github.com/cython/cython/issues/4750"))
* Calling unbound extension type methods without arguments could raise an
  `IndexError` instead of a `TypeError`.
  Patch by David Woods. (Github issue [#4779](https://github.com/cython/cython/issues/4779 "https://github.com/cython/cython/issues/4779"))
* Calling unbound `.__contains__()` super class methods on some builtin base
  types could trigger an infinite recursion.
  Patch by David Woods. (Github issue [#4785](https://github.com/cython/cython/issues/4785 "https://github.com/cython/cython/issues/4785"))
* The C union type in pure Python mode mishandled some field names.
  Patch by Jordan Brière. (Github issue [#4727](https://github.com/cython/cython/issues/4727 "https://github.com/cython/cython/issues/4727"))
* Allow users to overwrite the C macro `_USE_MATH_DEFINES`.
  Patch by Yuriy Chernyshov. (Github issue [#4690](https://github.com/cython/cython/issues/4690 "https://github.com/cython/cython/issues/4690"))
* Improved compatibility with CPython 3.10/11.
  Patches by Thomas Caswell, David Woods.
  (Github issues [#4609](https://github.com/cython/cython/issues/4609 "https://github.com/cython/cython/issues/4609"), [#4667](https://github.com/cython/cython/issues/4667 "https://github.com/cython/cython/issues/4667"), [#4721](https://github.com/cython/cython/issues/4721 "https://github.com/cython/cython/issues/4721"), [#4730](https://github.com/cython/cython/issues/4730 "https://github.com/cython/cython/issues/4730"), [#4777](https://github.com/cython/cython/issues/4777 "https://github.com/cython/cython/issues/4777"))
* Docstrings of descriptors are now provided in PyPy 7.3.9.
  Patch by Matti Picus. (Github issue [#4701](https://github.com/cython/cython/issues/4701 "https://github.com/cython/cython/issues/4701"))

## 0.29.28 (2022-02-17)[¶](#id155 "Link to this heading")

### Bugs fixed[¶](#id157 "Link to this heading")

* Due to backwards incompatible changes in CPython 3.11a4, the feature flags
  `CYTHON_FAST_THREAD_STATE` and `CYTHON_USE_EXC_INFO_STACK` are now disabled
  in Python 3.11 and later. They are enabled again in Cython 3.0.
  Patch by David Woods. (Github issue [#4610](https://github.com/cython/cython/issues/4610 "https://github.com/cython/cython/issues/4610"))
* A C compiler warning in older PyPy versions was resolved.
  Patch by Matti Picus. (Github issue [#4236](https://github.com/cython/cython/issues/4236 "https://github.com/cython/cython/issues/4236"))

## 0.29.27 (2022-01-28)[¶](#id158 "Link to this heading")

### Features added[¶](#id160 "Link to this heading")

* The `cythonize` command has a new option `-M` to generate `.dep` dependency
  files for the compilation unit. This can be used by external build tools to track
  these dependencies.
  Patch by Evgeni Burovski. (Github issue [#1214](https://github.com/cython/cython/issues/1214 "https://github.com/cython/cython/issues/1214"))

### Bugs fixed[¶](#id161 "Link to this heading")

* Compilation failures on PyPy were resolved.
  Patches by Matti Picus. (Github issues [#4509](https://github.com/cython/cython/issues/4509 "https://github.com/cython/cython/issues/4509"), [#4517](https://github.com/cython/cython/issues/4517 "https://github.com/cython/cython/issues/4517"))
* Calls to `range()` with more than three arguments did not fail.
  Original patch by Max Bachmann. (Github issue [#4550](https://github.com/cython/cython/issues/4550 "https://github.com/cython/cython/issues/4550"))
* Some C compiler warnings about missing type struct initialisers in Py3.10 were resolved.
* Cython no longer warns about using OpenMP 3.0 features since they are now
  considered generally available.

## 0.29.26 (2021-12-16)[¶](#id162 "Link to this heading")

### Bugs fixed[¶](#id164 "Link to this heading")

* An incompatibility with CPython 3.11.0a3 was resolved.
  (Github issue [#4499](https://github.com/cython/cython/issues/4499 "https://github.com/cython/cython/issues/4499"))
* The `in` operator failed on literal lists with starred expressions.
  Patch by Arvind Natarajan. (Github issue [#3938](https://github.com/cython/cython/issues/3938 "https://github.com/cython/cython/issues/3938"))
* A C compiler warning in PyPy about a missing struct field initialisation was resolved.

## 0.29.25 (2021-12-06)[¶](#id165 "Link to this heading")

### Bugs fixed[¶](#id167 "Link to this heading")

* Several incompatibilities with CPython 3.11 were resolved.
  Patches by David Woods, Victor Stinner, Thomas Caswell.
  (Github issues [#4411](https://github.com/cython/cython/issues/4411 "https://github.com/cython/cython/issues/4411"), [#4414](https://github.com/cython/cython/issues/4414 "https://github.com/cython/cython/issues/4414"), [#4415](https://github.com/cython/cython/issues/4415 "https://github.com/cython/cython/issues/4415"), [#4416](https://github.com/cython/cython/issues/4416 "https://github.com/cython/cython/issues/4416"), [#4420](https://github.com/cython/cython/issues/4420 "https://github.com/cython/cython/issues/4420"),
  [#4428](https://github.com/cython/cython/issues/4428 "https://github.com/cython/cython/issues/4428"), [#4473](https://github.com/cython/cython/issues/4473 "https://github.com/cython/cython/issues/4473"), [#4479](https://github.com/cython/cython/issues/4479 "https://github.com/cython/cython/issues/4479"), [#4480](https://github.com/cython/cython/issues/4480 "https://github.com/cython/cython/issues/4480"))
* Some C compiler warnings were resolved.
  Patches by Lisandro Dalcin and others. (Github issue [#4439](https://github.com/cython/cython/issues/4439 "https://github.com/cython/cython/issues/4439"))
* C++ `std::move()` should only be used automatically in MSVC versions that support it.
  Patch by Max Bachmann. (Github issue [#4191](https://github.com/cython/cython/issues/4191 "https://github.com/cython/cython/issues/4191"))

* The `Py_hash_t` type failed to accept arbitrary “index” values.
  (Github issue [#2752](https://github.com/cython/cython/issues/2752 "https://github.com/cython/cython/issues/2752"))

* Avoid copying unaligned 16-bit values since some platforms require them to be aligned.
  Use memcpy() instead to let the C compiler decide how to do it.
  (Github issue [#4343](https://github.com/cython/cython/issues/4343 "https://github.com/cython/cython/issues/4343"))
* Cython crashed on invalid truthiness tests on C++ types without `operator bool`.
  Patch by David Woods. (Github issue [#4348](https://github.com/cython/cython/issues/4348 "https://github.com/cython/cython/issues/4348"))
* The declaration of `PyUnicode_CompareWithASCIIString()` in `cpython.unicode` was incorrect.
  Patch by Max Bachmann. (Github issue [#4344](https://github.com/cython/cython/issues/4344 "https://github.com/cython/cython/issues/4344"))

## 0.29.24 (2021-07-14)[¶](#id168 "Link to this heading")

### Bugs fixed[¶](#id170 "Link to this heading")

* Inline functions in pxd files that used memory views could lead to invalid
  C code if the module that imported from them does not use memory views.
  Patch by David Woods. (Github issue [#1415](https://github.com/cython/cython/issues/1415 "https://github.com/cython/cython/issues/1415"))
* Several declarations in `libcpp.string` were added and corrected.
  Patch by Janek Bevendorff. (Github issue [#4268](https://github.com/cython/cython/issues/4268 "https://github.com/cython/cython/issues/4268"))
* Pickling unbound Cython compiled methods failed.
  Patch by Pierre Glaser. (Github issue [#2972](https://github.com/cython/cython/issues/2972 "https://github.com/cython/cython/issues/2972"))
* The tracing code was adapted to work with CPython 3.10.
* The optimised `in` operator failed on unicode strings in Py3.9 and later
  that were constructed from an external `wchar_t` source.
  Also, related C compiler warnings about deprecated C-API usage were resolved.
  (Github issue [#3925](https://github.com/cython/cython/issues/3925 "https://github.com/cython/cython/issues/3925"))
* Some compiler crashes were resolved.
  Patch by David Woods. (Github issues [#4214](https://github.com/cython/cython/issues/4214 "https://github.com/cython/cython/issues/4214"), [#2811](https://github.com/cython/cython/issues/2811 "https://github.com/cython/cython/issues/2811"))
* An incorrect warning about ‘unused’ generator expressions was removed.
  (GIthub issue [#1699](https://github.com/cython/cython/issues/1699 "https://github.com/cython/cython/issues/1699"))
* The attributes `gen.gi_frame` and `coro.cr_frame` of Cython compiled
  generators and coroutines now return an actual frame object for introspection,
  instead of `None`.
  (Github issue [#2306](https://github.com/cython/cython/issues/2306 "https://github.com/cython/cython/issues/2306"))

## 0.29.23 (2021-04-14)[¶](#id171 "Link to this heading")

### Bugs fixed[¶](#id173 "Link to this heading")

* Some problems with Python 3.10 were resolved.
  Patches by Victor Stinner and David Woods. (Github issues [#4046](https://github.com/cython/cython/issues/4046 "https://github.com/cython/cython/issues/4046"), [#4100](https://github.com/cython/cython/issues/4100 "https://github.com/cython/cython/issues/4100"))
* An incorrect “optimisation” was removed that allowed changes to a keyword
  dict to leak into keyword arguments passed into a function.
  Patch by Peng Weikang. (Github issue [#3227](https://github.com/cython/cython/issues/3227 "https://github.com/cython/cython/issues/3227"))
* Multiplied str constants could end up as bytes constants with language\_level=2.
  Patch by Alphadelta14 and David Woods. (Github issue [#3951](https://github.com/cython/cython/issues/3951 "https://github.com/cython/cython/issues/3951"))
* `PY_SSIZE_T_CLEAN` does not get defined any more if it is already defined.
  Patch by Andrew Jones. (Github issue [#4104](https://github.com/cython/cython/issues/4104 "https://github.com/cython/cython/issues/4104"))

## 0.29.22 (2021-02-20)[¶](#id174 "Link to this heading")

### Features added[¶](#id176 "Link to this heading")

* Some declarations were added to the provided pxd includes.
  Patches by Zackery Spytz and John Kirkham.
  (Github issues [#3811](https://github.com/cython/cython/issues/3811 "https://github.com/cython/cython/issues/3811"), [#3882](https://github.com/cython/cython/issues/3882 "https://github.com/cython/cython/issues/3882"), [#3899](https://github.com/cython/cython/issues/3899 "https://github.com/cython/cython/issues/3899"), [#3901](https://github.com/cython/cython/issues/3901 "https://github.com/cython/cython/issues/3901"))

### Bugs fixed[¶](#id177 "Link to this heading")

* A crash when calling certain functions in Py3.9 and later was resolved.
  (Github issue [#3917](https://github.com/cython/cython/issues/3917 "https://github.com/cython/cython/issues/3917"))
* `const` memory views of structs failed to compile.
  (Github issue [#2251](https://github.com/cython/cython/issues/2251 "https://github.com/cython/cython/issues/2251"))
* `const` template declarations could not be nested.
  Patch by Ashwin Srinath. (Github issue [#1355](https://github.com/cython/cython/issues/1355 "https://github.com/cython/cython/issues/1355"))
* The declarations in the `cpython.pycapsule` module were missing their
  `const` modifiers and generated incorrect C code.
  Patch by Warren Weckesser. (Github issue [#3964](https://github.com/cython/cython/issues/3964 "https://github.com/cython/cython/issues/3964"))
* Casts to memory views failed for fused dtypes.
  Patch by David Woods. (Github issue [#3881](https://github.com/cython/cython/issues/3881 "https://github.com/cython/cython/issues/3881"))
* `repr()` was assumed to return `str` instead of `unicode` with `language_level=3`.
  (Github issue [#3736](https://github.com/cython/cython/issues/3736 "https://github.com/cython/cython/issues/3736"))
* Calling `cpdef` functions from cimported modules crashed the compiler.
  Patch by David Woods. (Github issue [#4000](https://github.com/cython/cython/issues/4000 "https://github.com/cython/cython/issues/4000"))
* Cython no longer validates the ABI size of the NumPy classes it compiled against.
  See the discussion in [https://github.com/numpy/numpy/pull/432](https://github.com/numpy/numpy/pull/432 "https://github.com/numpy/numpy/pull/432")
* A C compiler warning about enum value casting was resolved in GCC.
  (Github issue [#2749](https://github.com/cython/cython/issues/2749 "https://github.com/cython/cython/issues/2749"))
* Coverage reporting in the annotated HTML file failed in Py3.9.
  Patch by Nick Pope. (Github issue [#3865](https://github.com/cython/cython/issues/3865 "https://github.com/cython/cython/issues/3865"))
* The embedding code now reports Python errors as exit status.
* Long type declarations could lead to (harmless) random changes in the
  C file when used in auto-generated Python wrappers or pickled classes.

### Other changes[¶](#id178 "Link to this heading")

* Variables defined as `cpdef` now generate a warning since this
  is currently useless and thus does not do what users would expect.
  Patch by David Woods. (Github issue [#3959](https://github.com/cython/cython/issues/3959 "https://github.com/cython/cython/issues/3959"))

## 0.29.21 (2020-07-09)[¶](#id179 "Link to this heading")

### Bugs fixed[¶](#id181 "Link to this heading")

* Fix a regression in 0.29.20 where `__div__` failed to be found in extension types.
  (Github issue [#3688](https://github.com/cython/cython/issues/3688 "https://github.com/cython/cython/issues/3688"))
* Fix a regression in 0.29.20 where a call inside of a finally clause could fail to compile.
  Patch by David Woods. (Github issue [#3712](https://github.com/cython/cython/issues/3712 "https://github.com/cython/cython/issues/3712"))
* Zero-sized buffers could fail to validate as C/Fortran-contiguous.
  Patch by Clemens Hofreither. (Github issue [#2093](https://github.com/cython/cython/issues/2093 "https://github.com/cython/cython/issues/2093"))
* `exec()` did not allow recent Python syntax features in Py3.8+ due to
  [https://bugs.python.org/issue35975](https://bugs.python.org/issue35975 "https://bugs.python.org/issue35975").
  (Github issue [#3695](https://github.com/cython/cython/issues/3695 "https://github.com/cython/cython/issues/3695"))
* Binding staticmethods of Cython functions were not behaving like Python methods in Py3.
  Patch by Jeroen Demeyer and Michał Górny. (Github issue [#3106](https://github.com/cython/cython/issues/3106 "https://github.com/cython/cython/issues/3106"))
* Pythran calls to NumPy methods no longer generate useless method lookup code.
* The `PyUnicode_GET_LENGTH()` macro was missing from the `cpython.*` declarations.
  Patch by Thomas Caswell. (Github issue [#3692](https://github.com/cython/cython/issues/3692 "https://github.com/cython/cython/issues/3692"))
* The deprecated `PyUnicode_*()` C-API functions are no longer used, except for Unicode
  strings that contain lone surrogates. Unicode strings that contain non-BMP characters
  or surrogate pairs now generate different C code on 16-bit Python 2.x Unicode deployments
  (such as MS-Windows). Generating the C code on Python 3.x is recommended in this case.
  Original patches by Inada Naoki and Victor Stinner.
  (Github issues [#3677](https://github.com/cython/cython/issues/3677 "https://github.com/cython/cython/issues/3677"), [#3721](https://github.com/cython/cython/issues/3721 "https://github.com/cython/cython/issues/3721"), [#3697](https://github.com/cython/cython/issues/3697 "https://github.com/cython/cython/issues/3697"))
* Some template parameters were missing from the C++ `std::unordered_map` declaration.
  Patch by will. (Github issue [#3685](https://github.com/cython/cython/issues/3685 "https://github.com/cython/cython/issues/3685"))
* Several internal code generation issues regarding temporary variables were resolved.
  (Github issue [#3708](https://github.com/cython/cython/issues/3708 "https://github.com/cython/cython/issues/3708"))

## 0.29.20 (2020-06-10)[¶](#id182 "Link to this heading")

### Bugs fixed[¶](#id184 "Link to this heading")

* Nested try-except statements with multiple `return` statements could crash
  due to incorrect deletion of the `except as` target variable.
  (Github issue [#3666](https://github.com/cython/cython/issues/3666 "https://github.com/cython/cython/issues/3666"))
* The `@classmethod` decorator no longer rejects unknown input from other decorators.
  Patch by David Woods. (Github issue [#3660](https://github.com/cython/cython/issues/3660 "https://github.com/cython/cython/issues/3660"))
* Fused types could leak into unrelated usages.
  Patch by David Woods. (Github issue [#3642](https://github.com/cython/cython/issues/3642 "https://github.com/cython/cython/issues/3642"))
* Now uses `Py_SET_SIZE()` and `Py_SET_REFCNT()` in Py3.9+ to avoid low-level
  write access to these object fields.
  Patch by Victor Stinner. (Github issue [#3639](https://github.com/cython/cython/issues/3639 "https://github.com/cython/cython/issues/3639"))
* The built-in `abs()` function could lead to undefined behaviour when used on
  the negative-most value of a signed C integer type.
  Patch by Serge Guelton. (Github issue [#1911](https://github.com/cython/cython/issues/1911 "https://github.com/cython/cython/issues/1911"))
* Usages of `sizeof()` and `typeid()` on uninitialised variables no longer
  produce a warning.
  Patch by Celelibi. (Github issue [#3575](https://github.com/cython/cython/issues/3575 "https://github.com/cython/cython/issues/3575"))
* The C++ `typeid()` function was allowed in C mode.
  Patch by Celelibi. (Github issue [#3637](https://github.com/cython/cython/issues/3637 "https://github.com/cython/cython/issues/3637"))
* The error position reported for errors found in f-strings was misleading.
  (Github issue [#3674](https://github.com/cython/cython/issues/3674 "https://github.com/cython/cython/issues/3674"))
* The new `c_api_binop_methods` directive was added for forward compatibility, but can
  only be set to True (the current default value). It can be disabled in Cython 3.0.

## 0.29.19 (2020-05-20)[¶](#id185 "Link to this heading")

### Bugs fixed[¶](#id187 "Link to this heading")

* A typo in Windows specific code in 0.29.18 was fixed that broke “libc.math”.
  (Github issue [#3622](https://github.com/cython/cython/issues/3622 "https://github.com/cython/cython/issues/3622"))
* A platform specific test failure in 0.29.18 was fixed.
  Patch by smutch. (Github issue [#3620](https://github.com/cython/cython/issues/3620 "https://github.com/cython/cython/issues/3620"))

## 0.29.18 (2020-05-18)[¶](#id188 "Link to this heading")

### Bugs fixed[¶](#id190 "Link to this heading")

* Exception position reporting could run into race conditions on threaded code.
  It now uses function-local variables again.
* Error handling early in the module init code could lead to a crash.
* Error handling in `cython.array` creation was improved to avoid calling
  C-API functions with an error held.
* A memory corruption was fixed when garbage collection was triggered during calls
  to `PyType_Ready()` of extension type subclasses.
  (Github issue [#3603](https://github.com/cython/cython/issues/3603 "https://github.com/cython/cython/issues/3603"))
* Memory view slicing generated unused error handling code which could negatively
  impact the C compiler optimisations for parallel OpenMP code etc. Also, it is
  now helped by static branch hints.
  (Github issue [#2987](https://github.com/cython/cython/issues/2987 "https://github.com/cython/cython/issues/2987"))
* Cython’s built-in OpenMP functions were not translated inside of call arguments.
  Original patch by Celelibi and David Woods. (Github issue [#3594](https://github.com/cython/cython/issues/3594 "https://github.com/cython/cython/issues/3594"))
* Complex buffer item types of structs of arrays could fail to validate.
  Patch by Leo and smutch. (Github issue [#1407](https://github.com/cython/cython/issues/1407 "https://github.com/cython/cython/issues/1407"))
* Decorators were not allowed on nested async def functions.
  (Github issue [#1462](https://github.com/cython/cython/issues/1462 "https://github.com/cython/cython/issues/1462"))
* C-tuples could use invalid C struct casting.
  Patch by MegaIng. (Github issue [#3038](https://github.com/cython/cython/issues/3038 "https://github.com/cython/cython/issues/3038"))
* Optimised `%d` string formatting into f-strings failed on float values.
  (Github issue [#3092](https://github.com/cython/cython/issues/3092 "https://github.com/cython/cython/issues/3092"))
* Optimised aligned string formatting (`%05s`, `%-5s`) failed.
  (Github issue [#3476](https://github.com/cython/cython/issues/3476 "https://github.com/cython/cython/issues/3476"))
* When importing the old Cython `build_ext` integration with distutils, the
  additional command line arguments leaked into the regular command.
  Patch by Kamekameha. (Github issue [#2209](https://github.com/cython/cython/issues/2209 "https://github.com/cython/cython/issues/2209"))
* When using the `CYTHON_NO_PYINIT_EXPORT` option in C++, the module init function
  was not declared as `extern "C"`.
  (Github issue [#3414](https://github.com/cython/cython/issues/3414 "https://github.com/cython/cython/issues/3414"))
* Three missing timedelta access macros were added in `cpython.datetime`.
* The signature of the NumPy C-API function `PyArray_SearchSorted()` was fixed.
  Patch by Brock Mendel. (Github issue [#3606](https://github.com/cython/cython/issues/3606 "https://github.com/cython/cython/issues/3606"))

## 0.29.17 (2020-04-26)[¶](#id191 "Link to this heading")

### Features added[¶](#id193 "Link to this heading")

* `std::move()` is now available from `libcpp.utility`.
  Patch by Omer Ozarslan. (Github issue [#2169](https://github.com/cython/cython/issues/2169 "https://github.com/cython/cython/issues/2169"))
* The `@cython.binding` decorator is available in Python code.
  (Github issue [#3505](https://github.com/cython/cython/issues/3505 "https://github.com/cython/cython/issues/3505"))

### Bugs fixed[¶](#id194 "Link to this heading")

* Creating an empty unicode slice with large bounds could crash.
  Patch by Sam Sneddon. (Github issue [#3531](https://github.com/cython/cython/issues/3531 "https://github.com/cython/cython/issues/3531"))
* Decoding an empty bytes/char\* slice with large bounds could crash.
  Patch by Sam Sneddon. (Github issue [#3534](https://github.com/cython/cython/issues/3534 "https://github.com/cython/cython/issues/3534"))
* Re-importing a Cython extension no longer raises the error
  “`__reduce_cython__ not found`”.
  (Github issue [#3545](https://github.com/cython/cython/issues/3545 "https://github.com/cython/cython/issues/3545"))
* Unused C-tuples could generate incorrect code in 0.29.16.
  Patch by Kirk Meyer. (Github issue [#3543](https://github.com/cython/cython/issues/3543 "https://github.com/cython/cython/issues/3543"))
* Creating a fused function attached it to the garbage collector before it
  was fully initialised, thus risking crashes in rare failure cases.
  Original patch by achernomorov. (Github issue [#3215](https://github.com/cython/cython/issues/3215 "https://github.com/cython/cython/issues/3215"))
* Temporary buffer indexing variables were not released and could show up in
  C compiler warnings, e.g. in generators.
  Patch by David Woods. (Github issues [#3430](https://github.com/cython/cython/issues/3430 "https://github.com/cython/cython/issues/3430"), [#3522](https://github.com/cython/cython/issues/3522 "https://github.com/cython/cython/issues/3522"))
* The compilation cache in `cython.inline("…")` failed to take the language
  level into account.
  Patch by will-ca. (Github issue [#3419](https://github.com/cython/cython/issues/3419 "https://github.com/cython/cython/issues/3419"))
* The deprecated `PyUnicode_GET_SIZE()` function is no longer used in Py3.

## 0.29.16 (2020-03-24)[¶](#id195 "Link to this heading")

### Bugs fixed[¶](#id197 "Link to this heading")

* Temporary internal variables in nested prange loops could leak into other
  threads. Patch by Frank Schlimbach. (Github issue [#3348](https://github.com/cython/cython/issues/3348 "https://github.com/cython/cython/issues/3348"))
* Default arguments on fused functions could crash.
  Patch by David Woods. (Github issue [#3370](https://github.com/cython/cython/issues/3370 "https://github.com/cython/cython/issues/3370"))
* C-tuples declared in `.pxd` files could generate incomplete C code.
  Patch by Kirk Meyer. (Github issue [#1427](https://github.com/cython/cython/issues/1427 "https://github.com/cython/cython/issues/1427"))
* Fused functions were not always detected and optimised as Cython
  implemented functions.
  Patch by David Woods. (Github issue [#3384](https://github.com/cython/cython/issues/3384 "https://github.com/cython/cython/issues/3384"))
* Valid Python object concatenation of (iterable) strings to non-strings
  could fail with an exception.
  Patch by David Woods. (Github issue [#3433](https://github.com/cython/cython/issues/3433 "https://github.com/cython/cython/issues/3433"))
* Using C functions as temporary values lead to invalid C code.
  Original patch by David Woods. (Github issue [#3418](https://github.com/cython/cython/issues/3418 "https://github.com/cython/cython/issues/3418"))
* Fix an unhandled C++ exception in comparisons.
  Patch by David Woods. (Github issue [#3361](https://github.com/cython/cython/issues/3361 "https://github.com/cython/cython/issues/3361"))
* Fix deprecated import of “imp” module.
  Patch by Matti Picus. (Github issue [#3350](https://github.com/cython/cython/issues/3350 "https://github.com/cython/cython/issues/3350"))
* Fix compatibility with Pythran 0.9.6 and later.
  Patch by Serge Guelton. (Github issue [#3308](https://github.com/cython/cython/issues/3308 "https://github.com/cython/cython/issues/3308"))
* The `_Py_PyAtExit()` function in `cpython.pylifecycle` was misdeclared.
  Patch by Zackery Spytz. (Github issue [#3382](https://github.com/cython/cython/issues/3382 "https://github.com/cython/cython/issues/3382"))
* Several missing declarations in `cpython.*` were added.
  Patches by Zackery Spytz. (Github issue [#3452](https://github.com/cython/cython/issues/3452 "https://github.com/cython/cython/issues/3452"), [#3421](https://github.com/cython/cython/issues/3421 "https://github.com/cython/cython/issues/3421"), [#3411](https://github.com/cython/cython/issues/3411 "https://github.com/cython/cython/issues/3411"), [#3402](https://github.com/cython/cython/issues/3402 "https://github.com/cython/cython/issues/3402"))
* A declaration for `libc.math.fpclassify()` was added.
  Patch by Zackery Spytz. (Github issue [#2514](https://github.com/cython/cython/issues/2514 "https://github.com/cython/cython/issues/2514"))
* Avoid “undeclared” warning about automatically generated pickle methods.
  Patch by David Woods. (Github issue [#3353](https://github.com/cython/cython/issues/3353 "https://github.com/cython/cython/issues/3353"))
* Avoid C compiler warning about unreachable code in `prange()`.
* Some C compiler warnings in PyPy were resolved.
  Patch by Matti Picus. (Github issue [#3437](https://github.com/cython/cython/issues/3437 "https://github.com/cython/cython/issues/3437"))

## 0.29.15 (2020-02-06)[¶](#id198 "Link to this heading")

### Bugs fixed[¶](#id200 "Link to this heading")

* Crash when returning a temporary Python object from an async-def function.
  (Github issue [#3337](https://github.com/cython/cython/issues/3337 "https://github.com/cython/cython/issues/3337"))
* Crash when using `**kwargs` in generators.
  Patch by David Woods. (Github issue [#3265](https://github.com/cython/cython/issues/3265 "https://github.com/cython/cython/issues/3265"))
* Double reference free in `__class__` cell handling for `super()` calls.
  (Github issue [#3246](https://github.com/cython/cython/issues/3246 "https://github.com/cython/cython/issues/3246"))
* Compile error when using `*args` as Python class bases.
  (Github issue [#3338](https://github.com/cython/cython/issues/3338 "https://github.com/cython/cython/issues/3338"))
* Import failure in IPython 7.11.
  (Github issue [#3297](https://github.com/cython/cython/issues/3297 "https://github.com/cython/cython/issues/3297"))
* Fixed C name collision in the auto-pickle code.
  Patch by ThePrez. (Github issue [#3238](https://github.com/cython/cython/issues/3238 "https://github.com/cython/cython/issues/3238"))
* Deprecated import failed in Python 3.9.
  (Github issue [#3266](https://github.com/cython/cython/issues/3266 "https://github.com/cython/cython/issues/3266"))

## 0.29.14 (2019-11-01)[¶](#id201 "Link to this heading")

### Bugs fixed[¶](#id203 "Link to this heading")

* The generated code failed to initialise the `tp_print` slot in CPython 3.8.
  Patches by Pablo Galindo and Orivej Desh. (Github issues [#3171](https://github.com/cython/cython/issues/3171 "https://github.com/cython/cython/issues/3171"), [#3201](https://github.com/cython/cython/issues/3201 "https://github.com/cython/cython/issues/3201"))
* `?` for `bool` was missing from the supported NumPy dtypes.
  Patch by Max Klein. (Github issue [#2675](https://github.com/cython/cython/issues/2675 "https://github.com/cython/cython/issues/2675"))
* `await` was not allowed inside of f-strings.
  Patch by Dmitro Getz. (Github issue [#2877](https://github.com/cython/cython/issues/2877 "https://github.com/cython/cython/issues/2877"))
* Coverage analysis failed for projects where the code resides in separate
  source sub-directories.
  Patch by Antonio Valentino. (Github issue [#1985](https://github.com/cython/cython/issues/1985 "https://github.com/cython/cython/issues/1985"))
* An incorrect compiler warning was fixed in automatic C++ string conversions.
  Patch by Gerion Entrup. (Github issue [#3108](https://github.com/cython/cython/issues/3108 "https://github.com/cython/cython/issues/3108"))
* Error reports in the Jupyter notebook showed unhelpful stack traces.
  Patch by Matthew Edwards (Github issue [#3196](https://github.com/cython/cython/issues/3196 "https://github.com/cython/cython/issues/3196")).
* `Python.h` is now also included explicitly from `public` header files.
  (Github issue [#3133](https://github.com/cython/cython/issues/3133 "https://github.com/cython/cython/issues/3133")).
* Distutils builds with `--parallel` did not work when using Cython’s
  deprecated `build_ext` command.
  Patch by Alphadelta14 (Github issue [#3187](https://github.com/cython/cython/issues/3187 "https://github.com/cython/cython/issues/3187")).

### Other changes[¶](#id204 "Link to this heading")

* The `PyMemoryView_*()` C-API is available in `cpython.memoryview`.
  Patch by Nathan Manville. (Github issue [#2541](https://github.com/cython/cython/issues/2541 "https://github.com/cython/cython/issues/2541"))

## 0.29.13 (2019-07-26)[¶](#id205 "Link to this heading")

### Bugs fixed[¶](#id206 "Link to this heading")

* A reference leak for `None` was fixed when converting a memoryview
  to a Python object. (Github issue [#3023](https://github.com/cython/cython/issues/3023 "https://github.com/cython/cython/issues/3023"))
* The declaration of `PyGILState_STATE` in `cpython.pystate` was unusable.
  Patch by Kirill Smelkov. (Github issue [#2997](https://github.com/cython/cython/issues/2997 "https://github.com/cython/cython/issues/2997"))

### Other changes[¶](#id207 "Link to this heading")

* The declarations in `posix.mman` were extended.
  Patches by Kirill Smelkov. (Github issues [#2893](https://github.com/cython/cython/issues/2893 "https://github.com/cython/cython/issues/2893"), [#2894](https://github.com/cython/cython/issues/2894 "https://github.com/cython/cython/issues/2894"), [#3012](https://github.com/cython/cython/issues/3012 "https://github.com/cython/cython/issues/3012"))

## 0.29.12 (2019-07-07)[¶](#id208 "Link to this heading")

### Bugs fixed[¶](#id209 "Link to this heading")

* Fix compile error in CPython 3.8b2 regarding the `PyCode_New()` signature.
  (Github issue [#3031](https://github.com/cython/cython/issues/3031 "https://github.com/cython/cython/issues/3031"))
* Fix a C compiler warning about a missing `int` downcast.
  (Github issue [#3028](https://github.com/cython/cython/issues/3028 "https://github.com/cython/cython/issues/3028"))
* Fix reported error positions of undefined builtins and constants.
  Patch by Orivej Desh. (Github issue [#3030](https://github.com/cython/cython/issues/3030 "https://github.com/cython/cython/issues/3030"))
* A 32 bit issue in the Pythran support was resolved.
  Patch by Serge Guelton. (Github issue [#3032](https://github.com/cython/cython/issues/3032 "https://github.com/cython/cython/issues/3032"))

## 0.29.11 (2019-06-30)[¶](#id210 "Link to this heading")

### Bugs fixed[¶](#id211 "Link to this heading")

* Fix compile error in CPython 3.8b2 regarding the `PyCode_New()` signature.
  Patch by Nick Coghlan. (Github issue [#3009](https://github.com/cython/cython/issues/3009 "https://github.com/cython/cython/issues/3009"))
* Invalid C code generated for lambda functions in cdef methods.
  Patch by Josh Tobin. (Github issue [#2967](https://github.com/cython/cython/issues/2967 "https://github.com/cython/cython/issues/2967"))
* Support slice handling in newer Pythran versions.
  Patch by Serge Guelton. (Github issue [#2989](https://github.com/cython/cython/issues/2989 "https://github.com/cython/cython/issues/2989"))
* A reference leak in power-of-2 calculation was fixed.
  Patch by Sebastian Berg. (Github issue [#3022](https://github.com/cython/cython/issues/3022 "https://github.com/cython/cython/issues/3022"))
* The search order for include files was changed. Previously it was
  `include_directories`, `Cython/Includes`, `sys.path`. Now it is
  `include_directories`, `sys.path`, `Cython/Includes`. This was done to
  allow third-party `*.pxd` files to override the ones in Cython.
  Original patch by Matti Picus. (Github issue [#2905](https://github.com/cython/cython/issues/2905 "https://github.com/cython/cython/issues/2905"))
* Setting `language_level=2` in a file did not work if `language_level=3`
  was enabled globally before.
  Patch by Jeroen Demeyer. (Github issue [#2791](https://github.com/cython/cython/issues/2791 "https://github.com/cython/cython/issues/2791"))

## 0.29.10 (2019-06-02)[¶](#id212 "Link to this heading")

### Bugs fixed[¶](#id213 "Link to this heading")

* Fix compile errors in CPython 3.8b1 due to the new “tp\_vectorcall” slots.
  (Github issue [#2976](https://github.com/cython/cython/issues/2976 "https://github.com/cython/cython/issues/2976"))

## 0.29.9 (2019-05-29)[¶](#id214 "Link to this heading")

### Bugs fixed[¶](#id215 "Link to this heading")

* Fix a crash regression in 0.29.8 when creating code objects fails.
* Remove an incorrect cast when using true-division in C++ operations.
  (Github issue [#1950](https://github.com/cython/cython/issues/1950 "https://github.com/cython/cython/issues/1950"))

## 0.29.8 (2019-05-28)[¶](#id216 "Link to this heading")

### Bugs fixed[¶](#id217 "Link to this heading")

* C compile errors with CPython 3.8 were resolved.
  Patch by Marcel Plch. (Github issue [#2938](https://github.com/cython/cython/issues/2938 "https://github.com/cython/cython/issues/2938"))
* Python tuple constants that compare equal but have different item
  types could incorrectly be merged into a single constant.
  (Github issue [#2919](https://github.com/cython/cython/issues/2919 "https://github.com/cython/cython/issues/2919"))
* Non-ASCII characters in unprefixed strings could crash the compiler when
  used with language level `3str`.
* Starred expressions in %-formatting tuples could fail to compile for
  unicode strings. (Github issue [#2939](https://github.com/cython/cython/issues/2939 "https://github.com/cython/cython/issues/2939"))
* Passing Python class references through `cython.inline()` was broken.
  (Github issue [#2936](https://github.com/cython/cython/issues/2936 "https://github.com/cython/cython/issues/2936"))

## 0.29.7 (2019-04-14)[¶](#id218 "Link to this heading")

### Bugs fixed[¶](#id219 "Link to this heading")

* Crash when the shared Cython config module gets unloaded and another Cython
  module reports an exceptions. Cython now makes sure it keeps an owned reference
  to the module.
  (Github issue [#2885](https://github.com/cython/cython/issues/2885 "https://github.com/cython/cython/issues/2885"))
* Resolved a C89 compilation problem when enabling the fast-gil sharing feature.
* Coverage reporting did not include the signature line of `cdef` functions.
  (Github issue [#1461](https://github.com/cython/cython/issues/1461 "https://github.com/cython/cython/issues/1461"))
* Casting a GIL-requiring function into a nogil function now issues a warning.
  (Github issue [#2879](https://github.com/cython/cython/issues/2879 "https://github.com/cython/cython/issues/2879"))
* Generators and coroutines were missing their return type annotation.
  (Github issue [#2884](https://github.com/cython/cython/issues/2884 "https://github.com/cython/cython/issues/2884"))

## 0.29.6 (2019-02-27)[¶](#id220 "Link to this heading")

### Bugs fixed[¶](#id221 "Link to this heading")

* Fix a crash when accessing the `__kwdefaults__` special attribute of
  fused functions. (Github issue [#1470](https://github.com/cython/cython/issues/1470 "https://github.com/cython/cython/issues/1470"))
* Fix the parsing of buffer format strings that contain numeric sizes, which
  could lead to incorrect input rejections. (Github issue [#2845](https://github.com/cython/cython/issues/2845 "https://github.com/cython/cython/issues/2845"))
* Avoid a C #pragma in old gcc versions that was only added in GCC 4.6.
  Patch by Michael Anselmi. (Github issue [#2838](https://github.com/cython/cython/issues/2838 "https://github.com/cython/cython/issues/2838"))
* Auto-encoding of Unicode strings to UTF-8 C/C++ strings failed in Python 3,
  even though the default encoding there is UTF-8.
  (Github issue [#2819](https://github.com/cython/cython/issues/2819 "https://github.com/cython/cython/issues/2819"))

## 0.29.5 (2019-02-09)[¶](#id222 "Link to this heading")

### Bugs fixed[¶](#id223 "Link to this heading")

* Crash when defining a Python subclass of an extension type and repeatedly calling
  a cpdef method on it. (Github issue [#2823](https://github.com/cython/cython/issues/2823 "https://github.com/cython/cython/issues/2823"))
* Compiler crash when `prange()` loops appear inside of with-statements.
  (Github issue [#2780](https://github.com/cython/cython/issues/2780 "https://github.com/cython/cython/issues/2780"))
* Some C compiler warnings were resolved.
  Patches by Christoph Gohlke. (Github issues [#2815](https://github.com/cython/cython/issues/2815 "https://github.com/cython/cython/issues/2815"), [#2816](https://github.com/cython/cython/issues/2816 "https://github.com/cython/cython/issues/2816"), [#2817](https://github.com/cython/cython/issues/2817 "https://github.com/cython/cython/issues/2817"), [#2822](https://github.com/cython/cython/issues/2822 "https://github.com/cython/cython/issues/2822"))
* Python conversion of C++ enums failed in 0.29.
  Patch by Orivej Desh. (Github issue [#2767](https://github.com/cython/cython/issues/2767 "https://github.com/cython/cython/issues/2767"))

## 0.29.4 (2019-02-01)[¶](#id224 "Link to this heading")

### Bugs fixed[¶](#id225 "Link to this heading")

* Division of numeric constants by a runtime value of 0 could fail to raise a
  `ZeroDivisionError`. (Github issue [#2820](https://github.com/cython/cython/issues/2820 "https://github.com/cython/cython/issues/2820"))

## 0.29.3 (2019-01-19)[¶](#id226 "Link to this heading")

### Bugs fixed[¶](#id227 "Link to this heading")

* Some C code for memoryviews was generated in a non-deterministic order.
  Patch by Martijn van Steenbergen. (Github issue [#2779](https://github.com/cython/cython/issues/2779 "https://github.com/cython/cython/issues/2779"))
* C89 compatibility was accidentally lost since 0.28.
  Patches by gastineau and true-pasky. (Github issues [#2778](https://github.com/cython/cython/issues/2778 "https://github.com/cython/cython/issues/2778"), [#2801](https://github.com/cython/cython/issues/2801 "https://github.com/cython/cython/issues/2801"))
* A C compiler cast warning was resolved.
  Patch by Michael Buesch. (Github issue [#2774](https://github.com/cython/cython/issues/2774 "https://github.com/cython/cython/issues/2774"))
* An compilation failure with complex numbers under MSVC++ was resolved.
  (Github issue [#2797](https://github.com/cython/cython/issues/2797 "https://github.com/cython/cython/issues/2797"))
* Coverage reporting could fail when modules were moved around after the build.
  Patch by Wenjun Si. (Github issue [#2776](https://github.com/cython/cython/issues/2776 "https://github.com/cython/cython/issues/2776"))

## 0.29.2 (2018-12-14)[¶](#id228 "Link to this heading")

### Bugs fixed[¶](#id229 "Link to this heading")

* The code generated for deduplicated constants leaked some references.
  (Github issue [#2750](https://github.com/cython/cython/issues/2750 "https://github.com/cython/cython/issues/2750"))
* The declaration of `sigismember()` in `libc.signal` was corrected.
  (Github issue [#2756](https://github.com/cython/cython/issues/2756 "https://github.com/cython/cython/issues/2756"))
* Crashes in compiler and test runner were fixed.
  (Github issue [#2736](https://github.com/cython/cython/issues/2736 "https://github.com/cython/cython/issues/2736"), [#2755](https://github.com/cython/cython/issues/2755 "https://github.com/cython/cython/issues/2755"))
* A C compiler warning about an invalid safety check was resolved.
  (Github issue [#2731](https://github.com/cython/cython/issues/2731 "https://github.com/cython/cython/issues/2731"))

## 0.29.1 (2018-11-24)[¶](#id230 "Link to this heading")

### Bugs fixed[¶](#id231 "Link to this heading")

* Extensions compiled with MinGW-64 under Windows could misinterpret integer
  objects larger than 15 bit and return incorrect results.
  (Github issue [#2670](https://github.com/cython/cython/issues/2670 "https://github.com/cython/cython/issues/2670"))
* Cython no longer requires the source to be writable when copying its data
  into a memory view slice.
  Patch by Andrey Paramonov. (Github issue [#2644](https://github.com/cython/cython/issues/2644 "https://github.com/cython/cython/issues/2644"))
* Line tracing of `try`-statements generated invalid C code.
  (Github issue [#2274](https://github.com/cython/cython/issues/2274 "https://github.com/cython/cython/issues/2274"))
* When using the `warn.undeclared` directive, Cython’s own code generated
  warnings that are now fixed.
  Patch by Nicolas Pauss. (Github issue [#2685](https://github.com/cython/cython/issues/2685 "https://github.com/cython/cython/issues/2685"))
* Cython’s memoryviews no longer require strides for setting the shape field
  but only the `PyBUF_ND` flag to be set.
  Patch by John Kirkham. (Github issue [#2716](https://github.com/cython/cython/issues/2716 "https://github.com/cython/cython/issues/2716"))
* Some C compiler warnings about unused memoryview code were fixed.
  Patch by Ho Cheuk Ting. (Github issue [#2588](https://github.com/cython/cython/issues/2588 "https://github.com/cython/cython/issues/2588"))
* A C compiler warning about implicit signed/unsigned conversion was fixed.
  (Github issue [#2729](https://github.com/cython/cython/issues/2729 "https://github.com/cython/cython/issues/2729"))
* Assignments to C++ references returned by `operator[]` could fail to compile.
  (Github issue [#2671](https://github.com/cython/cython/issues/2671 "https://github.com/cython/cython/issues/2671"))
* The power operator and the support for NumPy math functions were fixed
  in Pythran expressions.
  Patch by Serge Guelton. (Github issues [#2702](https://github.com/cython/cython/issues/2702 "https://github.com/cython/cython/issues/2702"), [#2709](https://github.com/cython/cython/issues/2709 "https://github.com/cython/cython/issues/2709"))
* Signatures with memory view arguments now show the expected type
  when embedded in docstrings.
  Patch by Matthew Chan and Benjamin Weigel. (Github issue [#2634](https://github.com/cython/cython/issues/2634 "https://github.com/cython/cython/issues/2634"))
* Some `from ... cimport ...` constructs were not correctly considered
  when searching modified dependencies in `cythonize()` to decide
  whether to recompile a module.
  Patch by Kryštof Pilnáček. (Github issue [#2638](https://github.com/cython/cython/issues/2638 "https://github.com/cython/cython/issues/2638"))
* A struct field type in the `cpython.array` declarations was corrected.
  Patch by John Kirkham. (Github issue [#2712](https://github.com/cython/cython/issues/2712 "https://github.com/cython/cython/issues/2712"))

## 0.29 (2018-10-14)[¶](#id232 "Link to this heading")

### Features added[¶](#id233 "Link to this heading")

* PEP-489 multi-phase module initialisation has been enabled again. Module
  reloads in other subinterpreters raise an exception to prevent corruption
  of the static module state.
* A set of `mypy` compatible PEP-484 declarations were added for Cython’s C data
  types to integrate with static analysers in typed Python code. They are available
  in the `Cython/Shadow.pyi` module and describe the types in the special `cython`
  module that can be used for typing in Python code.
  Original patch by Julian Gethmann. (Github issue [#1965](https://github.com/cython/cython/issues/1965 "https://github.com/cython/cython/issues/1965"))
* Memoryviews are supported in PEP-484/526 style type declarations.
  (Github issue [#2529](https://github.com/cython/cython/issues/2529 "https://github.com/cython/cython/issues/2529"))
* `@cython.nogil` is supported as a C-function decorator in Python code.
  (Github issue [#2557](https://github.com/cython/cython/issues/2557 "https://github.com/cython/cython/issues/2557"))
* Raising exceptions from nogil code will automatically acquire the GIL, instead
  of requiring an explicit `with gil` block.
* C++ functions can now be declared as potentially raising both C++ and Python
  exceptions, so that Cython can handle both correctly.
  (Github issue [#2615](https://github.com/cython/cython/issues/2615 "https://github.com/cython/cython/issues/2615"))
* `cython.inline()` supports a direct `language_level` keyword argument that
  was previously only available via a directive.
* A new language level name `3str` was added that mostly corresponds to language
  level 3, but keeps unprefixed string literals as type ‘str’ in both Py2 and Py3,
  and the builtin ‘str’ type unchanged. This will become the default in the next
  Cython release and is meant to help user code a) transition more easily to this
  new default and b) migrate to Python 3 source code semantics without making support
  for Python 2.x difficult.
* In CPython 3.6 and later, looking up globals in the module dict is almost
  as fast as looking up C globals.
  (Github issue [#2313](https://github.com/cython/cython/issues/2313 "https://github.com/cython/cython/issues/2313"))
* For a Python subclass of an extension type, repeated method calls to non-overridden
  cpdef methods can avoid the attribute lookup in Py3.6+, which makes them 4x faster.
  (Github issue [#2313](https://github.com/cython/cython/issues/2313 "https://github.com/cython/cython/issues/2313"))
* (In-)equality comparisons of objects to integer literals are faster.
  (Github issue [#2188](https://github.com/cython/cython/issues/2188 "https://github.com/cython/cython/issues/2188"))
* Some internal and 1-argument method calls are faster.
* Modules that cimport many external extension types from other Cython modules
  execute less import requests during module initialisation.
* Constant tuples and slices are deduplicated and only created once per module.
  (Github issue [#2292](https://github.com/cython/cython/issues/2292 "https://github.com/cython/cython/issues/2292"))
* The coverage plugin considers more C file extensions such as `.cc` and `.cxx`.
  (Github issue [#2266](https://github.com/cython/cython/issues/2266 "https://github.com/cython/cython/issues/2266"))
* The `cythonize` command accepts compile time variable values (as set by `DEF`)
  through the new `-E` option.
  Patch by Jerome Kieffer. (Github issue [#2315](https://github.com/cython/cython/issues/2315 "https://github.com/cython/cython/issues/2315"))
* `pyximport` can import from namespace packages.
  Patch by Prakhar Goel. (Github issue [#2294](https://github.com/cython/cython/issues/2294 "https://github.com/cython/cython/issues/2294"))
* Some missing numpy and CPython C-API declarations were added.
  Patch by John Kirkham. (Github issues [#2523](https://github.com/cython/cython/issues/2523 "https://github.com/cython/cython/issues/2523"), [#2520](https://github.com/cython/cython/issues/2520 "https://github.com/cython/cython/issues/2520"), [#2537](https://github.com/cython/cython/issues/2537 "https://github.com/cython/cython/issues/2537"))
* Declarations for the `pylifecycle` C-API functions were added in a new .pxd file
  `cpython.pylifecycle`.
* The Pythran support was updated to work with the latest Pythran 0.8.7.
  Original patch by Adrien Guinet. (Github issue [#2600](https://github.com/cython/cython/issues/2600 "https://github.com/cython/cython/issues/2600"))
* `%a` is included in the string formatting types that are optimised into f-strings.
  In this case, it is also automatically mapped to `%r` in Python 2.x.
* New C macro `CYTHON_HEX_VERSION` to access Cython’s version in the same style as
  `PY_VERSION_HEX`.
* Constants in `libc.math` are now declared as `const` to simplify their handling.
* An additional `check_size` clause was added to the `ctypedef class` name
  specification to allow suppressing warnings when importing modules with
  backwards-compatible `PyTypeObject` size changes.
  Patch by Matti Picus. (Github issue [#2627](https://github.com/cython/cython/issues/2627 "https://github.com/cython/cython/issues/2627"))

### Bugs fixed[¶](#id234 "Link to this heading")

* The exception handling in generators and coroutines under CPython 3.7 was adapted
  to the newly introduced exception stack. Users of Cython 0.28 who want to support
  Python 3.7 are encouraged to upgrade to 0.29 to avoid potentially incorrect error
  reporting and tracebacks. (Github issue [#1958](https://github.com/cython/cython/issues/1958 "https://github.com/cython/cython/issues/1958"))
* Crash when importing a module under Stackless Python that was built for CPython.
  Patch by Anselm Kruis. (Github issue [#2534](https://github.com/cython/cython/issues/2534 "https://github.com/cython/cython/issues/2534"))
* 2-value slicing of typed sequences failed if the start or stop index was None.
  Patch by Christian Gibson. (Github issue [#2508](https://github.com/cython/cython/issues/2508 "https://github.com/cython/cython/issues/2508"))
* Multiplied string literals lost their factor when they are part of another
  constant expression (e.g. ‘x’ \* 10 + ‘y’ => ‘xy’).
* String formatting with the ‘%’ operator didn’t call the special `__rmod__()`
  method if the right side is a string subclass that implements it.
  (Python issue 28598)
* The directive `language_level=3` did not apply to the first token in the
  source file. (Github issue [#2230](https://github.com/cython/cython/issues/2230 "https://github.com/cython/cython/issues/2230"))
* Overriding cpdef methods did not work in Python subclasses with slots.
  Note that this can have a performance impact on calls from Cython code.
  (Github issue [#1771](https://github.com/cython/cython/issues/1771 "https://github.com/cython/cython/issues/1771"))
* Fix declarations of builtin or C types using strings in pure python mode.
  (Github issue [#2046](https://github.com/cython/cython/issues/2046 "https://github.com/cython/cython/issues/2046"))
* Generator expressions and lambdas failed to compile in `@cfunc` functions.
  (Github issue [#459](https://github.com/cython/cython/issues/459 "https://github.com/cython/cython/issues/459"))
* Global names with `const` types were not excluded from star-import assignments
  which could lead to invalid C code.
  (Github issue [#2621](https://github.com/cython/cython/issues/2621 "https://github.com/cython/cython/issues/2621"))
* Several internal function signatures were fixed that lead to warnings in gcc-8.
  (Github issue [#2363](https://github.com/cython/cython/issues/2363 "https://github.com/cython/cython/issues/2363"))
* The numpy helper functions `set_array_base()` and `get_array_base()`
  were adapted to the current numpy C-API recommendations.
  Patch by Matti Picus. (Github issue [#2528](https://github.com/cython/cython/issues/2528 "https://github.com/cython/cython/issues/2528"))
* Some NumPy related code was updated to avoid deprecated API usage.
  Original patch by jbrockmendel. (Github issue [#2559](https://github.com/cython/cython/issues/2559 "https://github.com/cython/cython/issues/2559"))
* Several C++ STL declarations were extended and corrected.
  Patch by Valentin Valls. (Github issue [#2207](https://github.com/cython/cython/issues/2207 "https://github.com/cython/cython/issues/2207"))
* C lines of the module init function were unconditionally not reported in
  exception stack traces.
  Patch by Jeroen Demeyer. (Github issue [#2492](https://github.com/cython/cython/issues/2492 "https://github.com/cython/cython/issues/2492"))
* When PEP-489 support is enabled, reloading the module overwrote any static
  module state. It now raises an exception instead, given that reloading is
  not actually supported.
* Object-returning, C++ exception throwing functions were not checking that
  the return value was non-null.
  Original patch by Matt Wozniski (Github issue [#2603](https://github.com/cython/cython/issues/2603 "https://github.com/cython/cython/issues/2603"))
* The source file encoding detection could get confused if the
  `c_string_encoding` directive appeared within the first two lines.
  (Github issue [#2632](https://github.com/cython/cython/issues/2632 "https://github.com/cython/cython/issues/2632"))
* Cython generated modules no longer emit a warning during import when the
  size of the NumPy array type is larger than what was found at compile time.
  Instead, this is assumed to be a backwards compatible change on NumPy side.

### Other changes[¶](#id235 "Link to this heading")

* Cython now emits a warning when no `language_level` (2, 3 or ‘3str’) is set
  explicitly, neither as a `cythonize()` option nor as a compiler directive.
  This is meant to prepare the transition of the default language level from
  currently Py2 to Py3, since that is what most new users will expect these days.
  The future default will, however, not enforce unicode literals, because this
  has proven a major obstacle in the support for both Python 2.x and 3.x. The
  next major release is intended to make this change, so that it will parse all
  code that does not request a specific language level as Python 3 code, but with
  `str` literals. The language level 2 will continue to be supported for an
  indefinite time.
* The documentation was restructured, cleaned up and examples are now tested.
  The NumPy tutorial was also rewritten to simplify the running example.
  Contributed by Gabriel de Marmiesse. (Github issue [#2245](https://github.com/cython/cython/issues/2245 "https://github.com/cython/cython/issues/2245"))
* Cython compiles less of its own modules at build time to reduce the installed
  package size to about half of its previous size. This makes the compiler
  slightly slower, by about 5-7%.

## 0.28.6 (2018-11-01)[¶](#id236 "Link to this heading")

### Bugs fixed[¶](#id237 "Link to this heading")

* Extensions compiled with MinGW-64 under Windows could misinterpret integer
  objects larger than 15 bit and return incorrect results.
  (Github issue [#2670](https://github.com/cython/cython/issues/2670 "https://github.com/cython/cython/issues/2670"))
* Multiplied string literals lost their factor when they are part of another
  constant expression (e.g. ‘x’ \* 10 + ‘y’ => ‘xy’).

## 0.28.5 (2018-08-03)[¶](#id238 "Link to this heading")

### Bugs fixed[¶](#id239 "Link to this heading")

* The discouraged usage of GCC’s attribute `optimize("Os")` was replaced by the
  similar attribute `cold` to reduce the code impact of the module init functions.
  (Github issue [#2494](https://github.com/cython/cython/issues/2494 "https://github.com/cython/cython/issues/2494"))
* A reference leak in Py2.x was fixed when comparing str to unicode for equality.

## 0.28.4 (2018-07-08)[¶](#id240 "Link to this heading")

### Bugs fixed[¶](#id241 "Link to this heading")

* Reallowing `tp_clear()` in a subtype of an `@no_gc_clear` extension type
  generated an invalid C function call to the (non-existent) base type implementation.
  (Github issue [#2309](https://github.com/cython/cython/issues/2309 "https://github.com/cython/cython/issues/2309"))
* Exception catching based on a non-literal (runtime) tuple could fail to match the
  exception. (Github issue [#2425](https://github.com/cython/cython/issues/2425 "https://github.com/cython/cython/issues/2425"))
* Compile fix for CPython 3.7.0a2. (Github issue [#2477](https://github.com/cython/cython/issues/2477 "https://github.com/cython/cython/issues/2477"))

## 0.28.3 (2018-05-27)[¶](#id242 "Link to this heading")

### Bugs fixed[¶](#id243 "Link to this heading")

* Set iteration was broken in non-CPython since 0.28.
* `UnicodeEncodeError` in Py2 when `%s` formatting is optimised for
  unicode strings. (Github issue [#2276](https://github.com/cython/cython/issues/2276 "https://github.com/cython/cython/issues/2276"))
* Work around a crash bug in g++ 4.4.x by disabling the size reduction setting
  of the module init function in this version. (Github issue [#2235](https://github.com/cython/cython/issues/2235 "https://github.com/cython/cython/issues/2235"))
* Crash when exceptions occur early during module initialisation.
  (Github issue [#2199](https://github.com/cython/cython/issues/2199 "https://github.com/cython/cython/issues/2199"))

## 0.28.2 (2018-04-13)[¶](#id244 "Link to this heading")

### Features added[¶](#id245 "Link to this heading")

* `abs()` is faster for Python long objects.
* The C++11 methods `front()` and `end()` were added to the declaration of
  `libcpp.string`. Patch by Alex Huszagh. (Github issue [#2123](https://github.com/cython/cython/issues/2123 "https://github.com/cython/cython/issues/2123"))
* The C++11 methods `reserve()` and `bucket_count()` are declared for
  `libcpp.unordered_map`. Patch by Valentin Valls. (Github issue [#2168](https://github.com/cython/cython/issues/2168 "https://github.com/cython/cython/issues/2168"))

### Bugs fixed[¶](#id246 "Link to this heading")

* The copy of a read-only memoryview was considered read-only as well, whereas
  a common reason to copy a read-only view is to make it writable. The result
  of the copying is now a writable buffer by default.
  (Github issue [#2134](https://github.com/cython/cython/issues/2134 "https://github.com/cython/cython/issues/2134"))
* The `switch` statement generation failed to apply recursively to the body of
  converted if-statements.
* `NULL` was sometimes rejected as exception return value when the returned
  type is a fused pointer type.
  Patch by Callie LeFave. (Github issue [#2177](https://github.com/cython/cython/issues/2177 "https://github.com/cython/cython/issues/2177"))
* Fixed compatibility with PyPy 5.11.
  Patch by Matti Picus. (Github issue [#2165](https://github.com/cython/cython/issues/2165 "https://github.com/cython/cython/issues/2165"))

### Other changes[¶](#id247 "Link to this heading")

* The NumPy tutorial was rewritten to use memoryviews instead of the older
  buffer declaration syntax.
  Contributed by Gabriel de Marmiesse. (Github issue [#2162](https://github.com/cython/cython/issues/2162 "https://github.com/cython/cython/issues/2162"))

## 0.28.1 (2018-03-18)[¶](#id248 "Link to this heading")

### Bugs fixed[¶](#id249 "Link to this heading")

* `PyFrozenSet_New()` was accidentally used in PyPy where it is missing
  from the C-API.
* Assignment between some C++ templated types were incorrectly rejected
  when the templates mix `const` with `ctypedef`.
  (Github issue [#2148](https://github.com/cython/cython/issues/2148 "https://github.com/cython/cython/issues/2148"))
* Undeclared C++ no-args constructors in subclasses could make the compilation
  fail if the base class constructor was declared without `nogil`.
  (Github issue [#2157](https://github.com/cython/cython/issues/2157 "https://github.com/cython/cython/issues/2157"))
* Bytes %-formatting inferred `basestring` (bytes or unicode) as result type
  in some cases where `bytes` would have been safe to infer.
  (Github issue [#2153](https://github.com/cython/cython/issues/2153 "https://github.com/cython/cython/issues/2153"))
* `None` was accidentally disallowed as typed return value of `dict.pop()`.
  (Github issue [#2152](https://github.com/cython/cython/issues/2152 "https://github.com/cython/cython/issues/2152"))

## 0.28 (2018-03-13)[¶](#id250 "Link to this heading")

### Features added[¶](#id251 "Link to this heading")

* Cdef classes can now multiply inherit from ordinary Python classes.
  (The primary base must still be a c class, possibly `object`, and
  the other bases must not be cdef classes.)
* Type inference is now supported for Pythran compiled NumPy expressions.
  Patch by Nils Braun. (Github issue [#1954](https://github.com/cython/cython/issues/1954 "https://github.com/cython/cython/issues/1954"))
* The `const` modifier can be applied to memoryview declarations to allow
  read-only buffers as input. (Github issues [#1605](https://github.com/cython/cython/issues/1605 "https://github.com/cython/cython/issues/1605"), [#1869](https://github.com/cython/cython/issues/1869 "https://github.com/cython/cython/issues/1869"))
* C code in the docstring of a `cdef extern` block is copied verbatimly
  into the generated file.
  Patch by Jeroen Demeyer. (Github issue [#1915](https://github.com/cython/cython/issues/1915 "https://github.com/cython/cython/issues/1915"))
* When compiling with gcc, the module init function is now tuned for small
  code size instead of whatever compile flags were provided externally.
  Cython now also disables some code intensive optimisations in that function
  to further reduce the code size. (Github issue [#2102](https://github.com/cython/cython/issues/2102 "https://github.com/cython/cython/issues/2102"))
* Decorating an async coroutine with `@cython.iterable_coroutine` changes its
  type at compile time to make it iterable. While this is not strictly in line
  with PEP-492, it improves the interoperability with old-style coroutines that
  use `yield from` instead of `await`.
* The IPython magic has preliminary support for JupyterLab.
  (Github issue [#1775](https://github.com/cython/cython/issues/1775 "https://github.com/cython/cython/issues/1775"))
* The new TSS C-API in CPython 3.7 is supported and has been backported.
  Patch by Naotoshi Seo. (Github issue [#1932](https://github.com/cython/cython/issues/1932 "https://github.com/cython/cython/issues/1932"))
* Cython knows the new `Py_tss_t` type defined in PEP-539 and automatically
  initialises variables declared with that type to `Py_tss_NEEDS_INIT`,
  a value which cannot be used outside of static assignments.
* The set methods `.remove()` and `.discard()` are optimised.
  Patch by Antoine Pitrou. (Github issue [#2042](https://github.com/cython/cython/issues/2042 "https://github.com/cython/cython/issues/2042"))
* `dict.pop()` is optimised.
  Original patch by Antoine Pitrou. (Github issue [#2047](https://github.com/cython/cython/issues/2047 "https://github.com/cython/cython/issues/2047"))
* Iteration over sets and frozensets is optimised.
  (Github issue [#2048](https://github.com/cython/cython/issues/2048 "https://github.com/cython/cython/issues/2048"))
* Safe integer loops (< range(2^30)) are automatically optimised into C loops.
* `alist.extend([a,b,c])` is optimised into sequential `list.append()` calls
  for short literal sequences.
* Calls to builtin methods that are not specifically optimised into C-API calls
  now use a cache that avoids repeated lookups of the underlying C function.
  (Github issue [#2054](https://github.com/cython/cython/issues/2054 "https://github.com/cython/cython/issues/2054"))
* Single argument function calls can avoid the argument tuple creation in some cases.
* Some redundant extension type checks are avoided.
* Formatting C enum values in f-strings is faster, as well as some other special cases.
* String formatting with the ‘%’ operator is optimised into f-strings in simple cases.
* Subscripting (item access) is faster in some cases.
* Some `bytearray` operations have been optimised similar to `bytes`.
* Some PEP-484/526 container type declarations are now considered for
  loop optimisations.
* Indexing into memoryview slices with `view[i][j]` is now optimised into
  `view[i, j]`.
* Python compatible `cython.*` types can now be mixed with type declarations
  in Cython syntax.
* Name lookups in the module and in classes are faster.
* Python attribute lookups on extension types without instance dict are faster.
* Some missing signals were added to `libc/signal.pxd`.
  Patch by Jeroen Demeyer. (Github issue [#1914](https://github.com/cython/cython/issues/1914 "https://github.com/cython/cython/issues/1914"))
* The warning about repeated extern declarations is now visible by default.
  (Github issue [#1874](https://github.com/cython/cython/issues/1874 "https://github.com/cython/cython/issues/1874"))
* The exception handling of the function types used by CPython’s type slot
  functions was corrected to match the de-facto standard behaviour, so that
  code that uses them directly benefits from automatic and correct exception
  propagation. Patch by Jeroen Demeyer. (Github issue [#1980](https://github.com/cython/cython/issues/1980 "https://github.com/cython/cython/issues/1980"))
* Defining the macro `CYTHON_NO_PYINIT_EXPORT` will prevent the module init
  function from being exported as symbol, e.g. when linking modules statically
  in an embedding setup. Patch by AraHaan. (Github issue [#1944](https://github.com/cython/cython/issues/1944 "https://github.com/cython/cython/issues/1944"))

### Bugs fixed[¶](#id252 "Link to this heading")

* If a module name is explicitly provided for an `Extension()` that is compiled
  via `cythonize()`, it was previously ignored and replaced by the source file
  name. It can now be used to override the target module name, e.g. for compiling
  prefixed accelerator modules from Python files. (Github issue [#2038](https://github.com/cython/cython/issues/2038 "https://github.com/cython/cython/issues/2038"))
* The arguments of the `num_threads` parameter of parallel sections
  were not sufficiently validated and could lead to invalid C code.
  (Github issue [#1957](https://github.com/cython/cython/issues/1957 "https://github.com/cython/cython/issues/1957"))
* Catching exceptions with a non-trivial exception pattern could call into
  CPython with a live exception set. This triggered incorrect behaviour
  and crashes, especially in CPython 3.7.
* The signature of the special `__richcmp__()` method was corrected to recognise
  the type of the first argument as `self`. It was previously treated as plain
  object, but CPython actually guarantees that it always has the correct type.
  Note: this can change the semantics of user code that previously relied on
  `self` being untyped.
* Some Python 3 exceptions were not recognised as builtins when running Cython
  under Python 2.
* Some async helper functions were not defined in the generated C code when
  compiling simple async code. (Github issue [#2075](https://github.com/cython/cython/issues/2075 "https://github.com/cython/cython/issues/2075"))
* Line tracing did not include generators and coroutines.
  (Github issue [#1949](https://github.com/cython/cython/issues/1949 "https://github.com/cython/cython/issues/1949"))
* C++ declarations for `unordered_map` were corrected.
  Patch by Michael Schatzow. (Github issue [#1484](https://github.com/cython/cython/issues/1484 "https://github.com/cython/cython/issues/1484"))
* Iterator declarations in C++ `deque` and `vector` were corrected.
  Patch by Alex Huszagh. (Github issue [#1870](https://github.com/cython/cython/issues/1870 "https://github.com/cython/cython/issues/1870"))
* The const modifiers in the C++ `string` declarations were corrected, together
  with the coercion behaviour of string literals into C++ strings.
  (Github issue [#2132](https://github.com/cython/cython/issues/2132 "https://github.com/cython/cython/issues/2132"))
* Some declaration types in `libc.limits` were corrected.
  Patch by Jeroen Demeyer. (Github issue [#2016](https://github.com/cython/cython/issues/2016 "https://github.com/cython/cython/issues/2016"))
* `@cython.final` was not accepted on Python classes with an `@cython.cclass`
  decorator. (Github issue [#2040](https://github.com/cython/cython/issues/2040 "https://github.com/cython/cython/issues/2040"))
* Cython no longer creates useless and incorrect `PyInstanceMethod` wrappers for
  methods in Python 3. Patch by Jeroen Demeyer. (Github issue [#2105](https://github.com/cython/cython/issues/2105 "https://github.com/cython/cython/issues/2105"))
* The builtin `bytearray` type could not be used as base type of cdef classes.
  (Github issue [#2106](https://github.com/cython/cython/issues/2106 "https://github.com/cython/cython/issues/2106"))

### Other changes[¶](#id253 "Link to this heading")

## 0.27.3 (2017-11-03)[¶](#id254 "Link to this heading")

### Bugs fixed[¶](#id255 "Link to this heading")

* String forward references to extension types like `@cython.locals(x="ExtType")`
  failed to find the named type. (Github issue [#1962](https://github.com/cython/cython/issues/1962 "https://github.com/cython/cython/issues/1962"))
* NumPy slicing generated incorrect results when compiled with Pythran.
  Original patch by Serge Guelton (Github issue [#1946](https://github.com/cython/cython/issues/1946 "https://github.com/cython/cython/issues/1946")).
* Fix “undefined reference” linker error for generators on Windows in Py3.3-3.5.
  (Github issue [#1968](https://github.com/cython/cython/issues/1968 "https://github.com/cython/cython/issues/1968"))
* Adapt to recent C-API change of `PyThreadState` in CPython 3.7.
* Fix signature of `PyWeakref_GetObject()` API declaration.
  Patch by Jeroen Demeyer (Github issue [#1975](https://github.com/cython/cython/issues/1975 "https://github.com/cython/cython/issues/1975")).

## 0.27.2 (2017-10-22)[¶](#id256 "Link to this heading")

### Bugs fixed[¶](#id257 "Link to this heading")

* Comprehensions could incorrectly be optimised away when they appeared in boolean
  test contexts. (Github issue [#1920](https://github.com/cython/cython/issues/1920 "https://github.com/cython/cython/issues/1920"))
* The special methods `__eq__`, `__lt__` etc. in extension types did not type
  their first argument as the type of the class but `object`. (Github issue [#1935](https://github.com/cython/cython/issues/1935 "https://github.com/cython/cython/issues/1935"))
* Crash on first lookup of “cline\_in\_traceback” option during exception handling.
  (Github issue [#1907](https://github.com/cython/cython/issues/1907 "https://github.com/cython/cython/issues/1907"))
* Some nested module level comprehensions failed to compile.
  (Github issue [#1906](https://github.com/cython/cython/issues/1906 "https://github.com/cython/cython/issues/1906"))
* Compiler crash on some complex type declarations in pure mode.
  (Github issue [#1908](https://github.com/cython/cython/issues/1908 "https://github.com/cython/cython/issues/1908"))
* `std::unordered_map.erase()` was declared with an incorrect `void` return
  type in `libcpp.unordered_map`. (Github issue [#1484](https://github.com/cython/cython/issues/1484 "https://github.com/cython/cython/issues/1484"))
* Invalid use of C++ `fallthrough` attribute before C++11 and similar issue in clang.
  (Github issue [#1930](https://github.com/cython/cython/issues/1930 "https://github.com/cython/cython/issues/1930"))
* Compiler crash on misnamed properties. (Github issue [#1905](https://github.com/cython/cython/issues/1905 "https://github.com/cython/cython/issues/1905"))

## 0.27.1 (2017-10-01)[¶](#id258 "Link to this heading")

### Features added[¶](#id259 "Link to this heading")

* The Jupyter magic has a new debug option `--verbose` that shows details about
  the distutils invocation. Patch by Boris Filippov (Github issue [#1881](https://github.com/cython/cython/issues/1881 "https://github.com/cython/cython/issues/1881")).

### Bugs fixed[¶](#id260 "Link to this heading")

* Py3 list comprehensions in class bodies resulted in invalid C code.
  (Github issue [#1889](https://github.com/cython/cython/issues/1889 "https://github.com/cython/cython/issues/1889"))
* Modules built for later CPython 3.5.x versions failed to import in 3.5.0/3.5.1.
  (Github issue [#1880](https://github.com/cython/cython/issues/1880 "https://github.com/cython/cython/issues/1880"))
* Deallocating fused types functions and methods kept their GC tracking enabled,
  which could potentially lead to recursive deallocation attempts.
* Crash when compiling in C++ mode with old setuptools versions.
  (Github issue [#1879](https://github.com/cython/cython/issues/1879 "https://github.com/cython/cython/issues/1879"))
* C++ object arguments for the constructor of Cython implemented C++ are now
  passed by reference and not by value to allow for non-copyable arguments, such
  as `unique_ptr`.
* API-exported C++ classes with Python object members failed to compile.
  (Github issue [#1866](https://github.com/cython/cython/issues/1866 "https://github.com/cython/cython/issues/1866"))
* Some issues with the new relaxed exception value handling were resolved.
* Python classes as annotation types could prevent compilation.
  (Github issue [#1887](https://github.com/cython/cython/issues/1887 "https://github.com/cython/cython/issues/1887"))
* Cython annotation types in Python files could lead to import failures
  with a “cython undefined” error. Recognised types are now turned into strings.
* Coverage analysis could fail to report on extension modules on some platforms.
* Annotations could be parsed (and rejected) as types even with
  `annotation_typing=False`.

### Other changes[¶](#id261 "Link to this heading")

* PEP 489 support has been disabled by default to counter incompatibilities with
  import setups that try to reload or reinitialise modules.

## 0.27 (2017-09-23)[¶](#id262 "Link to this heading")

### Features added[¶](#id263 "Link to this heading")

* Extension module initialisation follows
  [PEP 489](https://www.python.org/dev/peps/pep-0489/ "https://www.python.org/dev/peps/pep-0489/") in CPython 3.5+, which
  resolves several differences with regard to normal Python modules. This makes
  the global names `__file__` and `__path__` correctly available to module
  level code and improves the support for module-level relative imports.
  (Github issues [#1715](https://github.com/cython/cython/issues/1715 "https://github.com/cython/cython/issues/1715"), [#1753](https://github.com/cython/cython/issues/1753 "https://github.com/cython/cython/issues/1753"), [#1035](https://github.com/cython/cython/issues/1035 "https://github.com/cython/cython/issues/1035"))
* Asynchronous generators ([PEP 525](https://www.python.org/dev/peps/pep-0525/ "https://www.python.org/dev/peps/pep-0525/"))
  and asynchronous comprehensions ([PEP 530](https://www.python.org/dev/peps/pep-0530/ "https://www.python.org/dev/peps/pep-0530/"))
  have been implemented. Note that async generators require finalisation support
  in order to allow for asynchronous operations during cleanup, which is only
  available in CPython 3.6+. All other functionality has been backported as usual.
* Variable annotations are now parsed according to
  [PEP 526](https://www.python.org/dev/peps/pep-0526/ "https://www.python.org/dev/peps/pep-0526/"). Cython types (e.g.
  `cython.int`) are evaluated as C type declarations and everything else as Python
  types. This can be disabled with the directive `annotation_typing=False`.
  Note that most complex PEP-484 style annotations are currently ignored. This will
  change in future releases. (Github issue [#1850](https://github.com/cython/cython/issues/1850 "https://github.com/cython/cython/issues/1850"))
* Extension types (also in pure Python mode) can implement the normal special methods
  `__eq__`, `__lt__` etc. for comparisons instead of the low-level `__richcmp__`
  method. (Github issue [#690](https://github.com/cython/cython/issues/690 "https://github.com/cython/cython/issues/690"))
* New decorator `@cython.exceptval(x=None, check=False)` that makes the signature
  declarations `except x`, `except? x` and `except *` available to pure Python
  code. Original patch by Antonio Cuni. (Github issue [#1653](https://github.com/cython/cython/issues/1653 "https://github.com/cython/cython/issues/1653"))
* Signature annotations are now included in the signature docstring generated by
  the `embedsignature` directive. Patch by Lisandro Dalcin (Github issue [#1781](https://github.com/cython/cython/issues/1781 "https://github.com/cython/cython/issues/1781")).
* The gdb support for Python code (`libpython.py`) was updated to the latest
  version in CPython 3.7 (git rev 5fe59f8).
* The compiler tries to find a usable exception return value for cdef functions
  with `except *` if the returned type allows it. Note that this feature is subject
  to safety limitations, so it is still better to provide an explicit declaration.
* C functions can be assigned to function pointers with a compatible exception
  declaration, not only with exact matches. A side-effect is that certain compatible
  signature overrides are now allowed and some more mismatches of exception signatures
  are now detected and rejected as errors that were not detected before.
* The IPython/Jupyter magic integration has a new option `%%cython --pgo` for profile
  guided optimisation. It compiles the cell with PGO settings for the C compiler,
  executes it to generate a runtime profile, and then compiles it again using that
  profile for C compiler optimisation. Currently only tested with gcc.
* `len(memoryview)` can be used in nogil sections to get the size of the
  first dimension of a memory view (`shape[0]`). (Github issue [#1733](https://github.com/cython/cython/issues/1733 "https://github.com/cython/cython/issues/1733"))
* C++ classes can now contain (properly refcounted) Python objects.
* NumPy dtype subarrays are now accessible through the C-API.
  Patch by Gerald Dalley (Github issue [#245](https://github.com/cython/cython/issues/245 "https://github.com/cython/cython/issues/245")).
* Resolves several issues with PyPy and uses faster async slots in PyPy3.
  Patch by Ronan Lamy (Github issues [#1871](https://github.com/cython/cython/issues/1871 "https://github.com/cython/cython/issues/1871"), [#1878](https://github.com/cython/cython/issues/1878 "https://github.com/cython/cython/issues/1878")).

### Bugs fixed[¶](#id264 "Link to this heading")

* Extension types that were cimported from other Cython modules could disagree
  about the order of fused cdef methods in their call table. This could lead
  to wrong methods being called and potentially also crashes. The fix required
  changes to the ordering of fused methods in the call table, which may break
  existing compiled modules that call fused cdef methods across module boundaries,
  if these methods were implemented in a different order than they were declared
  in the corresponding .pxd file. (Github issue [#1873](https://github.com/cython/cython/issues/1873 "https://github.com/cython/cython/issues/1873"))
* The exception state handling in generators and coroutines could lead to
  exceptions in the caller being lost if an exception was raised and handled
  inside of the coroutine when yielding. (Github issue [#1731](https://github.com/cython/cython/issues/1731 "https://github.com/cython/cython/issues/1731"))
* Loops over `range(enum)` were not converted into C for-loops. Note that it
  is still recommended to use an explicit cast to a C integer type in this case.
* Error positions of names (e.g. variables) were incorrectly reported after the
  name and not at the beginning of the name.
* Compile time `DEF` assignments were evaluated even when they occur inside of
  falsy `IF` blocks. (Github issue [#1796](https://github.com/cython/cython/issues/1796 "https://github.com/cython/cython/issues/1796"))
* Disabling the line tracing from a trace function could fail.
  Original patch by Dmitry Trofimov. (Github issue [#1769](https://github.com/cython/cython/issues/1769 "https://github.com/cython/cython/issues/1769"))
* Several issues with the Pythran integration were resolved.
* abs(signed int) now returns a signed rather than unsigned int.
  (Github issue [#1837](https://github.com/cython/cython/issues/1837 "https://github.com/cython/cython/issues/1837"))
* Reading `frame.f_locals` of a Cython function (e.g. from a debugger or profiler
  could modify the module globals. (Github issue [#1836](https://github.com/cython/cython/issues/1836 "https://github.com/cython/cython/issues/1836"))
* Buffer type mismatches in the NumPy buffer support could leak a reference to the
  buffer owner.
* Using the “is\_f\_contig” and “is\_c\_contig” memoryview methods together could leave
  one of them undeclared. (Github issue [#1872](https://github.com/cython/cython/issues/1872 "https://github.com/cython/cython/issues/1872"))
* Compilation failed if the for-in-range loop target was not a variable but a more
  complex expression, e.g. an item assignment. (Github issue [#1831](https://github.com/cython/cython/issues/1831 "https://github.com/cython/cython/issues/1831"))
* Compile time evaluations of (partially) constant f-strings could show incorrect
  results.
* Escape sequences in raw f-strings (`fr'...'`) were resolved instead of passing
  them through as expected.
* Some ref-counting issues in buffer error handling have been resolved.

### Other changes[¶](#id265 "Link to this heading")

* Type declarations in signature annotations are now parsed according to
  [PEP 484](https://www.python.org/dev/peps/pep-0484/ "https://www.python.org/dev/peps/pep-0484/")
  typing. Only Cython types (e.g. `cython.int`) and Python builtin types are
  currently considered as type declarations. Everything else is ignored, but this
  will change in a future Cython release.
  (Github issue [#1672](https://github.com/cython/cython/issues/1672 "https://github.com/cython/cython/issues/1672"))
* The directive `annotation_typing` is now `True` by default, which enables
  parsing type declarations from annotations.
* This release no longer supports Python 3.2.

## 0.26.1 (2017-08-29)[¶](#id267 "Link to this heading")

### Features added[¶](#id268 "Link to this heading")

### Bugs fixed[¶](#id269 "Link to this heading")

* `cython.view.array` was missing `.__len__()`.
* Extension types with a `.pxd` override for their `__releasebuffer__` slot
  (e.g. as provided by Cython for the Python `array.array` type) could leak
  a reference to the buffer owner on release, thus not freeing the memory.
  (Github issue [#1638](https://github.com/cython/cython/issues/1638 "https://github.com/cython/cython/issues/1638"))
* Auto-decoding failed in 0.26 for strings inside of C++ containers.
  (Github issue [#1790](https://github.com/cython/cython/issues/1790 "https://github.com/cython/cython/issues/1790"))
* Compile error when inheriting from C++ container types.
  (Github issue [#1788](https://github.com/cython/cython/issues/1788 "https://github.com/cython/cython/issues/1788"))
* Invalid C code in generators (declaration after code).
  (Github issue [#1801](https://github.com/cython/cython/issues/1801 "https://github.com/cython/cython/issues/1801"))
* Arithmetic operations on `const` integer variables could generate invalid code.
  (Github issue [#1798](https://github.com/cython/cython/issues/1798 "https://github.com/cython/cython/issues/1798"))
* Local variables with names of special Python methods failed to compile inside of
  closures. (Github issue [#1797](https://github.com/cython/cython/issues/1797 "https://github.com/cython/cython/issues/1797"))
* Problem with indirect Emacs buffers in cython-mode.
  Patch by Martin Albrecht (Github issue [#1743](https://github.com/cython/cython/issues/1743 "https://github.com/cython/cython/issues/1743")).
* Extension types named `result` or `PickleError` generated invalid unpickling code.
  Patch by Jason Madden (Github issue [#1786](https://github.com/cython/cython/issues/1786 "https://github.com/cython/cython/issues/1786")).
* Bazel integration failed to compile `.py` files.
  Patch by Guro Bokum (Github issue [#1784](https://github.com/cython/cython/issues/1784 "https://github.com/cython/cython/issues/1784")).
* Some include directories and dependencies were referenced with their absolute paths
  in the generated files despite lying within the project directory.
* Failure to compile in Py3.7 due to a modified signature of `_PyCFunctionFast()`

## 0.26 (2017-07-19)[¶](#id270 "Link to this heading")

### Features added[¶](#id271 "Link to this heading")

* Pythran can be used as a backend for evaluating NumPy array expressions.
  Patch by Adrien Guinet (Github issue [#1607](https://github.com/cython/cython/issues/1607 "https://github.com/cython/cython/issues/1607")).
* cdef classes now support pickling by default when possible.
  This can be disabled with the `auto_pickle` directive.
* Speed up comparisons of strings if their hash value is available.
  Patch by Claudio Freire (Github issue [#1571](https://github.com/cython/cython/issues/1571 "https://github.com/cython/cython/issues/1571")).
* Support pyximport from zip files.
  Patch by Sergei Lebedev (Github issue [#1485](https://github.com/cython/cython/issues/1485 "https://github.com/cython/cython/issues/1485")).
* IPython magic now respects the `__all__` variable and ignores
  names with leading-underscore (like `import *` does).
  Patch by Syrtis Major (Github issue [#1625](https://github.com/cython/cython/issues/1625 "https://github.com/cython/cython/issues/1625")).
* `abs()` is optimised for C complex numbers.
  Patch by David Woods (Github issue [#1648](https://github.com/cython/cython/issues/1648 "https://github.com/cython/cython/issues/1648")).
* The display of C lines in Cython tracebacks can now be enabled at runtime
  via `import cython_runtime; cython_runtime.cline_in_traceback=True`.
  The default has been changed to False.
* The overhead of calling fused types generic functions was reduced.
* “cdef extern” include files are now also searched relative to the current file.
  Patch by Jeroen Demeyer (Github issue [#1654](https://github.com/cython/cython/issues/1654 "https://github.com/cython/cython/issues/1654")).
* Optional optimization for re-acquiring the GIL, controlled by the
  fast\_gil directive.

### Bugs fixed[¶](#id272 "Link to this heading")

* Item lookup/assignment with a unicode character as index that is typed
  (explicitly or implicitly) as `Py_UCS4` or `Py_UNICODE` used the
  integer value instead of the Unicode string value. Code that relied on
  the previous behaviour now triggers a warning that can be disabled by
  applying an explicit cast. (Github issue [#1602](https://github.com/cython/cython/issues/1602 "https://github.com/cython/cython/issues/1602"))
* f-string processing was adapted to changes in PEP 498 and CPython 3.6.
* Invalid C code when decoding from UTF-16(LE/BE) byte strings.
  (Github issue [#1696](https://github.com/cython/cython/issues/1696 "https://github.com/cython/cython/issues/1696"))
* Unicode escapes in ‘ur’ raw-unicode strings were not resolved in Py2 code.
  Original patch by Aaron Gallagher (Github issue [#1594](https://github.com/cython/cython/issues/1594 "https://github.com/cython/cython/issues/1594")).
* File paths of code objects are now relative.
  Original patch by Jelmer Vernooij (Github issue [#1565](https://github.com/cython/cython/issues/1565 "https://github.com/cython/cython/issues/1565")).
* Decorators of cdef class methods could be executed twice.
  Patch by Jeroen Demeyer (Github issue [#1724](https://github.com/cython/cython/issues/1724 "https://github.com/cython/cython/issues/1724")).
* Dict iteration using the Py2 `iter*` methods failed in PyPy3.
  Patch by Armin Rigo (Github issue [#1631](https://github.com/cython/cython/issues/1631 "https://github.com/cython/cython/issues/1631")).
* Several warnings in the generated code are now suppressed.

### Other changes[¶](#id273 "Link to this heading")

* The `unraisable_tracebacks` option now defaults to `True`.
* Coercion of C++ containers to Python is no longer automatic on attribute
  access (Github issue [#1521](https://github.com/cython/cython/issues/1521 "https://github.com/cython/cython/issues/1521")).
* Access to Python attributes of cimported modules without the corresponding
  import is now a compile-time (rather than runtime) error.
* Do not use special dll linkage for “cdef public” functions.
  Patch by Jeroen Demeyer (Github issue [#1687](https://github.com/cython/cython/issues/1687 "https://github.com/cython/cython/issues/1687")).
* cdef/cpdef methods must match their declarations. See Github issue [#1732](https://github.com/cython/cython/issues/1732 "https://github.com/cython/cython/issues/1732").
  This is now a warning and will be an error in future releases.

## 0.25.2 (2016-12-08)[¶](#id274 "Link to this heading")

### Bugs fixed[¶](#id275 "Link to this heading")

* Fixes several issues with C++ template deduction.
* Fixes a issue with bound method type inference (Github issue [#551](https://github.com/cython/cython/issues/551 "https://github.com/cython/cython/issues/551")).
* Fixes a bug with cascaded tuple assignment (Github issue [#1523](https://github.com/cython/cython/issues/1523 "https://github.com/cython/cython/issues/1523")).
* Fixed or silenced many Clang warnings.
* Fixes bug with powers of pure real complex numbers (Github issue [#1538](https://github.com/cython/cython/issues/1538 "https://github.com/cython/cython/issues/1538")).

## 0.25.1 (2016-10-26)[¶](#id276 "Link to this heading")

### Bugs fixed[¶](#id277 "Link to this heading")

* Fixes a bug with `isinstance(o, Exception)` (Github issue [#1496](https://github.com/cython/cython/issues/1496 "https://github.com/cython/cython/issues/1496")).
* Fixes bug with `cython.view.array` missing utility code in some cases
  (Github issue [#1502](https://github.com/cython/cython/issues/1502 "https://github.com/cython/cython/issues/1502")).

### Other changes[¶](#id278 "Link to this heading")

* The distutils extension `Cython.Distutils.build_ext` has been reverted,
  temporarily, to be `old_build_ext` to give projects time to migrate.
  The new build\_ext is available as `new_build_ext`.

## 0.25 (2016-10-25)[¶](#id279 "Link to this heading")

### Features added[¶](#id280 "Link to this heading")

* def/cpdef methods of cdef classes benefit from Cython’s internal function
  implementation, which enables introspection and line profiling for them.
  Implementation sponsored by Turbostream (www.turbostream-cfd.com).
* Calls to Python functions are faster, following the recent “FastCall”
  optimisations that Victor Stinner implemented for CPython 3.6.
  See [https://bugs.python.org/issue27128](https://bugs.python.org/issue27128 "https://bugs.python.org/issue27128") and related issues.
* The new METH\_FASTCALL calling convention for PyCFunctions is supported
  in CPython 3.6. See [https://bugs.python.org/issue27810](https://bugs.python.org/issue27810 "https://bugs.python.org/issue27810")
* Initial support for using Cython modules in Pyston.
  Patch by Boxiang Sun.
* Dynamic Python attributes are allowed on cdef classes if an attribute
  `cdef dict __dict__` is declared in the class. Patch by empyrical.
* Cython implemented C++ classes can make direct calls to base class methods.
  Patch by empyrical.
* C++ classes can now have typedef members. STL containers updated with
  value\_type.
* New directive `cython.no_gc` to fully disable GC for a cdef class.
  Patch by Claudio Freire.
* Buffer variables are no longer excluded from `locals()`.
  Patch by David Woods.
* Building f-strings is faster, especially when formatting C integers.
* for-loop iteration over “std::string”.
* `libc/math.pxd` provides `e` and `pi` as alias constants to simplify
  usage as a drop-in replacement for Python’s math module.
* Speed up cython.inline().
* Binary lshift operations with small constant Python integers are faster.
* Some integer operations on Python long objects are faster in Python 2.7.
* Support for the C++ `typeid` operator.
* Support for bazel using a the pyx\_library rule in //Tools:rules.bzl.

### Significant Bugs fixed[¶](#significant-bugs-fixed "Link to this heading")

* Division of complex numbers avoids overflow by using Smith’s method.
* Some function signatures in `libc.math` and `numpy.pxd` were incorrect.
  Patch by Michael Seifert.

### Other changes[¶](#id281 "Link to this heading")

* The “%%cython” IPython/jupyter magic now defaults to the language level of
  the current jupyter kernel. The language level can be set explicitly with
  “%%cython -2” or “%%cython -3”.
* The distutils extension `Cython.Distutils.build_ext` has now been updated
  to use cythonize which properly handles dependencies. The old extension can
  still be found in `Cython.Distutils.old_build_ext` and is now deprecated.
* `directive_defaults` is no longer available in `Cython.Compiler.Options`,
  use `get_directive_defaults()` instead.

## 0.24.1 (2016-07-15)[¶](#id282 "Link to this heading")

### Bugs fixed[¶](#id283 "Link to this heading")

* IPython cell magic was lacking a good way to enable Python 3 code semantics.
  It can now be used as “%%cython -3”.
* Follow a recent change in [PEP 492](https://www.python.org/dev/peps/pep-0492/ "https://www.python.org/dev/peps/pep-0492/")
  and CPython 3.5.2 that now requires the `__aiter__()` method of asynchronous
  iterators to be a simple `def` method instead of an `async def` method.
* Coroutines and generators were lacking the `__module__` special attribute.
* C++ `std::complex` values failed to auto-convert from and to Python complex
  objects.
* Namespaced C++ types could not be used as memory view types due to lack of
  name mangling. Patch by Ivan Smirnov.
* Assignments between identical C++ types that were declared with differently
  typedefed template types could fail.
* Rebuilds could fail to evaluate dependency timestamps in C++ mode.
  Patch by Ian Henriksen.
* Macros defined in the `distutils` compiler option do not require values
  anymore. Patch by Ian Henriksen.
* Minor fixes for MSVC, Cygwin and PyPy.

## 0.24 (2016-04-04)[¶](#id284 "Link to this heading")

### Features added[¶](#id285 "Link to this heading")

* [PEP 498](https://www.python.org/dev/peps/pep-0498/ "https://www.python.org/dev/peps/pep-0498/"):
  Literal String Formatting (f-strings).
  Original patch by Jelle Zijlstra.
* [PEP 515](https://www.python.org/dev/peps/pep-0515/ "https://www.python.org/dev/peps/pep-0515/"):
  Underscores as visual separators in number literals.
* Parser was adapted to some minor syntax changes in Py3.6, e.g.
  [https://bugs.python.org/issue9232](https://bugs.python.org/issue9232 "https://bugs.python.org/issue9232")
* The embedded C code comments that show the original source code
  can be discarded with the new directive `emit_code_comments=False`.
* Cpdef enums are now first-class iterable, callable types in Python.
* Ctuples can now be declared in pure Python code.
* Posix declarations for DLL loading and stdio extensions were added.
  Patch by Lars Buitinck.
* The Py2-only builtins `unicode()`, `xrange()`, `reduce()` and
  `long` are now also available in compile time `DEF` expressions
  when compiling with Py3.
* Exception type tests have slightly lower overhead.
  This fixes ticket 868.
* @property syntax fully supported in cdef classes, old syntax deprecated.
* C++ classes can now be declared with default template parameters.

### Bugs fixed[¶](#id286 "Link to this heading")

* C++ exceptions raised by overloaded C++ operators were not always
  handled. Patch by Ian Henriksen.
* C string literals were previously always stored as non-const global
  variables in the module. They are now stored as global constants
  when possible, and otherwise as non-const C string literals in the
  generated code that uses them. This improves compatibility with
  strict C compiler options and prevents non-const strings literals
  with the same content from being incorrectly merged.
* Compile time evaluated `str` expressions (`DEF`) now behave in a
  more useful way by turning into Unicode strings when compiling under
  Python 3. This allows using them as intermediate values in expressions.
  Previously, they always evaluated to bytes objects.
* `isinf()` declarations in `libc/math.pxd` and `numpy/math.pxd` now
  reflect the actual tristate `int` return value instead of using `bint`.
* Literal assignments to ctuples avoid Python tuple round-trips in some
  more corner cases.
* Iteration over `dict(...).items()` failed to get optimised when dict
  arguments included keyword arguments.
* cProfile now correctly profiles cpdef functions and methods.

## 0.23.5 (2016-03-26)[¶](#id287 "Link to this heading")

* Compile errors and warnings in integer type conversion code. This fixes
  ticket 877. Patches by Christian Neukirchen, Nikolaus Rath, Ian Henriksen.
* Reference leak when `*args` argument was reassigned in closures.
* Truth-testing Unicode strings could waste time and memory in Py3.3+.
* Return values of async functions could be ignored and replaced by `None`.
* Compiler crash in CPython 3.6.
* Fix prange() to behave identically to range(). The end condition was
  miscalculated when the range was not exactly divisible by the step.
* Optimised `all(genexpr)`/`any(genexpr)` calls could warn about unused
  code. This fixes ticket 876.

## 0.23.4 (2015-10-10)[¶](#id288 "Link to this heading")

### Bugs fixed[¶](#id289 "Link to this heading")

* Memory leak when calling Python functions in PyPy.
* Compilation problem with MSVC in C99-ish mode.
* Warning about unused values in a helper macro.

## 0.23.3 (2015-09-29)[¶](#id290 "Link to this heading")

### Bugs fixed[¶](#id291 "Link to this heading")

* Invalid C code for some builtin methods. This fixes ticket 856 again.
* Incorrect C code in helper functions for PyLong conversion and string
  decoding. This fixes ticket 863, ticket 864 and ticket 865.
  Original patch by Nikolaus Rath.
* Large folded or inserted integer constants could use too small C
  integer types and thus trigger a value wrap-around.

### Other changes[¶](#id292 "Link to this heading")

* The coroutine and generator types of Cython now also register directly
  with the `Coroutine` and `Generator` ABCs in the `backports_abc`
  module if it can be imported. This fixes ticket 870.

## 0.23.2 (2015-09-11)[¶](#id293 "Link to this heading")

### Bugs fixed[¶](#id294 "Link to this heading")

* Compiler crash when analysing some optimised expressions.
* Coverage plugin was adapted to coverage.py 4.0 beta 2.
* C++ destructor calls could fail when ‘&’ operator is overwritten.
* Incorrect C literal generation for large integers in compile-time
  evaluated DEF expressions and constant folded expressions.
* Byte string constants could end up as Unicode strings when originating
  from compile-time evaluated DEF expressions.
* Invalid C code when caching known builtin methods.
  This fixes ticket 860.
* `ino_t` in `posix.types` was not declared as `unsigned`.
* Declarations in `libcpp/memory.pxd` were missing `operator!()`.
  Patch by Leo Razoumov.
* Static cdef methods can now be declared in .pxd files.

## 0.23.1 (2015-08-22)[¶](#id295 "Link to this heading")

### Bugs fixed[¶](#id296 "Link to this heading")

* Invalid C code for generators. This fixes ticket 858.
* Invalid C code for some builtin methods. This fixes ticket 856.
* Invalid C code for unused local buffer variables.
  This fixes ticket 154.
* Test failures on 32bit systems. This fixes ticket 857.
* Code that uses `from xyz import *` and global C struct/union/array
  variables could fail to compile due to missing helper functions.
  This fixes ticket 851.
* Misnamed PEP 492 coroutine property `cr_yieldfrom` renamed to
  `cr_await` to match CPython.
* Missing deallocation code for C++ object attributes in certain
  extension class hierarchies.
* Crash when async coroutine was not awaited.
* Compiler crash on `yield` in signature annotations and default
  argument values. Both are forbidden now.
* Compiler crash on certain constructs in `finally` clauses.
* Cython failed to build when CPython’s pgen is installed.

## 0.23 (2015-08-08)[¶](#id297 "Link to this heading")

### Features added[¶](#id298 "Link to this heading")

* [PEP 492](https://www.python.org/dev/peps/pep-0492/ "https://www.python.org/dev/peps/pep-0492/")
  (async/await) was implemented.
* [PEP 448](https://www.python.org/dev/peps/pep-0448/ "https://www.python.org/dev/peps/pep-0448/")
  (Additional Unpacking Generalizations) was implemented.
* Support for coverage.py 4.0+ can be enabled by adding the plugin
  “Cython.Coverage” to the “.coveragerc” config file.
* Annotated HTML source pages can integrate (XML) coverage reports.
* Tracing is supported in `nogil` functions/sections and module init code.
* When generators are used in a Cython module and the module imports the
  modules “inspect” and/or “asyncio”, Cython enables interoperability by
  patching these modules during the import to recognise Cython’s internal
  generator and coroutine types. This can be disabled by C compiling the
  module with “-D CYTHON\_PATCH\_ASYNCIO=0” or “-D CYTHON\_PATCH\_INSPECT=0”
* When generators or coroutines are used in a Cython module, their types
  are registered with the `Generator` and `Coroutine` ABCs in the
  `collections` or `collections.abc` stdlib module at import time to
  enable interoperability with code that needs to detect and process Python
  generators/coroutines. These ABCs were added in CPython 3.5 and are
  available for older Python versions through the `backports_abc` module
  on PyPI. See [https://bugs.python.org/issue24018](https://bugs.python.org/issue24018 "https://bugs.python.org/issue24018")
* Adding/subtracting/dividing/modulus and equality comparisons with
  constant Python floats and small integers are faster.
* Binary and/or/xor/rshift operations with small constant Python integers
  are faster.
* When called on generator expressions, the builtins `all()`, `any()`,
  `dict()`, `list()`, `set()`, `sorted()` and `unicode.join()`
  avoid the generator iteration overhead by inlining a part of their
  functionality into the for-loop.
* Keyword argument dicts are no longer copied on function entry when they
  are not being used or only passed through to other function calls (e.g.
  in wrapper functions).
* The `PyTypeObject` declaration in `cpython.object` was extended.
* The builtin `type` type is now declared as PyTypeObject in source,
  allowing for extern functions taking type parameters to have the correct
  C signatures. Note that this might break code that uses `type` just
  for passing around Python types in typed variables. Removing the type
  declaration provides a backwards compatible fix.
* `wraparound()` and `boundscheck()` are available as no-ops in pure
  Python mode.
* Const iterators were added to the provided C++ STL declarations.
* Smart pointers were added to the provided C++ STL declarations.
  Patch by Daniel Filonik.
* `NULL` is allowed as default argument when embedding signatures.
  This fixes ticket 843.
* When compiling with `--embed`, the internal module name is changed to
  `__main__` to allow arbitrary program names, including those that would
  be invalid for modules. Note that this prevents reuse of the generated
  C code as an importable module.
* External C++ classes that overload the assignment operator can be used.
  Patch by Ian Henriksen.
* Support operator bool() for C++ classes so they can be used in if statements.

### Bugs fixed[¶](#id300 "Link to this heading")

* Calling “yield from” from Python on a Cython generator that returned a
  value triggered a crash in CPython. This is now being worked around.
  See [https://bugs.python.org/issue23996](https://bugs.python.org/issue23996 "https://bugs.python.org/issue23996")
* Language level 3 did not enable true division (a.k.a. float division)
  for integer operands.
* Functions with fused argument types that included a generic ‘object’
  fallback could end up using that fallback also for other explicitly
  listed object types.
* Relative cimports could accidentally fall back to trying an absolute
  cimport on failure.
* The result of calling a C struct constructor no longer requires an
  intermediate assignment when coercing to a Python dict.
* C++ exception declarations with mapping functions could fail to compile
  when pre-declared in .pxd files.
* `cpdef void` methods are now permitted.
* `abs(cint)` could fail to compile in MSVC and used sub-optimal code
  in C++. Patch by David Vierra, original patch by Michael Enßlin.
* Buffer index calculations using index variables with small C integer
  types could overflow for large buffer sizes.
  Original patch by David Vierra.
* C unions use a saner way to coerce from and to Python dicts.
* When compiling a module `foo.pyx`, the directories in `sys.path`
  are no longer searched when looking for `foo.pxd`.
  Patch by Jeroen Demeyer.
* Memory leaks in the embedding main function were fixed.
  Original patch by Michael Enßlin.
* Some complex Python expressions could fail to compile inside of finally
  clauses.
* Unprefixed ‘str’ literals were not supported as C varargs arguments.
* Fixed type errors in conversion enum types to/from Python. Note that
  this imposes stricter correctness requirements on enum declarations.

### Other changes[¶](#id301 "Link to this heading")

* Changed mangling scheme in header files generated by `cdef api`
  declarations.
* Installation under CPython 3.3+ no longer requires a pass of the
  2to3 tool. This also makes it possible to run Cython in Python
  3.3+ from a source checkout without installing it first.
  Patch by Petr Viktorin.
* `jedi-typer.py` (in `Tools/`) was extended and renamed to
  `jedityper.py` (to make it importable) and now works with and
  requires Jedi 0.9. Patch by Tzer-jen Wei.

## 0.22.1 (2015-06-20)[¶](#id302 "Link to this heading")

### Bugs fixed[¶](#id303 "Link to this heading")

* Crash when returning values on generator termination.
* In some cases, exceptions raised during internal isinstance() checks were
  not propagated.
* Runtime reported file paths of source files (e.g for profiling and tracing)
  are now relative to the build root directory instead of the main source file.
* Tracing exception handling code could enter the trace function with an active
  exception set.
* The internal generator function type was not shared across modules.
* Comparisons of (inferred) ctuples failed to compile.
* Closures inside of cdef functions returning `void` failed to compile.
* Using `const` C++ references in intermediate parts of longer expressions
  could fail to compile.
* C++ exception declarations with mapping functions could fail to compile when
  pre-declared in .pxd files.
* C++ compilation could fail with an ambiguity error in recent MacOS-X Xcode
  versions.
* C compilation could fail in pypy3.
* Fixed a memory leak in the compiler when compiling multiple modules.
* When compiling multiple modules, external library dependencies could leak
  into later compiler runs. Fix by Jeroen Demeyer. This fixes ticket 845.

## 0.22 (2015-02-11)[¶](#id304 "Link to this heading")

### Features added[¶](#id305 "Link to this heading")

* C functions can coerce to Python functions, which allows passing them
  around as callable objects.
* C arrays can be assigned by value and auto-coerce from Python iterables
  and to Python lists (and tuples).
* Extern C functions can now be declared as cpdef to export them to
  the module’s Python namespace. Extern C functions in pxd files export
  their values to their own module, iff it exists.
* Anonymous C tuple types can be declared as (ctype1, ctype2, …).
* [PEP 479](https://www.python.org/dev/peps/pep-0479/ "https://www.python.org/dev/peps/pep-0479/"):
  turn accidental StopIteration exceptions that exit generators
  into a RuntimeError, activated with future import “generator\_stop”.
* Looping over `reversed(range())` is optimised in the same way as
  `range()`. Patch by Favian Contreras.

### Bugs fixed[¶](#id307 "Link to this heading")

* Mismatching ‘except’ declarations on signatures in .pxd and .pyx files failed
  to produce a compile error.
* Failure to find any files for the path pattern(s) passed into `cythonize()`
  is now an error to more easily detect accidental typos.
* The `logaddexp` family of functions in `numpy.math` now has correct
  declarations.
* In Py2.6/7 and Py3.2, simple Cython memory views could accidentally be
  interpreted as non-contiguous by CPython, which could trigger a CPython
  bug when copying data from them, thus leading to data corruption.
  See CPython issues 12834 and 23349.

### Other changes[¶](#id308 "Link to this heading")

* Preliminary support for defining the Cython language with a formal grammar.
  To try parsing your files against this grammar, use the –formal\_grammar directive.
  Experimental.
* `_` is no longer considered a cacheable builtin as it could interfere with
  gettext.
* Cythonize-computed metadata now cached in the generated C files.
* Several corrections and extensions in numpy, cpython, and libcpp pxd files.

## 0.21.2 (2014-12-27)[¶](#id309 "Link to this heading")

### Bugs fixed[¶](#id310 "Link to this heading")

* Crash when assigning a C value to both a Python and C target at the same time.
* Automatic coercion from C++ strings to `str` generated incomplete code that
  failed to compile.
* Declaring a constructor in a C++ child class erroneously required a default
  constructor declaration in the super class.
* `resize_smart()` in `cpython.array` was broken.
* Functions in `libcpp.cast` are now declared as `nogil`.
* Some missing C-API declarations were added.
* Py3 main code in embedding program code was lacking casts.
* Exception related to distutils “Distribution” class type in pyximport under
  latest CPython 2.7 and 3.4 releases when setuptools is being imported later.

## 0.21.1 (2014-10-18)[¶](#id311 "Link to this heading")

### Features added[¶](#id312 "Link to this heading")

* New `cythonize` option `-a` to generate the annotated HTML source view.
* Missing C-API declarations in `cpython.unicode` were added.
* Passing `language='c++'` into cythonize() globally enables C++ mode for
  all modules that were not passed as Extension objects (i.e. only source
  files and file patterns).
* `Py_hash_t` is a known type (used in CPython for hash values).
* `PySlice_*()` C-API functions are available from the `cpython.slice`
  module.
* Allow arrays of C++ classes.

### Bugs fixed[¶](#id313 "Link to this heading")

* Reference leak for non-simple Python expressions in boolean and/or expressions.
* To fix a name collision and to reflect availability on host platforms,
  standard C declarations [ clock(), time(), struct tm and tm\* functions ]
  were moved from posix/time.pxd to a new libc/time.pxd. Patch by Charles
  Blake.
* Rerunning unmodified modules in IPython’s cython support failed.
  Patch by Matthias Bussonier.
* Casting C++ `std::string` to Python byte strings failed when
  auto-decoding was enabled.
* Fatal exceptions in global module init code could lead to crashes
  if the already created module was used later on (e.g. through a
  stale reference in sys.modules or elsewhere).
* `cythonize.py` script was not installed on MS-Windows.

### Other changes[¶](#id314 "Link to this heading")

* Compilation no longer fails hard when unknown compilation options are
  passed. Instead, it raises a warning and ignores them (as it did silently
  before 0.21). This will be changed back to an error in a future release.

## 0.21 (2014-09-10)[¶](#id315 "Link to this heading")

### Features added[¶](#id316 "Link to this heading")

* C (cdef) functions allow inner Python functions.
* Enums can now be declared as cpdef to export their values to
  the module’s Python namespace. Cpdef enums in pxd files export
  their values to their own module, iff it exists.
* Allow @staticmethod decorator to declare static cdef methods.
  This is especially useful for declaring “constructors” for
  cdef classes that can take non-Python arguments.
* Taking a `char*` from a temporary Python string object is safer
  in more cases and can be done inside of non-trivial expressions,
  including arguments of a function call. A compile time error
  is raised only when such a pointer is assigned to a variable and
  would thus exceed the lifetime of the string itself.
* Generators have new properties `__name__` and `__qualname__`
  that provide the plain/qualified name of the generator function
  (following CPython 3.5). See [https://bugs.python.org/issue21205](https://bugs.python.org/issue21205 "https://bugs.python.org/issue21205")
* The `inline` function modifier is available as a decorator
  `@cython.inline` in pure mode.
* When cygdb is run in a virtualenv, it enables the same virtualenv
  inside of the debugger. Patch by Marc Abramowitz.
* PEP 465: dedicated infix operator for matrix multiplication (A @ B).
* HTML output of annotated code uses Pygments for code highlighting
  and generally received a major overhaul by Matthias Bussonier.
* IPython magic support is now available directly from Cython with
  the command “%load\_ext cython”. Cython code can directly be
  executed in a cell when marked with “%%cython”. Code analysis
  is available with “%%cython -a”. Patch by Martín Gaitán.
* Simple support for declaring Python object types in Python signature
  annotations. Currently requires setting the compiler directive
  `annotation_typing=True`.
* New directive `use_switch` (defaults to True) to optionally disable
  the optimization of chained if statement to C switch statements.
* Defines dynamic\_cast et al. in `libcpp.cast` and C++ heap data
  structure operations in `libcpp.algorithm`.
* Shipped header declarations in `posix.*` were extended to cover
  more of the POSIX API. Patches by Lars Buitinck and Mark Peek.

### Optimizations[¶](#id317 "Link to this heading")

* Simple calls to C implemented Python functions/methods are faster.
  This also speeds up many operations on builtins that Cython cannot
  otherwise optimise.
* The “and”/”or” operators try to avoid unnecessary coercions of their
  arguments. They now evaluate the truth value of each argument
  independently and only coerce the final result of the whole expression
  to the target type (e.g. the type on the left side of an assignment).
  This also avoids reference counting overhead for Python values during
  evaluation and generally improves the code flow in the generated C code.
* The Python expression “2 \*\* N” is optimised into bit shifting.
  See [https://bugs.python.org/issue21420](https://bugs.python.org/issue21420 "https://bugs.python.org/issue21420")
* Cascaded assignments (a = b = …) try to minimise the number of
  type coercions.
* Calls to `slice()` are translated to a straight C-API call.

### Bugs fixed[¶](#id318 "Link to this heading")

* Crash when assigning memory views from ternary conditional expressions.
* Nested C++ templates could lead to unseparated “>>” characters being
  generated into the C++ declarations, which older C++ compilers could
  not parse.
* Sending SIGINT (Ctrl-C) during parallel cythonize() builds could
  hang the child processes.
* No longer ignore local setup.cfg files for distutils in pyximport.
  Patch by Martin Teichmann.
* Taking a `char*` from an indexed Python string generated unsafe
  reference counting code.
* Set literals now create all of their items before trying to add them
  to the set, following the behaviour in CPython. This makes a
  difference in the rare case that the item creation has side effects
  and some items are not hashable (or if hashing them has side effects,
  too).
* Cython no longer generates the cross product of C functions for code
  that uses memory views of fused types in function signatures (e.g.
  `cdef func(floating[:] a, floating[:] b)`). This is considered the
  expected behaviour by most users and was previously inconsistent with
  other structured types like C arrays. Code that really wants all type
  combinations can create the same fused memoryview type under different
  names and use those in the signature to make it clear which types are
  independent.
* Names that were unknown at compile time were looked up as builtins at
  runtime but not as global module names. Trying both lookups helps with
  globals() manipulation.
* Fixed stl container conversion for typedef element types.
* `obj.pop(x)` truncated large C integer values of x to `Py_ssize_t`.
* `__init__.pyc` is recognised as marking a package directory
  (in addition to .py, .pyx and .pxd).
* Syntax highlighting in `cython-mode.el` for Emacs no longer
  incorrectly highlights keywords found as part of longer names.
* Correctly handle `from cython.submodule cimport name`.
* Fix infinite recursion when using super with cpdef methods.
* No-args `dir()` was not guaranteed to return a sorted list.

### Other changes[¶](#id319 "Link to this heading")

* The header line in the generated C files no longer contains the
  timestamp but only the Cython version that wrote it. This was
  changed to make builds more reproducible.
* Removed support for CPython 2.4, 2.5 and 3.1.
* The licensing implications on the generated code were clarified
  to avoid legal constraints for users.

## 0.20.2 (2014-06-16)[¶](#id320 "Link to this heading")

### Features added[¶](#id321 "Link to this heading")

* Some optimisations for set/frozenset instantiation.
* Support for C++ unordered\_set and unordered\_map.

### Bugs fixed[¶](#id322 "Link to this heading")

* Access to attributes of optimised builtin methods (e.g.
  `[].append.__name__`) could fail to compile.
* Memory leak when extension subtypes add a memory view as attribute
  to those of the parent type without having Python object attributes
  or a user provided dealloc method.
* Compiler crash on readonly properties in “binding” mode.
* Auto-encoding with `c_string_encoding=ascii` failed in Py3.3.
* Crash when subtyping freelist enabled Cython extension types with
  Python classes that use `__slots__`.
* Freelist usage is restricted to CPython to avoid problems with other
  Python implementations.
* Memory leak in memory views when copying overlapping, contiguous slices.
* Format checking when requesting non-contiguous buffers from
  `cython.array` objects was accidentally omitted in Py3.
* C++ destructor calls in extension types could fail to compile in clang.
* Buffer format validation failed for sequences of strings in structs.
* Docstrings on extension type attributes in .pxd files were rejected.

## 0.20.1 (2014-02-11)[¶](#id323 "Link to this heading")

### Bugs fixed[¶](#id324 "Link to this heading")

* Build error under recent MacOS-X versions where `isspace()` could not be
  resolved by clang.
* List/Tuple literals multiplied by more than one factor were only multiplied
  by the last factor instead of all.
* Lookups of special methods (specifically for context managers) could fail
  in Python <= 2.6/3.1.
* Local variables were erroneously appended to the signature introspection
  of Cython implemented functions with keyword-only arguments under Python 3.
* In-place assignments to variables with inferred Python builtin/extension
  types could fail with type errors if the result value type was incompatible
  with the type of the previous value.
* The C code generation order of cdef classes, closures, helper code,
  etc. was not deterministic, thus leading to high code churn.
* Type inference could fail to deduce C enum types.
* Type inference could deduce unsafe or inefficient types from integer
  assignments within a mix of inferred Python variables and integer
  variables.

## 0.20 (2014-01-18)[¶](#id325 "Link to this heading")

### Features added[¶](#id326 "Link to this heading")

* Support for CPython 3.4.
* Support for calling C++ template functions.
* `yield` is supported in `finally` clauses.
* The C code generated for finally blocks is duplicated for each exit
  case to allow for better optimisations by the C compiler.
* Cython tries to undo the Python optimisationism of assigning a bound
  method to a local variable when it can generate better code for the
  direct call.
* Constant Python float values are cached.
* String equality comparisons can use faster type specific code in
  more cases than before.
* String/Unicode formatting using the ‘%’ operator uses a faster
  C-API call.
* `bytearray` has become a known type and supports coercion from and
  to C strings. Indexing, slicing and decoding is optimised. Note that
  this may have an impact on existing code due to type inference.
* Using `cdef basestring stringvar` and function arguments typed as
  `basestring` is now meaningful and allows assigning exactly
  `str` and `unicode` objects, but no subtypes of these types.
* Support for the `__debug__` builtin.
* Assertions in Cython compiled modules are disabled if the running
  Python interpreter was started with the “-O” option.
* Some types that Cython provides internally, such as functions and
  generators, are now shared across modules if more than one Cython
  implemented module is imported.
* The type inference algorithm works more fine granular by taking the
  results of the control flow analysis into account.
* A new script in `bin/cythonize` provides a command line frontend
  to the cythonize() compilation function (including distutils build).
* The new extension type decorator `@cython.no_gc_clear` prevents
  objects from being cleared during cyclic garbage collection, thus
  making sure that object attributes are kept alive until deallocation.
* During cyclic garbage collection, attributes of extension types that
  cannot create reference cycles due to their type (e.g. strings) are
  no longer considered for traversal or clearing. This can reduce the
  processing overhead when searching for or cleaning up reference cycles.
* Package compilation (i.e. `__init__.py` files) now works, starting
  with Python 3.3.
* The cython-mode.el script for Emacs was updated. Patch by Ivan Andrus.
* An option common\_utility\_include\_dir was added to cythonize() to save
  oft-used utility code once in a separate directory rather than as
  part of each generated file.
* `unraisable_tracebacks` directive added to control printing of
  tracebacks of unraisable exceptions.

### Bugs fixed[¶](#id327 "Link to this heading")

* Abstract Python classes that subtyped a Cython extension type
  failed to raise an exception on instantiation, and thus ended
  up being instantiated.
* `set.add(a_tuple)` and `set.discard(a_tuple)` failed with a
  TypeError in Py2.4.
* The PEP 3155 `__qualname__` was incorrect for nested classes and
  inner classes/functions declared as `global`.
* Several corner cases in the try-finally statement were fixed.
* The metaclass of a Python class was not inherited from its parent
  class(es). It is now extracted from the list of base classes if not
  provided explicitly using the Py3 `metaclass` keyword argument.
  In Py2 compilation mode, a `__metaclass__` entry in the class
  dict will still take precedence if not using Py3 metaclass syntax,
  but only after creating the class dict (which may have been done
  by a metaclass of a base class, see PEP 3115). It is generally
  recommended to use the explicit Py3 syntax to define metaclasses
  for Python types at compile time.
* The automatic C switch statement generation behaves more safely for
  heterogeneous value types (e.g. mixing enum and char), allowing for
  a slightly wider application and reducing corner cases. It now always
  generates a ‘default’ clause to avoid C compiler warnings about
  unmatched enum values.
* Fixed a bug where class hierarchies declared out-of-order could result
  in broken generated code.
* Fixed a bug which prevented overriding const methods of C++ classes.
* Fixed a crash when converting Python objects to C++ strings fails.

### Other changes[¶](#id328 "Link to this heading")

* In Py3 compilation mode, Python2-style metaclasses declared by a
  `__metaclass__` class dict entry are ignored.
* In Py3.4+, the Cython generator type uses `tp_finalize()` for safer
  cleanup instead of `tp_del()`.

## 0.19.2 (2013-10-13)[¶](#id329 "Link to this heading")

### Features added[¶](#id330 "Link to this heading")

### Bugs fixed[¶](#id331 "Link to this heading")

* Some standard declarations were fixed or updated, including the previously
  incorrect declaration of `PyBuffer_FillInfo()` and some missing bits in
  `libc.math`.
* Heap allocated subtypes of `type` used the wrong base type struct at the
  C level.
* Calling the unbound method dict.keys/value/items() in dict subtypes could
  call the bound object method instead of the unbound supertype method.
* “yield” wasn’t supported in “return” value expressions.
* Using the “bint” type in memory views lead to unexpected results.
  It is now an error.
* Assignments to global/closure variables could catch them in an illegal state
  while deallocating the old value.

### Other changes[¶](#id332 "Link to this heading")

## 0.19.1 (2013-05-11)[¶](#id333 "Link to this heading")

### Features added[¶](#id334 "Link to this heading")

* Completely empty C-API structs for extension type slots (protocols like
  number/mapping/sequence) are no longer generated into the C code.
* Docstrings that directly follow a public/readonly attribute declaration
  in a cdef class will be used as docstring of the auto-generated property.
  This fixes ticket 206.
* The automatic signature documentation tries to preserve more semantics
  of default arguments and argument types. Specifically, `bint` arguments
  now appear as type `bool`.
* A warning is emitted when negative literal indices are found inside of
  a code section that disables `wraparound` handling. This helps with
  fixing invalid code that might fail in the face of future compiler
  optimisations.
* Constant folding for boolean expressions (and/or) was improved.
* Added a build\_dir option to cythonize() which allows one to place
  the generated .c files outside the source tree.

### Bugs fixed[¶](#id335 "Link to this heading")

* `isinstance(X, type)` failed to get optimised into a call to
  `PyType_Check()`, as done for other builtin types.
* A spurious `from datetime cimport *` was removed from the “cpython”
  declaration package. This means that the “datetime” declarations
  (added in 0.19) are no longer available directly from the “cpython”
  namespace, but only from “cpython.datetime”. This is the correct
  way of doing it because the declarations refer to a standard library
  module, not the core CPython C-API itself.
* The C code for extension types is now generated in topological order
  instead of source code order to avoid C compiler errors about missing
  declarations for subtypes that are defined before their parent.
* The `memoryview` type name no longer shows up in the module dict of
  modules that use memory views. This fixes trac ticket 775.
* Regression in 0.19 that rejected valid C expressions from being used
  in C array size declarations.
* In C++ mode, the C99-only keyword `restrict` could accidentally be
  seen by the GNU C++ compiler. It is now specially handled for both
  GCC and MSVC.
* Testing large (> int) C integer values for their truth value could fail
  due to integer wrap-around.

### Other changes[¶](#id336 "Link to this heading")

## 0.19 (2013-04-19)[¶](#id337 "Link to this heading")

### Features added[¶](#id338 "Link to this heading")

* New directives `c_string_type` and `c_string_encoding` to more easily
  and automatically convert between C strings and the different Python string
  types.
* The extension type flag `Py_TPFLAGS_HAVE_VERSION_TAG` is enabled by default
  on extension types and can be disabled using the `type_version_tag` compiler
  directive.
* EXPERIMENTAL support for simple Cython code level line tracing. Enabled by
  the “linetrace” compiler directive.
* Cython implemented functions make their argument and return type annotations
  available through the `__annotations__` attribute (PEP 3107).
* Access to non-cdef module globals and Python object attributes is faster.
* `Py_UNICODE*` coerces from and to Python unicode strings. This is
  helpful when talking to Windows APIs, which use compatible wchar\_t
  arrays for strings. Note that the `Py_UNICODE` type is otherwise
  deprecated as of CPython 3.3.
* `isinstance(obj, basestring)` is optimised. In Python 3 it only tests
  for instances of `str` (i.e. Py2 `unicode`).
* The `basestring` builtin is mapped to `str` (i.e. Py2 `unicode`) when
  compiling the generated C code under Python 3.
* Closures use freelists, which can speed up their creation quite substantially.
  This is also visible for short running generator expressions, for example.
* A new class decorator `@cython.freelist(N)` creates a static freelist of N
  instances for an extension type, thus avoiding the costly allocation step if
  possible. This can speed up object instantiation by 20-30% in suitable
  scenarios. Note that freelists are currently only supported for base types,
  not for types that inherit from others.
* Fast extension type instantiation using the `Type.__new__(Type)` idiom has
  gained support for passing arguments. It is also a bit faster for types defined
  inside of the module.
* The Python2-only dict methods `.iter*()` and `.view*()` (requires Python 2.7)
  are automatically mapped to the equivalent keys/values/items methods in Python 3
  for typed dictionaries.
* Slicing unicode strings, lists and tuples is faster.
* list.append() is faster on average.
* `raise Exception() from None` suppresses the exception context in Py3.3.
* Py3 compatible `exec(tuple)` syntax is supported in Py2 code.
* Keyword arguments are supported for cdef functions.
* External C++ classes can be declared nogil. Patch by John Stumpo. This fixes
  trac ticket 805.

### Bugs fixed[¶](#id339 "Link to this heading")

* 2-value slicing of unknown objects passes the correct slice when the `getitem`
  protocol is used instead of the `getslice` protocol (especially in Python 3),
  i.e. `None` values for missing bounds instead of `[0,maxsize]`. It is also
  a bit faster in some cases, e.g. for constant bounds. This fixes trac ticket 636.
* Cascaded assignments of None values to extension type variables failed with
  a `TypeError` at runtime.
* The `__defaults__` attribute was not writable for Cython implemented
  functions.
* Default values of keyword-only arguments showed up in `__defaults__` instead
  of `__kwdefaults__` (which was not implemented). Both are available for
  Cython implemented functions now, as specified in Python 3.x.
* `yield` works inside of `with gil` sections. It previously lead to a crash.
  This fixes trac ticket 803.
* Static methods without explicitly named positional arguments (e.g. having only
  `*args`) crashed when being called. This fixes trac ticket 804.
* `dir()` without arguments previously returned an unsorted list, which now
  gets sorted as expected.
* `dict.items()`, `dict.keys()` and `dict.values()` no longer return lists
  in Python 3.
* Exiting from an `except-as` clause now deletes the exception in Python 3 mode.
* The declarations of `frexp()` and `ldexp()` in `math.pxd` were incorrect.

### Other changes[¶](#id340 "Link to this heading")

## 0.18 (2013-01-28)[¶](#id341 "Link to this heading")

### Features added[¶](#id342 "Link to this heading")

* Named Unicode escapes (”N{…}”) are supported.
* Python functions/classes provide the special attribute “\_\_qualname\_\_”
  as defined by PEP 3155.
* Added a directive `overflowcheck` which raises an OverflowException when
  arithmetic with C ints overflow. This has a modest performance penalty, but
  is much faster than using Python ints.
* Calls to nested Python functions are resolved at compile time.
* Type inference works across nested functions.
* `py_bytes_string.decode(...)` is optimised.
* C `const` declarations are supported in the language.

### Bugs fixed[¶](#id343 "Link to this heading")

* Automatic C++ exception mapping didn’t work in nogil functions (only in
  “with nogil” blocks).

### Other changes[¶](#id344 "Link to this heading")

## 0.17.4 (2013-01-03)[¶](#id345 "Link to this heading")

### Bugs fixed[¶](#id346 "Link to this heading")

* Garbage collection triggered during deallocation of container classes could lead to a double-deallocation.

## 0.17.3 (2012-12-14)[¶](#id347 "Link to this heading")

### Features added[¶](#id348 "Link to this heading")

### Bugs fixed[¶](#id349 "Link to this heading")

* During final interpreter cleanup (with types cleanup enabled at compile time), extension types that inherit from base types over more than one level that were cimported from other modules could lead to a crash.
* Weak-reference support in extension types (with a `cdef __weakref__` attribute) generated incorrect deallocation code.
* In CPython 3.3, converting a Unicode character to the Py\_UNICODE type could fail to raise an overflow for non-BMP characters that do not fit into a wchar\_t on the current platform.
* Negative C integer constants lost their longness suffix in the generated C code.

### Other changes[¶](#id350 "Link to this heading")

## 0.17.2 (2012-11-20)[¶](#id351 "Link to this heading")

### Features added[¶](#id352 "Link to this heading")

* `cythonize()` gained a best effort compile mode that can be used to simply ignore .py files that fail to compile.

### Bugs fixed[¶](#id353 "Link to this heading")

* Replacing an object reference with the value of one of its cdef attributes could generate incorrect C code that accessed the object after deleting its last reference.
* C-to-Python type coercions during cascaded comparisons could generate invalid C code, specifically when using the ‘in’ operator.
* “obj[1,]” passed a single integer into the item getter instead of a tuple.
* Cyclic imports at module init time did not work in Py3.
* The names of C++ destructors for template classes were built incorrectly.
* In pure mode, type casts in Cython syntax and the C ampersand operator are now rejected. Use the pure mode replacements instead.
* In pure mode, C type names and the sizeof() function are no longer recognised as such and can be used as normal Python names.
* The extended C level support for the CPython array type was declared too late to be used by user defined classes.
* C++ class nesting was broken.
* Better checking for required nullary constructors for stack-allocated C++ instances.
* Remove module docstring in no-docstring mode.
* Fix specialization for varargs function signatures.
* Fix several compiler crashes.

### Other changes[¶](#id354 "Link to this heading")

* An experimental distutils script for compiling the CPython standard library was added as Tools/cystdlib.py.

## 0.17.1 (2012-09-26)[¶](#id355 "Link to this heading")

### Features added[¶](#id356 "Link to this heading")

### Bugs fixed[¶](#id357 "Link to this heading")

* A reference leak was fixed in the new dict iteration code when the loop target was not a plain variable but an unpacked tuple.
* Memory views did not handle the special case of a NULL buffer strides value, as allowed by PEP3118.

### Other changes[¶](#id358 "Link to this heading")

## 0.17 (2012-09-01)[¶](#id359 "Link to this heading")

### Features added[¶](#id360 "Link to this heading")

* Alpha quality support for compiling and running Cython generated extension modules in PyPy (through cpyext). Note that this requires at least PyPy 1.9 and in many cases also adaptations in user code, especially to avoid borrowed references when no owned reference is being held directly in C space (a reference in a Python list or dict is not enough, for example). See the documentation on porting Cython code to PyPy.
* “yield from” is supported (PEP 380) and a couple of minor problems with generators were fixed.
* C++ STL container classes automatically coerce from and to the equivalent Python container types on typed assignments and casts. Note that the data in the containers is copied during this conversion.
* C++ iterators can now be iterated over using “for x in cpp\_container” whenever cpp\_container has begin() and end() methods returning objects satisfying the iterator pattern (that is, it can be incremented, dereferenced, and compared (for non-equality)).
* cdef classes can now have C++ class members (provided a zero-argument constructor exists)
* A new cpython.array standard cimport file allows to efficiently talk to the stdlib array.array data type in Python 2. Since CPython does not export an official C-API for this module, it receives special casing by the compiler in order to avoid setup overhead on user side. In Python 3, both buffers and memory views on the array type already worked out of the box with earlier versions of Cython due to the native support for the buffer interface in the Py3 array module.
* Fast dict iteration is now enabled optimistically also for untyped variables when the common iteration methods are used.
* The unicode string processing code was adapted for the upcoming CPython 3.3 (PEP 393, new Unicode buffer layout).
* Buffer arguments and memory view arguments in Python functions can be declared “not None” to raise a TypeError on None input.
* c(p)def functions in pure mode can specify their return type with “@cython.returns()”.
* Automatic dispatch for fused functions with memoryview arguments
* Support newaxis indexing for memoryviews
* Support decorators for fused functions

### Bugs fixed[¶](#id361 "Link to this heading")

* Old-style Py2 imports did not work reliably in Python 3.x and were broken in Python 3.3. Regardless of this fix, it’s generally best to be explicit about relative and global imports in Cython code because old-style imports have a higher overhead. To this end, “from \_\_future\_\_ import absolute\_import” is supported in Python/Cython 2.x code now (previous versions of Cython already used it when compiling Python 3 code).
* Stricter constraints on the “inline” and “final” modifiers. If your code does not compile due to this change, chances are these modifiers were previously being ignored by the compiler and can be removed without any performance regression.
* Exceptions are always instantiated while raising them (as in Python), instead of risking to instantiate them in potentially unsafe situations when they need to be handled or otherwise processed.
* locals() properly ignores names that do not have Python compatible types (including automatically inferred types).
* Some garbage collection issues of memory views were fixed.
* numpy.pxd compiles in Python 3 mode.
* Several C compiler warnings were fixed.
* Several bugs related to memoryviews and fused types were fixed.
* Several bug-fixes and improvements related to cythonize(), including ccache-style caching.

### Other changes[¶](#id362 "Link to this heading")

* libc.string provides a convenience declaration for const uchar in addition to const char.
* User declared char\* types are now recognised as such and auto-coerce to and from Python bytes strings.
* callable() and next() compile to more efficient C code.
* list.append() is faster on average.
* Modules generated by @cython.inline() are written into the directory pointed to by the environment variable CYTHON\_CACHE\_DIR if set.

## 0.16 (2012-04-21)[¶](#id363 "Link to this heading")

### Features added[¶](#id364 "Link to this heading")

* Enhancements to Cython’s function type (support for weak references, default arguments, code objects, dynamic attributes, classmethods, staticmethods, and more)
* Fused Types - Template-like support for functions and methods CEP 522 (docs)
* Typed views on memory - Support for efficient direct and indirect buffers (indexing, slicing, transposing, …) CEP 517 (docs)
* super() without arguments
* Final cdef methods (which translate into direct calls on known instances)

### Bugs fixed[¶](#id365 "Link to this heading")

* fix alignment handling for record types in buffer support

### Other changes[¶](#id366 "Link to this heading")

* support default arguments for closures
* search sys.path for pxd files
* support C++ template casting
* faster traceback building and faster generator termination
* support inplace operators on indexed buffers
* allow nested prange sections

## 0.15.1 (2011-09-19)[¶](#id367 "Link to this heading")

### Features added[¶](#id368 "Link to this heading")

### Bugs fixed[¶](#id369 "Link to this heading")

### Other changes[¶](#id370 "Link to this heading")

## 0.15 (2011-08-05)[¶](#id371 "Link to this heading")

### Features added[¶](#id372 "Link to this heading")

* Generators (yield) - Cython has full support for generators, generator expressions and PEP 342 coroutines.
* The nonlocal keyword is supported.
* Re-acquiring the gil: with gil - works as expected within a nogil context.
* OpenMP support: prange.
* Control flow analysis prunes dead code and emits warnings and errors about uninitialised variables.
* Debugger command cy set to assign values of expressions to Cython variables and cy exec counterpart $cy\_eval().
* Exception chaining PEP 3134.
* Relative imports PEP 328.
* Improved pure syntax including cython.cclass, cython.cfunc, and cython.ccall.
* The with statement has its own dedicated and faster C implementation.
* Support for del.
* Boundschecking directives implemented for builtin Python sequence types.
* Several updates and additions to the shipped standard library .pxd files.
* Forward declaration of types is no longer required for circular references.

### Bugs fixed[¶](#id373 "Link to this heading")

### Other changes[¶](#id374 "Link to this heading")

* Uninitialized variables are no longer initialized to None and accessing them has the same semantics as standard Python.
* globals() now returns a read-only dict of the Cython module’s globals, rather than the globals of the first non-Cython module in the stack
* Many C++ exceptions are now special cased to give closer Python counterparts. This means that except+ functions that formerly raised generic RuntimeErrors may raise something else such as ArithmeticError.
* The inlined generator expressions (introduced in Cython 0.13) were disabled in favour of full generator expression support. This breaks code that previously used them inside of cdef functions (usage in def functions continues to work) and induces a performance regression for cases that continue to work but that were previously inlined. We hope to reinstate this feature in the near future.

## 0.14.1 (2011-02-04)[¶](#id375 "Link to this heading")

### Features added[¶](#id376 "Link to this heading")

* The gdb debugging support was extended to include all major Cython features, including closures.
* raise MemoryError() is now safe to use as Cython replaces it with the correct C-API call.

### Bugs fixed[¶](#id377 "Link to this heading")

### Other changes[¶](#id378 "Link to this heading")

* Decorators on special methods of cdef classes now raise a compile time error rather than being ignored.
* In Python 3 language level mode (-3 option), the ‘str’ type is now mapped to ‘unicode’, so that cdef str s declares a Unicode string even when running in Python 2.

## 0.14 (2010-12-14)[¶](#id379 "Link to this heading")

### Features added[¶](#id380 "Link to this heading")

* Python classes can now be nested and receive a proper closure at definition time.
* Redefinition is supported for Python functions, even within the same scope.
* Lambda expressions are supported in class bodies and at the module level.
* Metaclasses are supported for Python classes, both in Python 2 and Python 3 syntax. The Python 3 syntax (using a keyword argument in the type declaration) is preferred and optimised at compile time.
* “final” extension classes prevent inheritance in Python space. This feature is available through the new “cython.final” decorator. In the future, these classes may receive further optimisations.
* “internal” extension classes do not show up in the module dictionary. This feature is available through the new “cython.internal” decorator.
* Extension type inheritance from builtin types, such as “cdef class MyUnicode(unicode)”, now works without further external type redeclarations (which are also strongly discouraged now and continue to issue a warning).
* GDB support. [https://docs.cython.org/src/userguide/debugging.html](https://docs.cython.org/src/userguide/debugging.html "https://docs.cython.org/src/userguide/debugging.html")
* A new build system with support for inline distutils directives, correct dependency tracking, and parallel compilation. [https://github.com/cython/cython/wiki/enhancements-distutils\_preprocessing](https://github.com/cython/cython/wiki/enhancements-distutils_preprocessing "https://github.com/cython/cython/wiki/enhancements-distutils_preprocessing")
* Support for dynamic compilation at runtime via the new cython.inline function and cython.compile decorator. [https://github.com/cython/cython/wiki/enhancements-inline](https://github.com/cython/cython/wiki/enhancements-inline "https://github.com/cython/cython/wiki/enhancements-inline")
* “nogil” blocks are supported when compiling pure Python code by writing “with cython.nogil”.
* Iterating over arbitrary pointer types is now supported, as is an optimized version of the in operator, e.g. x in ptr[a:b].

### Bugs fixed[¶](#id381 "Link to this heading")

* In parallel assignments, the right side was evaluated in reverse order in 0.13. This could result in errors if it had side effects (e.g. function calls).
* In some cases, methods of builtin types would raise a SystemError instead of an AttributeError when called on None.

### Other changes[¶](#id382 "Link to this heading")

* Constant tuples are now cached over the lifetime of an extension module, just like CPython does. Constant argument tuples of Python function calls are also cached.
* Closures have tightened to include exactly the names used in the inner functions and classes. Previously, they held the complete locals of the defining function.
* The builtin “next()” function in Python 2.6 and later is now implemented internally and therefore available in all Python versions. This makes it the preferred and portable way of manually advancing an iterator.
* In addition to the previously supported inlined generator expressions in 0.13, “sorted(genexpr)” can now be used as well. Typing issues were fixed in “sum(genexpr)” that could lead to invalid C code being generated. Other known issues with inlined generator expressions were also fixed that make upgrading to 0.14 a strong recommendation for code that uses them. Note that general generators and generator expressions continue to be not supported.
* Inplace arithmetic operators now respect the cdivision directive and are supported for complex types.
* Typing a variable as type “complex” previously gave it the Python object type. It now uses the appropriate C/C++ double complex type. A side-effect is that assignments and typed function parameters now accept anything that Python can coerce to a complex, including integers and floats, and not only complex instances.
* Large integer literals pass through the compiler in a safer way. To prevent truncation in C code, non 32-bit literals are turned into Python objects if not used in a C context. This context can either be given by a clear C literal suffix such as “UL” or “LL” (or “L” in Python 3 code), or it can be an assignment to a typed variable or a typed function argument, in which case it is up to the user to take care of a sufficiently large value space of the target.
* Python functions are declared in the order they appear in the file, rather than all being created at module creation time. This is consistent with Python and needed to support, for example, conditional or repeated declarations of functions. In the face of circular imports this may cause code to break, so a new –disable-function-redefinition flag was added to revert to the old behavior. This flag will be removed in a future release, so should only be used as a stopgap until old code can be fixed.

## 0.13 (2010-08-25)[¶](#id383 "Link to this heading")

### Features added[¶](#id384 "Link to this heading")

* Closures are fully supported for Python functions. Cython supports inner functions and lambda expressions. Generators and generator expressions are not supported in this release.
* Proper C++ support. Cython knows about C++ classes, templates and overloaded function signatures, so that Cython code can interact with them in a straight forward way.
* Type inference is enabled by default for safe C types (e.g. double, bint, C++ classes) and known extension types. This reduces the need for explicit type declarations and can improve the performance of untyped code in some cases. There is also a verbose compile mode for testing the impact on user code.
* Cython’s for-in-loop can iterate over C arrays and sliced pointers. The type of the loop variable will be inferred automatically in this case.
* The Py\_UNICODE integer type for Unicode code points is fully supported, including for-loops and ‘in’ tests on unicode strings. It coerces from and to single character unicode strings. Note that untyped for-loop variables will automatically be inferred as Py\_UNICODE when iterating over a unicode string. In most cases, this will be much more efficient than yielding sliced string objects, but can also have a negative performance impact when the variable is used in a Python context multiple times, so that it needs to coerce to a unicode string object more than once. If this happens, typing the loop variable as unicode or object will help.
* The built-in functions any(), all(), sum(), list(), set() and dict() are inlined as plain for loops when called on generator expressions. Note that generator expressions are not generally supported apart from this feature. Also, tuple(genexpr) is not currently supported - use tuple([listcomp]) instead.
* More shipped standard library declarations. The python\_\* and stdlib/stdio .pxd files have been deprecated in favor of clib.\* and cpython[.\*] and may get removed in a future release.
* Pure Python mode no longer disallows non-Python keywords like ‘cdef’, ‘include’ or ‘cimport’. It also no longer recognises syntax extensions like the for-from loop.
* Parsing has improved for Python 3 syntax in Python code, although not all features are correctly supported. The missing Python 3 features are being worked on for the next release.
* from \_\_future\_\_ import print\_function is supported in Python 2.6 and later. Note that there is currently no emulation for earlier Python versions, so code that uses print() with this future import will require at least Python 2.6.
* New compiler directive language\_level (valid values: 2 or 3) with corresponding command line options -2 and -3 requests source code compatibility with Python 2.x or Python 3.x respectively. Language level 3 currently enforces unicode literals for unprefixed string literals, enables the print function (requires Python 2.6 or later) and keeps loop variables in list comprehensions from leaking.
* Loop variables in set/dict comprehensions no longer leak into the surrounding scope (following Python 2.7). List comprehensions are unchanged in language level 2.
* print >> stream

### Bugs fixed[¶](#id385 "Link to this heading")

### Other changes[¶](#id386 "Link to this heading")

* The availability of type inference by default means that Cython will also infer the type of pointers on assignments. Previously, code like this:

  ```
  cdef char* s = ...
  untyped_variable = s
  ```

  would convert the char\* to a Python bytes string and assign that. This is no longer the case and no coercion will happen in the example above. The correct way of doing this is through an explicit cast or by typing the target variable, i.e.

  ```
  cdef char* s = ...
  untyped_variable1 = <bytes>s
  untyped_variable2 = <object>s

  cdef object py_object = s
  cdef bytes  bytes_string = s
  ```
* bool is no longer a valid type name by default. The problem is that it’s not clear whether bool should refer to the Python type or the C++ type, and expecting one and finding the other has already led to several hard-to-find bugs. Both types are available for importing: you can use from cpython cimport bool for the Python bool type, and from libcpp cimport bool for the C++ type. bool is still a valid object by default, so one can still write bool(x).
* `__getsegcount__` is now correctly typed to take a `Py_size_t*` rather than an `int*`.

## 0.12.1 (2010-02-02)[¶](#id387 "Link to this heading")

### Features added[¶](#id388 "Link to this heading")

* Type inference improvements.

  + There have been several bug fixes and improvements to the type inferencer.
  + Notably, there is now a “safe” mode enabled by setting the infer\_types directive to None. (The None here refers to the “default” mode, which will be the default in 0.13.) This safe mode limits inference to Python object types and C doubles, which should speed up execution without affecting any semantics such as integer overflow behavior like infer\_types=True might. There is also an infer\_types.verbose option which allows one to see what types are inferred.
* The boundscheck directive works for lists and tuples as well as buffers.
* len(s) and s.decode(“encoding”) are efficiently supported for char\* s.
* Cython’s INLINE macro has been renamed to CYTHON\_INLINE to reduce conflict and has better support for the MSVC compiler on Windows. It is no longer clobbered if externally defined.
* Revision history is now omitted from the source package, resulting in a 85% size reduction. Running make repo will download the history and turn the directory into a complete Mercurial working repository.
* Cython modules don’t need to be recompiled when the size of an external type grows. (A warning, rather than an error, is produced.) This should be helpful for binary distributions relying on NumPy.

### Bugs fixed[¶](#id389 "Link to this heading")

* Several other bugs and minor improvements have been made. This release should be fully backwards compatible with 0.12.

### Other changes[¶](#id390 "Link to this heading")

## 0.12 (2009-11-23)[¶](#id391 "Link to this heading")

### Features added[¶](#id392 "Link to this heading")

* Type inference with the infer\_types directive
* Seamless C++ complex support
* Fast extension type instantiation using the normal Python meme obj = MyType.\_\_new\_\_(MyType)
* Improved support for Py3.1
* Cython now runs under Python 3.x using the 2to3 tool
* unittest support for doctests in Cython modules
* Optimised handling of C strings (char\*): for c in cstring[2:50] and cstring.decode()
* Looping over c pointers: for i in intptr[:50].
* pyximport improvements
* cython\_freeze improvements

### Bugs fixed[¶](#id393 "Link to this heading")

* Many bug fixes

### Other changes[¶](#id394 "Link to this heading")

* Many other optimisation, e.g. enumerate() loops, parallel swap assignments (a,b = b,a), and unicode.encode()
* More complete numpy.pxd

## 0.11.2 (2009-05-20)[¶](#id395 "Link to this heading")

### Features added[¶](#id396 "Link to this heading")

* There’s now native complex floating point support! C99 complex will be used if complex.h is included, otherwise explicit complex arithmetic working on all C compilers is used. [Robert Bradshaw]

  ```
  cdef double complex a = 1 + 0.3j
  cdef np.ndarray[np.complex128_t, ndim=2] arr = \
     np.zeros(10, np.complex128)
  ```
* Cython can now generate a main()-method for embedding of the Python interpreter into an executable (see [#289](https://github.com/cython/cython/issues/289 "https://github.com/cython/cython/issues/289")) [Robert Bradshaw]
* @wraparound directive (another way to disable arr[idx] for negative idx) [Dag Sverre Seljebotn]
* Correct support for NumPy record dtypes with different alignments, and “cdef packed struct” support [Dag Sverre Seljebotn]
* @callspec directive, allowing custom calling convention macros [Lisandro Dalcin]

### Bugs fixed[¶](#id397 "Link to this heading")

### Other changes[¶](#id398 "Link to this heading")

* Bug fixes and smaller improvements. For the full list, see [1].

[![Logo](../_static/cythonlogo.png)](../index.html "../index.html")

### [Table of Contents](../index.html "../index.html")

* [Cython Changelog](# "#")
  + [3.2.0b1 (2025-10-??)](#b1-2025-10 "#b1-2025-10")
    - [Features added](#features-added "#features-added")
    - [Bugs fixed](#bugs-fixed "#bugs-fixed")
    - [Other changes](#other-changes "#other-changes")
  + [3.1.5 (2025-??-??)](#id1 "#id1")
    - [Bugs fixed](#id2 "#id2")
  + [3.1.4 (2025-09-16)](#id3 "#id3")
    - [Features added](#id4 "#id4")
    - [Bugs fixed](#id5 "#id5")
  + [3.1.3 (2025-08-13)](#id6 "#id6")
    - [Bugs fixed](#id7 "#id7")
  + [3.1.2 (2025-06-09)](#id8 "#id8")
    - [Bugs fixed](#id9 "#id9")
  + [3.1.1 (2025-05-19)](#id10 "#id10")
    - [Bugs fixed](#id11 "#id11")
  + [3.1.0 (2025-05-08)](#id12 "#id12")
    - [Other changes](#id13 "#id13")
  + [3.1.0 rc 2 (2025-05-07)](#rc-2-2025-05-07 "#rc-2-2025-05-07")
    - [Features added](#id14 "#id14")
    - [Bugs fixed](#id15 "#id15")
  + [3.1.0 rc 1 (2025-05-01)](#rc-1-2025-05-01 "#rc-1-2025-05-01")
    - [Features added](#id16 "#id16")
    - [Bugs fixed](#id17 "#id17")
    - [Other changes](#id18 "#id18")
  + [3.1.0 beta 1 (2025-04-03)](#beta-1-2025-04-03 "#beta-1-2025-04-03")
    - [Features added](#id19 "#id19")
    - [Bugs fixed](#id20 "#id20")
    - [Other changes](#id21 "#id21")
  + [3.1.0 alpha 1 (2024-11-08)](#alpha-1-2024-11-08 "#alpha-1-2024-11-08")
    - [Features added](#id22 "#id22")
    - [Bugs fixed](#id23 "#id23")
    - [Other changes](#id24 "#id24")
  + [3.0.12 (2025-02-11)](#id25 "#id25")
    - [Bugs fixed](#id26 "#id26")
  + [3.0.11 (2024-08-05)](#id27 "#id27")
    - [Features added](#id28 "#id28")
    - [Bugs fixed](#id29 "#id29")
  + [3.0.10 (2024-03-30)](#id30 "#id30")
    - [Bugs fixed](#id31 "#id31")
  + [3.0.9 (2024-03-05)](#id32 "#id32")
    - [Features added](#id33 "#id33")
    - [Bugs fixed](#id34 "#id34")
    - [Other changes](#id35 "#id35")
  + [3.0.8 (2024-01-10)](#id36 "#id36")
    - [Bugs fixed](#id37 "#id37")
  + [3.0.7 (2023-12-19)](#id38 "#id38")
    - [Bugs fixed](#id39 "#id39")
  + [3.0.6 (2023-11-26)](#id40 "#id40")
    - [Features added](#id41 "#id41")
    - [Bugs fixed](#id42 "#id42")
  + [3.0.5 (2023-10-31)](#id43 "#id43")
    - [Features added](#id44 "#id44")
    - [Bugs fixed](#id45 "#id45")
  + [3.0.4 (2023-10-17)](#id46 "#id46")
    - [Features added](#id47 "#id47")
    - [Bugs fixed](#id48 "#id48")
  + [3.0.3 (2023-10-05)](#id49 "#id49")
    - [Features added](#id50 "#id50")
    - [Bugs fixed](#id51 "#id51")
    - [Other changes](#id52 "#id52")
  + [3.0.2 (2023-08-27)](#id53 "#id53")
    - [Bugs fixed](#id54 "#id54")
  + [3.0.1 (2023-08-25)](#id55 "#id55")
    - [Features added](#id56 "#id56")
    - [Bugs fixed](#id57 "#id57")
  + [3.0.0 unified release notes](#unified-release-notes "#unified-release-notes")
  + [Major themes in 3.0.0](#major-themes-in-3-0-0 "#major-themes-in-3-0-0")
    - [Compatibility with CPython and the Python C API](#compatibility-with-cpython-and-the-python-c-api "#compatibility-with-cpython-and-the-python-c-api")
      * [Related changes](#related-changes "#related-changes")
    - [Compatibility with other Python implementations](#compatibility-with-other-python-implementations "#compatibility-with-other-python-implementations")
      * [Related changes](#id58 "#id58")
    - [Initial support for Limited API](#initial-support-for-limited-api "#initial-support-for-limited-api")
      * [Related changes](#id59 "#id59")
    - [Improved fidelity to Python semantics](#improved-fidelity-to-python-semantics "#improved-fidelity-to-python-semantics")
      * [Implemented PEPs](#implemented-peps "#implemented-peps")
      * [Related changes](#id60 "#id60")
    - [Improvements in Pure Python mode](#improvements-in-pure-python-mode "#improvements-in-pure-python-mode")
      * [Related changes](#id61 "#id61")
    - [Code generation changes](#code-generation-changes "#code-generation-changes")
      * [Related changes](#id62 "#id62")
    - [Interaction with numpy](#interaction-with-numpy "#interaction-with-numpy")
      * [Related changes](#id63 "#id63")
    - [Exception handling](#exception-handling "#exception-handling")
      * [Related changes](#id64 "#id64")
    - [Optimizations](#optimizations "#optimizations")
      * [Related changes](#id65 "#id65")
    - [Compatibility with C](#compatibility-with-c "#compatibility-with-c")
      * [Related changes](#id66 "#id66")
    - [Compatibility with C++](#id67 "#id67")
      * [Related changes](#id68 "#id68")
    - [Commandline Interface](#commandline-interface "#commandline-interface")
      * [Related changes](#id69 "#id69")
    - [Build integration](#build-integration "#build-integration")
      * [Related changes](#id70 "#id70")
    - [Deprecations](#deprecations "#deprecations")
      * [Related changes](#id71 "#id71")
    - [Editor support](#editor-support "#editor-support")
      * [Related changes](#id72 "#id72")
    - [Other changes](#id73 "#id73")
  + [3.0.0 (2023-07-17)](#id74 "#id74")
    - [Bugs fixed](#id75 "#id75")
  + [3.0.0 rc 2 (2023-07-13)](#rc-2-2023-07-13 "#rc-2-2023-07-13")
    - [Bugs fixed](#id76 "#id76")
  + [3.0.0 rc 1 (2023-07-12)](#rc-1-2023-07-12 "#rc-1-2023-07-12")
    - [Features added](#id77 "#id77")
    - [Bugs fixed](#id78 "#id78")
    - [Other changes](#id79 "#id79")
  + [3.0.0 beta 3 (2023-05-24)](#beta-3-2023-05-24 "#beta-3-2023-05-24")
    - [Features added](#id80 "#id80")
    - [Bugs fixed](#id81 "#id81")
    - [Other changes](#id82 "#id82")
  + [3.0.0 beta 2 (2023-03-27)](#beta-2-2023-03-27 "#beta-2-2023-03-27")
    - [Features added](#id83 "#id83")
    - [Bugs fixed](#id84 "#id84")
  + [3.0.0 beta 1 (2023-02-25)](#beta-1-2023-02-25 "#beta-1-2023-02-25")
    - [Features added](#id85 "#id85")
    - [Bugs fixed](#id86 "#id86")
    - [Other changes](#id87 "#id87")
  + [3.0.0 alpha 11 (2022-07-31)](#alpha-11-2022-07-31 "#alpha-11-2022-07-31")
    - [Features added](#id88 "#id88")
    - [Bugs fixed](#id89 "#id89")
    - [Other changes](#id90 "#id90")
  + [3.0.0 alpha 10 (2022-01-06)](#alpha-10-2022-01-06 "#alpha-10-2022-01-06")
    - [Features added](#id91 "#id91")
    - [Bugs fixed](#id92 "#id92")
    - [Other changes](#id93 "#id93")
  + [3.0.0 alpha 9 (2021-07-21)](#alpha-9-2021-07-21 "#alpha-9-2021-07-21")
    - [Features added](#id94 "#id94")
    - [Bugs fixed](#id95 "#id95")
    - [Other changes](#id96 "#id96")
  + [3.0.0 alpha 8 (2021-07-02)](#alpha-8-2021-07-02 "#alpha-8-2021-07-02")
    - [Features added](#id97 "#id97")
    - [Bugs fixed](#id98 "#id98")
    - [Other changes](#id99 "#id99")
  + [3.0.0 alpha 7 (2021-05-24)](#alpha-7-2021-05-24 "#alpha-7-2021-05-24")
    - [Features added](#id100 "#id100")
    - [Bugs fixed](#id101 "#id101")
  + [3.0.0 alpha 6 (2020-07-31)](#alpha-6-2020-07-31 "#alpha-6-2020-07-31")
    - [Features added](#id102 "#id102")
    - [Bugs fixed](#id103 "#id103")
    - [Other changes](#id104 "#id104")
  + [3.0.0 alpha 5 (2020-05-19)](#alpha-5-2020-05-19 "#alpha-5-2020-05-19")
    - [Features added](#id105 "#id105")
    - [Bugs fixed](#id106 "#id106")
  + [3.0.0 alpha 4 (2020-05-05)](#alpha-4-2020-05-05 "#alpha-4-2020-05-05")
    - [Features added](#id107 "#id107")
    - [Bugs fixed](#id108 "#id108")
    - [Other changes](#id109 "#id109")
  + [3.0.0 alpha 3 (2020-04-27)](#alpha-3-2020-04-27 "#alpha-3-2020-04-27")
    - [Features added](#id110 "#id110")
    - [Bugs fixed](#id111 "#id111")
  + [3.0.0 alpha 2 (2020-04-23)](#alpha-2-2020-04-23 "#alpha-2-2020-04-23")
    - [Features added](#id112 "#id112")
    - [Bugs fixed](#id113 "#id113")
  + [3.0.0 alpha 1 (2020-04-12)](#alpha-1-2020-04-12 "#alpha-1-2020-04-12")
    - [Features added](#id114 "#id114")
    - [Bugs fixed](#id115 "#id115")
    - [Other changes](#id116 "#id116")
  + [0.29.37 (2023-12-18)](#id124 "#id124")
    - [Bugs fixed](#id126 "#id126")
  + [0.29.36 (2023-07-04)](#id127 "#id127")
    - [Bugs fixed](#id129 "#id129")
  + [0.29.35 (2023-05-24)](#id130 "#id130")
    - [Bugs fixed](#id132 "#id132")
  + [0.29.34 (2023-04-02)](#id133 "#id133")
    - [Bugs fixed](#id135 "#id135")
  + [0.29.33 (2023-01-06)](#id136 "#id136")
    - [Features added](#id138 "#id138")
    - [Bugs fixed](#id139 "#id139")
    - [Other changes](#id140 "#id140")
  + [0.29.32 (2022-07-29)](#id141 "#id141")
    - [Bugs fixed](#id143 "#id143")
  + [0.29.31 (2022-07-27)](#id144 "#id144")
    - [Features added](#id146 "#id146")
    - [Bugs fixed](#id147 "#id147")
  + [0.29.30 (2022-05-16)](#id148 "#id148")
    - [Bugs fixed](#id150 "#id150")
  + [0.29.29 (2022-05-16)](#id151 "#id151")
    - [Features added](#id153 "#id153")
    - [Bugs fixed](#id154 "#id154")
  + [0.29.28 (2022-02-17)](#id155 "#id155")
    - [Bugs fixed](#id157 "#id157")
  + [0.29.27 (2022-01-28)](#id158 "#id158")
    - [Features added](#id160 "#id160")
    - [Bugs fixed](#id161 "#id161")
  + [0.29.26 (2021-12-16)](#id162 "#id162")
    - [Bugs fixed](#id164 "#id164")
  + [0.29.25 (2021-12-06)](#id165 "#id165")
    - [Bugs fixed](#id167 "#id167")
  + [0.29.24 (2021-07-14)](#id168 "#id168")
    - [Bugs fixed](#id170 "#id170")
  + [0.29.23 (2021-04-14)](#id171 "#id171")
    - [Bugs fixed](#id173 "#id173")
  + [0.29.22 (2021-02-20)](#id174 "#id174")
    - [Features added](#id176 "#id176")
    - [Bugs fixed](#id177 "#id177")
    - [Other changes](#id178 "#id178")
  + [0.29.21 (2020-07-09)](#id179 "#id179")
    - [Bugs fixed](#id181 "#id181")
  + [0.29.20 (2020-06-10)](#id182 "#id182")
    - [Bugs fixed](#id184 "#id184")
  + [0.29.19 (2020-05-20)](#id185 "#id185")
    - [Bugs fixed](#id187 "#id187")
  + [0.29.18 (2020-05-18)](#id188 "#id188")
    - [Bugs fixed](#id190 "#id190")
  + [0.29.17 (2020-04-26)](#id191 "#id191")
    - [Features added](#id193 "#id193")
    - [Bugs fixed](#id194 "#id194")
  + [0.29.16 (2020-03-24)](#id195 "#id195")
    - [Bugs fixed](#id197 "#id197")
  + [0.29.15 (2020-02-06)](#id198 "#id198")
    - [Bugs fixed](#id200 "#id200")
  + [0.29.14 (2019-11-01)](#id201 "#id201")
    - [Bugs fixed](#id203 "#id203")
    - [Other changes](#id204 "#id204")
  + [0.29.13 (2019-07-26)](#id205 "#id205")
    - [Bugs fixed](#id206 "#id206")
    - [Other changes](#id207 "#id207")
  + [0.29.12 (2019-07-07)](#id208 "#id208")
    - [Bugs fixed](#id209 "#id209")
  + [0.29.11 (2019-06-30)](#id210 "#id210")
    - [Bugs fixed](#id211 "#id211")
  + [0.29.10 (2019-06-02)](#id212 "#id212")
    - [Bugs fixed](#id213 "#id213")
  + [0.29.9 (2019-05-29)](#id214 "#id214")
    - [Bugs fixed](#id215 "#id215")
  + [0.29.8 (2019-05-28)](#id216 "#id216")
    - [Bugs fixed](#id217 "#id217")
  + [0.29.7 (2019-04-14)](#id218 "#id218")
    - [Bugs fixed](#id219 "#id219")
  + [0.29.6 (2019-02-27)](#id220 "#id220")
    - [Bugs fixed](#id221 "#id221")
  + [0.29.5 (2019-02-09)](#id222 "#id222")
    - [Bugs fixed](#id223 "#id223")
  + [0.29.4 (2019-02-01)](#id224 "#id224")
    - [Bugs fixed](#id225 "#id225")
  + [0.29.3 (2019-01-19)](#id226 "#id226")
    - [Bugs fixed](#id227 "#id227")
  + [0.29.2 (2018-12-14)](#id228 "#id228")
    - [Bugs fixed](#id229 "#id229")
  + [0.29.1 (2018-11-24)](#id230 "#id230")
    - [Bugs fixed](#id231 "#id231")
  + [0.29 (2018-10-14)](#id232 "#id232")
    - [Features added](#id233 "#id233")
    - [Bugs fixed](#id234 "#id234")
    - [Other changes](#id235 "#id235")
  + [0.28.6 (2018-11-01)](#id236 "#id236")
    - [Bugs fixed](#id237 "#id237")
  + [0.28.5 (2018-08-03)](#id238 "#id238")
    - [Bugs fixed](#id239 "#id239")
  + [0.28.4 (2018-07-08)](#id240 "#id240")
    - [Bugs fixed](#id241 "#id241")
  + [0.28.3 (2018-05-27)](#id242 "#id242")
    - [Bugs fixed](#id243 "#id243")
  + [0.28.2 (2018-04-13)](#id244 "#id244")
    - [Features added](#id245 "#id245")
    - [Bugs fixed](#id246 "#id246")
    - [Other changes](#id247 "#id247")
  + [0.28.1 (2018-03-18)](#id248 "#id248")
    - [Bugs fixed](#id249 "#id249")
  + [0.28 (2018-03-13)](#id250 "#id250")
    - [Features added](#id251 "#id251")
    - [Bugs fixed](#id252 "#id252")
    - [Other changes](#id253 "#id253")
  + [0.27.3 (2017-11-03)](#id254 "#id254")
    - [Bugs fixed](#id255 "#id255")
  + [0.27.2 (2017-10-22)](#id256 "#id256")
    - [Bugs fixed](#id257 "#id257")
  + [0.27.1 (2017-10-01)](#id258 "#id258")
    - [Features added](#id259 "#id259")
    - [Bugs fixed](#id260 "#id260")
    - [Other changes](#id261 "#id261")
  + [0.27 (2017-09-23)](#id262 "#id262")
    - [Features added](#id263 "#id263")
    - [Bugs fixed](#id264 "#id264")
    - [Other changes](#id265 "#id265")
  + [0.26.1 (2017-08-29)](#id267 "#id267")
    - [Features added](#id268 "#id268")
    - [Bugs fixed](#id269 "#id269")
  + [0.26 (2017-07-19)](#id270 "#id270")
    - [Features added](#id271 "#id271")
    - [Bugs fixed](#id272 "#id272")
    - [Other changes](#id273 "#id273")
  + [0.25.2 (2016-12-08)](#id274 "#id274")
    - [Bugs fixed](#id275 "#id275")
  + [0.25.1 (2016-10-26)](#id276 "#id276")
    - [Bugs fixed](#id277 "#id277")
    - [Other changes](#id278 "#id278")
  + [0.25 (2016-10-25)](#id279 "#id279")
    - [Features added](#id280 "#id280")
    - [Significant Bugs fixed](#significant-bugs-fixed "#significant-bugs-fixed")
    - [Other changes](#id281 "#id281")
  + [0.24.1 (2016-07-15)](#id282 "#id282")
    - [Bugs fixed](#id283 "#id283")
  + [0.24 (2016-04-04)](#id284 "#id284")
    - [Features added](#id285 "#id285")
    - [Bugs fixed](#id286 "#id286")
  + [0.23.5 (2016-03-26)](#id287 "#id287")
  + [0.23.4 (2015-10-10)](#id288 "#id288")
    - [Bugs fixed](#id289 "#id289")
  + [0.23.3 (2015-09-29)](#id290 "#id290")
    - [Bugs fixed](#id291 "#id291")
    - [Other changes](#id292 "#id292")
  + [0.23.2 (2015-09-11)](#id293 "#id293")
    - [Bugs fixed](#id294 "#id294")
  + [0.23.1 (2015-08-22)](#id295 "#id295")
    - [Bugs fixed](#id296 "#id296")
  + [0.23 (2015-08-08)](#id297 "#id297")
    - [Features added](#id298 "#id298")
    - [Bugs fixed](#id300 "#id300")
    - [Other changes](#id301 "#id301")
  + [0.22.1 (2015-06-20)](#id302 "#id302")
    - [Bugs fixed](#id303 "#id303")
  + [0.22 (2015-02-11)](#id304 "#id304")
    - [Features added](#id305 "#id305")
    - [Bugs fixed](#id307 "#id307")
    - [Other changes](#id308 "#id308")
  + [0.21.2 (2014-12-27)](#id309 "#id309")
    - [Bugs fixed](#id310 "#id310")
  + [0.21.1 (2014-10-18)](#id311 "#id311")
    - [Features added](#id312 "#id312")
    - [Bugs fixed](#id313 "#id313")
    - [Other changes](#id314 "#id314")
  + [0.21 (2014-09-10)](#id315 "#id315")
    - [Features added](#id316 "#id316")
    - [Optimizations](#id317 "#id317")
    - [Bugs fixed](#id318 "#id318")
    - [Other changes](#id319 "#id319")
  + [0.20.2 (2014-06-16)](#id320 "#id320")
    - [Features added](#id321 "#id321")
    - [Bugs fixed](#id322 "#id322")
  + [0.20.1 (2014-02-11)](#id323 "#id323")
    - [Bugs fixed](#id324 "#id324")
  + [0.20 (2014-01-18)](#id325 "#id325")
    - [Features added](#id326 "#id326")
    - [Bugs fixed](#id327 "#id327")
    - [Other changes](#id328 "#id328")
  + [0.19.2 (2013-10-13)](#id329 "#id329")
    - [Features added](#id330 "#id330")
    - [Bugs fixed](#id331 "#id331")
    - [Other changes](#id332 "#id332")
  + [0.19.1 (2013-05-11)](#id333 "#id333")
    - [Features added](#id334 "#id334")
    - [Bugs fixed](#id335 "#id335")
    - [Other changes](#id336 "#id336")
  + [0.19 (2013-04-19)](#id337 "#id337")
    - [Features added](#id338 "#id338")
    - [Bugs fixed](#id339 "#id339")
    - [Other changes](#id340 "#id340")
  + [0.18 (2013-01-28)](#id341 "#id341")
    - [Features added](#id342 "#id342")
    - [Bugs fixed](#id343 "#id343")
    - [Other changes](#id344 "#id344")
  + [0.17.4 (2013-01-03)](#id345 "#id345")
    - [Bugs fixed](#id346 "#id346")
  + [0.17.3 (2012-12-14)](#id347 "#id347")
    - [Features added](#id348 "#id348")
    - [Bugs fixed](#id349 "#id349")
    - [Other changes](#id350 "#id350")
  + [0.17.2 (2012-11-20)](#id351 "#id351")
    - [Features added](#id352 "#id352")
    - [Bugs fixed](#id353 "#id353")
    - [Other changes](#id354 "#id354")
  + [0.17.1 (2012-09-26)](#id355 "#id355")
    - [Features added](#id356 "#id356")
    - [Bugs fixed](#id357 "#id357")
    - [Other changes](#id358 "#id358")
  + [0.17 (2012-09-01)](#id359 "#id359")
    - [Features added](#id360 "#id360")
    - [Bugs fixed](#id361 "#id361")
    - [Other changes](#id362 "#id362")
  + [0.16 (2012-04-21)](#id363 "#id363")
    - [Features added](#id364 "#id364")
    - [Bugs fixed](#id365 "#id365")
    - [Other changes](#id366 "#id366")
  + [0.15.1 (2011-09-19)](#id367 "#id367")
    - [Features added](#id368 "#id368")
    - [Bugs fixed](#id369 "#id369")
    - [Other changes](#id370 "#id370")
  + [0.15 (2011-08-05)](#id371 "#id371")
    - [Features added](#id372 "#id372")
    - [Bugs fixed](#id373 "#id373")
    - [Other changes](#id374 "#id374")
  + [0.14.1 (2011-02-04)](#id375 "#id375")
    - [Features added](#id376 "#id376")
    - [Bugs fixed](#id377 "#id377")
    - [Other changes](#id378 "#id378")
  + [0.14 (2010-12-14)](#id379 "#id379")
    - [Features added](#id380 "#id380")
    - [Bugs fixed](#id381 "#id381")
    - [Other changes](#id382 "#id382")
  + [0.13 (2010-08-25)](#id383 "#id383")
    - [Features added](#id384 "#id384")
    - [Bugs fixed](#id385 "#id385")
    - [Other changes](#id386 "#id386")
  + [0.12.1 (2010-02-02)](#id387 "#id387")
    - [Features added](#id388 "#id388")
    - [Bugs fixed](#id389 "#id389")
    - [Other changes](#id390 "#id390")
  + [0.12 (2009-11-23)](#id391 "#id391")
    - [Features added](#id392 "#id392")
    - [Bugs fixed](#id393 "#id393")
    - [Other changes](#id394 "#id394")
  + [0.11.2 (2009-05-20)](#id395 "#id395")
    - [Features added](#id396 "#id396")
    - [Bugs fixed](#id397 "#id397")
    - [Other changes](#id398 "#id398")

#### Previous topic

[The Test Suite](devguide/tests.html "previous chapter")

### This Page

* [Show Source](../_sources/src/changes.rst.txt "../_sources/src/changes.rst.txt")

### Quick search

### Navigation

* [previous](devguide/tests.html "The Test Suite")
* [Cython 3.2.0b1 documentation](../index.html "../index.html") »
* Cython Changelog

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

