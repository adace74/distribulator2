######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding an external command."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import commands
import os
import os.path
import time

######################################################################

class ExternalCommand:
    """This class holds data regarding an external command."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################
# Unix command line string.
######################################################################

    def getCommand(self):
        """This is a typical accessor method."""

        return self._command

######################################################################

    def setCommand(self, PassedCommand):
        """This is a typical accessor method."""

        self._command = PassedCommand

######################################################################
# Only to be used in console mode.
######################################################################

    def runConsole(self, isLoggable=False):
        """This method is responsible for running a given command in console mode."""

        if ( self._globalConfig.isBatchMode() ):
            self._globalConfig.getLogger().error(
                "ExternalCommand.run() called in batch mode." )
            return False

        # This could be a pass-through command, no need to log that.
        if (isLoggable):
            self._globalConfig.getMultiLogger().LogMsgDebug(
                "EXEC: " + self._command )

        myStatus = os.system(self._command)
        self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

        if (myStatus != 0):
            self._globalConfig.getMultiLogger().LogMsgWarn("Local shell returned error state.")

        # If we have a global deley set, wait for that long.
        # Otherwise, sleep just a -little- bit to allow for catching CTRL-C's
        time.sleep( self._globalConfig.getDelaySecs() )

        return myStatus

######################################################################
# Only to be used for batch mode.
######################################################################

    def runBatch(self):
        """This method is responsible for running a given command in batch mode."""

        self._globalConfig.getMultiLogger().LogMsgDebug(
            "EXEC: " + self._command )

        myStatus, myOutput = commands.getstatusoutput(self._command)

        for myLine in myOutput.split('\n'):
            self._globalConfig.getMultiLogger().LogMsgDebug(
                "OUT:  " + myLine )

        if (myStatus != 0):
            myWarn = "Local shell returned error state."
            self._globalConfig.getMultiLogger().LogMsgWarn(myWarn)

            self._globalConfig.setExitSuccess(False)

        self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

        # If we have a global deley set, wait for that long.
        # Otherwise, sleep just a -little- bit to allow for catching CTRL-C's
        time.sleep( self._globalConfig.getDelaySecs() )

        return myStatus

######################################################################
