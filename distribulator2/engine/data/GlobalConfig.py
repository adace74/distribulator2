######################################################################
#
# $Id$
#
# Name: GlobalConfig.py
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

class GlobalConfig:
    #
    # Global settings.
    #
    # Our configuration directory path.
    #
    def getConfigDir(self):
        return self.thisConfigDir

    def setConfigDir(self, PassedConfigDir):
        self.thisConfigDir = PassedConfigDir
    #
    # System binary locations.
    #
    def getScpBinary(self):
        return self.thisScpBinary

    def setScpBinary(self, PassedScpBinary):
        self.thisScpBinary = PassedScpBinary

    def getSshBinary(self):
        return self.thisSshBinary

    def setSshBinary(self, PassedSshBinary):
        self.thisSshBinary = PassedSshBinary
    #
    # Unix command "pass through" list.
    #
    def getPassThruList(self):
        return self.thisPassThruList

    def setPassThruList(self, PassedPassThruList):
        self.thisPassThruList = PassedPassThruList
    #
    # Servers and ServerGroups
    #

######################################################################
