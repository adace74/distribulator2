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

######################################################################

class ConfigLoader:

    def load(self, myCommLine, myConfigDir):
        # Load GNU Readline history.
        print("Loading config. from " + myConfigDir + ":")
        myCommLine.initHistory()
        print("- Readline history.")
        
        # Load Unix pass-through commands.

        print("- Pass-through Unix commands.")

        # Parse XML...ouchies.
        print("- Application settings and server lists.")
        print("- Entering interactive mode...")
        print

######################################################################
