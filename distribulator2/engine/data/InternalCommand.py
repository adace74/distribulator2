######################################################################
#
# $Id$
#
# Name: InternalCommand.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import os
    import os.path
    import string
    import sys

except ImportError:
    print "An error occured while loading Python modules, exiting..."
    sys.exit(1)

######################################################################

class InternalCommand:
    #
    # Constructor.
    #
    def __init__(self):
        self.thisCommandList = [ 'copy', 'help', 'login', 'remote-shell',
                                 'run', 'server-group', 'server-list' ]
    #
    # Unix command line string.
    #
    def getCommand(self):
        return self.thisCommand
    
    def setCommand(self, PassedCommand):
        self.thisCommand = PassedCommand
    #
    # Function methods.
    #
    def parse(self):
        self.thisTokens = self.thisCommand.split()
        print "ERROR: Command '" + self.thisTokens[0] + "' unknown."

######################################################################
