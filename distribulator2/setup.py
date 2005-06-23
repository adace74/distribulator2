#!@PYTHON_BIN@
######################################################################
#
# $Id$
#
######################################################################

# Pydoc comments
"""Distutils-based setup logic for The Distribulator."""

# File version tag
__version__ = '$Revision$'[11:-2]

# Standard modules
import os
import glob
from distutils.core import setup

# Uhhh...this is code...
docs =  [x for x in glob.glob('doc/**') if os.path.isfile(x)]
confs = [x for x in glob.glob('conf/**') if os.path.isfile(x)]
examples = [x for x in glob.glob('examples/**') if os.path.isfile(x)]

# Uhhh...this is more code...
setup(name = "Distribulator",
      author = 'Adam W. Dace',
      author_email = 'adam@turing.com',
      data_files = [
        ('conf', confs),
        ('doc', docs),
        ('log', []),
        ('examples', examples),
      ]
      packages = [
        'engine', 'engine.command', 'engine.conf',
        'engine.data', 'engine.misc', 'engine.mode',
        'generic'
      ],
      scripts = ['distribulator.py'],
      url='http://www.sf.net/projects/distribulator/',
      version = '0.9.1',
)
