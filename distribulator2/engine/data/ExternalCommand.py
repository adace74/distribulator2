######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
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
import string
import sys
import time

######################################################################

class ExternalCommand:
    """This class holds data regarding an external command."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig
        self._seperator = '----------------------------------------------------------------------'

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
            self._globalConfig.getSysLogger().LogMsgError(
                "ERROR:ExternalCommand.run() called in batch mode." )
            return False

        # This could be a pass-through command, no need to log that.
        if (isLoggable):
            self._globalConfig.getSysLogger().LogMsgInfo(
                "EXEC:  " + self._command )

        print("EXEC:  " + self._command)

        thisStatus = os.system(self._command)
        print(self._seperator)

        if (thisStatus != 0):
            print("ERROR: Local shell returned error state.")

        # Sleep just a -little- bit to allow for catching CTRL-C's
        time.sleep(0.05)

        return thisStatus

######################################################################
# Only to be used for batch mode.
######################################################################

    def runBatch(self):
        """This method is responsible for running a given command in batch mode."""

        self._globalConfig.getSysLogger().LogMsgInfo(
            "EXEC:  " + self._command )
        if (self._globalConfig.isQuietMode() == False):
            print("EXEC:  " + self._command)

        thisStatus, thisOutput = commands.getstatusoutput(self._command)

        for thisLine in thisOutput.split('\n'):
            self._globalConfig.getSysLogger().LogMsgInfo(
                "OUTPUT:" + thisLine )
            if (self._globalConfig.isQuietMode() == False):
                print(thisLine)

        if (thisStatus != 0):
            thisError = "ERROR: Local shell returned error state."

            self._globalConfig.getSysLogger().LogMsgError(thisError)
            if ( self._globalConfig.isQuietMode() == False):
                print(thisError)

            self._globalConfig.setExitSuccess(False)

        if (self._globalConfig.isQuietMode() == False):
            print(self._seperator)

        # Sleep just a -little- bit to allow for catching CTRL-C's
        time.sleep(0.05)

        return thisStatus

######################################################################
