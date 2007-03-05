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
Advanced class to allow for better pinging capabilities.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import socket

######################################################################

class HostPinger:
    """Advanced class to allow for better pinging capabilities."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

    def ping(self, PassedHostname):
        """Attempts to ping a given host."""

        try:
            mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            mySocket.settimeout( self._globalConfig.getPingTimeout() )
            mySocket.connect( (PassedHostname, self._globalConfig.getPingPort()) )

            # Check for a banner if specified.
            if ( len(self._globalConfig.getPingBanner() ) > 0):
                myString = mySocket.recv(1024)

                # Fix to actually do a string compare!
                if (myString.find(self._globalConfig.getPingBanner()) == -1):
                        myError = "Received non-matching service banner!"
                        self._globalConfig.getMultiLogger().LogMsgWarn(myError)
                        return 3

            mySocket.close()
            return 0

        except socket.error, myErrorInfo:
            myError = "OS Reports: [%s] during TCP ping attempt." % (myErrorInfo)
            self._globalConfig.getMultiLogger().LogMsgWarn(myError)
            return 1

        except socket.herror, (errno, strerror):
            myError = "OS Reports: [Errno %s: %s] during TCP ping attempt." % (errno, strerror)
            self._globalConfig.getMultiLogger().LogMsgWarn(myError)
            return 2

        except socket.gaierror, (errno, strerror):
            myError = "OS Reports: [Errno %s: %s] during TCP ping attempt." % (errno, strerror)
            self._globalConfig.getMultiLogger().LogMsgWarn(myError)
            return 3

        except socket.timeout:
            myError = "OS Reports: [Socket timeout] during TCP ping attempt."
            self._globalConfig.getMultiLogger().LogMsgWarn(myError)
            return 4

#######################################################################
