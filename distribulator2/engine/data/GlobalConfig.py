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

    def getConfigDir(self):
        """This is a typical accessor method."""

        return self._configDir

######################################################################

    def setConfigDir(self, PassedConfigDir):
        """This is a typical accessor method."""

        self._configDir = PassedConfigDir

######################################################################
# Our exit code.
######################################################################

    def getExitCode(self):
        """This is a typical accessor method."""

        return self._exitCode

######################################################################

    def setExitCode(self, PassedExitCode):
        """This is a typical accessor method."""

        self._exitCode = PassedExitCode

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
# Syslogger Object.
######################################################################

    def getSysLogger(self):
        """This is a typical accessor method."""

        return self._sysLogger

######################################################################

    def setSysLogger(self, PassedSysLogger):
        """This is a typical accessor method."""

        self._sysLogger = PassedSysLogger

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

        for thisServerGroup in self._serverGroupList:
            if ( thisServerGroup.getServerByName(PassedServerName) ):
                return thisServerGroup.getServerByName(PassedServerName)

        return False

######################################################################

    def getServerGroupByName(self, PassedServerGroupName):
        """This is a typical accessor method, including some search logic."""

        PassedServerGroupName = PassedServerGroupName.strip()

        for thisServerGroup in self._serverGroupList:
            if (PassedServerGroupName == thisServerGroup.getName()):
                return thisServerGroup

        return False

######################################################################
