######################################################################
#
# $Id$
#
# Name: ExternalCommand.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

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

    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig
        self._seperator = '----------------------------------------------------------------------'

######################################################################
# Unix command line string.
######################################################################

    def getCommand(self):
        return self._command

######################################################################

    def setCommand(self, PassedCommand):
        self._command = PassedCommand

######################################################################
# Only to be used in console mode.
######################################################################

    def run(self, isLoggable=False):
        if ( self._globalConfig.isBatchMode() ):
            self._globalConfig.getSysLogger().LogMsgError(
                "ERROR:ExternalCommand.run() called in batch mode." )
            return False

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

    def runAtomic(self):
        if ( self._globalConfig.isQuietMode() ):
            self._globalConfig.getSysLogger().LogMsgInfo(
                "EXEC:  " + self._command )
        else:
            print("EXEC:  " + self._command)
            self._globalConfig.getSysLogger().LogMsgInfo(
                "EXEC:  " + self._command )

        thisStatus, thisOutput = commands.getstatusoutput(self._command)

        for thisLine in thisOutput.split('\n'):
            if ( self._globalConfig.isQuietMode() ):
                self._globalConfig.getSysLogger().LogMsgInfo(
                    "OUTPUT:" + thisLine )
            else:
                print(thisLine)
                self._globalConfig.getSysLogger().LogMsgInfo(
                    "OUTPUT:" + thisLine )

        if (thisStatus != 0):
            thisError = "ERROR: Local shell returned error state."

            if ( self._globalConfig.isQuietMode() ):
                self._globalConfig.getSysLogger().LogMsgError(thisError)
            else:
                print(thisError)
                self._globalConfig.getSysLogger().LogMsgError(thisError)

        if (self._globalConfig.isQuietMode() == False):
            print(self._seperator)

        # Sleep just a -little- bit to allow for catching CTRL-C's
        time.sleep(0.05)

        return thisStatus

######################################################################
