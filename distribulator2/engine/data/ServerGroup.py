######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding a given server group."""

# Version tag
__version__= '$Revision$'[11:-2]

######################################################################

class ServerGroup:
    """This class holds data regarding a given server group."""

    def __init__(self):
        """Constructor."""

        self._serverCount = 0
        self._serverList = []

######################################################################
# Name.
######################################################################

    def getName(self):
        """This is a typical accessor method."""

        return self._name

######################################################################

    def setName(self, PassedName):
        """This is a typical accessor method."""

        self._name = PassedName

######################################################################
# Username.
######################################################################

    def getUsername(self):
        """This is a typical accessor method."""

        return self._username

######################################################################

    def setUsername(self, PassedUsername):
        """This is a typical accessor method."""

        self._username = PassedUsername

######################################################################
# SSH Version.
######################################################################

    def getVersion(self):
        """This is a typical accessor method."""

        return self._version

######################################################################

    def setVersion(self, PassedVersion):
        """This is a typical accessor method."""

        self._version = PassedVersion

######################################################################
# Servers.
######################################################################

    def getServerCount(self):
        """This is a typical accessor method."""

        return self._serverCount

######################################################################

    def getServerList(self):
        """This is a typical accessor method."""

        return self._serverList

######################################################################

    def addServer(self, PassedServer):
        """This is a typical accessor method."""

        self._serverCount = self._serverCount + 1
        self._serverList.append(PassedServer)

######################################################################

    def getServerByName(self, PassedServerName):
        """This is a typical accessor method."""

        PassedServerName = PassedServerName.strip()

        for myServer in self._serverList:

            # Match by full hostname.
            # i.e. 'app01.somewhere.com' will match 'app01.somewhere.com'
            if (PassedServerName == myServer.getName()):
                return myServer

            # Match by hostname prefix.
            # i.e. 'app01' will match app01.somewhere.com
            myDotIndex = myServer.getName().find('.')

            if (myDotIndex != -1):
                if (PassedServerName == myServer.getName()[:myDotIndex]):
                    return myServer

        return False

######################################################################
