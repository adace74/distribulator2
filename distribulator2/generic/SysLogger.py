######################################################################
#
# $Id$
#
# Name: SysLogger.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import syslog

######################################################################

class SysLogger:

    def __init__(self, PassedFacility):
        self._facility = PassedFacility

    def LogMsgInfo(self, PassedMessage):
        syslog.openlog('distribulator.py', syslog.LOG_PID, self._facility)
        syslog.syslog(syslog.LOG_INFO, PassedMessage)
        syslog.closelog()

    def LogMsgWarn(self, PassedMessage):
        syslog.openlog('distribulator.py', syslog.LOG_PID, self._facility)
        syslog.syslog(syslog.LOG_WARNING, PassedMessage)
        syslog.closelog()

    def LogMsgError(self, PassedMessage):
        syslog.openlog('distribulator.py', syslog.LOG_PID, self._facility)
        syslog.syslog(syslog.LOG_ERR, PassedMessage)
        syslog.closelog()

######################################################################
