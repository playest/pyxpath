The --help is pretty self-explanatory.

```
usage: pyxpath [-h] [-a ACTION] [-f [FILE]] [-d] exprs [exprs ...]

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
```

Try : cat explxml.xml | ./pypath.py '//country'

= Install

To install pyxpath you can download the sources (or clone the repository) and run :
	`pip install --user -e path/to/source/directory`
or :
	`pip install --user -e git://github.com/playest/pyxpath.git#egg=pyxpath`

It will install the program into the current directory.

