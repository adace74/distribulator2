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
Simple generic class whose purpose is to provide a wrapper around
the standard logging module.
"""

# Version tag
__version__= '$Revision$'[11:-2]

######################################################################

class MultiLogger:
    """
    Simple class whose purpose is to provide a wrapper around
    the generic SysLogger module.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

    def LogMsgDebug(self, PassedMessage):
        """Logs and possibly prints a given message with the log level DEBUG."""

        self._globalConfig.getLogger().debug(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print("DEBUG: " + PassedMessage)

    def LogMsgInfoSeperator(self):
        """Logs and possibly prints a seperator with the log level INFO."""

        self._globalConfig.getLogger().info( \
            self._globalConfig.getSeperator() )

        if (self._globalConfig.isQuietMode() == False):
            print( "INFO: " + self._globalConfig.getSeperator() )

    def LogMsgInfo(self, PassedMessage):
        """Logs and possibly prints a given message with the log level INFO."""

        self._globalConfig.getLogger().info(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print("INFO: " + PassedMessage)

    def LogMsgWarn(self, PassedMessage):
        """Logs and possibly prints given message with the log level WARNING."""

        self._globalConfig.getLogger().warning(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print("WARN: " + PassedMessage)

    def LogMsgError(self, PassedMessage):
        """Logs and possibly prints a given message with the log level ERROR."""

        self._globalConfig.getLogger().error(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print("ERROR: " + PassedMessage)

######################################################################
