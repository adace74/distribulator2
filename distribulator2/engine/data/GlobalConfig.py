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
        return self.thisConfigDir

    def setConfigDir(self, PassedConfigDir):
        self.thisConfigDir = PassedConfigDir
    #
    # Our helpfiles path.
    #
    def getHelpDir(self):
        return self.thisHelpDir

    def setHelpDir(self, PassedHelpDir):
        self.thisHelpDir = PassedHelpDir
    #
    # Number of config lines loaded.
    #
    def getConfigLines(self):
        return self.thisConfigLines

    def setConfigLines(self, PassedConfigLines):
        self.thisConfigLines = PassedConfigLines
    #
    # System binary locations.
    #
    def getScpBinary(self):
        return self.thisScpBinary

    def setScpBinary(self, PassedScpBinary):
        self.thisScpBinary = PassedScpBinary

    def getSshBinary(self):
        return self.thisSshBinary

    def setSshBinary(self, PassedSshBinary):
        self.thisSshBinary = PassedSshBinary
    #
    # Syslog Facility.
    #
    def getSyslogFacility(self):
        return self.thisSyslogFacility

    def setSyslogFacility(self, PassedSyslogFacility):
        self.thisSyslogFacility = PassedSyslogFacility
    #
    # Server Environment.
    #
    def getServerEnv(self):
        return self.thisServerEnv

    def setServerEnv(self, PassedServerEnv):
        self.thisServerEnv = PassedServerEnv
    #
    # Unix command "pass through" list.
    #
    def getPassThruList(self):
        return self.thisPassThruList

    def setPassThruList(self, PassedPassThruList):
        self.thisPassThruList = PassedPassThruList
    #
    # Servers and ServerGroups
    #
    def getCurrentServerGroup(self):
        return self.thisCurrentServerGroup

    def setCurrentServerGroup(self, PassedServerGroup):
        self.thisCurrentServerGroup = PassedServerGroup

    def getServerGroupList(self):
        return self.thisServerGroupList

    def setServerGroupList(self, PassedServerGroupList):
        self.thisServerGroupList = PassedServerGroupList

    def addServerGroup(self, PassedServerGroup):
        self.thisServerGroupList.append(PassedServerGroup)

    def getServerGroupByName(self, PassedServerGroupName):
        for thisServerGroup in self.thisServerGroupList:
            if (PassedServerGroupName == thisServerGroup.getName()):
                return thisServerGroup

######################################################################
