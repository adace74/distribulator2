######################################################################
#
# $Id$
#
# Name: ExternalCommand.py
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

    #
    # Constructor.
    #
    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig
        self._seperator = '----------------------------------------------------------------------'

    #
    # Unix command line string.
    #
    def getCommand(self):
        return self._command
    
    def setCommand(self, PassedCommand):
        self._command = PassedCommand
    #
    # Function methods.
    #
    # run() -- Only to be used in console mode.
    # runAtomic() -- Only to be used for non-interactive sessions.
    #
    def run(self):
        if ( self._globalConfig.isBatchMode() ):
            self._globalConfig.getSysLogger().LogMsgError(
                "ERROR:ExternalCommand.run() called in batch mode." )
            return False

        print("EXEC:  " + self._command)

        thisStatus = os.system(self._command)
        print(self._seperator)

        if (thisStatus != 0):
            print("ERROR: Local shell returned error state.")

        # Sleep 1/4 second to allow for CTRL-C's
        time.sleep(0.25)

        return thisStatus

    def runAtomic(self):
        if ( self._globalConfig.isBatchMode() ):
            self._globalConfig.getSysLogger().LogMsgInfo(
                "EXEC:  " + self._command )
        else:
            print("EXEC:  " + self._command)
            self._globalConfig.getSysLogger().LogMsgInfo(
                "EXEC:  " + self._command )

        thisStatus, thisOutput = commands.getstatusoutput(self._command)

        for thisLine in thisOutput:
            if ( self._globalConfig.isBatchMode() ):
                self._globalConfig.getSysLogger().LogMsgInfo(
                    "EXECO: " + thisLine )
            else:
                print(thisLine)
                self._globalConfig.getSysLogger().LogMsgInfo(
                    "EXECO: " + thisLine )

        if (thisStatus != 0):
            thisError = "ERROR: Local shell returned error state."

            if ( self._globalConfig.isBatchMode() ):
                self._globalConfig.getSysLogger().LogMsgError(thisError)
            else:
                print(thisError)
                self._globalConfig.getSysLogger().LogMsgError(thisError)

        # Sleep 1/4 second to allow for CTRL-C's
        time.sleep(0.25)

        return thisStatus

######################################################################
