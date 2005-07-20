######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is the base abstract class for all runtime commands."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import sys

######################################################################

class Command:
    """This class is the base abstract class for all runtime commands."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        pass

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""
        
        pass

######################################################################

    def doAreYouSure(self):
        """This method simply asks the never-ending question: Are You Sure?"""

        try:
            sys.stdout.write("INPUT   |Yes / No> ")
            myInput = sys.stdin.readline()
            myInput = myInput.strip()

        except (EOFError, KeyboardInterrupt):
            myInfo = "Caught CTRL-C / CTRL-D keystroke."
            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
            return False

        if (myInput.lower() == 'yes'):
            return True
        else:
            return False

######################################################################
