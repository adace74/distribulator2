######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class holds data regarding a given server."""

# Version tag
__version__= '$Revision$'[11:-2]

######################################################################

class Server:
    """This class holds data regarding a given server."""

    def __init__(self):
        """Constructor."""

        pass

######################################################################
# Name.
######################################################################

    def getName(self):
        """This is a typical accessor method."""

        return self._name

######################################################################

    def setName(self, PassedName):
        """This is a typical accessor method."""

        self._name = PassedName

######################################################################
# Username.
######################################################################

    def getUsername(self):
        """This is a typical accessor method."""

        return self._username

######################################################################

    def setUsername(self, PassedUsername):
        """This is a typical accessor method."""

        self._username = PassedUsername

######################################################################

######################################################################
# SSH Flags.
######################################################################

    def getFlags(self):
        """This is a typical accessor method."""

        return self._flags

######################################################################

    def setFlags(self, PassedFlags):
        """This is a typical accessor method."""
 
        self._flags = PassedFlags

######################################################################
