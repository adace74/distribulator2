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
import glob
import os
import sys
from distutils.core import setup

# Glob magic courtesy of Brian Zimmer.
doc =  [x for x in glob.glob('doc/**') if os.path.isfile(x)]
conf = [x for x in glob.glob('conf/**') if os.path.isfile(x)]
examples = [x for x in glob.glob('examples/**') if os.path.isfile(x)]
src = [x for x in glob.glob('src/**') if os.path.isfile(x)]

# Setup magic courtesy of a combo of Brian Zimmer, Karl D'adamo, and Adace Dace.
setup(name = "Distribulator",
      author = 'Adam W. Dace',
      author_email = 'adam@turing.com',
      data_files = [
        ('conf', conf),
        ('doc', doc),
        ('log', []),
        ('examples', examples)
      ],
      description = 'Distributed Computing For The Rest Of Us',
      long_description = 'This is an SSH-based command execution and file transfer utility that includes support for batch, console, and shell integration modes, multiple server enviornments, and full audit logs.',
      packages = [
        'distribulator.engine', 'distribulator.engine.command',
        'distribulator.engine.conf', 'distribulator.engine.data', 'distribulator.engine.misc',
        'distribulator.engine.mode', 'distribulator.generic'
      ],
      scripts = [ 'scripts/distribulator.py' ],
      url = 'http://sourceforge.net/projects/distribulator/',
      version = '0.9.1'
)

# Sed-style magic to de-templatize a few files.
print "Boo"
