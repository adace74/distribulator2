######################################################################
#
# $Id$
#
# Name: BatchRunner.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import stat
import string
import sys

# Custom modules
import engine.CommandRunner
import engine.data.ExternalCommand
import engine.data.InternalCommand

class BatchRunner:

    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig

    def invoke(self):
        # Let's make sure the file we've been given is readable.
        try:
            if ( stat.S_ISREG(os.stat(
                self._globalConfig.getBatchFile())[stat.ST_MODE]) \
                 == False ):
                print("ERROR: File '" + self._globalConfig.getBatchFile() +
                      "' is accessible, but not regular.")
                return False
        except OSError, (errno, strerror):
            thisError = "ERROR:[Errno %s] %s: %s" % ( errno, strerror, \
                                                       self._globalConfig.getBatchFile() )
            print(thisError)
            self._globalConfig.getSysLogger().LogMsgError(thisError)
            return False

        # Let everyone know what we're doing.
        self._globalConfig.getSysLogger().LogMsgInfo(
            "INFO: Attempting command run using file '" + \
            self._globalConfig.getBatchFile() + "'.")

        try:
            thisFile = open(self._globalConfig.getBatchFile(), 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.strip()
                print "LINE: " + thisLine

            thisFile.close()

        except IOError, (errno, strerror):
            thisError = "ERROR:[Errno %s] %s: %s" % \
                        (errno, strerror, thisFilename)
            print(thisError)
            self._globalConfig.getSysLogger().LogMsgError(thisError)
            sys.exit(1)

        return True

######################################################################
