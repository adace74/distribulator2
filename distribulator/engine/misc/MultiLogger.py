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
Simple generic class whose purpose is to provide a wrapper around
the standard logging module.
"""

# Version tag
__version__= '$Revision$'[11:-2]

######################################################################

class MultiLogger:
    """
    Simple class whose purpose is to provide a wrapper around
    the generic logger module.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

    def LogMsgCrit(self, PassedMessage):
        """Logs and possibly prints a given message with the log level CRITICAL."""

        self._globalConfig.getAuditLogger().critical(PassedMessage)
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().critical(PassedMessage)

    def LogMsgDebug(self, PassedMessage):
        """Logs and possibly prints a given message with the log level DEBUG."""

        self._globalConfig.getAuditLogger().debug(PassedMessage)
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().debug(PassedMessage)

    def LogMsgDebugSeperator(self):
        """Logs and possibly prints a seperator with the log level DEBUG."""

        self._globalConfig.getAuditLogger().debug( self._globalConfig.getSeperator() )
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().debug( self._globalConfig.getSeperator() )

    def LogMsgInfo(self, PassedMessage):
        """Logs and possibly prints a given message with the log level INFO."""

        self._globalConfig.getAuditLogger().info(PassedMessage)
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().info(PassedMessage)

    def LogMsgInfoSeperator(self):
        """Logs and possibly prints a seperator with the log level INFO."""

        self._globalConfig.getAuditLogger().info( self._globalConfig.getSeperator() )
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().info( self._globalConfig.getSeperator() )

    def LogMsgWarn(self, PassedMessage):
        """Logs and possibly prints given message with the log level WARNING."""

        self._globalConfig.getAuditLogger().warning(PassedMessage)
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().warning(PassedMessage)

    def LogMsgError(self, PassedMessage):
        """Logs and possibly prints a given message with the log level ERROR."""

        self._globalConfig.getAuditLogger().error(PassedMessage)
        if (not self._globalConfig.isListMode()):
            self._globalConfig.getStdoutLogger().error(PassedMessage)

######################################################################
