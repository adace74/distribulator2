######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for handling the console mode of the application."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import atexit
import getpass
import os
import os.path
import readline
import rlcompleter
import string
import sys

# Custom modules
import engine.CommandRunner
import engine.data.ExternalCommand
import engine.data.InternalCommand

######################################################################

class ServerLister:
    """This class is responsible for handling the console mode of the application."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""

        thisGroupList = []
        thisOutput = '';
        thisServerGroupList = []
        thisServerNameList = []

        self._listString = self._globalConfig.getRequestedList()

        #
        # Step 1: Assemble two lists based on command syntax.
        #
        # thisServerNameList will contain a list of server names.
        # -or-
        # thisServerGroupList will contain a list of server groups.
        #
        # If this works, back-patch me into CommandRunner.py
        if (self._listString.find(',') == -1):
            thisGroupList.append(self._listString)
        else:
            thisGroupList = self._listString.split(',')

        for thisLoopStr in thisGroupList:
            thisLoopStr = thisLoopStr.strip()
            # Check for server name match.
            thisServer = self._globalConfig.getServerByName(thisLoopStr)

            if (thisServer):
                thisServerNameList.append(thisServer.getName())
                continue

            # Check for server group match.
            thisServerGroup = self._globalConfig.getServerGroupByName(thisLoopStr)
            if (thisServerGroup):
                thisServerGroupList.append(thisLoopStr)
            else:
                thisError = "ERROR: No matching server name or group '" + \
                            thisLoopStr + "'."
                self._globalConfig.getMultiLogger().LogMsgError(thisError)
                return False

        #
        # Step 2: Make sure noone's trying to mix
        # server hostnames and server group names together.
        #
        if ( (len(thisServerNameList) > 0) & (len(thisServerGroupList) > 0) ):
            thisError = "ERROR: Mixing of server name(s) and server group(s) is unsupported."
            self._globalConfig.getMultiLogger().LogMsgError(thisError)
            return False

        #
        # Step 3: If we found server name(s), then run with that.
        # Otherwise, do the same with the server group(s) given.
        #
        if ( len(thisServerNameList) > 0 ):
            for thisNameStr in thisServerNameList:
                thisServer = self._globalConfig.getServerByName(thisNameStr)

                thisOutput = thisOutput + thisServer.getUsername() + "@" + \
                    thisServer.getName() + " "
        else:
            # If we found server group names, then run with that.
            #
            for thisGroupStr in thisServerGroupList:
                thisServerGroup = self._globalConfig.getServerGroupByName(
                    thisGroupStr)

                thisServerList = thisServerGroup.getServerList()

                for thisServer in thisServerList:
                    thisOutput = thisOutput + thisServer.getUsername() + "@" + \
                        thisServer.getName() + " "

        thisOutput = thisOutput.strip()
        print thisOutput

        return

######################################################################
