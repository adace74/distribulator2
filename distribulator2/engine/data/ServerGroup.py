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
    def getServerList(self):
        return self.thisServerList

    def setServerList(self, PassedServerList):
        self.thisServerList = PassedServerList

    def addServer(self, PassedServer):
        self.thisServerList.append(PassedServer)

    def getServerByName(self, PassedServerName):
        for thisServer in self.thisServerList:
            if ( PassedServerName == thisServer.getName() ):
                return thisServer

######################################################################
