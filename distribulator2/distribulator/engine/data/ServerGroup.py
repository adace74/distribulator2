######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding a given server group."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import re
import string

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

    def getAttribValueServerList(self, PassedAttribValue):
        """This is a typical accessor method."""

        myTempList=[]
        PassedAttribValue = string.replace(PassedAttribValue, '[', '')
        PassedAttribValue = string.replace(PassedAttribValue, ']', '')

        for myServer in self._serverList:
             for myValue in myServer.getAttributes().values():
                 if (myValue == PassedAttribValue):
                     myTempList.append(myServer)

        return myTempList

######################################################################

    def getRegExServerList(self, regex):
        """This is a typical accessor method."""

	newlist=[]
	reggie=re.compile(regex)
	for i in self._serverList:
		if (reggie.search(i.getName()) != None):
			newlist.append(i)
        return newlist

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
