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
This class is responsible for doing the actual reading of a given
batch file, and pre-processing the input before calling the
CommandRunner for command expansion work.
"""

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
    """
    This class is responsible for doing the actual reading of a given
    batch file, and pre-processing the input before calling the
    CommandRunner for command expansion work.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def outputError(self, PassedError):
        """
        This method is responsible for logging error messages
        in a manner consistent with a quite mode, if applicable.
        """

        if ( self._globalConfig.isQuietMode() ):
            self._globalConfig.getSysLogger().LogMsgError(
                PassedError)
        else:
            print(PassedError)
            self._globalConfig.getSysLogger().LogMsgError(
                PassedError)

######################################################################

    def outputInfo(self, PassedInfo):
        """
        This method is responsible for logging info messages 
        in a manner consistent with a quite mode, if applicable.
        """

        if ( self._globalConfig.isQuietMode() ):
            self._globalConfig.getSysLogger().LogMsgInfo(
                PassedInfo)
        else:
            print(PassedInfo)
            self._globalConfig.getSysLogger().LogMsgInfo(
                PassedInfo)

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""

        # Let's make sure the file we've been given is readable.
        try:
            if ( stat.S_ISREG(os.stat(
                self._globalConfig.getBatchFile())[stat.ST_MODE]) \
                 == False ):
                thisError = "ERROR: File '" + \
                            self._globalConfig.getBatchFile() + \
                            "' is accessible, but not regular."
                self.outputError(thisError)

                self._globalConfig.setExitSuccess(False)
                return

        except OSError, (errno, strerror):
            thisError = "ERROR: [Errno %s] %s: %s" % ( errno, strerror, \
                                                       self._globalConfig.getBatchFile() )
            self.outputError(thisError)

            self._globalConfig.setExitSuccess(False)
            return

        # Let everyone know what we're doing.        
        thisInfo = "INFO:  Batch File: " + \
            self._globalConfig.getBatchFile()
        self.outputInfo(thisInfo)

        thisCommandCount = 0
        thisError = ''
        thisIsMore = False
        thisLineBuffer = ''
        thisLineCount = 0
        thisTimeDuration = 0
        thisTimeStarted = time.time()
        thisTimeFinished = 0
        thisVerboseMode = False

        try:
            # First Pass: Validation
            thisFile = open(self._globalConfig.getBatchFile(), 'r')

            for thisLine in thisFile:
                thisLineCount = thisLineCount + 1

                if (thisLine.find('$var1') != -1):
                    if (len(self._globalConfig.getVar1()) == 0):
                        thisError = "ERROR: Variable $var1 referenced on line %d, but not defined." % thisLineCount
                elif (thisLine.find('$var2') != -1):
                    if (len(self._globalConfig.getVar2()) == 0):
                        thisError = "ERROR: Variable $var2 referenced on line %d, but not defined." % thisLineCount
                elif (thisLine.find('$var3') != -1):
                    if (len(self._globalConfig.getVar3()) == 0):
                        thisError = "ERROR: Variable $var3 referenced on line %d, but not defined." % thisLineCount

                if (len(thisError) != 0):
                    self.outputError(thisError)

                    self._globalConfig.setExitSuccess(False)
                    return

            thisFile.close()

            # Second Pass: Execution
            thisFile = open(self._globalConfig.getBatchFile(), 'r')

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
                if ( thisLine.find('$env') != -1 ):
                    thisLine = string.replace( thisLine, '$env', \
                                               self._globalConfig.getServerEnv() )
                if ( thisLine.find('$var1') != -1 ):
                    thisLine = string.replace( thisLine, '$var1',
                                               self._globalConfig.getVar1() )
                if ( thisLine.find('$var2') != -1 ):
                    thisLine = string.replace( thisLine, '$var2',
                                               self._globalConfig.getVar2() )
                if ( thisLine.find('$var3') != -1 ):
                    thisLine = string.replace( thisLine, '$var3',
                                               self._globalConfig.getVar3() )

                #
                # Step 1: Check to see if this is an empty line.
                #         If so, skip it.
                #
                if (len(thisLine) == 0):
                    continue

                #
                # Step 2: Check to see if this is a comment line.
                #         If so, skip it.
                #
                thisTokens = thisLine.split()

                if (thisTokens[0].find('#') == 0):
                    thisIsMore = False
                    continue

                #
                # Step 3: If the line contains a backslash indicating
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
                # Step 4: Handle "exit" from this chunk of code.
                #
                if (thisTokens[0] == 'exit'):
                    thisInfo = "INFO:  Received exit command.  Wrote history.  Dying..."
                    self.outputInfo(thisInfo)

                    return

                #
                # Step 5: Check for Unix "pass through" commands.
                #
                for thisCommand in self._globalConfig.getPassThruList():
                    if (thisTokens[0] == thisCommand):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                        thisExternalCommand.setCommand(thisLine)
                        # Wrap it just in case.
                        try:
                            thisExternalCommand.runBatch()

                        except KeyboardInterrupt:
                            thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                            self.handleInfo(thisInfo)

                        thisCommandCount = thisCommandCount + 1
                        del thisExternalCommand
                        thisFoundIt = True
                        break

                # Icky flow-control hack.
                if (thisFoundIt):
                    continue

                #
                # Step 6: Create InternalCommand object and fire up
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
            self.outputError(thisError)

            self._globalConfig.setExitSuccess(False)
            return

        #
        # Output our "footer" for batch mode.
        #
        # Define a pretty seperator.
        thisSeperator = '----------------------------------------------------------------------'
        self.outputInfo(thisSeperator)

        thisInfo = "INFO:  Commands Run:      %d commands" % \
              thisCommandCount
        self.outputInfo(thisInfo)

        thisTimeFinished = time.time()
        thisTimeDuration = thisTimeFinished - thisTimeStarted

        thisInfo = "INFO:  Run Time:          %.2f seconds" % \
              thisTimeDuration
        self.outputInfo(thisInfo)

        if ( (int(thisTimeDuration) > 0) & (int(thisCommandCount) > 0) ):
            thisInfo = "INFO:  Avg. Command Time: %.2f seconds" % \
                  (thisTimeDuration / thisCommandCount)
        else:
            thisInfo = "INFO:  Avg. Command Time: 0 seconds"

        self.outputInfo(thisInfo)

        return

######################################################################
