######################################################################
#
# $Id$
#
# Name: SysLogger.py
#
######################################################################
# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import string
import sys

# Custom modules
import engine.CommandLine

######################################################################

class GlobalConfig:

    #
    # Global settings.
    #
    #
    # Unix command "pass through" list.
    #
    def getPassThruList(self):
        return self.thisPassThruList
    
    def setPassThruList(self, PassedPassThruList):
        self.thisPassThruList = PassedPassThruList
    #
    # Servers and ServerGroups
    #

######################################################################
