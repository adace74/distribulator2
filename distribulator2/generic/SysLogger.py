######################################################################
#
# $Id$
#
# Name: SysLogger.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import atexit
import os
import os.path
import readline
import sys

class SysLogger:
    "A simple example class"
    i = 12345
    def hello(self):
        print "Hello world"
        return
