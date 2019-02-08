#!/usr/bin/env python

from distutils.core import setup

MAJOR       = 0
MINOR       = 1
PRERELEASE  = 'alpha'
ISRELEASED  = False
if PRERELEASE:
  VERSION = '%d.%d-%s' % (MAJOR, MINOR, PRERELEASE)
else:
  VERSION = '%d.%d' % (MAJOR, MINOR)


setup(
  name='VenomSeq',
  version=VERSION,
  description='Python code for performing the data analysis in the VenomSeq workflow',
  author='Joseph D. Romano',
  author_email='jdromano2@gmail.com',
  url='https://jdr.bio/research',
  packages=['venomseq'],
  package_dir={'venomseq': 'venomseq'}
)