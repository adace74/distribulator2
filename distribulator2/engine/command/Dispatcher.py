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
This class is responsible for dispatching the job of
a given command to the appropriate subclass.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Custom modules
import CopyCommand
import DelayCommand
import EnvCommand
import LoginCommand
import MiscCommand
import PasswordCommand
import RunCommand
import ServerCommand
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
            self._globalConfig.getMultiLogger().LogMsgDebug("CMD:  " + self._commString)

        try:
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
            elif (self._commTokens[1] == 'delay'):
                if (self._commTokens[0] == 'set'):
                    myCommand = engine.command.DelayCommand.DelayCommand(self._globalConfig)
                    myCommandCount = myCommand.doSetDelaySecs(self._commString)
                elif (self._commTokens[0] == 'show'):
                    myCommand = engine.command.DelayCommand.DelayCommand(self._globalConfig)
                    myCommandCount = myCommand.doShowDelaySecs(self._commString)
            elif (self._commTokens[1] == 'environment'):
                if (self._commTokens[0] == 'set'):
                    myCommand = engine.command.EnvCommand.EnvCommand(self._globalConfig)
                    myCommandCount = myCommand.doSetEnvironment(self._commString)
                elif (self._commTokens[0] == 'show'):
                    myCommand = engine.command.EnvCommand.EnvCommand(self._globalConfig)
                    myCommandCount = myCommand.doShowEnvironment(self._commString)
            elif (self._commTokens[1] == 'password'):
                if (self._commTokens[0] == 'set'):
                    myCommand = engine.command.PasswordCommand.PasswordCommand(self._globalConfig)
                    myCommandCount = myCommand.doSetPassword(self._commString)
                elif (self._commTokens[0] == 'show'):
                    myCommand = engine.command.PasswordCommand.PasswordCommand(self._globalConfig)
                    myCommandCount = myCommand.doShowPassword(self._commString)
            elif (self._commTokens[1] == 'server-group'):
                if (self._commTokens[0] == 'set'):
                    myCommand = engine.command.ServerCommand.ServerCommand(self._globalConfig)
                    myCommandCount = myCommand.doSetServerGroup(self._commString)
                elif (self._commTokens[0] == 'show'):
                    myCommand = engine.command.ServerCommand.ServerCommand(self._globalConfig)
                    myCommandCount = myCommand.doShowServerGroup(self._commString)
            else:
                myError = "Unknown Command: '" + self._commString + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False

            del myCommand

        except IndexError:
            myError = "Unknown Command: '" + self._commString + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        return myCommandCount

######################################################################
