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

######################################################################

class PasswordCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doSetPassword(self, PassedPassword):
        """This method is responsible for the processing of the 'set password' command."""

        # Tokenize!
        self._commTokens = PassedPassword.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a password, set it.
        if ( len(self._commTokens) > 2 ):
            self._globalConfig.setRemotePassword( self._commTokens[2] )
            myInfo = "Remote password has been set."
            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
            return True
        else:
            myError = "No remote password given."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

######################################################################

    def doShowPassword(self, PassedPassword):
        """This method is responsible for the processing of the 'show server-group' command."""

        myError = "This operation is a little too scary to bother implementing."
        self._globalConfig.getMultiLogger().LogMsgError(myError)
        return False

######################################################################
