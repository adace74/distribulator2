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

# Standard modules
import syslog

######################################################################

class SysLogger:
    """
    Simple generic class whose purpose is to provide a wrapper around
    the standard syslog module.
    """

    def __init__(self, PassedFacility, PassedProcName):
        """Constructor."""

        self._facility = PassedFacility
        self._procname = PassedProcName

    def LogMsgInfo(self, PassedMessage):
        """Logs a given message with the syslog level INFO."""

        syslog.openlog(self._procname, syslog.LOG_PID, self._facility)
        syslog.syslog(syslog.LOG_INFO, PassedMessage)
        syslog.closelog()

    def LogMsgWarn(self, PassedMessage):
        """Logs a given message with the syslog level WARNING."""

        syslog.openlog(self._procname, syslog.LOG_PID, self._facility)
        syslog.syslog(syslog.LOG_WARNING, PassedMessage)
        syslog.closelog()

    def LogMsgError(self, PassedMessage):
        """Logs a given message with the syslog level WARNING."""

        syslog.openlog(self._procname, syslog.LOG_PID, self._facility)
        syslog.syslog(syslog.LOG_ERR, PassedMessage)
        syslog.closelog()

######################################################################
