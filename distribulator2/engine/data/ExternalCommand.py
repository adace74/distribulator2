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
import os
import os.path
import string
import sys

######################################################################

class ExternalCommand:

    #
    # Unix command line string.
    #
    def getCommandLine(self):
        return self.thisCommandLine
    
    def setCommandLine(self, PassedCommandLine):
        self.thisCommandLine = PassedCommandLine
    #
    # Other options.  What else should go here?
    #
    # isLogged()
    # setLogged()
    #

######################################################################
