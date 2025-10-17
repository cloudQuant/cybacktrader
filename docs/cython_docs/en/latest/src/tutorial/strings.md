




Unicode and passing strings — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/tutorial/strings.html "/en/stable/src/tutorial/strings.html").

### Navigation

* [next](memory_allocation.html "Memory Allocation")
* [previous](profiling_tutorial.html "Profiling") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Unicode and passing strings

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Unicode and passing strings[¶](#unicode-and-passing-strings "Link to this heading")

Note

This page uses two different syntax variants:

* Cython specific `cdef` syntax, which was designed to make type declarations
  concise and easily readable from a C/C++ perspective.
* Pure Python syntax which allows static Cython type declarations in
  [pure Python code](pure.html#pep484-type-annotations "pure.html#pep484-type-annotations"),
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

Similar to the string semantics in Python 3, Cython strictly separates
byte strings and unicode strings. Above all, this means that by default
there is no automatic conversion between byte strings and unicode strings
(except for what Python 2 does in string operations). All encoding and
decoding must pass through an explicit encoding/decoding step. To ease
conversion between Python and C strings in simple cases, the module-level
`c_string_type` and `c_string_encoding` directives can be used to
implicitly insert these encoding/decoding steps.

## Python string types in Cython code[¶](#python-string-types-in-cython-code "Link to this heading")

Cython supports four Python string types: [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"), [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"),
`unicode` and `basestring`. The [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") and `unicode` types
are the specific types known from normal Python 2.x (named [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)")
and [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") in Python 3). Additionally, Cython also supports the
[`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") type which behaves like the [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") type, except
that it is mutable.

The [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") type is special in that it is the byte string in Python 2
and the Unicode string in Python 3 (for Cython code compiled with
language level 2, i.e. the default). Meaning, it always corresponds
exactly with the type that the Python runtime itself calls [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)").
Thus, in Python 2, both [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") and [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") represent the byte string
type, whereas in Python 3, both [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and `unicode` represent the
Python Unicode string type. The switch is made at C compile time, the
Python version that is used to run Cython is not relevant.

When compiling Cython code with language level 3, the [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") type is
identified with exactly the Unicode string type at Cython compile time,
i.e. it does not identify with [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") when running in Python 2.

Note that the [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") type is not compatible with the `unicode`
type in Python 2, i.e. you cannot assign a Unicode string to a variable
or argument that is typed [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)"). The attempt will result in either
a compile time error (if detectable) or a [`TypeError`](https://docs.python.org/3/library/exceptions.html#TypeError "(in Python v3.14)") exception at
runtime. You should therefore be careful when you statically type a
string variable in code that must be compatible with Python 2, as this
Python version allows a mix of byte strings and unicode strings for data
and users normally expect code to be able to work with both. Code that
only targets Python 3 can safely type variables and arguments as either
[`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") or `unicode`.

The `basestring` type represents both the types [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") and `unicode`,
i.e. all Python text string types in Python 2 and Python 3. This can be
used for typing text variables that normally contain Unicode text (at
least in Python 3) but must additionally accept the [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") type in
Python 2 for backwards compatibility reasons. It is not compatible with
the [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") type. Its usage should be rare in normal Cython code as
the generic [`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") type (i.e. untyped code) will normally be good
enough and has the additional advantage of supporting the assignment of
string subtypes. Support for the `basestring` type was added in Cython
0.20.

## String literals[¶](#string-literals "Link to this heading")

Cython understands all Python string type prefixes:

* `b'bytes'` for byte strings
* `u'text'` for Unicode strings
* `f'formatted {value}'` for formatted Unicode string literals as defined by
  [PEP 498](https://peps.python.org/pep-0498/ "https://peps.python.org/pep-0498/") (added in Cython 0.24)

Unprefixed string literals become [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") objects when compiling
with language level 2 and [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") objects
(i.e. `unicode`) with language level 3.

## General notes about C strings[¶](#general-notes-about-c-strings "Link to this heading")

In many use cases, C strings (a.k.a. character pointers) are slow
and cumbersome. For one, they usually require manual memory
management in one way or another, which makes it more likely to
introduce bugs into your code.

Then, Python string objects cache their length, so requesting it
(e.g. to validate the bounds of index access or when concatenating
two strings into one) is an efficient constant time operation.
In contrast, calling `strlen()` to get this information
from a C string takes linear time, which makes many operations on
C strings rather costly.

Regarding text processing, Python has built-in support for Unicode,
which C lacks completely. If you are dealing with Unicode text,
you are usually better off using Python Unicode string objects than
trying to work with encoded data in C strings. Cython makes this
quite easy and efficient.

Generally speaking: unless you know what you are doing, avoid
using C strings where possible and use Python string objects instead.
The obvious exception to this is when passing them back and forth
from and to external C code. Also, C++ strings remember their length
as well, so they can provide a suitable alternative to Python bytes
objects in some cases, e.g. when reference counting is not needed
within a well defined context.

## Passing byte strings[¶](#passing-byte-strings "Link to this heading")

We have dummy C functions declared that we are going to reuse throughout this tutorial:

Pure PythonCython

c\_func.py[¶](#id1 "Link to this code")

```
from cython.cimports.libc.stdlib import malloc
from cython.cimports.libc.string import strcpy, strlen

hello_world = cython.declare(cython.p_char, 'hello world')
n = cython.declare(cython.Py_ssize_t, strlen(hello_world))

@cython.cfunc
def c_call_returning_a_c_string() -> cython.p_char:
    c_string: cython.p_char = cython.cast(cython.p_char, malloc(
        (n + 1) * cython.sizeof(cython.char)))

    if not c_string:
        return cython.NULL  # malloc failed

    strcpy(c_string, hello_world)
    return c_string

@cython.cfunc
def get_a_c_string(c_string_ptr: cython.pp_char,
                   length: cython.p_Py_ssize_t) -> cython.int:
    c_string_ptr[0] = cython.cast(cython.p_char, malloc(
        (n + 1) * cython.sizeof(cython.char)))

    if not c_string_ptr[0]:
        return -1  # malloc failed

    strcpy(c_string_ptr[0], hello_world)
    length[0] = n
    return 0
```

Warning

The code provided above / on this page uses an external
native (non-Python) library through a `cimport` (`cython.cimports`).
Cython compilation enables this, but there is no support for this from
plain Python. Trying to run this code from Python (without compilation)
will fail when accessing the external library.
This is described in more detail in [Calling C functions](pure.html#calling-c-functions "pure.html#calling-c-functions").

c\_func.pyx[¶](#id2 "Link to this code")

```
from libc.stdlib cimport malloc
from libc.string cimport strcpy, strlen

cdef char* hello_world = 'hello world'
cdef size_t n = strlen(hello_world)


cdef char* c_call_returning_a_c_string():
    cdef char* c_string = <char *> malloc(
        (n + 1) * sizeof(char))

    if not c_string:
        return NULL  # malloc failed

    strcpy(c_string, hello_world)
    return c_string


cdef int get_a_c_string(char** c_string_ptr,
                         Py_ssize_t *length):
    c_string_ptr[0] = <char *> malloc(
        (n + 1) * sizeof(char))

    if not c_string_ptr[0]:
        return -1  # malloc failed

    strcpy(c_string_ptr[0], hello_world)
    length[0] = n
    return 0
```

We make a corresponding `c_func.pxd` to be able to cimport those functions:

c\_func.pxd[¶](#id3 "Link to this code")

```
cdef char* c_call_returning_a_c_string()
cdef int get_a_c_string(char** c_string, Py_ssize_t *length)
```

It is very easy to pass byte strings between C code and Python.
When receiving a byte string from a C library, you can let Cython
convert it into a Python byte string by simply assigning it to a
Python variable:

Pure PythonCython

```
from cython.cimports.c_func import c_call_returning_a_c_string

c_string = cython.declare(cython.p_char, c_call_returning_a_c_string())
if c_string is cython.NULL:
    ...  # handle error

py_string = cython.declare(bytes, c_string)
```

```
from c_func cimport c_call_returning_a_c_string

cdef char* c_string = c_call_returning_a_c_string()
if c_string is NULL:
    ...  # handle error

cdef bytes py_string = c_string
```

A type cast to [`object`](https://docs.python.org/3/library/functions.html#object "(in Python v3.14)") or [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") will do the same thing:

Pure PythonCython

```
py_string = cython.cast(bytes, c_string)
```

```
py_string = <bytes> c_string
```

This creates a Python byte string object that holds a copy of the
original C string. It can be safely passed around in Python code, and
will be garbage collected when the last reference to it goes out of
scope. It is important to remember that null bytes in the string act
as terminator character, as generally known from C. The above will
therefore only work correctly for C strings that do not contain null
bytes.

Besides not working for null bytes, the above is also very inefficient
for long strings, since Cython has to call `strlen()` on the
C string first to find out the length by counting the bytes up to the
terminating null byte. In many cases, the user code will know the
length already, e.g. because a C function returned it. In this case,
it is much more efficient to tell Cython the exact number of bytes by
slicing the C string. Here is an example:

Pure PythonCython

```
from cython.cimports.libc.stdlib import free
from cython.cimports.c_func import get_a_c_string


def main():
    c_string: cython.p_char = cython.NULL
    length: cython.Py_ssize_t = 0

    # get pointer and length from a C function
    get_a_c_string(cython.address(c_string), cython.address(length))

    try:
        py_bytes_string = c_string[:length]  # Performs a copy of the data
    finally:
        free(c_string)
```

```
from libc.stdlib cimport free
from c_func cimport get_a_c_string


def main():
    cdef char* c_string = NULL
    cdef Py_ssize_t length = 0

    # get pointer and length from a C function
    get_a_c_string(&c_string, &length)

    try:
        py_bytes_string = c_string[:length]  # Performs a copy of the data
    finally:
        free(c_string)
```

Here, no additional byte counting is required and `length` bytes from
the `c_string` will be copied into the Python bytes object, including
any null bytes. Keep in mind that the slice indices are assumed to be
accurate in this case and no bounds checking is done, so incorrect
slice indices will lead to data corruption and crashes.

Note that the creation of the Python bytes string can fail with an
exception, e.g. due to insufficient memory. If you need to
`free()` the string after the conversion, you should wrap
the assignment in a try-finally construct:

Pure PythonCython

```
from cython.cimports.libc.stdlib import free
from cython.cimports.c_func import c_call_returning_a_c_string

py_string = cython.declare(bytes)
c_string = cython.declare(cython.p_char, c_call_returning_a_c_string())
try:
    py_string = c_string
finally:
    free(c_string)
```

```
from libc.stdlib cimport free
from c_func cimport c_call_returning_a_c_string

cdef bytes py_string
cdef char* c_string = c_call_returning_a_c_string()
try:
    py_string = c_string
finally:
    free(c_string)
```

To convert the byte string back into a C char\*, use the
opposite assignment:

Pure PythonCython

```
other_c_string = cython.declare(cython.p_char, py_string)  # other_c_string is a 0-terminated string.
```

```
cdef char* other_c_string = py_string  # other_c_string is a 0-terminated string.
```

This is a very fast operation after which `other_c_string` points to
the byte string buffer of the Python string itself. It is tied to the
life time of the Python string. When the Python string is garbage
collected, the pointer becomes invalid. It is therefore important to
keep a reference to the Python string as long as the char\*
is in use. Often enough, this only spans the call to a C function that
receives the pointer as parameter. Special care must be taken,
however, when the C function stores the pointer for later use. Apart
from keeping a Python reference to the string object, no manual memory
management is required.

Starting with Cython 0.20, the [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") type is supported and
coerces in the same way as the [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") type. However, when using it
in a C context, special care must be taken not to grow or shrink the
object buffer after converting it to a C string pointer. These
modifications can change the internal buffer address, which will make
the pointer invalid.

## Accepting strings from Python code[¶](#accepting-strings-from-python-code "Link to this heading")

The other side, receiving input from Python code, may appear simple
at first sight, as it only deals with objects. However, getting this
right without making the API too narrow or too unsafe may not be
entirely obvious.

In the case that the API only deals with byte strings, i.e. binary
data or encoded text, it is best not to type the input argument as
something like [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"), because that would restrict the allowed
input to exactly that type and exclude both subtypes and other kinds
of byte containers, e.g. [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") objects or memory views.

Depending on how (and where) the data is being processed, it may be a
good idea to instead receive a 1-dimensional memory view, e.g.

Pure PythonCython

```
def process_byte_data(data: cython.uchar[:]):
    length = data.shape[0]
    first_byte = data[0]
    slice_view = data[1:-1]
    # ...
```

```
def process_byte_data(unsigned char[:] data):
    length = data.shape[0]
    first_byte = data[0]
    slice_view = data[1:-1]
    # ...
```

Cython’s memory views are described in more detail in
[Typed Memoryviews](../userguide/memoryviews.html "../userguide/memoryviews.html"), but the above example already shows
most of the relevant functionality for 1-dimensional byte views. They
allow for efficient processing of arrays and accept anything that can
unpack itself into a byte buffer, without intermediate copying. The
processed content can finally be returned in the memory view itself
(or a slice of it), but it is often better to copy the data back into
a flat and simple [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") or [`bytearray`](https://docs.python.org/3/library/stdtypes.html#bytearray "(in Python v3.14)") object, especially
when only a small slice is returned. Since memoryviews do not copy the
data, they would otherwise keep the entire original buffer alive. The
general idea here is to be liberal with input by accepting any kind of
byte buffer, but strict with output by returning a simple, well adapted
object. This can simply be done as follows:

Pure PythonCython

```
def process_byte_data(data: cython.uchar[:]):
    # ... process the data, here, dummy processing.
    return_all: cython.bint = (data[0] == 108)

    if return_all:
        return bytes(data)
    else:
        # example for returning a slice
        return bytes(data[5:7])
```

```
def process_byte_data(unsigned char[:] data):
    # ... process the data, here, dummy processing.
    cdef bint return_all = (data[0] == 108)

    if return_all:
        return bytes(data)
    else:
        # example for returning a slice
        return bytes(data[5:7])
```

For read-only buffers, like [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)"), the memoryview item type should
be declared as `const` (see [Read-only views](../userguide/memoryviews.html#readonly-views "../userguide/memoryviews.html#readonly-views")). If the byte input is
actually encoded text, and the further processing should happen at the
Unicode level, then the right thing to do is to decode the input straight
away. This is almost only a problem in Python 2.x, where Python code
expects that it can pass a byte string ([`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")) with encoded text into
a text API. Since this usually happens in more than one place in the
module’s API, a helper function is almost always the way to go, since it
allows for easy adaptation of the input normalisation process later.

This kind of input normalisation function will commonly look similar to
the following:

Pure PythonCython

to\_unicode.py[¶](#id4 "Link to this code")

```
from cython.cimports.cpython.version import PY_MAJOR_VERSION

@cython.cfunc
def _text(s) -> str:
    if type(s) is str:
        # Fast path for most common case(s).
        return cython.cast(str, s)

    elif PY_MAJOR_VERSION < 3 and isinstance(s, bytes):
        # Only accept byte strings as text input in Python 2.x, not in Py3.
        return cython.cast(bytes, s).decode('ascii')

    elif isinstance(s, str):
        # We know from the fast path above that 's' can only be a subtype here.
        # An evil cast to <str> might still work in some(!) cases,
        # depending on what the further processing does.  To be safe,
        # we can always create a copy instead.
        return str(s)

    else:
        raise TypeError("Could not convert to str.")
```

to\_unicode.pyx[¶](#id5 "Link to this code")

```
from cpython.version cimport PY_MAJOR_VERSION


cdef str _text(s):
    if type(s) is str:
        # Fast path for most common case(s).
        return <str>s

    elif PY_MAJOR_VERSION < 3 and isinstance(s, bytes):
        # Only accept byte strings as text input in Python 2.x, not in Py3.
        return (<bytes>s).decode('ascii')

    elif isinstance(s, str):
        # We know from the fast path above that 's' can only be a subtype here.
        # An evil cast to <str> might still work in some(!) cases,
        # depending on what the further processing does.  To be safe,
        # we can always create a copy instead.
        return str(s)

    else:
        raise TypeError("Could not convert to str.")
```

to\_unicode.pxd[¶](#id6 "Link to this code")

```
cdef str _text(s)
```

And should then be used like this:

Pure PythonCython

```
from cython.cimports.to_unicode import _text

def api_func(s):
    text_input = _text(s)
    # ...
```

```
from to_unicode cimport _text

def api_func(s):
    text_input = _text(s)
    # ...
```

Similarly, if the further processing happens at the byte level, but Unicode
string input should be accepted, then the following might work, if you are
using memory views:

Pure PythonCython

```
# define a global name for whatever char type is used in the module
char_type = cython.typedef(cython.uchar)

@cython.cfunc
def _chars(s) -> char_type[:]:
    if isinstance(s, str):
        # encode to the specific encoding used inside of the module
        s = cython.cast(str, s).encode('utf8')
    return s
```

```
# define a global name for whatever char type is used in the module
ctypedef unsigned char char_type


cdef char_type[:] _chars(s):
    if isinstance(s, str):
        # encode to the specific encoding used inside of the module
        s = (<str>s).encode('utf8')
    return s
```

In this case, you might want to additionally ensure that byte string
input really uses the correct encoding, e.g. if you require pure ASCII
input data, you can run over the buffer in a loop and check the highest
bit of each byte. This should then also be done in the input normalisation
function.

## Dealing with “const”[¶](#dealing-with-const "Link to this heading")

Many C libraries use the `const` modifier in their API to declare
that they will not modify a string, or to require that users must
not modify a string they return, for example:

someheader.h[¶](#id7 "Link to this code")

```
typedef const char specialChar;
int process_string(const char* s);
const unsigned char* look_up_cached_string(const unsigned char* key);
```

Cython has support for the `const` modifier in
the language, so you can declare the above functions straight away as
follows:

```
cdef extern from "someheader.h":
    ctypedef const char specialChar
    int process_string(const char* s)
    const unsigned char* look_up_cached_string(const unsigned char* key)
```

## Decoding bytes to text[¶](#decoding-bytes-to-text "Link to this heading")

The initially presented way of passing and receiving C strings is
sufficient if your code only deals with binary data in the strings.
When we deal with encoded text, however, it is best practice to decode
the C byte strings to Python Unicode strings on reception, and to
encode Python Unicode strings to C byte strings on the way out.

With a Python byte string object, you would normally just call the
`bytes.decode()` method to decode it into a Unicode string:

```
ustring = byte_string.decode('UTF-8')
```

Cython allows you to do the same for a C string, as long as it
contains no null bytes:

Pure PythonCython

```
from cython.cimports.c_func import c_call_returning_a_c_string

some_c_string = cython.declare(cython.p_char, c_call_returning_a_c_string())
ustring = some_c_string.decode('UTF-8')
```

```
from c_func cimport c_call_returning_a_c_string

cdef char* some_c_string = c_call_returning_a_c_string()
ustring = some_c_string.decode('UTF-8')
```

And, more efficiently, for strings where the length is known:

Pure PythonCython

```
from cython.cimports.c_func import get_a_c_string

c_string = cython.declare(cython.p_char, cython.NULL)
length = cython.declare(cython.Py_ssize_t, 0)

# get pointer and length from a C function
get_a_c_string(cython.address(c_string), cython.address(length))

ustring = c_string[:length].decode('UTF-8')
```

```
from c_func cimport get_a_c_string

cdef char* c_string = NULL
cdef Py_ssize_t length = 0

# get pointer and length from a C function
get_a_c_string(&c_string, &length)

ustring = c_string[:length].decode('UTF-8')
```

The same should be used when the string contains null bytes, e.g. when
it uses an encoding like UCS-4, where each character is encoded in four
bytes most of which tend to be 0.

Again, no bounds checking is done if slice indices are provided, so
incorrect indices lead to data corruption and crashes. However, using
negative indices is possible and will inject a call
to `strlen()` in order to determine the string length.
Obviously, this only works for 0-terminated strings without internal
null bytes. Text encoded in UTF-8 or one of the ISO-8859 encodings is
usually a good candidate. If in doubt, it’s better to pass indices
that are ‘obviously’ correct than to rely on the data to be as expected.

It is common practice to wrap string conversions (and non-trivial type
conversions in general) in dedicated functions, as this needs to be
done in exactly the same way whenever receiving text from C. This
could look as follows:

Pure PythonCython

```
from cython.cimports.libc.stdlib import free

@cython.cfunc
def tounicode(s: cython.p_char) -> str:
    return s.decode('UTF-8', 'strict')

@cython.cfunc
def tounicode_with_length(
        s: cython.p_char, length: cython.size_t) -> str:
    return s[:length].decode('UTF-8', 'strict')

@cython.cfunc
def tounicode_with_length_and_free(
        s: cython.p_char, length: cython.size_t) -> str:
    try:
        return s[:length].decode('UTF-8', 'strict')
    finally:
        free(s)
```

```
from libc.stdlib cimport free


cdef str tounicode(char* s):
    return s.decode('UTF-8', 'strict')


cdef str tounicode_with_length(
        char* s, size_t length):
    return s[:length].decode('UTF-8', 'strict')


cdef str tounicode_with_length_and_free(
        char* s, size_t length):
    try:
        return s[:length].decode('UTF-8', 'strict')
    finally:
        free(s)
```

Most likely, you will prefer shorter function names in your code based
on the kind of string being handled. Different types of content often
imply different ways of handling them on reception. To make the code
more readable and to anticipate future changes, it is good practice to
use separate conversion functions for different types of strings.

## Encoding text to bytes[¶](#encoding-text-to-bytes "Link to this heading")

The reverse way, converting a Python unicode string to a C
char\*, is pretty efficient by itself, assuming that what
you actually want is a memory managed byte string:

Pure PythonCython

```
py_byte_string = py_unicode_string.encode('UTF-8')
c_string = cython.declare(cython.p_char, py_byte_string)
```

```
py_byte_string = py_unicode_string.encode('UTF-8')
cdef char* c_string = py_byte_string
```

As noted before, this takes the pointer to the byte buffer of the
Python byte string. Trying to do the same without keeping a reference
to the Python byte string will fail with a compile error:

Pure PythonCython

```
# this will not compile !
c_string = cython.declare(cython.p_char, py_unicode_string.encode('UTF-8'))
```

```
# this will not compile !
cdef char* c_string = py_unicode_string.encode('UTF-8')
```

Here, the Cython compiler notices that the code takes a pointer to a
temporary string result that will be garbage collected after the
assignment. Later access to the invalidated pointer will read invalid
memory and likely result in a segfault. Cython will therefore refuse
to compile this code.

## C++ strings[¶](#c-strings "Link to this heading")

When wrapping a C++ library, strings will usually come in the form of
the std::string class. As with C strings, Python byte strings
automatically coerce from and to C++ strings:

Pure PythonCython

```
# distutils: language = c++

from cython.cimports.libcpp.string import string

def get_bytes():
    py_bytes_object = b'hello world'
    s: string = py_bytes_object

    s.append(b'abc')
    py_bytes_object = s
    return py_bytes_object
```

```
# distutils: language = c++

from libcpp.string cimport string

def get_bytes():
    py_bytes_object = b'hello world'
    cdef string s = py_bytes_object

    s.append(b'abc')
    py_bytes_object = s
    return py_bytes_object
```

The memory management situation is different than in C because the
creation of a C++ string makes an independent copy of the string
buffer which the string object then owns. It is therefore possible
to convert temporarily created Python objects directly into C++
strings. A common way to make use of this is when encoding a Python
unicode string into a C++ string:

Pure PythonCython

```
cpp_string = cython.declare(string, py_unicode_string.encode('UTF-8'))
```

```
cdef string cpp_string = py_unicode_string.encode('UTF-8')
```

Note that this involves a bit of overhead because it first encodes
the Unicode string into a temporarily created Python bytes object
and then copies its buffer into a new C++ string.

For the other direction, efficient decoding support is available
in Cython 0.17 and later:

Pure PythonCython

```
# distutils: language = c++

from cython.cimports.libcpp.string import string

def get_ustrings():
    s: string = string(b'abcdefg')

    ustring1 = s.decode('UTF-8')
    ustring2 = s[2:-2].decode('UTF-8')
    return ustring1, ustring2
```

```
# distutils: language = c++

from libcpp.string cimport string

def get_ustrings():
    cdef string s = string(b'abcdefg')

    ustring1 = s.decode('UTF-8')
    ustring2 = s[2:-2].decode('UTF-8')
    return ustring1, ustring2
```

For C++ strings, decoding slices will always take the proper length
of the string into account and apply Python slicing semantics (e.g.
return empty strings for out-of-bounds indices).

## Auto encoding and decoding[¶](#auto-encoding-and-decoding "Link to this heading")

Automatic conversions are controlled by the directives `c_string_type` and
`c_string_encoding`. They can be used to change the Python string
types that C/C++ strings coerce from and to. By default, they only
coerce from and to the bytes type, and encoding or decoding must
be done explicitly, as described above.

This can be inconvenient if all
C strings that are being processed (or the large majority) contain
text, and automatic encoding and decoding from and to Python unicode
objects can reduce the code overhead a little. In this case, you
can set the `c_string_type` directive in your module to `unicode`
and the `c_string_encoding` to the encoding that your C code uses,
for example:

```
# cython: c_string_type=unicode, c_string_encoding=utf8

cdef char* c_string = 'abcdefg'

# implicit decoding:
cdef object py_unicode_object = c_string

# explicit conversion to Python bytes:
py_bytes_object = <bytes>c_string
```

The other direction, i.e. automatic encoding to C strings, is only
supported for ASCII/UTF-8. CPython handles the memory
management in this case by keeping an encoded copy of the string alive
together with the original unicode string. Otherwise, there would be no
way to limit the lifetime of the encoded string in any sensible way,
thus rendering any attempt to extract a C string pointer from it a
dangerous endeavour. The following safely converts a Unicode string to
UTF-8 (change `c_string_encoding` to `ASCII` to limit it to that):

```
# cython: c_string_type=unicode, c_string_encoding=UTF8

def func():
    ustring: str = 'abc'
    cdef const char* s = ustring
    return s[0]    # returns 'a' as a Unicode text string
```

(This example uses a function context in order to safely control the
lifetime of the Unicode string. Global Python variables can be
modified from the outside, which makes it dangerous to rely on the
lifetime of their values.)

## Source code encoding[¶](#source-code-encoding "Link to this heading")

When string literals appear in the code, the source code encoding is
important. It determines the byte sequence that Cython will store in
the C code for bytes literals, and the Unicode code points that Cython
builds for unicode literals when parsing the byte encoded source file.
Following [PEP 263](https://peps.python.org/pep-0263/ "https://peps.python.org/pep-0263/"), Cython supports the explicit declaration of
source file encodings. For example, putting the following comment at
the top of an `ISO-8859-15` (Latin-9) encoded source file (into the
first or second line) is required to enable `ISO-8859-15` decoding
in the parser:

```
# -*- coding: ISO-8859-15 -*-
```

When no explicit encoding declaration is provided, the source code is
parsed as UTF-8 encoded text, as specified by [PEP 3120](https://peps.python.org/pep-3120/ "https://peps.python.org/pep-3120/"). [UTF-8](https://en.wikipedia.org/wiki/UTF-8 "https://en.wikipedia.org/wiki/UTF-8")
is a very common encoding that can represent the entire Unicode set of
characters and is compatible with plain ASCII encoded text that it
encodes efficiently. This makes it a very good choice for source code
files which usually consist mostly of ASCII characters.

As an example, putting the following line into a UTF-8 encoded source
file will print `5`, as UTF-8 encodes the letter `'ö'` in the two
byte sequence `'\xc3\xb6'`:

```
print( len(b'abcö') )
```

whereas the following `ISO-8859-15` encoded source file will print
`4`, as the encoding uses only 1 byte for this letter:

```
# -*- coding: ISO-8859-15 -*-
print( len(b'abcö') )
```

Note that the unicode literal `u'abcö'` is a correctly decoded four
character Unicode string in both cases, whereas the unprefixed Python
[`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") literal `'abcö'` will become a byte string in Python 2 (thus
having length 4 or 5 in the examples above), and a 4 character Unicode
string in Python 3. If you are not familiar with encodings, this may
not appear obvious at first read. See [CEP 108](https://github.com/cython/cython/wiki/enhancements-stringliterals "https://github.com/cython/cython/wiki/enhancements-stringliterals") for details.

As a rule of thumb, it is best to avoid unprefixed non-ASCII [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)")
literals and to use unicode string literals for all text. Cython also
supports the `__future__` import `unicode_literals` that instructs
the parser to read all unprefixed [`str`](https://docs.python.org/3/library/stdtypes.html#str "(in Python v3.14)") literals in a source file as
unicode string literals, just like Python 3.

## Single bytes and characters[¶](#single-bytes-and-characters "Link to this heading")

The Python C-API uses the normal C char type to represent
a byte value, but it has two special integer types for a Unicode code
point value, i.e. a single Unicode character: [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)")
and [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)"). Cython supports the
first natively, support for [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)") is new in Cython 0.15.
[`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") is either defined as an unsigned 2-byte or
4-byte integer, or as wchar\_t, depending on the platform.
The exact type is a compile time option in the build of the CPython
interpreter and extension modules inherit this definition at C
compile time. The advantage of [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)") is that it is
guaranteed to be large enough for any Unicode code point value,
regardless of the platform. It is defined as a 32bit unsigned int
or long.

In Cython, the char type behaves differently from the
[`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") and [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)") types when coercing
to Python objects. Similar to the behaviour of the bytes type in
Python 3, the char type coerces to a Python integer
value by default, so that the following prints 65 and not `A`:

Pure PythonCython

```
# -*- coding: ASCII -*-

char_val = declare(cython.char, 'A')
assert char_val == 65   # ASCII encoded byte value of 'A'
print( char_val )
```

```
# -*- coding: ASCII -*-

cdef char char_val = 'A'
assert char_val == 65   # ASCII encoded byte value of 'A'
print( char_val )
```

If you want a Python bytes string instead, you have to request it
explicitly, and the following will print `A` (or `b'A'` in Python
3):

Pure PythonCython

```
print( cython.cast(bytes, char_val) )
```

```
print( <bytes>char_val )
```

The explicit coercion works for any C integer type. Values outside of
the range of a char or unsigned char will raise an
[`OverflowError`](https://docs.python.org/3/library/exceptions.html#OverflowError "(in Python v3.14)") at runtime. Coercion will also happen automatically
when assigning to a typed variable, e.g.:

Pure PythonCython

```
py_byte_string = cython.declare(bytes)
py_byte_string = char_val
```

```
cdef bytes py_byte_string
py_byte_string = char_val
```

On the other hand, the [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") and [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)")
types are rarely used outside of the context of a Python unicode string,
so their default behaviour is to coerce to a Python unicode object. The
following will therefore print the character `A`, as would the same
code with the [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") type:

Pure PythonCython

```
uchar_val = cython.declare(cython.Py_UCS4, u'A')
assert uchar_val == 65 # character point value of u'A'
print( uchar_val )
```

```
cdef Py_UCS4 uchar_val = u'A'
assert uchar_val == 65 # character point value of u'A'
print( uchar_val )
```

Again, explicit casting will allow users to override this behaviour.
The following will print 65:

Pure PythonCython

```
uchar_val = cython.declare(cython.Py_UCS4, u'A')
print( cython.cast(long, uchar_val) )
```

```
cdef Py_UCS4 uchar_val = u'A'
print( <long>uchar_val )
```

Note that casting to a C long (or unsigned long) will work
just fine, as the maximum code point value that a Unicode character
can have is 1114111 (`0x10FFFF`). On platforms with 32bit or more,
int is just as good.

## Narrow Unicode builds[¶](#narrow-unicode-builds "Link to this heading")

In narrow Unicode builds of CPython before version 3.3, i.e. builds
where `sys.maxunicode` is 65535 (such as all Windows builds, as
opposed to 1114111 in wide builds), it is still possible to use
Unicode character code points that do not fit into the 16 bit wide
[`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") type. For example, such a CPython build will
accept the unicode literal `u'\U00012345'`. However, the
underlying system level encoding leaks into Python space in this
case, so that the length of this literal becomes 2 instead of 1.
This also shows when iterating over it or when indexing into it.
The visible substrings are `u'\uD808'` and `u'\uDF45'` in this
example. They form a so-called surrogate pair that represents the
above character.

For more information on this topic, it is worth reading the [Wikipedia
article about the UTF-16 encoding](https://en.wikipedia.org/wiki/UTF-16/UCS-2 "https://en.wikipedia.org/wiki/UTF-16/UCS-2").

The same properties apply to Cython code that gets compiled for a
narrow CPython runtime environment. In most cases, e.g. when
searching for a substring, this difference can be ignored as both the
text and the substring will contain the surrogates. So most Unicode
processing code will work correctly also on narrow builds. Encoding,
decoding and printing will work as expected, so that the above literal
turns into exactly the same byte sequence on both narrow and wide
Unicode platforms.

However, programmers should be aware that a single [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)")
value (or single ‘character’ unicode string in CPython) may not be
enough to represent a complete Unicode character on narrow platforms.
For example, if an independent search for `u'\uD808'` and
`u'\uDF45'` in a unicode string succeeds, this does not necessarily
mean that the character `u'\U00012345` is part of that string. It
may well be that two different characters are in the string that just
happen to share a code unit with the surrogate pair of the character
in question. Looking for substrings works correctly because the two
code units in the surrogate pair use distinct value ranges, so the
pair is always identifiable in a sequence of code points.

As of version 0.15, Cython has extended support for surrogate pairs so
that you can safely use an `in` test to search character values from
the full [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)") range even on narrow platforms:

Pure PythonCython

```
uchar = cython.declare(cython.Py_UCS4, 0x12345)
print( uchar in some_unicode_string )
```

```
cdef Py_UCS4 uchar = 0x12345
print( uchar in some_unicode_string )
```

Similarly, it can coerce a one character string with a high Unicode
code point value to a Py\_UCS4 value on both narrow and wide Unicode
platforms:

Pure PythonCython

```
uchar = cython.declare(cython.Py_UCS4, u'\U00012345')
assert uchar == 0x12345
```

```
cdef Py_UCS4 uchar = u'\U00012345'
assert uchar == 0x12345
```

In CPython 3.3 and later, the [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") type is an alias
for the system specific wchar\_t type and is no longer tied
to the internal representation of the Unicode string. Instead, any
Unicode character can be represented on all platforms without
resorting to surrogate pairs. This implies that narrow builds no
longer exist from that version on, regardless of the size of
[`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)"). See [PEP 393](https://peps.python.org/pep-0393/ "https://peps.python.org/pep-0393/") for details.

Cython 0.16 and later handles this change internally and does the right
thing also for single character values as long as either type inference
is applied to untyped variables or the portable [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)") type
is explicitly used in the source code instead of the platform specific
[`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") type. Optimisations that Cython applies to the
Python unicode type will automatically adapt to [PEP 393](https://peps.python.org/pep-0393/ "https://peps.python.org/pep-0393/") at C compile
time, as usual.

## Iteration[¶](#iteration "Link to this heading")

Cython 0.13 supports efficient iteration over char\*,
bytes and unicode strings, as long as the loop variable is
appropriately typed. So the following will generate the expected
C code:

Pure PythonCython

```
def iterate_char():
    c_string: cython.p_char = "Hello to A C-string's world"

    c: cython.char
    for c in c_string[:11]:
        if c == b'A':
            print("Found the letter A")
```

```
def iterate_char():
    cdef char* c_string = "Hello to A C-string's world"

    cdef char c
    for c in c_string[:11]:
        if c == b'A':
            print("Found the letter A")
```

The same applies to bytes objects:

Pure PythonCython

```
def iterate_bytes():
    bytes_string: bytes = b"hello to A bytes' world"

    c: cython.char
    for c in bytes_string:
        if c == b'A':
            print("Found the letter A")
```

```
def iterate_bytes():
    cdef bytes bytes_string = b"hello to A bytes' world"

    cdef char c
    for c in bytes_string:
        if c == b'A':
            print("Found the letter A")
```

For unicode objects, Cython will automatically infer the type of the
loop variable as [`Py_UCS4`](https://docs.python.org/3/c-api/unicode.html#c.Py_UCS4 "(in Python v3.14)"):

Pure PythonCython

```
def iterate_string():
    ustring: unicode = u'Hello world'

    # NOTE: no typing required for 'uchar' !
    for uchar in ustring:
        if uchar == u'A':
            print("Found the letter A")
```

```
def iterate_string():
    cdef unicode ustring = u'Hello world'

    # NOTE: no typing required for 'uchar' !
    for uchar in ustring:
        if uchar == u'A':
            print("Found the letter A")
```

The automatic type inference usually leads to much more efficient code
here. However, note that some unicode operations still require the
value to be a Python object, so Cython may end up generating redundant
conversion code for the loop variable value inside of the loop. If
this leads to a performance degradation for a specific piece of code,
you can either type the loop variable as a Python object explicitly,
or assign its value to a Python typed variable somewhere inside of the
loop to enforce one-time coercion before running Python operations on
it.

There are also optimisations for `in` tests, so that the following
code will run in plain C code, (actually using a switch statement):

Pure PythonCython

```
@cython.ccall
def is_in(uchar_val: cython.Py_UCS4) -> cython.void:
    if uchar_val in u'abcABCxY':
        print("The character is in the string.")
    else:
        print("The character is not in the string")
```

```
cpdef void is_in(Py_UCS4 uchar_val):
    if uchar_val in u'abcABCxY':
        print("The character is in the string.")
    else:
        print("The character is not in the string")
```

Combined with the looping optimisation above, this can result in very
efficient character switching code, e.g. in unicode parsers.

## Windows and wide character APIs[¶](#windows-and-wide-character-apis "Link to this heading")

Warning

The use of [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") strings outside of Windows is
strongly discouraged. [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") is inherently not
portable between different platforms and Python versions.

Support for the `Py_UNICODE` C-API has been removed in CPython 3.12.
Code that uses it will no longer compile in recent CPython releases.
Since version 3.3, CPython provides a flexible internal representation of
unicode strings ([PEP 393](https://peps.python.org/pep-0393/ "https://peps.python.org/pep-0393/")), that makes all [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") related
APIs deprecated and inefficient.

Windows system APIs natively support Unicode in the form of
zero-terminated UTF-16 encoded wchar\_t\* strings, so called
“wide strings”.

By default, Windows builds of CPython define [`Py_UNICODE`](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)") as
a synonym for wchar\_t. This makes internal `unicode`
representation compatible with UTF-16 and allows for efficient zero-copy
conversions. This also means that Windows builds are always
[Narrow Unicode builds](#narrow-unicode-builds "#narrow-unicode-builds") with all the caveats.

To aid interoperation with Windows APIs, Cython 0.19 supports wide
strings (in the form of [Py\_UNICODE](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)")\*) and implicitly converts
them to and from `unicode` string objects. These conversions behave the
same way as they do for char\* and [`bytes`](https://docs.python.org/3/library/stdtypes.html#bytes "(in Python v3.14)") as described in
[Passing byte strings](#passing-byte-strings "#passing-byte-strings").

In addition to automatic conversion, unicode literals that appear
in C context become C-level wide string literals and [`len()`](https://docs.python.org/3/library/functions.html#len "(in Python v3.14)")
built-in function is specialized to compute the length of zero-terminated
[Py\_UNICODE](https://docs.python.org/3/c-api/unicode.html#c.Py_UNICODE "(in Python v3.14)")\* string or array.

Here is an example of how one would call a Unicode API on Windows:

```
cdef extern from "Windows.h":

    ctypedef Py_UNICODE WCHAR
    ctypedef const WCHAR* LPCWSTR
    ctypedef void* HWND

    int MessageBoxW(HWND hWnd, LPCWSTR lpText, LPCWSTR lpCaption, int uType)

title = u"Windows Interop Demo - Python %d.%d.%d" % sys.version_info[:3]
MessageBoxW(NULL, u"Hello Cython \u263a", title, 0)
```

One consequence of CPython 3.3 changes is that [`len()`](https://docs.python.org/3/library/functions.html#len "(in Python v3.14)") of
`unicode` strings is always measured in code points (“characters”),
while Windows API expect the number of UTF-16 code units
(where each surrogate is counted individually). To always get the number
of code units, call `PyUnicode_GetSize()` directly.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Unicode and passing strings](# "#")
  + [Python string types in Cython code](#python-string-types-in-cython-code "#python-string-types-in-cython-code")
  + [String literals](#string-literals "#string-literals")
  + [General notes about C strings](#general-notes-about-c-strings "#general-notes-about-c-strings")
  + [Passing byte strings](#passing-byte-strings "#passing-byte-strings")
  + [Accepting strings from Python code](#accepting-strings-from-python-code "#accepting-strings-from-python-code")
  + [Dealing with “const”](#dealing-with-const "#dealing-with-const")
  + [Decoding bytes to text](#decoding-bytes-to-text "#decoding-bytes-to-text")
  + [Encoding text to bytes](#encoding-text-to-bytes "#encoding-text-to-bytes")
  + [C++ strings](#c-strings "#c-strings")
  + [Auto encoding and decoding](#auto-encoding-and-decoding "#auto-encoding-and-decoding")
  + [Source code encoding](#source-code-encoding "#source-code-encoding")
  + [Single bytes and characters](#single-bytes-and-characters "#single-bytes-and-characters")
  + [Narrow Unicode builds](#narrow-unicode-builds "#narrow-unicode-builds")
  + [Iteration](#iteration "#iteration")
  + [Windows and wide character APIs](#windows-and-wide-character-apis "#windows-and-wide-character-apis")

#### Previous topic

[Profiling](profiling_tutorial.html "previous chapter")

#### Next topic

[Memory Allocation](memory_allocation.html "next chapter")

### This Page

* [Show Source](../../_sources/src/tutorial/strings.rst.txt "../../_sources/src/tutorial/strings.rst.txt")

### Quick search

### Navigation

* [next](memory_allocation.html "Memory Allocation")
* [previous](profiling_tutorial.html "Profiling") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Tutorials](index.html "index.html") »
* Unicode and passing strings

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

