




Special Methods of Extension Types — Cython 3.1.4 documentation

### Navigation

* [next](sharing_declarations.html "Sharing Declarations Between Cython Modules")
* [previous](extension_types.html "Extension Types") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Special Methods of Extension Types

🤝 Like the tool? Help making it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Special Methods of Extension Types[¶](#special-methods-of-extension-types "Link to this heading")

Note

This page uses two different syntax variants:

* Cython specific `cdef` syntax, which was designed to make type declarations
  concise and easily readable from a C/C++ perspective.
* Pure Python syntax which allows static Cython type declarations in
  [pure Python code](../tutorial/pure.html#pep484-type-annotations "../tutorial/pure.html#pep484-type-annotations"),
  following [PEP-484](https://www.python.org/dev/peps/pep-0484/ "https://www.python.org/dev/peps/pep-0484/") type hints
  and [PEP 526](https://www.python.org/dev/peps/pep-0526/ "https://www.python.org/dev/peps/pep-0526/") variable annotations.

  To make use of C data types in Python syntax, you need to import the special
  `cython` module in the Python module that you want to compile, e.g.

  ```
  import cython
  ```

  If you use the pure Python syntax we strongly recommend you use a recent
  Cython 3 release, since significant improvements have been made here
  compared to the 0.29.x releases.

This page describes the special methods currently supported by Cython extension
types. A complete list of all the special methods appears in the table at the
bottom. Some of these methods behave differently from their Python
counterparts or have no direct Python counterparts, and require special
mention.

Note

Everything said on this page applies only to extension types, defined
with the [`cdef`](language_basics.html#cdef "language_basics.html#cdef") class statement or decorated using `@cclass` decorator.
It doesn’t apply to classes defined with the
Python [`class`](https://docs.python.org/3/reference/compound_stmts.html#class "(in Python v3.13)") statement, where the normal Python rules apply.

## Declaration[¶](#declaration "Link to this heading")

Special methods of extension types must be declared with [`def`](https://docs.python.org/3/reference/compound_stmts.html#def "(in Python v3.13)"), not
[`cdef`](language_basics.html#cdef "language_basics.html#cdef")/`@cfunc`. This does not impact their performance–Python uses different
calling conventions to invoke these special methods.

## Docstrings[¶](#docstrings "Link to this heading")

Currently, docstrings are not fully supported in some special methods of extension
types. You can place a docstring in the source to serve as a comment, but it
won’t show up in the corresponding `__doc__` attribute at run time. (This
seems to be is a Python limitation – there’s nowhere in the [`PyTypeObject`](https://docs.python.org/3/c-api/type.html#c.PyTypeObject "(in Python v3.13)")
data structure to put such docstrings.)

## Initialisation methods: `__cinit__()` and `__init__()`[¶](#initialisation-methods-cinit-and-init "Link to this heading")

There are two methods concerned with initialising the object, the normal Python
`__init__()` method and a special `__cinit__()` method where basic
C level initialisation can be performed.

The main difference between the two is when they are called.
The `__cinit__()` method is guaranteed to be called as part of the object
allocation, but before the object is fully initialised. Specifically, methods
and object attributes that belong to subclasses or that were overridden by
subclasses may not have been initialised at all yet and must not be used by
`__cinit__()` in a base class. Note that the object allocation in Python
clears all fields and sets them to zero (or `NULL`). Cython additionally
takes responsibility of setting all object attributes to `None`, but again,
this may not yet have been done for the attributes defined or overridden by
subclasses. If your object needs anything more than this basic attribute
clearing in order to get into a correct and safe state, `__cinit__()`
may be a good place to do it.

The `__init__()` method, on the other hand, works exactly like in Python.
It is called after allocation and basic initialisation of the object, including
the complete inheritance chain.
By the time `__init__()` is called, the object is a fully valid Python object
and all operations are safe. Any initialisation which cannot safely be done in
the `__cinit__()` method should be done in the `__init__()` method.
However, as in Python, it is the responsibility of the subclasses to call up the
hierarchy and make sure that the `__init__()` methods in the base class are
called correctly. If a subclass forgets (or refuses) to call the `__init__()`
method of one of its base classes, that method will not be called.
Also, if the object gets created by calling directly its `__new__()` method [[1]](#id4 "#id4")
(as opposed to calling the class itself), then none of the `__init__()`
methods will be called.

The `__cinit__()` method is where you should perform basic safety C-level
initialisation of the object, possibly including allocation of any C data
structures that your object will own. In contrast to `__init__()`,
your `__cinit__()` method is guaranteed to be called exactly once.

If your extension type has a base type, any existing `__cinit__()` methods in
the base type hierarchy are automatically called before your `__cinit__()`
method. You cannot explicitly call the inherited `__cinit__()` methods, and the
base types are free to choose whether they implement `__cinit__()` at all.
If you need to pass a modified argument list to the base type, you will have to do
the relevant part of the initialisation in the `__init__()` method instead,
where the normal rules for calling inherited methods apply.

Any arguments passed to the constructor will be passed to both the
`__cinit__()` method and the `__init__()` method. If you anticipate
subclassing your extension type, you may find it useful to give the
`__cinit__()` method `*` and `**` arguments so that it can accept and
ignore arbitrary extra arguments, since the arguments that are passed through
the hierarchy during allocation cannot be changed by subclasses.
Alternatively, as a convenience, if you declare your `__cinit__()` method
to take no arguments (other than self) it will simply ignore any extra arguments
passed to the constructor without complaining about the signature mismatch.

Note

All constructor arguments will be passed as Python objects.
This implies that non-convertible C types such as pointers or C++ objects
cannot be passed into the constructor, neither from Python nor from Cython code.
If this is needed, use a factory function or method instead that handles the
object initialisation.
It often helps to directly call the `__new__()` method in this function to
explicitly bypass the call to the `__init__()` constructor.

See [Instantiation from existing C/C++ pointers](extension_types.html#existing-pointers-instantiation "extension_types.html#existing-pointers-instantiation") for an example.

Note

Implementing a `__cinit__()` method currently excludes the type from
[auto-pickling](extension_types.html#auto-pickle "extension_types.html#auto-pickle").

[[1](#id3 "#id3")]

[https://docs.python.org/reference/datamodel.html#object.\_\_new\_\_](https://docs.python.org/reference/datamodel.html#object.__new__ "https://docs.python.org/reference/datamodel.html#object.__new__")

## Finalization methods: `__dealloc__()` and `__del__()`[¶](#finalization-methods-dealloc-and-del "Link to this heading")

The counterpart to the `__cinit__()` method is the `__dealloc__()`
method, which should perform the inverse of the `__cinit__()` method. Any
C data that you explicitly allocated (e.g. via malloc) in your
`__cinit__()` method should be freed in your `__dealloc__()` method.

You need to be careful what you do in a `__dealloc__()` method. By the time your
`__dealloc__()` method is called, the object may already have been partially
destroyed and may not be in a valid state as far as Python is concerned, so
you should avoid invoking any Python operations which might touch the object.
In particular, don’t call any other methods of the object or do anything which
might cause the object to be resurrected. It’s best if you stick to just
deallocating C data.

You don’t need to worry about deallocating Python attributes of your object,
because that will be done for you by Cython after your `__dealloc__()` method
returns.

When subclassing extension types, be aware that the `__dealloc__()` method
of the superclass will always be called, even if it is overridden. This is in
contrast to typical Python behavior where superclass methods will not be
executed unless they are explicitly called by the subclass.

Python 3.4 made it possible for extension types to safely define
finalizers for objects. When running a Cython module on Python 3.4 and
higher you can add a `__del__()` method to extension types in
order to perform Python cleanup operations. When the `__del__()`
is called the object is still in a valid state (unlike in the case of
`__dealloc__()`), permitting the use of Python operations
on its class members. On Python <3.4 `__del__()` will not be called.

## Arithmetic methods[¶](#arithmetic-methods "Link to this heading")

Arithmetic operator methods, such as `__add__()`, used to behave differently
from their Python counterparts in Cython 0.x, following the low-level semantics
of the C-API slot functions. Since Cython 3.0, they are called in the same way
as in Python, including the separate “reversed” versions of these methods
(`__radd__()`, etc.).

Previously, if the first operand could not perform the operation, the same method
of the second operand was called, with the operands in the same order.
This means that you could not rely on the first parameter of these methods being
“self” or being the right type, and you needed to test the types of both operands
before deciding what to do.

If backwards compatibility is needed, the normal operator method (`__add__`, etc.)
can still be implemented to support both variants, applying a type check to the
arguments. The reversed method (`__radd__`, etc.) can always be implemented
with `self` as first argument and will be ignored by older Cython versions, whereas
Cython 3.x and later will only call the normal method with the expected argument order,
and otherwise call the reversed method instead.

Alternatively, the old Cython 0.x (or native C-API) behaviour is still available with
the directive `c_api_binop_methods=True`.

If you can’t handle the combination of types you’ve been given, you should return
`NotImplemented`. This will let Python’s operator implementation first try to apply
the reversed operator to the second operand, and failing that as well, report an
appropriate error to the user.

This change in behaviour also applies to the in-place arithmetic method `__ipow__()`.
It does not apply to any of the other in-place methods (`__iadd__()`, etc.)
which always take `self` as the first argument.

## Rich comparisons[¶](#rich-comparisons "Link to this heading")

There are a few ways to implement comparison methods.
Depending on the application, one way or the other may be better:

* Use the 6 Python
  [special methods](https://docs.python.org/3/reference/datamodel.html#basic-customization "https://docs.python.org/3/reference/datamodel.html#basic-customization")
  `__eq__()`, `__lt__()`, etc.
  This is supported since Cython 0.27 and works exactly as in plain Python classes.
* Use a single special method `__richcmp__()`.
  This implements all rich comparison operations in one method.
  The signature is `def __richcmp__(self, other, int op)`.
  The integer argument `op` indicates which operation is to be performed
  as shown in the table below:

   <  Py\_LT  ==  Py\_EQ  >  Py\_GT  <=  Py\_LE  !=  Py\_NE  >=  Py\_GE 

  These constants can be cimported from the `cpython.object` module.
* If you use the [functools.total\_ordering](https://docs.python.org/3/library/functools.html#functools.total_ordering "https://docs.python.org/3/library/functools.html#functools.total_ordering")
  decorator on an extension type/`cdef` class, Cython replaces it with a low-level reimplementation
  designed specifically for extension types. (On a normal Python classes, the `functools`
  decorator continues to work as before.) As a shortcut you can also use `cython.total_ordering`, which
  applies the same re-implementation but also transforms the class to an extension type if it
  isn’t already.

Pure PythonCython

```
import functools
import cython

@functools.total_ordering
@cython.cclass
class ExtGe:
    x: cython.int

    def __ge__(self, other):
        if not isinstance(other, ExtGe):
            return NotImplemented
        return self.x >= cython.cast(ExtGe, other).x

    def __eq__(self, other):
        return isinstance(other, ExtGe) and self.x == cython.cast(ExtGe, other).x
```

```
import functools



@functools.total_ordering
cdef class ExtGe:
    cdef int x

    def __ge__(self, other):
        if not isinstance(other, ExtGe):
            return NotImplemented
        return self.x >= (<ExtGe>other).x

    def __eq__(self, other):
        return isinstance(other, ExtGe) and self.x == (<ExtGe>other).x
```

## The `__next__()` method[¶](#the-next-method "Link to this heading")

Extension types wishing to implement the iterator interface should define a
method called `__next__()`, not next. The Python system will automatically
supply a next method which calls your `__next__()`. Do NOT explicitly
give your type a `next()` method, or bad things could happen.

## Special Method Table[¶](#special-method-table "Link to this heading")

This table lists all of the special methods together with their parameter and
return types. In the table below, a parameter name of self is used to indicate
that the parameter has the type that the method belongs to. Other parameters
with no type specified in the table are generic Python objects.

You don’t have to declare your method as taking these parameter types. If you
declare different types, conversions will be performed as necessary.

### General[¶](#general "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#special-method-names](https://docs.python.org/3/reference/datamodel.html#special-method-names "https://docs.python.org/3/reference/datamodel.html#special-method-names")

 Name  Parameters  Return type  Description  \_\_cinit\_\_  self, …  Basic initialisation (no direct Python equivalent)  \_\_init\_\_  self, …  Further initialisation  \_\_dealloc\_\_  self  Basic deallocation (no direct Python equivalent)  \_\_cmp\_\_  x, y  int  3-way comparison (Python 2 only)  \_\_str\_\_  self  object  str(self)  \_\_repr\_\_  self  object  repr(self)  \_\_hash\_\_  self  Py\_hash\_t  Hash function (returns 32/64 bit integer)  \_\_call\_\_  self, …  object  self(…)  \_\_iter\_\_  self  object  Return iterator for sequence  \_\_getattr\_\_  self, name  object  Get attribute  \_\_getattribute\_\_  self, name  object  Get attribute, unconditionally  \_\_setattr\_\_  self, name, val  Set attribute  \_\_delattr\_\_  self, name  Delete attribute 

### Rich comparison operators[¶](#rich-comparison-operators "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#basic-customization](https://docs.python.org/3/reference/datamodel.html#basic-customization "https://docs.python.org/3/reference/datamodel.html#basic-customization")

You can choose to either implement the standard Python special methods
like `__eq__()` or the single special method `__richcmp__()`.
Depending on the application, one way or the other may be better.

 Name  Parameters  Return type  Description  \_\_eq\_\_  self, y  object  self == y  \_\_ne\_\_  self, y  object  self != y (falls back to `__eq__` if not available)  \_\_lt\_\_  self, y  object  self < y  \_\_gt\_\_  self, y  object  self > y  \_\_le\_\_  self, y  object  self <= y  \_\_ge\_\_  self, y  object  self >= y  \_\_richcmp\_\_  self, y, int op  object  Joined rich comparison method for all of the above
(no direct Python equivalent) 

### Arithmetic operators[¶](#arithmetic-operators "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types "https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types")

 Name  Parameters  Return type  Description  \_\_add\_\_, \_\_radd\_\_  self, other  object  binary + operator  \_\_sub\_\_, \_\_rsub\_\_  self, other  object  binary - operator  \_\_mul\_\_, \_\_rmul\_\_  self, other  object  \* operator  \_\_div\_\_, \_\_rdiv\_\_  self, other  object  / operator for old-style division  \_\_floordiv\_\_, \_\_rfloordiv\_\_  self, other  object  // operator  \_\_truediv\_\_, \_\_rtruediv\_\_  self, other  object  / operator for new-style division  \_\_mod\_\_, \_\_rmod\_\_  self, other  object  % operator  \_\_divmod\_\_, \_\_rdivmod\_\_  self, other  object  combined div and mod  \_\_pow\_\_, \_\_rpow\_\_  self, other, [mod]  object  \*\* operator or pow(x, y, [mod])  \_\_neg\_\_  self  object  unary - operator  \_\_pos\_\_  self  object  unary + operator  \_\_abs\_\_  self  object  absolute value  \_\_nonzero\_\_  self  int  convert to boolean  \_\_invert\_\_  self  object  ~ operator  \_\_lshift\_\_, \_\_rlshift\_\_  self, other  object  << operator  \_\_rshift\_\_, \_\_rrshift\_\_  self, other  object  >> operator  \_\_and\_\_, \_\_rand\_\_  self, other  object  & operator  \_\_or\_\_, \_\_ror\_\_  self, other  object  | operator  \_\_xor\_\_, \_\_rxor\_\_  self, other  object  ^ operator 

Note that Cython 0.x did not make use of the `__r...__` variants and instead
used the bidirectional C slot signature for the regular methods, thus making the
first argument ambiguous (not ‘self’ typed).
Since Cython 3.0, the operator calls are passed to the respective special methods.
See the section on [Arithmetic methods](#arithmetic-methods "#arithmetic-methods") above.
Cython 0.x also did not support the 2 argument version of `__pow__` and
`__rpow__`, or the 3 argument version of `__ipow__`.

### Numeric conversions[¶](#numeric-conversions "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types "https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types")

 Name  Parameters  Return type  Description  \_\_int\_\_  self  object  Convert to integer  \_\_long\_\_  self  object  Convert to long integer  \_\_float\_\_  self  object  Convert to float  \_\_oct\_\_  self  object  Convert to octal  \_\_hex\_\_  self  object  Convert to hexadecimal  \_\_index\_\_  self  object  Convert to sequence index 

### In-place arithmetic operators[¶](#in-place-arithmetic-operators "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types](https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types "https://docs.python.org/3/reference/datamodel.html#emulating-numeric-types")

 Name  Parameters  Return type  Description  \_\_iadd\_\_  self, x  object  += operator  \_\_isub\_\_  self, x  object  -= operator  \_\_imul\_\_  self, x  object  \*= operator  \_\_idiv\_\_  self, x  object  /= operator for old-style division  \_\_ifloordiv\_\_  self, x  object  //= operator  \_\_itruediv\_\_  self, x  object  /= operator for new-style division  \_\_imod\_\_  self, x  object  %= operator  \_\_ipow\_\_  self, y, [z]  object  \*\*= operator (3-arg form only on Python >= 3.8)  \_\_ilshift\_\_  self, x  object  <<= operator  \_\_irshift\_\_  self, x  object  >>= operator  \_\_iand\_\_  self, x  object  &= operator  \_\_ior\_\_  self, x  object  |= operator  \_\_ixor\_\_  self, x  object  ^= operator 

### Sequences and mappings[¶](#sequences-and-mappings "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#emulating-container-types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types "https://docs.python.org/3/reference/datamodel.html#emulating-container-types")

 Name  Parameters  Return type  Description  \_\_len\_\_  self  Py\_ssize\_t  len(self)  \_\_getitem\_\_  self, x  object  self[x]  \_\_setitem\_\_  self, x, y  self[x] = y  \_\_delitem\_\_  self, x  del self[x]  \_\_getslice\_\_  self, Py\_ssize\_t i, Py\_ssize\_t j  object  self[i:j]  \_\_setslice\_\_  self, Py\_ssize\_t i, Py\_ssize\_t j, x  self[i:j] = x  \_\_delslice\_\_  self, Py\_ssize\_t i, Py\_ssize\_t j  del self[i:j]  \_\_contains\_\_  self, x  int  x in self 

### Iterators[¶](#iterators "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#emulating-container-types](https://docs.python.org/3/reference/datamodel.html#emulating-container-types "https://docs.python.org/3/reference/datamodel.html#emulating-container-types")

 Name  Parameters  Return type  Description  \_\_next\_\_  self  object  Get next item (called next in Python) 

### Buffer interface [[PEP 3118](https://peps.python.org/pep-3118/ "https://peps.python.org/pep-3118/")] (no Python equivalents - see note 1)[¶](#buffer-interface-pep-3118-no-python-equivalents-see-note-1 "Link to this heading")

 Name  Parameters  Return type  Description  \_\_getbuffer\_\_  self, Py\_buffer \*view, int flags  \_\_releasebuffer\_\_  self, Py\_buffer \*view 

### Customizing class creation[¶](#customizing-class-creation "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#customizing-class-creation](https://docs.python.org/3/reference/datamodel.html#customizing-class-creation "https://docs.python.org/3/reference/datamodel.html#customizing-class-creation")

 Name  Parameters  Return type  Description  \_\_set\_name\_\_  self, owner, name  Automatically called at the time the owning class owner is created. 

### Descriptor objects (see note 2)[¶](#descriptor-objects-see-note-2 "Link to this heading")

[https://docs.python.org/3/reference/datamodel.html#implementing-descriptors](https://docs.python.org/3/reference/datamodel.html#implementing-descriptors "https://docs.python.org/3/reference/datamodel.html#implementing-descriptors")

 Name  Parameters  Return type  Description  \_\_get\_\_  self, instance, class  object  Get value of attribute  \_\_set\_\_  self, instance, value  Set value of attribute  \_\_delete\_\_  self, instance  Delete attribute 

Note

(1) The buffer interface was intended for use by C code and is not directly
accessible from Python. For a how-to guide to the new API, see [Implementing the buffer protocol](buffer.html#buffer "buffer.html#buffer").
The old Python 2 buffer protocol (`` `__getreadbuffer__ ``, `__getwritebuffer__`,
`__getsegcount__`, `__getcharbuffer__`) is no longer supported from Cython 3.1
since Python 2 is no longer supported.

Note

(2) Descriptor objects are part of the support mechanism for new-style
Python classes. See the discussion of descriptors in the Python documentation.
See also [PEP 252](https://peps.python.org/pep-0252/ "https://peps.python.org/pep-0252/"), “Making Types Look More Like Classes”, and [PEP 253](https://peps.python.org/pep-0253/ "https://peps.python.org/pep-0253/"),
“Subtyping Built-In Types”.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Special Methods of Extension Types](# "#")
  + [Declaration](#declaration "#declaration")
  + [Docstrings](#docstrings "#docstrings")
  + [Initialisation methods: `__cinit__()` and `__init__()`](#initialisation-methods-cinit-and-init "#initialisation-methods-cinit-and-init")
  + [Finalization methods: `__dealloc__()` and `__del__()`](#finalization-methods-dealloc-and-del "#finalization-methods-dealloc-and-del")
  + [Arithmetic methods](#arithmetic-methods "#arithmetic-methods")
  + [Rich comparisons](#rich-comparisons "#rich-comparisons")
  + [The `__next__()` method](#the-next-method "#the-next-method")
  + [Special Method Table](#special-method-table "#special-method-table")
    - [General](#general "#general")
    - [Rich comparison operators](#rich-comparison-operators "#rich-comparison-operators")
    - [Arithmetic operators](#arithmetic-operators "#arithmetic-operators")
    - [Numeric conversions](#numeric-conversions "#numeric-conversions")
    - [In-place arithmetic operators](#in-place-arithmetic-operators "#in-place-arithmetic-operators")
    - [Sequences and mappings](#sequences-and-mappings "#sequences-and-mappings")
    - [Iterators](#iterators "#iterators")
    - [Buffer interface [PEP 3118] (no Python equivalents - see note 1)](#buffer-interface-pep-3118-no-python-equivalents-see-note-1 "#buffer-interface-pep-3118-no-python-equivalents-see-note-1")
    - [Customizing class creation](#customizing-class-creation "#customizing-class-creation")
    - [Descriptor objects (see note 2)](#descriptor-objects-see-note-2 "#descriptor-objects-see-note-2")

#### Previous topic

[Extension Types](extension_types.html "previous chapter")

#### Next topic

[Sharing Declarations Between Cython Modules](sharing_declarations.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/special_methods.rst.txt "../../_sources/src/userguide/special_methods.rst.txt")

### Quick search

### Navigation

* [next](sharing_declarations.html "Sharing Declarations Between Cython Modules")
* [previous](extension_types.html "Extension Types") |
* [Cython 3.1.4 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Special Methods of Extension Types

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

