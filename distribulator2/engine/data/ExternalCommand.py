######################################################################
#
# $Id$
#
# Name: ExternalCommand.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import commands
import os
import os.path
import string
import sys

######################################################################

class ExternalCommand:

    #
    # Constructor.
    #
    def __init__(self):
        self.thisSeperator = '============================================================'

    #
    # Unix command line string.
    #
    def getCommand(self):
        return self.thisCommand
    
    def setCommand(self, PassedCommand):
        self.thisCommand = PassedCommand
    #
    # Function methods.
    #
    def run(self):
        print "EXEC:  " + self.thisCommand
        self.thisStatus, self.thisOutput = commands.getstatusoutput(self.thisCommand)
        print self.thisOutput
        print self.thisSeperator

        if (self.thisStatus != 0):
            print "ERROR: Local shell returned error state."

######################################################################
