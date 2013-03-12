# -*- coding:Utf-8 -*-

import urllib2
import logging
import os
import codecs

try:
    import html5lib
except ImportError:
    logging.critical(sys.path)
    logging.critical(sys.argv[0])
    raise

from html5lib import treebuilders
from BeautifulSoup import UnicodeDammit
from BeautifulSoup import BeautifulSoup

def decode_html(html_string):
    """Convert a string into the UTF-8 encoding"""
    converted = UnicodeDammit(html_string, isHTML=True)
    if not converted.unicode:
        raise UnicodeDecodeError("Failed to detect encoding, tried [%s]", ', '.join(converted.triedEncodings))
    return converted.unicode

class PageLoader:
    def __init__(self, cache_url=None):
        self.cache_url = cache_url
        self.parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("lxml"), namespaceHTMLElements=False)

    def put_in_cache(self, url, content):
        if self.cache_url != None:
            filtered_url = self.filter_url(url)
            cached_page = codecs.open(os.path.join(self.cache_url, filtered_url), "w+", encoding='utf-8')
            cached_page.write(content)
    
    def get_from_cache(self, url):
        filtered_url = self.filter_url(url)
        cached_page = codecs.open(os.path.join(self.cache_url, filtered_url), "r", encoding='utf-8')
        content = cached_page.read()
        return content
        
    def is_cached(self, url):
        if self.cache_url == None:
            return False
        else:
            filtered_url = self.filter_url(url)
            return os.path.exists(os.path.join(self.cache_url, filtered_url))
    
    def filter_url(self, url):
        return url.replace("http://", "").replace("?", "_").replace("/", "_").replace("=", "_").replace("&", "_")
    
    def load_and_parse_page(self, url):
        """load a web page and parse it, return the dom tree"""
        logging.info("load " + url)

        if self.is_cached(url):
            html_of_page = self.get_from_cache(url)
        else:
            try:
                web_page_socket = urllib2.urlopen(url)
                html_of_page = decode_html(web_page_socket.read())
                self.put_in_cache(url, html_of_page)
            except urllib2.HTTPError as err:
                logging.critical(err.url)
                logging.critical(dir(err))
                raise

        etree_document = self.parser.parse(html_of_page)
        return etree_document
