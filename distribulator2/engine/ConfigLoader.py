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
import os
import os.path
import string
import sys

# Custom modules
import engine.CommandLine

######################################################################

class ConfigLoader:

    def load(self, myCommLine, myConfigDir):
        # Load GNU Readline history.
        print('Loading config. from ' + myConfigDir)
        myLinesLoaded = myCommLine.initHistory()
        print("- Readline history: %d lines loaded." % myLinesLoaded)
        
        # Load Unix pass-through commands.
        myPassThruList = []

        myFile = open( os.path.join(myConfigDir, 'pass_through_cmds.txt'), 'r' )

        for myLine in myFile:
            myLine = myLine.strip()
            myPassThruList.append(myLine)

        myFile.close()

        print( "- Pass-through Unix commands: %d lines loaded." \
               % len(myPassThruList) )

        # Parse XML...ouchies.
        print("- Global options and settings.")
        print("- Entering interactive mode...")
        print

        return myPassThruList

######################################################################
