######################################################################
#
# $Id$
#
# Name: BatchRunner.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import stat
import string
import sys

# Custom modules
import engine.CommandRunner
import engine.data.ExternalCommand
import engine.data.InternalCommand

class BatchRunner:

    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig

    def invoke(self):
        # Let's make sure the file we've been given is readable.
        try:
            if ( stat.S_ISREG(os.stat(
                self._globalConfig.getBatchFile())[stat.ST_MODE]) \
                 == False ):
                print("ERROR: File '" + self._globalConfig.getBatchFile() +
                      "' is accessible, but not regular.")
                return False
        except OSError, (errno, strerror):
            thisError = "ERROR: [Errno %s] %s: %s" % ( errno, strerror, \
                                                       self._globalConfig.getBatchFile() )
            print(thisError)
            self._globalConfig.getSysLogger().LogMsgError(thisError)
            return False

        # Let everyone know what we're doing.
        self._globalConfig.getSysLogger().LogMsgInfo(
            "INFO:  Attempting command run using file '" + \
            self._globalConfig.getBatchFile() + "'.")

        try:
            thisFile = open(self._globalConfig.getBatchFile(), 'r')
            
            for thisInput in thisFile:
                thisFoundIt = False

                thisInput = thisInput.strip()
                thisTokens = thisInput.split()

                #
                # Step 1 - Handle "exit" from this chunk of code.
                # Should probably be moved into the parser proper.
                #
                if (thisTokens[0] == 'exit'):
                    thisInfo = "INFO:  Received exit command.  Wrote history.  Dying..."
                    self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)
                    break

                #
                # Step 2 - Check for Unix "pass through" commands.
                #
                for thisCommand in self._globalConfig.getPassThruList():
                    if (thisTokens[0] == thisCommand):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                        thisExternalCommand.setCommand(thisInput)
                        # Wrap it just in case.
                        try:
                            thisExternalCommand.run()
                        except KeyboardInterrupt:
                            thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                            self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)
                        del thisExternalCommand
                        thisFoundIt = True
                        break

                # Icky flow-control hack.
                if (thisFoundIt):
                    continue

                #
                # Step 3 - Create InternalCommand object and fire up
                #          the parser.
                #
                thisInternalCommand = engine.data.InternalCommand.InternalCommand()
                thisInternalCommand.setCommand(thisInput)
                thisCommandRunner = engine.CommandRunner.CommandRunner(self._globalConfig)
                thisCommandRunner.run(thisInternalCommand)
                del thisInternalCommand
                del thisCommandRunner

            thisFile.close()

        except IOError, (errno, strerror):
            thisError = "ERROR: [Errno %s] %s: %s" % \
                        (errno, strerror, thisFilename)
            print(thisError)
            self._globalConfig.getSysLogger().LogMsgError(thisError)
            sys.exit(1)

        return True

######################################################################
