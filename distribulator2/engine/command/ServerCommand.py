######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
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

# Standard modules

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

    def doServerGroup(self, PassedCommString):
        """This method is responsible for the processing of the 'server-group' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a group name, set it.
        if ( len(self._commTokens) > 1 ):
            myServerGroup = self._globalConfig.getServerGroupByName( self._commTokens[1] )

            if (myServerGroup == False):
                myError = "ERROR: No matching server group '" + \
                            self._commTokens[1] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
            else:
                self._globalConfig.setCurrentServerGroup(myServerGroup)
                print("INFO:  Current server group is now '" + self._commTokens[1] + "'.")
                return True
        else:
            # Otherwise, display the server group list given at startup.
            myServerGroupStr = "Known server groups for environment '" + \
                                 self._globalConfig.getServerEnv() + "'\n"
            myServerGroupStr = myServerGroupStr + \
                                 "--------------------------------------------------\n"
            myTotalServerCount = 0
            myColumnCount = 0

            for myServerGroup in self._globalConfig.getServerGroupList():
                myColumnCount = myColumnCount + 1
                myTotalServerCount = myTotalServerCount + \
                                       myServerGroup.getServerCount()
                myServerGroupStr = myServerGroupStr + '%10s (%2d) ' % \
                                     (myServerGroup.getName(), myServerGroup.getServerCount())

                if (myColumnCount == 4):
                    myColumnCount = 0
                    myServerGroupStr = myServerGroupStr + '\n'

            print(myServerGroupStr)

            return True

######################################################################

    def doServerList(self, PassedCommString):
        """This method is responsible for the processing of the 'server-list' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a server group name, display servers in that group.
        if ( len(self._commTokens) > 1 ):
            myServerGroup = self._globalConfig.getServerGroupByName( \
                self._commTokens[1] )
        else:
            # Otherwise, display servers in the current working server group.
            myServerGroup = self._globalConfig.getCurrentServerGroup()

        # Check for errors.
        if (myServerGroup == False):
            myError = "ERROR: No matching server group '" + \
                        self._commTokens[1] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)

            return False
        else:
            print("Known servers for group '" + myServerGroup.getName() + "'")
            print("--------------------------------------------------")
            # Actual server list goes here.
            myTempStr = ''

            for myServer in myServerGroup.getServerList():
                if ( len(myTempStr) > 0 ):
                    print (myTempStr + "\t" + myServer.getName())
                    myTempStr = ''
                else:
                    myTempStr = myServer.getName()

            if ( len(myTempStr) > 0 ):
                print(myTempStr)

            return True

######################################################################
