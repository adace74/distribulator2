######################################################################
#
# $Id$
#
# Name: CommandParser.py
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

class CommandParser:

    def parse(self, PassedTokenList):
        print "Implement Me!"

######################################################################
