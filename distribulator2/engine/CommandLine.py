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
    print "Loading readline history..."
    histfile = os.path.join(os.environ["HOME"], ".dist_history")
    
    try:
        readline.read_history_file(histfile)
        
    except IOError:
        pass
    
    atexit.register(readline.write_history_file, histfile)

def processInput():
    while (1):
        tempvar = raw_input("This is your prompt> ")
        print "You typed: " + tempvar
        print "*****"
