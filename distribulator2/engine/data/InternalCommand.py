######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding an internal command."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import string
import sys

######################################################################

class InternalCommand:
    """This class holds data regarding an external command."""

    def __init__(self):
        """Constructor."""

        pass

######################################################################
# Unix command line string.
######################################################################

    def getCommand(self):
        """This is a typical accessor method."""

        return self._command

######################################################################

    def setCommand(self, PassedCommand):
        """This is a typical accessor method."""

        self._command = PassedCommand

######################################################################
