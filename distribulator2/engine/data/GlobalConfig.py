######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding our global configuraiton."""

# Version tag
__version__= '$Revision$'[11:-2]

######################################################################

class GlobalConfig:
    """This class holds data regarding our global configuraiton."""

    def __init__(self):
        """Constructor."""

        pass

######################################################################
#
# Application state flags.
#
######################################################################

    def isBatchMode(self):
        """This is a typical accessor method."""

        return self._isbatchflag

######################################################################

    def setBatchMode(self, PassedBatchMode):
        """This is a typical accessor method."""

        self._isbatchflag = PassedBatchMode

######################################################################

    def isBreakState(self):
        """This is a typical accessor method."""
    
        return self._breakState

######################################################################

    def setBreakState(self, PassedBreakState):
        """This is a typical accessor method."""
    
        self._breakState = PassedBreakState

######################################################################

    def isConsoleMode(self):
        """This is a typical accessor method."""

        return self._isconsoleflag

######################################################################

    def setConsoleMode(self, PassedConsoleMode):
        """This is a typical accessor method."""

        self._isconsoleflag = PassedConsoleMode

######################################################################

    def isExitSuccess(self):
        """This is a typical accessor method."""

        return self._exitSuccess

######################################################################

    def setExitSuccess(self, PassedExitSuccess):
        """This is a typical accessor method."""

        self._exitSuccess = PassedExitSuccess

######################################################################

    def isListMode(self):
        """This is a typical accessor method."""

        return self._islistflag

######################################################################

    def setListMode(self, PassedListMode):
        """This is a typical accessor method."""

        self._islistflag = PassedListMode

######################################################################

    def isLoadUsername(self):
        """This is a typical accessor method."""

        return self._isLoadUsername

######################################################################

    def setLoadUsername(self, PassedLoadUsername):
        """This is a typical accessor method."""

        self._isLoadUsername = PassedLoadUsername

######################################################################

    def isPrintUsername(self):
        """This is a typical accessor method."""

        return self._isPrintUsername

######################################################################

    def setPrintUsername(self, PassedPrintUsername):
        """This is a typical accessor method."""

        self._isPrintUsername = PassedPrintUsername

######################################################################
#
# Application filename storage.
#
######################################################################

    def getAppConfigFile(self):
        """This is a typical accessor method."""

        return self._appConfigFile

######################################################################

    def setAppConfigFile(self, PassedAppConfigFile):
        """This is a typical accessor method."""

        self._appConfigFile = PassedAppConfigFile

######################################################################

    def getBatchFile(self):
        """This is a typical accessor method."""

        return self._batchFile

######################################################################

    def setBatchFile(self, PassedBatchFile):
        """This is a typical accessor method."""

        self._batchFile = PassedBatchFile

######################################################################

    def getHelpDir(self):
        """This is a typical accessor method."""

        return self._helpDir

######################################################################

    def setHelpDir(self, PassedHelpDir):
        """This is a typical accessor method."""

        self._helpDir = PassedHelpDir

######################################################################

    def getLoggingConfigFile(self):
        """This is a typical accessor method."""
    
        return self._loggingConfigFile

######################################################################

    def setLoggingConfigFile(self, PassedLoggingConfigFile):
        """This is a typical accessor method."""
    
        self._loggingConfigFile = PassedLoggingConfigFile

######################################################################

    def getPassThruFile(self):
        """This is a typical accessor method."""

        return self._passThruFile

######################################################################

    def setPassThruFile(self, PassedPassThruFile):
        """This is a typical accessor method."""

        self._passThruFile = PassedPassThruFile

######################################################################
#
# Application runtime user settings
#
######################################################################

    def getDelaySecs(self):
        """This is a typical accessor method."""

        return self._delaySecs

######################################################################

    def setDelaySecs(self, PassedDelaySecs):
        """This is a typical accessor method."""

        self._delaySecs = PassedDelaySecs

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
# Logging Functionality.
######################################################################

    def getAuditLogger(self):
        """This is a typical accessor method."""

        return self._auditLogger

######################################################################

    def setAuditLogger(self, PassedAuditLogger):
        """This is a typical accessor method."""

        self._auditLogger = PassedAuditLogger

######################################################################

    def getStdoutLogger(self):
        """This is a typical accessor method."""
    
        return self._stdoutLogger

######################################################################

    def setStdoutLogger(self, PassedStdoutLogger):
        """This is a typical accessor method."""
    
        self._stdoutLogger = PassedStdoutLogger

######################################################################

    def getVerboseLevel(self):
        """This is a typical accessor method."""
   
        return self._verboseLevel

######################################################################
    
    def setVerboseLevel(self, PassedVerboseLevel):
        """This is a typical accessor method."""
        
        self._verboseLevel = PassedVerboseLevel

######################################################################
# Ping Options.
######################################################################

    def getPingBanner(self):      
        """This is a typical accessor method."""

        return self._pingBanner

######################################################################

    def setPingBanner(self, PassedPingBanner):
        """This is a typical accessor method."""

        self._pingBanner = PassedPingBanner

######################################################################

    def getPingPort(self):
        """This is a typical accessor method."""

        return self._pingPort

######################################################################

    def setPingPort(self, PassedPingPort):
        """This is a typical accessor method."""

        self._pingPort = PassedPingPort

######################################################################

    def getPingTimeout(self):      
        """This is a typical accessor method."""

        return self._pingTimeout

######################################################################

    def setPingTimeout(self, PassedPingTimeout):
        """This is a typical accessor method."""

        self._pingTimeout = PassedPingTimeout

######################################################################
# Config lines loaded.
######################################################################

    def getConfigLines(self):
        """This is a typical accessor method."""

        return self._configLines

######################################################################

    def setConfigLines(self, PassedConfigLines):
        """This is a typical accessor method."""

        self._configLines = PassedConfigLines

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
# Seperator bar.
######################################################################

    def getSeperator(self):
        """This is a typical accessor method."""

        return '----------------------------------------------------------------------'

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
#
# Servers and ServerGroups handlers
#
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
