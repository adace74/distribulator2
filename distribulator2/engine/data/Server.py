######################################################################
#
# $Id$
#
# Name: Server.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import os
    import os.path
    import string
    import sys

except ImportError:
    print "An error occured while loading Python modules, exiting..."
    sys.exit(1)

######################################################################

class Server:
    #
    # Name.
    #
    def getName(self):
        return self.thisName

    def setName(self, PassedName):
        self.thisName = PassedName
    #
    # Username.
    #
    def getUsername(self):
        return self.thisUsername

    def setUsername(self, PassedUsername):
        self.thisUsername = PassedUsername

######################################################################
