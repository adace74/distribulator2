######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding our global configuraiton."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import string
import sys

######################################################################

class GlobalConfig:
    """This class holds data regarding our global configuraiton."""

    def __init__(self):
        """Constructor."""

        pass

######################################################################
# Which mode we're operating in.
######################################################################

    def isBatchMode(self):
        """This is a typical accessor method."""

        return self._isbatchflag

######################################################################

    def setBatchMode(self, PassedBatchMode):
        """This is a typical accessor method."""

        self._isbatchflag = PassedBatchMode

######################################################################
# Which mode we're operating in.
######################################################################

    def isConsoleMode(self):
        """This is a typical accessor method."""

        return self._isconsoleflag

######################################################################

    def setConsoleMode(self, PassedConsoleMode):
        """This is a typical accessor method."""

        self._isconsoleflag = PassedConsoleMode

######################################################################
# Which mode we're operating in.
######################################################################

    def isListMode(self):
        """This is a typical accessor method."""

        return self._islistflag

######################################################################

    def setListMode(self, PassedListMode):
        """This is a typical accessor method."""

        self._islistflag = PassedListMode

######################################################################
# Batch file name, if applicable.
######################################################################

    def getBatchFile(self):
        """This is a typical accessor method."""

        return self._batchFile

######################################################################

    def setBatchFile(self, PassedBatchFile):
        """This is a typical accessor method."""

        self._batchFile = PassedBatchFile

######################################################################
# Our configuration directory path.
######################################################################

    def getConfigFile(self):
        """This is a typical accessor method."""

        return self._configFile

######################################################################

    def setConfigFile(self, PassedConfigFile):
        """This is a typical accessor method."""

        self._configFile = PassedConfigFile

######################################################################
# Our exit code.
######################################################################

    def isExitSuccess(self):
        """This is a typical accessor method."""

        return self._exitSuccess

######################################################################

    def setExitSuccess(self, PassedExitSuccess):
        """This is a typical accessor method."""

        self._exitSuccess = PassedExitSuccess

######################################################################
# Our helpfiles path.
######################################################################

    def getHelpDir(self):
        """This is a typical accessor method."""

        return self._helpDir

######################################################################

    def setHelpDir(self, PassedHelpDir):
        """This is a typical accessor method."""

        self._helpDir = PassedHelpDir

######################################################################
# Our pass-through file path.
######################################################################

    def getPassThruFile(self):
        """This is a typical accessor method."""

        return self._passThruFile

######################################################################

    def setPassThruFile(self, PassedPassThruFile):
        """This is a typical accessor method."""

        self._passThruFile = PassedPassThruFile

######################################################################
# Should we be quiet?
######################################################################

    def isQuietMode(self):
        """This is a typical accessor method."""

        return self._quietMode

######################################################################

    def setQuietMode(self, PassedQuietMode):
        """This is a typical accessor method."""

        self._quietMode = PassedQuietMode

######################################################################
# Requested server or server group list, if applicable.
######################################################################

    def getRequestedList(self):
        """This is a typical accessor method."""

        return self._requestedlist

######################################################################

    def setRequestedList(self, PassedRequestedList):
        """This is a typical accessor method."""

        self._requestedlist = PassedRequestedList

######################################################################
# User-defined substitution variables.
######################################################################

    def getVar1(self):
        """This is a typical accessor method."""

        return self._var1

######################################################################

    def setVar1(self, PassedVar1):
        """This is a typical accessor method."""

        self._var1 = PassedVar1

######################################################################

    def getVar2(self):
        """This is a typical accessor method."""

        return self._var2

######################################################################

    def setVar2(self, PassedVar2):
        """This is a typical accessor method."""

        self._var2 = PassedVar2

######################################################################

    def getVar3(self):
        """This is a typical accessor method."""

        return self._var3

######################################################################

    def setVar3(self, PassedVar3):
        """This is a typical accessor method."""

        self._var3 = PassedVar3

######################################################################
# Number of config lines loaded.
######################################################################

    def getConfigLines(self):
        """This is a typical accessor method."""

        return self._configLines

######################################################################

    def setConfigLines(self, PassedConfigLines):
        """This is a typical accessor method."""

        self._configLines = PassedConfigLines

######################################################################
# System binary locations.
######################################################################

    def getLognameBinary(self):
        """This is a typical accessor method."""

        return self._lognameBinary

