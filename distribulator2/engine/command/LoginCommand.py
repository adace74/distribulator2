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
import generic.FilePrinter
import generic.HostPinger

######################################################################

class LoginCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doLogin(self, PassedCommString):
        """This method is responsible for the processing of the 'login' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # Check for server name.
        if ( len(self._commTokens) > 1):
            if ( self._globalConfig.getServerByName(self._commTokens[1]) ):
                myServer = self._globalConfig.getServerByName(self._commTokens[1])
            else:
                myError = "ERROR: No matching server '" + \
                            self._commTokens[1] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
        else:
            myError = "ERROR: No server name given."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # Run the expanded shell command.
        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
        myExternalCommand.setCommand( \
            self._globalConfig.getSshBinary() + " -l " + \
            myServer.getUsername() + " " + myServer.getName() )
        try:
            myExternalCommand.runConsole(True)
        except (EOFError, KeyboardInterrupt):
            myInfo = "INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt..."
            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return True

######################################################################
