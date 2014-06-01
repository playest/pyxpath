from __future__ import print_function

import argparse
import sys
import html5lib
import io
import collections

from html5lib import treebuilders
from lxml import etree
from BeautifulSoup import UnicodeDammit

def format_error_log_lxml(error_log):
    return str(error_log)
    #return "Error at line " + str(error_log[0].line) + ", col " + str(error_log[0].column) + ": " + error_log[0].message
    

def anymlToTree(stream, debug=False):
    ml_string = stream.read()
    parser = etree.XMLParser(strip_cdata=False, ns_clean=True)
    try:
        if debug: sys.stderr.write("xml\n")
        etree_document = etree.XML(ml_string.decode("utf-8-sig").encode("utf8"), parser)
    except (etree.XMLSyntaxError, UnicodeDecodeError) as err:
        try:
            if debug: sys.stderr.write("err = " + str(err) + "\n" + format_error_log_lxml(parser.error_log) + "\n" + "xml with root\n")
            ml_string2 = u"<root>" + ml_string.decode("utf-8-sig").encode("utf8") + u"</root>"
            etree_document = etree.XML(ml_string2, parser)
            ml_string = ml_string2
        except (etree.XMLSyntaxError, UnicodeDecodeError):
            if debug: sys.stderr.write("html\n" + format_error_log_lxml(parser.error_log) + "\n")
            parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
            etree_document = parser.parse(ml_string, parser)
    
    if debug and etree_document is None: sys.stderr.write(format_error_log_lxml(parser.error_log))
    
    return etree_document

#cat explxml.xml | ./pypath.py '//country' -a "concat('--', \$0/@name, ',', '.')"
#cat explxml.xml | ./pypath.py '//country' -a 'concat($0/@name, " ", $0/rank)'

def main():
    parser = argparse.ArgumentParser(description='pyxpath filter an html flux with an xpath expression.')
    parser.add_argument('exprs', nargs="+", default=".", help="one or more xpath expressions")
    parser.add_argument('-a', '--action', default=None, help="action to apply on the results. The default is to display the node.")
    parser.add_argument('-f', '--file', nargs="?", default=None, help="file to read, if not set will read stdin.")
    parser.add_argument('-d', '--debug', action='store_true', help='display debug messages.')
    
    args = parser.parse_args()
    
    if args.file is None:
        input_stream = sys.stdin
    else:
        input_stream = open(args.file, "r")
    
    etree_document = anymlToTree(input_stream, args.debug)
    doc = etree.ElementTree()

    if args.debug: sys.stderr.write("action: " + str(args.action) + "\n")
    
    if args.action is None:
        elems = etree_document.xpath(args.exprs[0])
        if args.debug: sys.stderr.write("elems: " + str(len(elems)) + "\n")
        for elem in elems:
            try:
                if args.debug: sys.stderr.write("normal node\n")
                print(etree.tostring(elem, pretty_print=True), end="")
            except TypeError: # a text node
                if args.debug: sys.stderr.write("text node\n")
                sys.stdout.write(elem.encode("utf8"))
                if not elem.endswith(u"\n"):
                    print("")
    else:
        results = []
        for expr in args.exprs:
            result = []
            for elem in etree_document.xpath(expr):
                if isinstance(elem, str):
                    node = etree.Element(u"text")
                    node.text = elem
                else:
                    node = elem
                result.append(node)
            
            results.append(result)
        
        i = 0
        for result in results[0]:
            try:
                if args.debug: sys.stderr.write(etree.tostring(result, pretty_print=True))
                col = {str(k):r[i] for (k,r) in enumerate(results)}
                print(etree_document.xpath(args.action, **col).encode("utf8"))
                i += 1
            except IndexError:
                sys.stderr.write( str(i) + ", " + str(dir(result)) + "\n")

    input_stream.close()
