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

    def loadAll(self, PassedCommLine, PassedConfigDir):
        # Load GNU Readline history.
        print('Loading config. from ' + PassedConfigDir)
        thisLinesLoaded = PassedCommLine.initHistory()
        print("- Readline history: %d lines loaded." % thisLinesLoaded)
        
        # Load Unix pass-through commands.
        thisPassThruList = []

        thisFile = open( os.path.join(PassedConfigDir, \
                                      'pass_through_cmds.txt'), 'r' )

        for thisLine in thisFile:
            thisLine = thisLine.strip()
            thisPassThruList.append(thisLine)

        thisFile.close()

        print( "- Pass-through Unix commands: %d lines loaded." \
               % len(thisPassThruList) )

        # Parse XML...ouchies.
        print("- Global options and settings.")
        print("- Entering interactive mode...")
        print

        return thisPassThruList

######################################################################
