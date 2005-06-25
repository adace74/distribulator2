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

######################################################################

class Environment:
    """This class holds data regarding a given server group."""

    def __init__(self):
        """Constructor."""

        self._serverGroupCount = 0
        self._serverGroupList = []

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
# Servers.
######################################################################

    def getServerByName(self, PassedServerName):
        """This is a typical accessor method, including some search logic."""

        PassedServerName = PassedServerName.strip()

        for myServerGroup in self._serverGroupList:
            if ( myServerGroup.getServerByName(PassedServerName) ):
                return myServerGroup.getServerByName(PassedServerName)

        return False

######################################################################
# ServerGroups.
######################################################################

    def getServerGroupCount(self):
        """This is a typical accessor method."""

        return self._serverGroupCount

######################################################################

    def getServerGroupList(self):
        """This is a typical accessor method."""

        return self._serverGroupList

######################################################################

    def setServerGroupList(self, PassedServerGroupList):
        """This is a typical accessor method."""

        self._serverGroupList = PassedServerGroupList

######################################################################

    def getServerGroupByName(self, PassedServerGroupName):
        """This is a typical accessor method, including some search logic."""

        PassedServerGroupName = PassedServerGroupName.strip()

        # Handle regex.
        reggie = re.compile(r'(.*):r\'(.*)\'')
        maggie = reggie.match(PassedServerGroupName)

        if maggie != None:
            for myServerGroup in self._serverGroupList:
                if (maggie.group(1) == myServerGroup.getName()):
                     return myServerGroup
        else:
            for myServerGroup in self._serverGroupList:
                if (PassedServerGroupName == myServerGroup.getName()):
                     return myServerGroup

        return False

######################################################################

    def addServerGroup(self, PassedServerGroup):
        """This is a typical accessor method."""

        self._serverGroupCount = self._serverGroupCount + 1
        self._serverGroupList.append(PassedServerGroup)

######################################################################

    def getDefaultServerGroup(self):
        """This is a typical accessor method."""

        return self._defaultServerGroup

######################################################################

    def setDefaultServerGroup(self, PassedDefaultServerGroup):
        """This is a typical accessor method."""

        self._defaultServerGroup = PassedDefaultServerGroup

######################################################################
