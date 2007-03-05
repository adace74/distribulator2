######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved.
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""
This class is responsible for doing the actual work of
expanding a given distribulator command into a set of
SSH commands and running them.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Custom modules
import Command
import engine.data.ExternalCommand

######################################################################

class ServerCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doSetServerGroup(self, PassedCommString):
        """This method is responsible for the processing of the 'set server-group' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # Check for attributes.
        if (self._commTokens[2].find('[') != -1):
            myError = "Attributes are currently unsupported for the 'set server-group' command.  Doheth!"
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a group name, set it.
        if ( len(self._commTokens) > 2 ):
            myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName( self._commTokens[2] )

            if (not myServerGroup):
                myError = "No matching server group '" + \
                            self._commTokens[2] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
            else:
                self._globalConfig.setCurrentServerGroup(myServerGroup)
                myInfo = "Current server group is now '" + self._commTokens[2] + "'."
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                return True
        else:
            myError = "No server group name given."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

            return True

######################################################################

    def doShowServerGroup(self, PassedCommString):
        """This method is responsible for the processing of the 'show server-group' command."""

        myColumnCount = 0
        myTempStr = ''

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a server group name, display servers in that group.
        if ( len(self._commTokens) > 2 ):
            # Check for server group match, with and without attributes.
            myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName(self._commTokens[2])

            # Check for errors.
            if (not myServerGroup):
                myError = "No matching server group '" + self._commTokens[2] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)

                return False

            myTempStr = "Known servers for group '" + myServerGroup.getName() + "'\n"
            myTempStr = myTempStr = "--------------------------------------------------\n"

            if (self._commTokens[2].find('[') == -1):
                myServerList = myServerGroup.getServerList()
            else:
                myServerList = myServerGroup.getAttribValueServerList(self._commTokens[2])

            for myServer in myServerList:
                myColumnCount = myColumnCount + 1

                if (myColumnCount == 2):
                    myColumnCount = 0
                    myTempStr = myTempStr + myServer.getName() + '\n'
                else:
                    myTempStr = myTempStr + myServer.getName() + '\t\t'
        else:
            # Otherwise, display the server group list given at startup.
            myTempStr = "Known server groups for environment '" + \
                        self._globalConfig.getCurrentEnvName() + "'\n"
            myTempStr = myTempStr + "--------------------------------------------------\n"

            for myServerGroup in self._globalConfig.getCurrentEnv().getServerGroupList():
                myColumnCount = myColumnCount + 1
                myTempStr = myTempStr + "%10s (%2d) " % \
                            (myServerGroup.getName(), myServerGroup.getServerCount())

                if (myColumnCount == 4):
                    myColumnCount = 0
                    myTempStr = myTempStr + '\n'

        if ( len(myTempStr) > 0 ):
            for myLine in myTempStr.split('\n'):
                if ( len(myLine) > 0 ):
                    self._globalConfig.getMultiLogger().LogMsgInfo(
                        "OUT:  " + myLine )

        return True

######################################################################
