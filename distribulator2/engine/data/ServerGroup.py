######################################################################
#
# $Id$
#
# Name: ServerGroup.py
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
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

class ServerGroup:
    #
    # Constructor.
    #
    def __init__(self):
        self.thisServerCount = 0
        self.thisServerList = []
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
    #
    # Servers.
    #
    def getServerCount(self):
        return self.thisServerCount

    def getServerList(self):
        return self.thisServerList

    def addServer(self, PassedServer):
        self.thisServerCount = self.thisServerCount + 1
        self.thisServerList.append(PassedServer)

    def getServerByName(self, PassedServerName):
        for thisServer in self.thisServerList:
            if ( PassedServerName == thisServer.getName() ):
                return thisServer

        return False

######################################################################
