######################################################################
#
# $Id$
#
# Name: CommandLine.py
#
######################################################################

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
import engine.CommandRunner
import engine.data.ExternalCommand
import engine.data.InternalCommand

######################################################################

class CommandLine:

    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig
        self._commList = [ 'copy', 'exit', 'help', 'login', 'run',
                           'server-group', 'server-list' ]

    def getAttemptedCompletion(self, thisString, thisIndex):
        # Don't ask me exactly how, but this seems to work well.
        if ( (thisIndex == 0) & (readline.get_begidx() == 0) ):
            if (len(thisString) > 0):
                for thisCommStr in self._commList:
                    if (string.find(thisCommStr, thisString) != -1):
                        return thisCommStr + ' '
            else:
                return 'help '

        return None

    def initHistory(self):
        thisCounter = 0
        thisHistory = os.path.join(os.environ['HOME'], ".dist_history")
    
        try:
            thisFile = open(thisHistory, 'r')
            for thisLine in thisFile:
                thisCounter = thisCounter + 1
            thisFile.close()

            # Load readline history.
            readline.set_history_length(256)
            readline.read_history_file(thisHistory)
        
        except IOError:
            pass

        # Save readline history on exit.
        atexit.register(readline.write_history_file, thisHistory)

        # Enable TAB filename-completion, instead of Python's default
        # object completion.
        #readline.set_completer()
        readline.set_completer(self.getAttemptedCompletion)
        readline.parse_and_bind("tab: complete")
        readline.set_completer(self.getAttemptedCompletion)

        return thisCounter

    def invoke(self):

        thisPromptEnv = self._globalConfig.getServerEnv()
        thisPromptUser = self._globalConfig.getUsername()

        while (1):
            #
            # Reset critical variables every time around the loop.
            #
            thisFoundIt = False
            thisInput = ''
            thisPromptGroup = self._globalConfig.getCurrentServerGroup().getName()
            thisPrompt = '<' + thisPromptUser + '@' + thisPromptEnv + \
            '[' + thisPromptGroup + ']:' + os.getcwd() + '> '

            try:
                thisInput = raw_input(thisPrompt)

            except EOFError:
                print
                print
                print("INFO:  Caught CTRL-D keystroke.  Wrote history.  Dying...")
                print

                return

            except KeyboardInterrupt:
                print

            if (thisInput):
                thisTokens = thisInput.split()

                #
                # Step 1 - Handle both "cd" and "exit" from this chunk of code.
                # Should probably be moved into the parser proper,
                #
                if (thisTokens[0] == 'exit'):
                    print
                    print("Received exit command.  Wrote history.  Dying...")
                    print

                    return
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
                            print "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
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

######################################################################
