######################################################################
#
# $Id$
#
# Name: CommandLine.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Import modules
import atexit
import commands
import getpass
import os
import os.path
import readline
import rlcompleter
import sys

######################################################################

class CommandLine:

    def initHistory(self):
        thisCounter = 0
        thisHistory = os.path.join(os.environ['HOME'], ".dist_history")
    
        try:
            thisFile = open(thisHistory, 'r')
            for thisLine in thisFile:
                thisCounter = thisCounter + 1
            thisFile.close()

            # Load readline history.
            readline.read_history_file(thisHistory)
        
        except IOError:
            pass

        # Save readline history on exit.    
        atexit.register(readline.write_history_file, thisHistory)

        # Enable TAB filename-completion, instead of Python's default
        # object completion.
        readline.set_completer()
        readline.parse_and_bind("tab: complete")

        return thisCounter

    def invoke(self, thisGlobalConfig):
        thisPromptEnv = 'sample'
        thisPromptUser = getpass.getuser()
        thisPromptGroup = 'wlx'
        thisSeperator = '============================================================'

        while (1):

            thisPrompt = '<' + thisPromptUser + '@' + thisPromptEnv + \
            '[' + thisPromptGroup + ']:' + os.getcwd() + '> '

            thisInput = ''

            try:
                thisInput = raw_input(thisPrompt)

            except EOFError:
                print
                print
                print("Caught CTRL-D keystroke.  Wrote history.  Dying...")
                print
                return

            except KeyboardInterrupt:
                print

            if (thisInput):
                thisTokens = thisInput.split()

                if (thisTokens[0] == 'exit'):
                    print
                    print("Received exit command.  Wrote history.  Dying...")
                    print
                    return
                #
                # Only with objects can one -truly- cheat in life!
                #
                # This most likely should follow the
                # InternalCommand / ExternalCommand / CommandRunner standard
                # but for now I'm just too lazy to rework it.
                #
                # Step 1 - If they want to cd, let them!
                #
                try:
                    if (thisTokens[0] == 'cd'):
                        os.chdir(thisTokens[1])
                        continue

                except OSError, (errno, strerror):
                    print "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisTokens[1])
                #
                # Step 2 - Check for Unix "pass through" commands.
                #
                for thisCommand in thisGlobalConfig.getPassThruList():
                    if (thisTokens[0] == thisCommand):
                        print "EXEC:  " + thisInput
                        thisStatus, thisOutput = commands.getstatusoutput(thisInput)
                        print thisOutput
                        print thisSeperator

                        if (thisStatus != 0):
                            print "ERROR: Local shell returned error state."

                        continue

                #
                # Step 3 - Invoke Das Parser!
                #

######################################################################
