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
the standard syslog module.
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

    def LogMsgInfoSeperator(self):
        """Logs and possibly prints a seperator with the syslog level INFO."""

        self._globalConfig.getSysLogger().LogMsgInfo( \
            self._globalConfig.getSeperator() )

        if (self._globalConfig.isQuietMode() == False):
            print(mySeperator)

    def LogMsgInfo(self, PassedMessage):
        """Logs and possibly prints a given message with the syslog level INFO."""

        self._globalConfig.getSysLogger().LogMsgInfo(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print(PassedMessage)

    def LogMsgWarn(self, PassedMessage):
        """Logs and possibly prints given message with the syslog level WARNING."""

        self._globalConfig.getSysLogger().LogMsgWarn(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print(PassedMessage)

    def LogMsgError(self, PassedMessage):
        """Logs and possibly prints a given message with the syslog level WARNING."""

        self._globalConfig.getSysLogger().LogMsgError(PassedMessage)

        if (self._globalConfig.isQuietMode() == False):
            print(PassedMessage)

######################################################################
