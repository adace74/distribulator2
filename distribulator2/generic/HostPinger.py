######################################################################
#
# $Id$
#
# Name: HostPinger.py
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
