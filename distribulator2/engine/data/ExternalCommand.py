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
# Go go go!!!
######################################################################

    def run(self, PassedIsInteractive=False):
        """This method is responsible for running a given command in various ways."""

        myStatus = 0

        # A little validation never hurt anyone...
        if ( self._globalConfig.isBatchMode() & PassedIsInteractive ):
            self._globalConfig.getMultiLogger().LogMsgError(
                "ExternalCommand.run(True) called in batch mode." )
            return False

        self._globalConfig.getMultiLogger().LogMsgDebug(
            "EXEC: " + self._command )

        #
        # Here we branch pased on the PassedIsInteractive flag.
        # If true, this indicates we're running a non-interactive command.
        # If false, this indicates we're running a local pass-through or remote interactive command.
        #
        if (PassedIsInteractive):
            myStatus = os.system(self._command)
        else:
            myStatus, myOutput = commands.getstatusoutput(self._command)

            for myLine in myOutput.split('\n'):
                self._globalConfig.getMultiLogger().LogMsgInfo(
                    "OUT:  " + myLine )

            if (myStatus != 0):
                self._globalConfig.setExitSuccess(False)

        self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

        if (myStatus != 0):
            self._globalConfig.getMultiLogger().LogMsgError("Local shell returned error state.")

        # If we have a global deley set, wait for that long.
        # Otherwise, sleep just a -little- bit to allow for catching CTRL-C's
        time.sleep( self._globalConfig.getDelaySecs() )

        return myStatus

######################################################################
