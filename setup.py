#!/usr/bin/env python

from distutils.core import setup

setup(name='pyxpath',
      version='0.1',
      description='PYthon XPATH interpretor',
      author='playest',
      author_email='playest.ff@laposte.net',
      #packages=['pyxpath'],
      py_modules=['pyxpath'],
      scripts = ['bin/pyxpath']
     )