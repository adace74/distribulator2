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
import sys

def initHistory():
    myHistory = os.path.join(os.environ["HOME"], ".dist_history")
    
    try:
        readline.read_history_file(myHistory)
        
    except IOError:
        pass
    
    atexit.register(readline.write_history_file, myHistory)

def processInput():
    while (1):
        myPromptEnv = 'sample'
        myPromptUser = 'awd'
        myPromptGroup = 'wlx'
        myPrompt = "<" + myPromptUser + "@" + myPromptEnv + "[" + myPromptGroup + "]:" + os.getcwd() + "> "

        myInput = raw_input(myPrompt)
        print "You typed: " + myInput
        print "*****"

        if (myInput == "exit"):
            print
            print("Received exit command.  Wrote history.  Dying...")
            print
            sys.exit(0)
