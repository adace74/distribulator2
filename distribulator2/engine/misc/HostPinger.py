######################################################################
#
# $Id$
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
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
                        myError = "ERROR: Received non-matching service banner!"
                        self._globalConfig.getMultiLogger().LogMsgError(myError)
                        return 3

            mySocket.close()
            return 0

        # Add a debug mode someday!
        except socket.error, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, PassedHostname)
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return 1

        except socket.herror, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, PassedHostname)
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return 2

        except socket.gaierror, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, PassedHostname)
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return 3

        except socket.timeout:
            myError = "ERROR: Socket timed out while connecting to server."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return 4

#######################################################################
