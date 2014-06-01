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

