######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""
This class is responsible for doing the actual reading of a given
batch file, and pre-processing the input before calling the
Dispatcher for command expansion work.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
#import os.path
import socket
import stat
import string
#import sys
import time

# Custom modules
import Mode
import engine.command.Dispatcher
import engine.data.ExternalCommand
import engine.data.InternalCommand

class BatchMode(Mode.Mode):
    """
    This class is responsible for doing the actual reading of a given
    batch file, and pre-processing the input before calling the
    Dispatcher for command expansion work.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""

        # Let's make sure the file we've been given is readable.
        try:
            if ( stat.S_ISREG(os.stat(
                self._globalConfig.getBatchFile())[stat.ST_MODE]) \
                 == False ):
                myError = "ERROR: File '" + \
                            self._globalConfig.getBatchFile() + \
                            "' is accessible, but not regular."
                self._globalConfig.getMultiLogger().LogMsgError(myError)

                self._globalConfig.setExitSuccess(False)
                return

        except OSError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % ( errno, strerror, \
                                                       self._globalConfig.getBatchFile() )
            self._globalConfig.getMultiLogger().LogMsgError(myError)

            self._globalConfig.setExitSuccess(False)
            return

        # Let everyone know what we're doing.        
        myInfo = "INFO:  Batch File: " + \
            self._globalConfig.getBatchFile()
        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        myCommandCount = 0
        myError = ''
        myIsMore = False
        myLineBuffer = ''
        myLineCount = 0
        myTimeDuration = 0
        myTimeStarted = time.time()
        myTimeFinished = 0
        myVerboseMode = False

        try:
            # First Pass: Validation
            myFile = open(self._globalConfig.getBatchFile(), 'r')

            for myLine in myFile:
                myLineCount = myLineCount + 1

                if (myLine.find('$var1') != -1):
                    if (len(self._globalConfig.getVar1()) == 0):
                        myError = "ERROR: Variable $var1 referenced on line %d, but not defined." % myLineCount
                elif (myLine.find('$var2') != -1):
                    if (len(self._globalConfig.getVar2()) == 0):
                        myError = "ERROR: Variable $var2 referenced on line %d, but not defined." % myLineCount
                elif (myLine.find('$var3') != -1):
                    if (len(self._globalConfig.getVar3()) == 0):
                        myError = "ERROR: Variable $var3 referenced on line %d, but not defined." % myLineCount

                if (len(myError) != 0):
                    self._globalConfig.getMultiLogger().LogMsgError(myError)

                    self._globalConfig.setExitSuccess(False)
                    return

            myFile.close()

            # Second Pass: Execution
            myFile = open(self._globalConfig.getBatchFile(), 'r')

            for myLine in myFile:
                myFoundIt = False
                #
                # Pre-processing.
                # * Strip any linefeeds / CR's.
                # * Turn tabs into spaces.
                # * Do variable substitution.
                # * Tokenzie.
                #
                myLine = myLine.strip()
                myLine = string.replace(myLine, '\t', ' ')

                # Variable substitution
                if ( myLine.find('$env') != -1 ):
                    myLine = string.replace( myLine, '$env', \
                                             self._globalConfig.getServerEnv() )
                if ( myLine.find('$hostname') != -1 ):
                    myLine = string.replace( myLine, '$hostname', \
                                             socket.gethostname() )
                if ( myLine.find('$var1') != -1 ):
                    myLine = string.replace( myLine, '$var1',
                                             self._globalConfig.getVar1() )
                if ( myLine.find('$var2') != -1 ):
                    myLine = string.replace( myLine, '$var2',
                                             self._globalConfig.getVar2() )
                if ( myLine.find('$var3') != -1 ):
                    myLine = string.replace( myLine, '$var3',
                                             self._globalConfig.getVar3() )

                #
                # Step 1: Check to see if my is an empty line.
                #         If so, skip it.
                #
                if (len(myLine) == 0):
                    continue

                #
                # Step 2: Check to see if my is a comment line.
                #         If so, skip it.
                #
                myTokens = myLine.split()

                if (myTokens[0].find('#') == 0):
                    myIsMore = False
                    continue

                #
                # Step 3: If the line contains a backslash indicating
                #         logical line continuation, honor it.
                #
                # The last line ended with a \
                if (myIsMore):
                    # And my line ends with another.
                    if ( myLine.find('\\') == (len(myLine) - 1) ):
                        # Strip the \ before concatenating.
                        myLineBuffer = myLineBuffer + \
                                         string.replace(myLine, '\\', '')
                        continue
                    # If not, concatenate and continue.
                    else:
                        # Add the last of the line, and reset variables.
                        myLine = myLineBuffer + myLine
                        myIsMore = False
                        myLineBuffer = ''
                else:
                    # This line ends with a \.
                    if ( myLine.find('\\') == (len(myLine) - 1) ):
                        # Strip the \ before concatenating.
                        myLineBuffer = myLineBuffer + \
                                         string.replace(myLine, '\\', '')
                        # Set our state flag.
                        myIsMore = True
                        continue

                #
                # Step 4: Handle "exit" from my chunk of code.
                #
                if (myTokens[0] == 'exit'):
                    myInfo = "INFO:  Received exit command.  Wrote history.  Dying..."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

                    return

                #
                # Step 5: Check for Unix "pass through" commands.
                #
                for myCommand in self._globalConfig.getPassThruList():
                    if (myTokens[0] == myCommand):
                        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                        myExternalCommand.setCommand(myLine)
                        # Wrap it just in case.
                        try:
                            myExternalCommand.runBatch()

                        except KeyboardInterrupt:
                            myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                            self.handleInfo(myInfo)

                        myCommandCount = myCommandCount + 1
                        del myExternalCommand
                        myFoundIt = True
                        break

                # Icky flow-control hack.
                if (myFoundIt):
                    continue

                #
                # Step 6: Create InternalCommand object and fire up
                #         the parser.
                #
                myInternalCommand = engine.data.InternalCommand.InternalCommand()
                myInternalCommand.setCommand(myLine)
                myDispatcher = engine.command.Dispatcher.Dispatcher(self._globalConfig)
                myCommandCount = myCommandCount + \
                                   myDispatcher.invoke(myInternalCommand)
                del myInternalCommand
                del myDispatcher

            myFile.close()

        except IOError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % \
                        (errno, strerror, myFilename)
            self._globalConfig.getMultiLogger().LogMsgError(myError)

            self._globalConfig.setExitSuccess(False)
            return

        #
        # Output our "footer" for batch mode.
        #
        # Define a pretty seperator.
        mySeperator = '----------------------------------------------------------------------'
        self._globalConfig.getMultiLogger().LogMsgInfo(mySeperator)

        myInfo = "INFO:  Commands Run:      %d commands" % \
              myCommandCount
        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        myTimeFinished = time.time()
        myTimeDuration = myTimeFinished - myTimeStarted

        myInfo = "INFO:  Run Time:          %.2f seconds" % \
              myTimeDuration
        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        if ( (int(myTimeDuration) > 0) & (int(myCommandCount) > 0) ):
            myInfo = "INFO:  Avg. Command Time: %.2f seconds" % \
                  (myTimeDuration / myCommandCount)
        else:
            myInfo = "INFO:  Avg. Command Time: 0 seconds"

        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return

######################################################################
