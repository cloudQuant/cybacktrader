




Tempita templating language — Cython 3.2.0b1 documentation

This version of the documentation is for the latest and greatest in-development branch of Cython.
For the last release version, see
[here](/en/stable/src/userguide/tempita.html "/en/stable/src/userguide/tempita.html").

### Navigation

* [next](troubleshooting.html "Troubleshooting")
* [previous](freethreading.html "Free threading") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Tempita templating language

🤝 Like the tool? Help make it better! [Your donation helps!](../donating.html "../donating.html") 🤝

# Tempita templating language[¶](#tempita-templating-language "Link to this heading")

This document describes the Tempita Templating Engine.
It was originally developed by Ian Bicking.
The original version of Tempita is available on [PyPI](https://pypi.org/project/Tempita/ "https://pypi.org/project/Tempita/") and documentation can be found at [https://github.com/TurboGears/tempita/blob/main/README.rst](https://github.com/TurboGears/tempita/blob/main/README.rst "https://github.com/TurboGears/tempita/blob/main/README.rst").

Tempita is used internally in Cython for non-trivial code-generation purposes.
It is also available to users as a public API for generating or customizing code when building a Cython module.

## Overview[¶](#overview "Link to this heading")

Tempita is a simple templating language, similar to Jinja.
Basic usage is as follows:

```
from Cython.Tempita import Template

tmpl1 = Template(template_string)       # load from string
tmpl2 = Template.from_filename(path)    # load template from file

tmpl1.substitute(**kwargs)     # pass parameters as named arguments.
tmpl2.sub_vars(mapping)        # pass an argument as dict-like mapping.
```

Tempita also provides a shortcut function:

```
from Cython.Tempita import sub
sub(template_string, **kwargs)
```

## Templating Syntax[¶](#templating-syntax "Link to this heading")

Below are the different directive types and expression forms supported.

### Simple Expression Substitution[¶](#simple-expression-substitution "Link to this heading")

Write expressions as `{{ ... }}`, which are evaluated in the template context.

Example:

```
>>> sub("Hello {{name}}!", name="World")
'Hello World!'
```

Expressions can be any valid Python expression: arithmetic, attribute access,
indexing, function calls etc.:

```
>>> sub("2 * 3 = {{2 * 3}}")
'2 * 3 = 6'
>>> class User:
...     name = 'Mark'
...
>>> sub("User: {{ user.name }}", user=User())
'User: Mark'
>>> sub("Hex: {{ hex(num) }}", num=10)
'Hex: 0xa'
>>> sub("Number: {{ func(num) }}", func=abs, num=-10)
'Number: 10'
>>> sub("List[0] = {{ mylist[0] }}", mylist=[10,20,30])
'List[0] = 10'
>>> sub("Dist['name'] = {{ mydict['name'] }}", mydict={'name': 'Miss Islington'})
"Dist['name'] = Miss Islington"
>>> sub("Uppercase {{ string.upper() }}", string="hello")
'Uppercase HELLO'
```

### Default Values[¶](#default-values "Link to this heading")

You can specify a default value for a variable using the `default` keyword,
and overwrite it by passing it as argument to the template substitution:

```
>>> tmpl = Template("""
... {{default name = "Sir Lancelot the Brave"}}
... My name is {{name}}.
... """
... )
>>> tmpl.substitute()
'My name is Sir Lancelot the Brave.\n'
>>> tmpl.substitute(name="Sir Bedevere the Wise")
'My name is Sir Bedevere the Wise.\n'
```

### Inline Python Code[¶](#inline-python-code "Link to this heading")

Arbitrary Python statements can be inserted inline with `{{py: ...}}`.
These do not emit output directly but can modify the template context.

```
>>> tmpl = Template("""
... {{py: x = 5}}
... Value of x: {{x}}
... """)
>>> tmpl.substitute()
'Value of x: 5\n'
```

### Comments[¶](#comments "Link to this heading")

Comments are introduced with `{{# ... }}`. They are completely removed
from output.

```
>>> sub("Hello {{# This is a comment }}World.")
'Hello World.'
```

### Custom delimiter characters[¶](#custom-delimiter-characters "Link to this heading")

In cases where the double braces that Tempita normally uses as delimiters (`{{...}}`) get in the way,
you can replace them with other characters:

```
>>> sub("Show literal braces: {{<<name>>}}", delimiters=['<<', '>>'], name="x")
'Show literal braces: {{x}}'
```

Note

The `delimiters` can also be passed as an argument to the `Template` class,

thus keeping them together with the template definition that uses them,
rather than needing to remember them later in the substitution step.

`Template("...", delimiters=['((', '))'])`

### Filters[¶](#filters "Link to this heading")

You can post-process the result of an expression before it is written into the template.
Below, the `filtername` refers to a callable (function) that will be called by the template engine
and receives the result of the preceding expression as argument.
Whatever it outputs will then be written into the templating result.

```
{{ expression | filtername }}
```

Example:

```
>>> sub("Lowercase: {{ name | lower }}", name="ALICE", lower=lambda x: x.lower())
'Lowercase: alice'
```

## Control Blocks[¶](#control-blocks "Link to this heading")

Tempita supports Python-like control flow directives.
These are evaluated at runtime and allow conditional rendering and iteration.

Each block has an explicit closing directive such as `endif` or `endfor`.

### `if` / `elif` / `else` block[¶](#if-elif-else-block "Link to this heading")

Conditional execution based on an expression.

Syntax:

```
{{if condition}}
  ... content if true ...
{{elif other_condition}}
  ... content if elif is true ...
{{else}}
  ... content if all above are false ...
{{endif}}
```

Example:

```
>>> tmpl = Template("""
... {{if x > 0}}
... Positive
... {{elif x == 0}}
... Zero
... {{else}}
... Negative
... {{endif}}
... """)
>>> tmpl.substitute(x=-5)
'Negative\n'
```

### `for` block[¶](#for-block "Link to this heading")

Iterate over a sequence and render the body for each element.

Syntax:

```
{{for var in iterable}}
  ... body using {{var}} ...
{{endfor}}
```

You may also unpack tuples or iterate with multiple variables, as known from Python for-loops.

Example:

```
>>> tmpl = Template("""
... {{for name, score in scores}}
... {{name}}: {{score}}
... {{endfor}}
... """)
>>> print(tmpl.substitute(scores=[("Alice", 95), ("Bob", 88)]))
Alice: 95
Bob: 88
```

Note

As known from Python’s for-loop, Tempita `for` blocks also support `{{break}}` and `{{continue}}` statements.

### Nesting Blocks[¶](#nesting-blocks "Link to this heading")

Blocks can be nested arbitrarily.

```
>>> tmpl = Template("""
... {{for item in items}}
...   {{if item < 0}}
...   {{continue}}
...   {{elif item % 2 == 0}}
...   {{item}} is even
...   {{else}}
...   {{item}} is odd
...   {{endif}}
... {{endfor}}
... """)
>>> print(tmpl.substitute(items=[-1, 1, 2, 3]))
  1 is odd
  2 is even
  3 is odd
```

### Indentation, Whitespace, and Newlines[¶](#indentation-whitespace-and-newlines "Link to this heading")

* Templates preserve whitespace exactly as written around directives.
* Newlines in templates become newlines in outputs.
* Indentation is preserved, so control block bodies should be indented
  meaningfully by the template author if you want nice output.

## Examples[¶](#examples "Link to this heading")

Here are consolidated examples showing most of the available syntax in use:

```
from Cython.Tempita import Template

tmpl = Template("""
Header
{{# This is a comment }}

{{if user["is_admin"]}}
  Welcome, Admin {{user["name"]}}!
{{else}}
  Hello, {{user["name"] or 'Guest'}}.
{{endif}}

{{for item in items}}
  * {{item["name"]}}: {{item["value"]}}
{{endfor}}

{{py: x = 1 + 2}}
Inline code result: {{x}}

Expression: 1 + 2 = {{1 + 2}}

""")

print(tmpl.substitute(user={'name': 'Bob', 'is_admin': False},
                      items=[{'name':'A','value':10},
                             {'name':'B','value':20}]))
```

Output:

```
Header
  Hello, Bob.

  * A: 10
  * B: 20

Expression: 1 + 2 = 3
```

## Notes and Limitations[¶](#notes-and-limitations "Link to this heading")

* Templates are evaluated when they are substituted, rather than when they are created; errors show up when calling
  `substitute()`.
* There is no sandbox: template code can execute arbitrary Python expressions.

[![Logo](../../_static/cythonlogo.png)](../../index.html "../../index.html")

### [Table of Contents](../../index.html "../../index.html")

* [Tempita templating language](# "#")
  + [Overview](#overview "#overview")
  + [Templating Syntax](#templating-syntax "#templating-syntax")
    - [Simple Expression Substitution](#simple-expression-substitution "#simple-expression-substitution")
    - [Default Values](#default-values "#default-values")
    - [Inline Python Code](#inline-python-code "#inline-python-code")
    - [Comments](#comments "#comments")
    - [Custom delimiter characters](#custom-delimiter-characters "#custom-delimiter-characters")
    - [Filters](#filters "#filters")
  + [Control Blocks](#control-blocks "#control-blocks")
    - [`if` / `elif` / `else` block](#if-elif-else-block "#if-elif-else-block")
    - [`for` block](#for-block "#for-block")
    - [Nesting Blocks](#nesting-blocks "#nesting-blocks")
    - [Indentation, Whitespace, and Newlines](#indentation-whitespace-and-newlines "#indentation-whitespace-and-newlines")
  + [Examples](#examples "#examples")
  + [Notes and Limitations](#notes-and-limitations "#notes-and-limitations")

#### Previous topic

[Free threading](freethreading.html "previous chapter")

#### Next topic

[Troubleshooting](troubleshooting.html "next chapter")

### This Page

* [Show Source](../../_sources/src/userguide/tempita.rst.txt "../../_sources/src/userguide/tempita.rst.txt")

### Quick search

### Navigation

* [next](troubleshooting.html "Troubleshooting")
* [previous](freethreading.html "Free threading") |
* [Cython 3.2.0b1 documentation](../../index.html "../../index.html") »
* [Users Guide](index.html "index.html") »
* Tempita templating language

© Copyright 2025, Stefan Behnel, Robert Bradshaw, Dag Sverre Seljebotn, Greg Ewing, William Stein, Gabriel Gellner, et al..
Created using [Sphinx](https://www.sphinx-doc.org/ "https://www.sphinx-doc.org/") 7.2.6.

