######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for handling the console mode of the application."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import atexit
import getpass
import os
import os.path
import readline
import rlcompleter
import string
import sys

# Custom modules
import Mode
import engine.command.Dispatcher
import engine.data.ExternalCommand
import engine.data.InternalCommand

######################################################################

class ConsoleMode(Mode.Mode):
    """This class is responsible for handling the console mode of the application."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig
        self._commList = [ 'copy', 'exit', 'help', 'login', 'run',
                           'set', 'show' ]

######################################################################

    def getAttemptedCompletion(self, myString, myIndex):
        """This method is registered with GNU readline and called for tab-completion."""

        # Don't ask me exactly how, but my seems to work well.
        if ( (myIndex == 0) & (readline.get_begidx() == 0) ):
            if (len(myString) > 0):
                for myCommStr in self._commList:
                    if (string.find(myCommStr, myString) != -1):
                        return myCommStr + ' '
            else:
                return 'help '

        return None

######################################################################

    def initHistory(self):
        """This method loads history data for use with GNU readline."""

        myCounter = 0
        myHistory = os.path.join(os.environ['HOME'], ".dist_history")
    
        try:
            myFile = open(myHistory, 'r')
            for myLine in myFile:
                myCounter = myCounter + 1
            myFile.close()

            # Load readline history.
            readline.set_history_length(256)
            readline.read_history_file(myHistory)
        
        except IOError:
            pass

        # Save readline history on exit.
        atexit.register(readline.write_history_file, myHistory)

        # Enable TAB filename-completion, instead of Python's default
        # object completion.
        #readline.set_completer()
        readline.set_completer(self.getAttemptedCompletion)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.getAttemptedCompletion)

        return myCounter

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""

        myPromptEnv = self._globalConfig.getServerEnv()
        myPromptUser = self._globalConfig.getUsername()

        while (1):
            #
            # Step 1: Reset critical variables every time around the loop.
            #
            myFoundIt = False
            myInput = ''
            myPromptGroup = self._globalConfig.getCurrentServerGroup().getName()
            myPrompt = '<' + myPromptUser + '@' + myPromptEnv + \
            '[' + myPromptGroup + ']:' + os.getcwd() + '> '

            try:
                myInput = raw_input(myPrompt)

            except EOFError:
                myInfo = "INFO:  Caught CTRL-D keystroke.  Wrote history.  Dying..."
                print
                print(myInfo)
                self._globalConfig.getSysLogger().LogMsgInfo(myInfo)

                return

            except KeyboardInterrupt:
                print

            if ( len(myInput.strip()) > 0 ):
                myTokens = myInput.split()

                #
                # Step 2: Check for Unix "pass through" commands.
                #
                for myCommand in self._globalConfig.getPassThruList():
                    if (myTokens[0] == myCommand):
                        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                        myExternalCommand.setCommand(myInput)
                        # Wrap it just in case.
                        try:
                            myExternalCommand.runConsole()
                        except KeyboardInterrupt:
                            myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                            print(myInfo)
                            self._globalConfig.getSysLogger().LogMsgInfo(myInfo)
                        del myExternalCommand
                        myFoundIt = True
                        break

                # Icky flow-control hack.
                if (myFoundIt):
                    continue
                #
                # Step 3: Create InternalCommand object and
                #         fire up the parser.
                #
                try:
                    myInternalCommand = engine.data.InternalCommand.InternalCommand()
                    myInternalCommand.setCommand(myInput)
                    myDispatcher = engine.command.Dispatcher.Dispatcher(self._globalConfig)
                    myDispatcher.invoke(myInternalCommand)

                    del myInternalCommand
                    del myDispatcher

                except KeyboardInterrupt:
                    myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

                # Icky flow-control hack.
                if (myTokens[0] == 'exit'):
                    return

######################################################################
