######################################################################
#
# $Id$
#
# Name: GlobalConfig.py
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

class GlobalConfig:
    #
    # Global settings.
    #
    # Our configuration directory path.
    #
    def getConfigDir(self):
        return self._configDir

    def setConfigDir(self, PassedConfigDir):
        self._configDir = PassedConfigDir
    #
    # Our helpfiles path.
    #
    def getHelpDir(self):
        return self._helpDir

    def setHelpDir(self, PassedHelpDir):
        self._helpDir = PassedHelpDir
    #
    # Number of config lines loaded.
    #
    def getConfigLines(self):
        return self._configLines

    def setConfigLines(self, PassedConfigLines):
        self._configLines = PassedConfigLines
    #
    # System binary locations.
    #
    def getScpBinary(self):
        return self._scpBinary

    def setScpBinary(self, PassedScpBinary):
        self._scpBinary = PassedScpBinary

    def getSshBinary(self):
        return self._sshBinary

    def setSshBinary(self, PassedSshBinary):
        self._sshBinary = PassedSshBinary
    #
    # Syslog Facility.
    #
    def getSyslogFacility(self):
        return self._syslogFacility

    def setSyslogFacility(self, PassedSyslogFacility):
        self._syslogFacility = PassedSyslogFacility
    #
    # Server Environment.
    #
    def getServerEnv(self):
        return self._serverEnv

    def setServerEnv(self, PassedServerEnv):
        self._serverEnv = PassedServerEnv
    #
    # Unix command "pass through" list.
    #
    def getPassThruList(self):
        return self._passThruList

    def setPassThruList(self, PassedPassThruList):
        self._passThruList = PassedPassThruList
    #
    # Servers and ServerGroups
    #
    def getCurrentServerGroup(self):
        return self._currentServerGroup

    def setCurrentServerGroup(self, PassedServerGroup):
        self._currentServerGroup = PassedServerGroup

    def getServerGroupList(self):
        return self._serverGroupList

    def setServerGroupList(self, PassedServerGroupList):
        self._serverGroupList = PassedServerGroupList

    def addServerGroup(self, PassedServerGroup):
        self._serverGroupList.append(PassedServerGroup)

    def getServerGroupByName(self, PassedServerGroupName):
        for thisServerGroup in self._serverGroupList:
            if (PassedServerGroupName == thisServerGroup.getName()):
                return thisServerGroup

        return False

######################################################################
