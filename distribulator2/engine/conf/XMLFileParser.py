######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for loading in data from our XML configuration file."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import sys
import syslog
import xml.dom.minidom

# Custom modules
import engine.data.GlobalConfig
import engine.data.Server
import engine.data.ServerGroup

######################################################################

class XMLFileParser:
    """This class is responsible for loading in data from our XML configuration file.""" 

    def __init__(self):
        """Constructor."""

        pass

######################################################################

    def parse(self, PassedGlobalConfig):
        """This method represents the main entry point into the XML parsing logic."""

        self._globalConfig = PassedGlobalConfig
        self._isEnvFound = False
        self._serverGroupList = []

        myFilename = self._globalConfig.getConfigFile()

        try:
            myConfigLines = 0

            myFile = open(myFilename, 'r')
            for myLine in myFile:
                myConfigLines = myConfigLines + 1
            myFile.close()

            self._globalConfig.setConfigLines(myConfigLines)
            
            myDom = xml.dom.minidom.parse(myFilename)

        except IOError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % \
                        (errno, strerror, myFilename)
            # NOTE: Would be nice to syslog, but This just isn't
            # possible until the config is fully loaded.
            print(myError)

            sys.exit(True)

        self.handleConfig(myDom)

        if (self._isEnvFound):
            return self._globalConfig
        else:
            myError = "ERROR: No matching tags found for environment '" + \
                        self._globalConfig.getServerEnv() + "' in config.xml!"
            # NOTE: Would be nice to syslog, but This just isn't
            # possible until the config is fully loaded.
            print(myError)

            sys.exit(True)

######################################################################

    def getText(self, nodelist):
        """
        This method is responsible for walking the DOM tree and
        finding a given node's relevant text.
        """

        rc = ''
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                return rc

######################################################################

    def handleConfig(self, PassedConfig):
        """This method branches processing off into sub-methods."""

        self.handleBinaries(PassedConfig.getElementsByTagName('binary'))
        self.handleLogging(PassedConfig.getElementsByTagName('logging')[0])
        self.handlePing(PassedConfig.getElementsByTagName('ping')[0])
        self.handleEnvironments(PassedConfig.getElementsByTagName('environment'))

######################################################################
# Binary locations.
######################################################################

    def handleBinaries(self, PassedBinaries):
        """This method branches processing off into sub-methods."""

        for Binary in PassedBinaries:
            self.handleBinary(Binary)

######################################################################

    def handleBinary(self, PassedBinary):
        """This method handles a single <Binary> tag."""

        myName = PassedBinary.getAttribute('name')
        myValue = PassedBinary.getAttribute('value')
        if (myName == 'logname'):
            self._globalConfig.setLognameBinary(myValue)
        elif (myName == 'scp'):
            self._globalConfig.setScpBinary(myValue)
        elif (myName == 'ssh'):
            self._globalConfig.setSshBinary(myValue)

######################################################################
# Logging options.
######################################################################

    def handleLogging(self, PassedLogging):
        """This method handles a single <Logging> tag."""

        self._globalConfig.setSyslogFacility(
            eval("syslog.LOG_" + PassedLogging.getAttribute('facility').strip()) )

######################################################################
# Ping options.
######################################################################

    def handlePing(self, PassedPing):
        """This method handles a single <Ping> tag."""

        if (PassedPing.getAttribute('banner')):
            self._globalConfig.setPingBanner(PassedPing.getAttribute('banner'))
        else:
            self._globalConfig.setPingBanner('')

        if (PassedPing.getAttribute('port')):
            self._globalConfig.setPingPort( int(PassedPing.getAttribute('port').strip()) )
        else:
            self._globalConfig.setPingPort(22)

        if (PassedPing.getAttribute('timeout')):
            self._globalConfig.setPingTimeout( int(PassedPing.getAttribute('timeout').strip()) )
        else:
            self._globalConfig.setPingTimeout(10)

######################################################################
# Server environments, groups, and individual servers.
######################################################################

    def handleEnvironments(self, PassedEnvironments):
        """This method branches processing off into sub-methods."""

        for Environment in PassedEnvironments:
            self.handleEnvironment(Environment)

######################################################################

    def handleEnvironment(self, PassedEnvironment):
        """This method handles a specific <Environment> tag."""

        # Only load the environment specified on startup.
        if ( PassedEnvironment.getAttribute('name') ==
             self._globalConfig.getServerEnv() ):
            self._isEnvFound = True
            self.handleServerGroups(
                PassedEnvironment.getElementsByTagName('servergroup') )
            if (PassedEnvironment.getAttribute('default')):
                self._globalConfig.setCurrentServerGroup(
                    self._globalConfig.getServerGroupByName(PassedEnvironment.getAttribute('default')))

######################################################################

    def handleServerGroups(self, PassedServerGroups):
        """This method branches processing off into sub-methods."""

        for ServerGroup in PassedServerGroups:
            self._serverGroupList.append( self.handleServerGroup(ServerGroup) )

        self._globalConfig.setServerGroupList(self._serverGroupList)

######################################################################

    def handleServerGroup(self, PassedServerGroup):
        """This method handles a single <ServerGroup> tag."""

        myServerGroup = engine.data.ServerGroup.ServerGroup()
        myServerGroup.setName(
            PassedServerGroup.getAttribute('name').strip() )

        if ( len(PassedServerGroup.getAttribute('username').strip()) > 0 ):
            myServerGroup.setUsername(
                PassedServerGroup.getAttribute('username').strip() )
        else:
            myServerGroup.setUsername( self._globalConfig.getUsername() )

        myServerGroup = self.handleServers( myServerGroup,
                                              PassedServerGroup.getElementsByTagName('server') )

        return myServerGroup

######################################################################

    def handleServers(self, PassedServerGroup, PassedServers):
        """This method branches processing off into sub-methods."""

        myServerGroup = PassedServerGroup

        for myServer in PassedServers:
            myServerGroup.addServer( self.handleServer(myServer) )

        for myServer in myServerGroup.getServerList():
            myServer.setUsername( myServerGroup.getUsername() )

        return myServerGroup

######################################################################

    def handleServer(self, PassedServer):
        """This method handles a single <Server> tag."""

        myServer = engine.data.Server.Server()
        myServer.setName( self.getText(PassedServer.childNodes).strip() )

        return myServer

######################################################################
