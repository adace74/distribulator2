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
import os
import os.path
import stat
import string
import sys

# Custom modules
import engine.command.Command
import engine.data.ExternalCommand
import generic.FilePrinter

######################################################################

class MiscCommand(engine.command.Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doChdir(self, PassedCommString):
        """This method is responsible for the processing of the 'cd' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # If the user just types 'cd', do what most shells would do.
        if (len(self._commTokens) == 1):
            myDirStr = os.environ.get('HOME')
        else:
            myDirStr = self._commTokens[1]

        try:
            if (self._commTokens[0] == 'cd'):
                os.chdir(myDirStr)

        except OSError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                      self._commTokens[1])
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        return True

######################################################################

    def doExit(self, PassedCommString):
        """This method is responsible for the processing of the 'exit' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        myInfo = "INFO:  Received exit command.  Wrote history.  Dying..."

        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return True

######################################################################

    def doHelp(self, PassedCommString):
        """This method is responsible for the processing of the 'help' command."""

        # Tokenize!
        self._commTokens = PassedCommString.split()

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        if ( len(self._commTokens) > 1 ):
            myFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        self._commTokens[1] + '-desc.txt')
        else:
            myFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        'help.txt')

        myFilePrinter = generic.FilePrinter.FilePrinter()

        if (myFilePrinter.printFile(myFileName) == False):
            myError = "ERROR: Cannot find help for specified command '" + \
                        self._commTokens[1] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        return True

######################################################################
