#! /usr/bin/env python

from __future__ import print_function

import argparse
import sys
import html5lib
import io

from page_loader import *
from html5lib import treebuilders
from lxml import etree
from BeautifulSoup import UnicodeDammit

def anymlToTree(stream, debug=False):
    ml_string = stream.read()
    parser = etree.XMLParser(remove_blank_text=True)
    try:
        if debug: sys.stderr.write("xml\n")
        etree_document = etree.XML(ml_string.decode("utf8"), parser)
    except (etree.XMLSyntaxError, UnicodeDecodeError):
        try:
            if debug: sys.stderr.write("xml with root\n")
            ml_string2 = u"<root>" + ml_string.decode("utf8") + u"</root>"
            etree_document = etree.XML(ml_string2, parser)
            ml_string = ml_string2
        except (etree.XMLSyntaxError, UnicodeDecodeError):
            if debug: sys.stderr.write("html\n")
            parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)
            etree_document = parser.parse(ml_string, parser)
    
    return etree_document

def main():
    parser = argparse.ArgumentParser(description='pyxpath filter an html flux with an xpath expression.')
    parser.add_argument('xpathexpr', default=".", help="xpath expression")
    parser.add_argument('file', nargs="?", default=None, help="file to read, if not set will read stdin")
    parser.add_argument('-d', '--debug', action='store_true', help='display debug messages')
    
    # Read the args
    args = parser.parse_args()
    
    if args.file is None:
        input_stream = sys.stdin
    else:
        input_stream = open(args.file, "r")
    
    etree_document = anymlToTree(input_stream)

    doc = etree.ElementTree()
    
    for elem in etree_document.xpath(args.xpathexpr):
        try:
            print(etree.tostring(elem, pretty_print=True), end="")
        except TypeError: # a text node
            sys.stdout.write(elem.encode("utf8"))
            if not elem.endswith("\n"):
                print("")

if __name__ == "__main__":
    try:
        main()
        sys.stdout.flush()
    except KeyboardInterrupt:
        sys.exit(130)
    except (IOError, OSError):
        sys.exit(141)
        


