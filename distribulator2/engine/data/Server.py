######################################################################
#
# $Id$
#
# Name: Server.py
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

class Server:
    #
    # Name.
    #
    def getName(self):
        return self._name

    def setName(self, PassedName):
        self._name = PassedName
    #
    # Username.
    #
    def getUsername(self):
        return self._username

    def setUsername(self, PassedUsername):
        self._username = PassedUsername

######################################################################
