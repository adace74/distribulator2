######################################################################
#
# $Id$
#
# Name: ConfigLoader.py
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

# Custom modules
import engine.CommandLine

def load(myConfigDir):
    print("Loading configuration:")
    engine.CommandLine.initHistory()
    print("- Readline history.")
    print("- Pass-through Unix commands.")
    print("- Application settings and server lists.")
    print
