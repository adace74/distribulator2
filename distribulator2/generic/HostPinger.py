######################################################################
#
# $Id$
#
# Name: HostPinger.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import commands

######################################################################

class HostPinger:

    def __init__(self, PassedCommand):
        self._command = PassedCommand

    def ping(self, PassedHostname):
        thisStatus, thisOutput = \
        commands.getstatusoutput(self._command + " " + PassedHostname)

        return thisStatus

#######################################################################
