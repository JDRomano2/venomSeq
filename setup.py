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

with open("README.md", "r") as fp:
  long_description = fp.read()

setup(
  name='VenomSeq',
  version=VERSION,
  description='Python code for performing the data analysis in the VenomSeq workflow',
  long_description=long_description,
  author='Joseph D. Romano',
  author_email='jdromano2@gmail.com',
  url='https://github.com/jdromano2/venomseq',
  packages=['venomseq'],
  package_dir={'venomseq': 'venomseq'},
  classifiers=[
    "Development Status :: 3 - Alpha",
    "Environment :: Console",
    "Intended Audience :: Science/Research",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Programming Language :: Python :: 3.6",
    "Topic :: Scientific/Engineering :: Bio-Informatics"
  ]
)