######################################################################
#
# $Id$
#
# Name: XMLParser.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import string
import sys
import xml.dom.minidom

# Custom modules
import engine.data.GlobalConfig
import engine.data.Server
import engine.data.ServerGroup

######################################################################

class XMLFileParser:

    def parse(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig
        self._isEnvFound = False
        self._serverGroupList = []

        thisFilename = os.path.join(self._globalConfig.getConfigDir(), \
                                    'config.xml')

        try:
            thisConfigLines = 0

            thisFile = open(thisFilename, 'r')
            for thisLine in thisFile:
                thisConfigLines = thisConfigLines + 1
            thisFile.close()

            self._globalConfig.setConfigLines(thisConfigLines)
            
            thisDom = xml.dom.minidom.parse(thisFilename)

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename))
            sys.exit(1)

        self.handleConfig(thisDom)

        if (self._isEnvFound):
            return self._globalConfig
        else:
            print("ERROR: No matching tags found for environment '" +
                  self._globalConfig.getServerEnv() + "' in config.xml!")
            sys.exit(1)

    # Gotta clean this up some day...
    def getText(self, nodelist):
        rc = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                return rc

    def handleConfig(self, PassedConfig):
        self.handleBinaries(PassedConfig.getElementsByTagName('binary'))
        self.handleLogging(PassedConfig.getElementsByTagName('logging')[0])
        self.handleEnvironments(PassedConfig.getElementsByTagName('environment'))

    # Binary locations.
    def handleBinaries(self, PassedBinaries):
        for Binary in PassedBinaries:
            self.handleBinary(Binary)

    def handleBinary(self, PassedBinary):
        thisName = PassedBinary.getAttribute('name')
        thisValue = PassedBinary.getAttribute('value')
        if (thisName == 'logname'):
            self._globalConfig.setLognameBinary(thisValue)
        elif (thisName == 'ping'):
            self._globalConfig.setPingBinary(thisValue)
        elif (thisName == 'scp'):
            self._globalConfig.setScpBinary(thisValue)
        elif (thisName == 'ssh'):
            self._globalConfig.setSshBinary(thisValue)

    # Logging options.
    def handleLogging(self, PassedLogging):
        self._globalConfig.setSyslogFacility(
            PassedLogging.getAttribute('facility').strip() )

    # Server environments, groups, and individual servers.
    def handleEnvironments(self, PassedEnvironments):
        for Environment in PassedEnvironments:
            self.handleEnvironment(Environment)

    def handleEnvironment(self, PassedEnvironment):
        # Only load the environment specified on startup.
        if ( PassedEnvironment.getAttribute('name') ==
             self._globalConfig.getServerEnv() ):
            self._isEnvFound = True
            self.handleServerGroups(
                PassedEnvironment.getElementsByTagName('servergroup') )

    def handleServerGroups(self, PassedServerGroups):
        for ServerGroup in PassedServerGroups:
            self._serverGroupList.append( self.handleServerGroup(ServerGroup) )

        self._globalConfig.setServerGroupList(self._serverGroupList)

    def handleServerGroup(self, PassedServerGroup):
        thisServerGroup = engine.data.ServerGroup.ServerGroup()
        thisServerGroup.setName(
            PassedServerGroup.getAttribute('name').strip() )
        thisServerGroup.setUsername(
            PassedServerGroup.getAttribute('username').strip() )
        thisServerGroup = self.handleServers( thisServerGroup,
                                              PassedServerGroup.getElementsByTagName('server') )

        return thisServerGroup

    def handleServers(self, PassedServerGroup, PassedServers):
        thisServerGroup = PassedServerGroup

        for thisServer in PassedServers:
            thisServerGroup.addServer( self.handleServer(thisServer) )

        for thisServer in thisServerGroup.getServerList():
            thisServer.setUsername( thisServerGroup.getUsername() )

        return thisServerGroup

    def handleServer(self, PassedServer):
        thisServer = engine.data.Server.Server()
        thisServer.setName( self.getText(PassedServer.childNodes).strip() )

        return thisServer

######################################################################
