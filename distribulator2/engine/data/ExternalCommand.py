######################################################################
#
# $Id$
#
# Name: ExternalCommand.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import commands
    import os
    import os.path
    import string
    import sys

except ImportError:
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

class ExternalCommand:

    #
    # Constructor.
    #
    def __init__(self):
        self._seperator = '----------------------------------------------------------------------'

    #
    # Unix command line string.
    #
    def getCommand(self):
        return self._command
    
    def setCommand(self, PassedCommand):
        self._command = PassedCommand
    #
    # Function methods.
    #
    def run(self):
        print("EXEC:  " + self._command)

        thisStatus, thisOutput = commands.getstatusoutput(self._command)
        print(thisOutput)
        print(self._seperator)

        if (thisStatus != 0):
            print("ERROR: Local shell returned error state.")

        return thisStatus

######################################################################
