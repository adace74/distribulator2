######################################################################
#
# $Id$
#
# Name: ServerGroup.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
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

class ServerGroup:

    def __init__(self):
        self._serverCount = 0
        self._serverList = []

######################################################################
# Name.
######################################################################

    def getName(self):
        return self._name

######################################################################

    def setName(self, PassedName):
        self._name = PassedName

######################################################################
# Username.
######################################################################

    def getUsername(self):
        return self._username

######################################################################

    def setUsername(self, PassedUsername):
        self._username = PassedUsername

######################################################################
# Servers.
######################################################################

    def getServerCount(self):
        return self._serverCount

######################################################################

    def getServerList(self):
        return self._serverList

######################################################################

    def addServer(self, PassedServer):
        self._serverCount = self._serverCount + 1
        self._serverList.append(PassedServer)

######################################################################

    def getServerByName(self, PassedServerName):
        PassedServerName = PassedServerName.strip()

        for thisServer in self._serverList:

            # Match by full hostname.
            # i.e. 'app01.somewhere.com' will match 'app01.somewhere.com'
            if (PassedServerName == thisServer.getName()):
                return thisServer

            # Match by hostname prefix.
            # i.e. 'app01' will match app01.somewhere.com
            thisDotIndex = thisServer.getName().find('.')

            if (thisDotIndex != -1):
                if (PassedServerName == thisServer.getName()[:thisDotIndex]):
                    return thisServer

        return False

######################################################################
