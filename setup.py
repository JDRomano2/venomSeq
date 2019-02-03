#!/usr/bin/env python

from distutils.core import setup

setup(
  name='VenomSeq',
  version='1.0a',
  description='Python code for performing the data analysis in the VenomSeq workflow',
  author='Joseph D. Romano',
  author_email='jdromano2@gmail.com',
  url='https://jdr.bio/research',
  packages=['venomseq'],
  package_dir={'venomseq': 'venomseq'}
)