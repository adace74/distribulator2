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
        self._serverCount = 0
        self._serverList = []
    #
    # Name.
    #
    def getName(self):
        return self._name

    def setName(self, PassedName):
        self._name = PassedName
    #
    # Username.
    #
    def getUsername(self):
        return self._username

    def setUsername(self, PassedUsername):
        self._username = PassedUsername
    #
    # Servers.
    #
    def getServerCount(self):
        return self._serverCount

    def getServerList(self):
        return self._serverList

    def addServer(self, PassedServer):
        self._serverCount = self._serverCount + 1
        self._serverList.append(PassedServer)

    def getServerByName(self, PassedServerName):
        for thisServer in self._serverList:
            thisIndex = string.find(thisServer.getName(), PassedServerName)

            if (thisIndex != -1):
                return thisServer

        return False

######################################################################
