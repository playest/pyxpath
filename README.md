# Usage

```
usage: pyxpath [-h] [-a ACTION] [-f [FILE]] [-d] [-i] exprs [exprs ...]

pyxpath filter an html flux with an xpath expression.

positional arguments:
  exprs                 one or more xpath expressions

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        action to apply on the results. The default is to
                        display the node.
  -f [FILE], --file [FILE]
                        file to read, if not set will read stdin.
  -d, --debug           display debug messages.
  -i, --ignore-namespace
                        ignore namespaces.
```

# Examples

```xml
<root>
	<a>a</a>
	<a>aa</a>
	<b>
		<a>aaa</a>
	</b>
	<a>aaaa</a>
	<c>
		<d>ddd</d>
		<d>dd</d>
		<d>d</d>
	</c>
</root>
```

run: `pyxpath -f example.xml '//a'` (or `cat example.xml | pyxpath '//a'`)

will give :

```
<a>a</a>
<a>aa</a>
<a>aaa</a>
<a>aaaa</a>
```

You can also use the --action flag to do more complicated xpath commands : `pyxpath -f example.xml '//a' -a 'concat("#", $0)'`
will give :
```
#a
#aa
#aaa
#aaaa
```
Here `$0` refers to the first XPath expression (be careful with bash escaping and $ signs, in general use simple quotes).

With multiple expressions you can do stuffs like that: `pyxpath -f example.xml '//a' '//d' -a 'concat($0, "_", $1)'`
and get:
```
a_ddd
aa_dd
aaa_d
```
`$0` refers to '//a' and `$1` refers to '//d'. Note that the `<a>aaaa</a>` is ignored because there is only 3 `<d>` tags.

# Install

To install pyxpath you can download the sources (or clone the repository) and run :

	`pip install --user -e path/to/source/directory`

or :

	`pip install --user -e git://github.com/playest/pyxpath.git#egg=pyxpath`

It will install the program into the current directory.

