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

class DelayCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doSetDelaySecs(self, PassedCommString):
        """This method is responsible for the processing of the 'set delay' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # If given a new delay time, set it.
        if ( len(self._commTokens) > 2 ):
            try:
                self._globalConfig.setDelaySecs( int(self._commTokens[2]) )

            except ValueError:
                myError = "Invalid delay of '" + self._commTokens[2] + "' entered.  Please use an integer number."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False

            myInfo = "Current delay between remote commands is %d seconds." % self._globalConfig.getDelaySecs()
            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
            return True
        else:
            myError = "No delay time specified."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

######################################################################

    def doShowDelaySecs(self, PassedCommString):
        """This method is responsible for the processing of the 'show delay' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Display the current delay setting.
        myInfo = "Current delay between remote commands is %d seconds." % self._globalConfig.getDelaySecs()
        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
        return True

######################################################################
