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

# Standard modules
import errno

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

        try:
            self._globalConfig.getAuditLogger().critical(PassedMessage)
            self._globalConfig.getStdoutLogger().critical(PassedMessage)

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise 

    def LogMsgDebug(self, PassedMessage):
        """Logs and possibly prints a given message with the log level DEBUG."""

        try:
            self._globalConfig.getAuditLogger().debug(PassedMessage)
            self._globalConfig.getStdoutLogger().debug(PassedMessage)

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def LogMsgDebugSeperator(self):
        """Logs and possibly prints a seperator with the log level DEBUG."""

        try:
            self._globalConfig.getAuditLogger().debug( self._globalConfig.getSeperator() )
            self._globalConfig.getStdoutLogger().debug( self._globalConfig.getSeperator() )

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def LogMsgInfo(self, PassedMessage):
        """Logs and possibly prints a given message with the log level INFO."""

        try:
            self._globalConfig.getAuditLogger().info(PassedMessage)
            self._globalConfig.getStdoutLogger().info(PassedMessage)

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def LogMsgInfoSeperator(self):
        """Logs and possibly prints a seperator with the log level INFO."""

        try:
            self._globalConfig.getAuditLogger().info( self._globalConfig.getSeperator() )
            self._globalConfig.getStdoutLogger().info( self._globalConfig.getSeperator() )

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def LogMsgWarn(self, PassedMessage):
        """Logs and possibly prints given message with the log level WARNING."""

        try:
            self._globalConfig.getAuditLogger().warning(PassedMessage)
            self._globalConfig.getStdoutLogger().warning(PassedMessage)

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

    def LogMsgError(self, PassedMessage):
        """Logs and possibly prints a given message with the log level ERROR."""

        try:
            self._globalConfig.getAuditLogger().error(PassedMessage)
            self._globalConfig.getStdoutLogger().error(PassedMessage)

        except IOError, e:
            if e.errno != errno.EPIPE:
                raise

######################################################################
