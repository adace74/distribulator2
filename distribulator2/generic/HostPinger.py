######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""
Simple generic class whose funciton is to attempt to ping a given host.

TODO:
- Change this from a pass-through to the ping command to a real
  independent test.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import commands

######################################################################

class HostPinger:
    """Simple generic class whose funciton is to attempt to ping a given host."""

    def __init__(self, PassedCommand):
        """Constructor."""
        self._command = PassedCommand

    def ping(self, PassedHostname):
        """Attempts to ping a given host."""

        thisStatus, thisOutput = \
        commands.getstatusoutput(self._command + " " + PassedHostname)

        return thisStatus

#######################################################################
