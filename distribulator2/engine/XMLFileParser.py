######################################################################
#
# $Id$
#
# Name: XMLParser.py
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
    import xml.dom.minidom

    # Custom modules
    import engine.data.GlobalConfig
    import engine.data.Server
    import engine.data.ServerGroup

except ImportError:
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

class XMLFileParser:

    def parse(self, PassedGlobalConfig):
        self.thisGlobalConfig = PassedGlobalConfig
        self.thisFoundEnv = False
        self.thisServerGroupList = []

        thisFilename = os.path.join(self.thisGlobalConfig.getConfigDir(), \
                                    'config.xml')

        try:
            thisConfigLines = 0

            thisFile = open(thisFilename, 'r')
            for thisLine in thisFile:
                thisConfigLines = thisConfigLines + 1
            thisFile.close()

            self.thisGlobalConfig.setConfigLines(thisConfigLines)
            
            thisDom = xml.dom.minidom.parse(thisFilename)

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename))
            sys.exit(1)

        self.handleConfig(thisDom)

        if (self.thisFoundEnv):
            return self.thisGlobalConfig
        else:
            print("ERROR: No matching tags found for environment '" + self.thisGlobalConfig.getServerEnv() + "' in config.xml!")
            sys.exit(1)

    # Gotta clean this up some day...
    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                return rc

    def handleConfig(self, PassedConfig):
        self.handleBinary(PassedConfig.getElementsByTagName("binary")[0])
        self.handleLogging(PassedConfig.getElementsByTagName("logging")[0])
        self.handleEnvironments(PassedConfig.getElementsByTagName("environment"))

    # Binary locations.
    def handleBinary(self, PassedBinary):
        self.handleScp(PassedBinary.getElementsByTagName("scp")[0])
        self.handleSsh(PassedBinary.getElementsByTagName("ssh")[0])

    def handleScp(self, PassedScp):
        self.thisGlobalConfig.setScpBinary( self.getText(PassedScp.childNodes) )

    def handleSsh(self, PassedSsh):
        self.thisGlobalConfig.setSshBinary( self.getText(PassedSsh.childNodes) )

    # Logging options.
    def handleLogging(self, PassedLogging):
        self.handleFacility(PassedLogging.getElementsByTagName("facility")[0])

    def handleFacility(self, PassedFacility):
        self.thisGlobalConfig.setSyslogFacility( self.getText(PassedFacility.childNodes) )

    # Server environments, groups, and individual servers.
    def handleEnvironments(self, PassedEnvironments):
        for Environment in PassedEnvironments:
            self.handleEnvironment(Environment)

    def handleEnvironment(self, PassedEnvironment):
        if (self.handleEnvName(PassedEnvironment.getElementsByTagName("name")[0])):
            self.thisFoundEnv = True
            self.handleServerGroups(PassedEnvironment.getElementsByTagName("servergroup"))

    def handleEnvName(self, PassedEnvName):
        if ( self.thisGlobalConfig.getServerEnv() == self.getText(PassedEnvName.childNodes) ):
            return True
        else:
            return False

    def handleServerGroups(self, PassedServerGroups):
        for ServerGroup in PassedServerGroups:
            self.thisServerGroupList.append( self.handleServerGroup(ServerGroup) )

        self.thisGlobalConfig.setServerGroupList(self.thisServerGroupList)

    def handleServerGroup(self, PassedServerGroup):
        thisServerGroup = engine.data.ServerGroup.ServerGroup()
        thisServerGroup.setName( self.handleGroupName(PassedServerGroup.getElementsByTagName("name")[0]) )
        thisServerGroup.setUsername( self.handleUsername(PassedServerGroup.getElementsByTagName("username")[0]) )
        thisServerGroup = self.handleServers( thisServerGroup, PassedServerGroup.getElementsByTagName("server") )

        return thisServerGroup

    def handleGroupName(self, PassedGroupName):
        return self.getText(PassedGroupName.childNodes)

    def handleUsername(self, PassedUsername):
        return self.getText(PassedUsername.childNodes)

    def handleServers(self, PassedServerGroup, PassedServers):
        thisServerGroup = PassedServerGroup

        for Server in PassedServers:
            thisServerGroup.addServer( self.handleServer(Server) )

        return thisServerGroup

    def handleServer(self, PassedServer):
        thisServer = engine.data.Server.Server()
        thisServer.setName( self.getText(PassedServer.childNodes) )

        return thisServer

######################################################################
