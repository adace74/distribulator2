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
This class is responsible for dispatching the job of
a given command to the appropriate subclass.
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
import engine.command.CopyCommand
import engine.command.LoginCommand
import engine.command.MiscCommand
import engine.command.RunCommand
import engine.command.ServerCommand
import engine.data.ExternalCommand

######################################################################

class Dispatcher:
    """
    This class is responsible for dispatching the job of
    a given command to the appropriate subclass.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def invoke(self, PassedInternalCommand):
        """This method is the main entry point into the expansion engine."""

        # Make sure there's really a command to process.
        if (len(PassedInternalCommand.getCommand()) == 0):
            return False
        else:
            self._commString = PassedInternalCommand.getCommand()
            self._commTokens = self._commString.split()

        myCommand = 0
        myCommandCount = 0

        if (self._commTokens[0] != 'cd'):
            # Log it.
            self._globalConfig.getSysLogger().LogMsgInfo("CMD:   " + \
                                                         self._commString)
            # If we're not being quiet, print it.
            if ( self._globalConfig.isQuietMode() == False ):
                print("CMD:   " + self._commString)

        # Cheezy branching logic.  Works well, though.
        if (self._commTokens[0] == 'cd'):
            myCommand = engine.command.MiscCommand.MiscCommand(self._globalConfig)
            myCommandCount = myCommand.doChdir(self._commString)
        elif (self._commTokens[0] == 'copy'):
            myCommand = engine.command.CopyCommand.CopyCommand(self._globalConfig)
            myCommandCount = myCommand.doCopy(self._commString)
        elif (self._commTokens[0] == 'exit'):
            myCommand = engine.command.MiscCommand.MiscCommand(self._globalConfig)
            myCommandCount = myCommand.doExit(self._commString)
        elif (self._commTokens[0] == 'help'):
            myCommand = engine.command.MiscCommand.MiscCommand(self._globalConfig)
            myCommandCount = myCommand.doHelp(self._commString)
        elif (self._commTokens[0] == 'login'):
            myCommand = engine.command.LoginCommand.LoginCommand(self._globalConfig)
            myCommandCount = myCommand.doLogin(self._commString)
        elif (self._commTokens[0] == 'run'):
            myCommand = engine.command.RunCommand.RunCommand(self._globalConfig)
            myCommandCount = myCommand.doRun(self._commString)
        elif (self._commTokens[0] == 'server-group'):
            myCommand = engine.command.ServerCommand.ServerCommand(self._globalConfig)
            myCommandCount = myCommand.doServerGroup(self._commString)
        elif (self._commTokens[0] == 'server-list'):
            myCommand = engine.command.ServerCommand.ServerCommand(self._globalConfig)
            myCommandCount = myCommand.doServerList(self._commString)
        else:
            myError = "ERROR: Unknown Command: '" + \
                            self._commTokens[0] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        del myCommand

        return myCommandCount

######################################################################
