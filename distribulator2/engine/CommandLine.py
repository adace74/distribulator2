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
        myCounter = 0
        myHistory = os.path.join(os.environ['HOME'], ".dist_history")
    
        try:
            myFile = open(myHistory, 'r')
            for myLine in myFile:
                myCounter = myCounter + 1
            myFile.close()

            # Load readline history.
            readline.read_history_file(myHistory)
        
        except IOError:
            pass

        # Save readline history on exit.    
        atexit.register(readline.write_history_file, myHistory)

        # Enable TAB filename-completion, instead of Python's default
        # object completion.
        readline.set_completer()
        readline.parse_and_bind("tab: complete")

        return myCounter

    def processInput(self, PassedPassThruList):
        myPromptEnv = 'sample'
        myPromptUser = getpass.getuser()
        myPromptGroup = 'wlx'
        mySeperator = '============================================================'

        while (1):

            myPrompt = '<' + myPromptUser + '@' + myPromptEnv + \
            '[' + myPromptGroup + ']:' + os.getcwd() + '> '

            myInput = ''

            try:
                myInput = raw_input(myPrompt)

            except EOFError:
                print
                print
                print("Caught CTRL-D keystroke.  Wrote history.  Dying...")
                print
                return

            except KeyboardInterrupt:
                pass

            if (myInput):
                myTokens = myInput.split()

                if (myTokens[0] == 'exit'):
                    print
                    print("Received exit command.  Wrote history.  Dying...")
                    print
                    return

                try:
                    if (myTokens[0] == 'cd'):
                        os.chdir(myTokens[1])

                except OSError, (errno, strerror):
                    print "ERROR: [Errno %s] %s: %s" % (errno, strerror, myTokens[1])

                for myCommand in PassedPassThruList:
                    if (myTokens[0] == myCommand):
                        print "EXEC:  " + myInput
                        myStatus, myOutput = commands.getstatusoutput(myInput)
                        print myOutput
                        print mySeperator

                        if (myStatus != 0):
                            print "ERROR: Local shell returned error state."

######################################################################
