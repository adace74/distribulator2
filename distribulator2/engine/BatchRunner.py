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
import time

# Custom modules
import engine.CommandRunner
import engine.data.ExternalCommand
import engine.data.InternalCommand

class BatchRunner:

    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig

######################################################################

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

        thisCommandCount = 0
        thisIsMore = False
        thisLineBuffer = ''
        thisTimeDuration = 0
        thisTimeStarted = time.time()
        thisTimeFinished = 0

        try:
            thisFile = open(self._globalConfig.getBatchFile(), 'r')

            # The Big Loop
            for thisLine in thisFile:
                thisFoundIt = False

                #
                # Pre-processing.
                # * Strip any linefeeds / CR's.
                # * Turn tabs into spaces.
                # * Do variable substitution.
                # * Tokenzie.
                #
                thisLine = thisLine.strip()
                thisLine = string.replace(thisLine, '\t', ' ')

                # Variable substitution
                thisLine = string.replace( thisLine, '$env', \
                                           self._globalConfig.getServerEnv() )

                if ( self._globalConfig.getVar1() ):
                    thisLine = string.replace( thisLine, '$var1',
                                               self._globalConfig.getVar1() )
                if ( self._globalConfig.getVar2() ):
                    thisLine = string.replace( thisLine, '$var2',
                                               self._globalConfig.getVar2() )
                if ( self._globalConfig.getVar3() ):
                    thisLine = string.replace( thisLine, '$var3',
                                               self._globalConfig.getVar3() )

                thisTokens = thisLine.split()

                #
                # Step 1: Check to see if this is a comment line.
                #         If so, skip it.
                #
                if (thisTokens[0].find('#') == 0):
                    thisIsMore = False
                    continue

                #
                # Step 2: If the line contains a backslash indicating
                #         logical line continuation, honor it.
                #
                # The last line ended with a \
                if (thisIsMore):
                    # And this line ends with another.
                    if ( thisLine.find('\\') == (len(thisLine) - 1) ):
                        # Strip the \ before concatenating.
                        thisLineBuffer = thisLineBuffer + \
                                         string.replace(thisLine, '\\', '')
                        continue
                    # If not, concatenate and continue.
                    else:
                        # Add the last of the line, and reset variables.
                        thisLine = thisLineBuffer + thisLine
                        thisIsMore = False
                        thisLineBuffer = ''
                else:
                    # This line ends with a \.
                    if ( thisLine.find('\\') == (len(thisLine) - 1) ):
                        # Strip the \ before concatenating.
                        thisLineBuffer = thisLineBuffer + \
                                         string.replace(thisLine, '\\', '')
                        # Set our state flag.
                        thisIsMore = True
                        continue

                #
                # Step 3: Handle "exit" from this chunk of code.
                #
                if (thisTokens[0] == 'exit'):
                    thisInfo = "INFO:  Received exit command.  Wrote history.  Dying..."
                    self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)
                    break

                #
                # Step 4: Check for Unix "pass through" commands.
                #
                for thisCommand in self._globalConfig.getPassThruList():
                    if (thisTokens[0] == thisCommand):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                        thisExternalCommand.setCommand(thisLine)
                        # Wrap it just in case.
                        try:
                            thisExternalCommand.run()

                        except KeyboardInterrupt:
                            thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                            self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)
                        thisCommandCount = thisCommandCount + 1
                        del thisExternalCommand
                        thisFoundIt = True
                        break

                # Icky flow-control hack.
                if (thisFoundIt):
                    continue

                #
                # Step 5: Create InternalCommand object and fire up
                #         the parser.
                #
                thisInternalCommand = engine.data.InternalCommand.InternalCommand()
                thisInternalCommand.setCommand(thisLine)
                thisCommandRunner = engine.CommandRunner.CommandRunner(self._globalConfig)
                thisCommandCount = thisCommandCount + \
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

        thisInfo = "INFO:  Commands Run:      %d commands" % \
              thisCommandCount
        self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)

        thisTimeFinished = time.time()
        thisTimeDuration = thisTimeFinished - thisTimeStarted

        thisInfo = "INFO:  Run Time:          %.2f seconds" % \
              thisTimeDuration
        self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)

        if (int(thisTimeDuration) > 0):
            thisInfo = "INFO:  Avg. Command Time: %.2f seconds" % \
                  (thisTimeDuration / thisCommandCount)
        else:
            thisInfo = "INFO:  Avg. Command Time: 0 seconds"
        self._globalConfig.getSysLogger().LogMsgInfo(thisInfo)

        return True

######################################################################
