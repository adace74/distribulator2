######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved.
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""
Simple generic class whose funciton is to attempt to ping a given host.
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

        myStatus, myOutput = \
        commands.getstatusoutput(self._command + " " + PassedHostname)

        return myStatus

#######################################################################
