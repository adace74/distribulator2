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
import os
import os.path
import readline
import rlcompleter
import sys

######################################################################

class CommandLine:

    def initHistory(self):
        myHistory = os.path.join(os.environ["HOME"], ".dist_history")
    
        try:
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

    def processInput(self):
        while (1):
            myPromptEnv = 'sample'
            myPromptUser = 'awd'
            myPromptGroup = 'wlx'
            myPrompt = "<" + myPromptUser + "@" + myPromptEnv + "[" + myPromptGroup + "]:" + os.getcwd() + "> "

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
                print "You typed: " + myInput
                print "*****"

                if (myInput == "exit"):
                    print
                    print("Received exit command.  Wrote history.  Dying...")
                    print
                    return
            else:
                print

######################################################################