######################################################################

    def setLognameBinary(self, PassedLognameBinary):
        """This is a typical accessor method."""

        self._lognameBinary = PassedLognameBinary

######################################################################

    def getPingBinary(self):
        """This is a typical accessor method."""

        return self._pingBinary

######################################################################

    def setPingBinary(self, PassedPingBinary):
        """This is a typical accessor method."""

        self._pingBinary = PassedPingBinary

######################################################################

    def getScpBinary(self):
        """This is a typical accessor method."""

        return self._scpBinary

######################################################################

    def setScpBinary(self, PassedScpBinary):
        """This is a typical accessor method."""

        self._scpBinary = PassedScpBinary

######################################################################

    def getSshBinary(self):
        """This is a typical accessor method."""

        return self._sshBinary

######################################################################

    def setSshBinary(self, PassedSshBinary):
        """This is a typical accessor method."""

        self._sshBinary = PassedSshBinary

######################################################################
# Syslog Facility.
######################################################################

    def getSyslogFacility(self):
        """This is a typical accessor method."""

        return self._syslogFacility

######################################################################

    def setSyslogFacility(self, PassedSyslogFacility):
        """This is a typical accessor method."""

        self._syslogFacility = PassedSyslogFacility

######################################################################
# SysLogger Object.
######################################################################

    def getSysLogger(self):
        """This is a typical accessor method."""

        return self._sysLogger

######################################################################

    def setSysLogger(self, PassedSysLogger):
        """This is a typical accessor method."""

        self._sysLogger = PassedSysLogger

######################################################################
# MultiLogger Object.
######################################################################

    def getMultiLogger(self):
        """This is a typical accessor method."""

        return self._multiLogger

######################################################################

    def setMultiLogger(self, PassedMultiLogger):
        """This is a typical accessor method."""

        self._multiLogger = PassedMultiLogger

######################################################################
# Server Environment.
######################################################################

    def getServerEnv(self):
        """This is a typical accessor method."""

        return self._serverEnv

######################################################################

    def setServerEnv(self, PassedServerEnv):
        """This is a typical accessor method."""

        self._serverEnv = PassedServerEnv

######################################################################
# Unix command "pass through" list.
######################################################################

    def getPassThruList(self):
        """This is a typical accessor method."""

        return self._passThruList

######################################################################

    def setPassThruList(self, PassedPassThruList):
        """This is a typical accessor method."""

        self._passThruList = PassedPassThruList

######################################################################
# Local Unix username.
######################################################################

    def getUsername(self):
        """This is a typical accessor method."""

        return self._username

######################################################################

    def setUsername(self, PassedUsername):
        """This is a typical accessor method."""

        self._username = PassedUsername

######################################################################
# Local effective Unix username.
######################################################################

    def getRealUsername(self):
        """This is a typical accessor method."""

        return self._realUsername

######################################################################

    def setRealUsername(self, PassedRealUsername):
        """This is a typical accessor method."""

        self._realUsername = PassedRealUsername

######################################################################
# Servers and ServerGroups
######################################################################

    def getCurrentServerGroup(self):
        """This is a typical accessor method."""

        return self._currentServerGroup

######################################################################

    def setCurrentServerGroup(self, PassedServerGroup):
        """This is a typical accessor method."""

        self._currentServerGroup = PassedServerGroup

######################################################################

    def getServerGroupList(self):
        """This is a typical accessor method."""

        return self._serverGroupList

######################################################################

    def setServerGroupList(self, PassedServerGroupList):
        """This is a typical accessor method."""

        self._serverGroupList = PassedServerGroupList

######################################################################

    def addServerGroup(self, PassedServerGroup):
        """This is a typical accessor method."""

        self._serverGroupList.append(PassedServerGroup)

######################################################################

    def getServerByName(self, PassedServerName):
        """This is a typical accessor method, including some search logic."""

        PassedServerName = PassedServerName.strip()

        for myServerGroup in self._serverGroupList:
            if ( myServerGroup.getServerByName(PassedServerName) ):
                return myServerGroup.getServerByName(PassedServerName)

        return False

######################################################################

    def getServerGroupByName(self, PassedServerGroupName):
        """This is a typical accessor method, including some search logic."""

        PassedServerGroupName = PassedServerGroupName.strip()

        for myServerGroup in self._serverGroupList:
            if (PassedServerGroupName == myServerGroup.getName()):
                return myServerGroup

        return False

######################################################################
