######################################################################
#
# $Id$
#
# Name: InternalCommand.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import string
import sys

######################################################################

class InternalCommand:
    #
    # Unix command line string.
    #
    def getCommand(self):
        return self._command
    
    def setCommand(self, PassedCommand):
        self._command = PassedCommand

######################################################################
