######################################################################
#
# $Id$
#
# Name: SysLogger.py
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
        syslog.syslog(syslog.LOG_WARN, PassedMessage)
        syslog.closelog()

    def LogMsgError(self, PassedMessage):
        syslog.openlog('distribulator.py', syslog.LOG_PID, self._facility)
        syslog.syslog(LOG_ERROR, PassedMessage)
        syslog.closelog()

######################################################################
