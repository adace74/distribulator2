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

class EnvCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doSetEnvironment(self, PassedCommString):
        """This method is responsible for the processing of the 'set environment' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given an environment name, set it.
        if ( len(self._commTokens) > 2 ):
            myEnvironment = self._globalConfig.getEnvironmentByName( self._commTokens[2] )

            if (not myEnvironment):
                myError = "No matching environment '" + \
                            self._commTokens[2] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
            else:
                self._globalConfig.setCurrentEnv(myEnvironment)
                self._globalConfig.setCurrentEnvName( self._commTokens[2] )
                myInfo = "Current environment is now '" + self._commTokens[2] + "'."
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                return True
        else:
            myError = "No environment name given."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

            return True

######################################################################

    def doShowEnvironment(self, PassedCommString):
        """This method is responsible for the processing of the 'show environment' command."""

        myColumnCount = 0
        myTempStr = ''

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a environment name, display server groups in that group.
        if ( len(self._commTokens) > 2 ):
            myEnvironment = self._globalConfig.getEnvironmentByName( self._commTokens[2] )
        else:
            myEnvironment = self._globalConfig.getCurrentEnv()

        # Check for errors.
        if (not myEnvironment):
            myError = "No matching environment '" + self._commTokens[2] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)

            return False
        else:
            # Otherwise, display the server group list given at startup.
            myTempStr = "Known server groups for environment '" + myEnvironment.getName() + "'\n"
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
