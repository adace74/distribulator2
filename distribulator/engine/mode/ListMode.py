#####################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved.
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for handling the list mode of the application."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import getpass
import os
import os.path
import readline
import rlcompleter
import string
import sys

# Custom modules
import Mode
import engine.data.ExternalCommand
import engine.data.InternalCommand

######################################################################

class ListMode(Mode.Mode):
    """This class is responsible for handling the list mode of the application."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""

        myGroupList = []
        myOutput = '';
        myServerGroupList = []
        myServerNameList = []

        self._listString = self._globalConfig.getRequestedList()

        #
        # Step 1: Assemble two lists based on command syntax.
        #
        # myServerNameList will contain a list of server names.
        # -or-
        # myServerGroupList will contain a list of server groups.
        #
        # If this works, port back into Dispatcher.py...
        #
        if (self._listString.find(',') == -1):
            myGroupList.append(self._listString)
        else:
            myGroupList = self._listString.split(',')

        for myLoopStr in myGroupList:
            myLoopStr = myLoopStr.strip()
            # Check for server name match.
            myServer = self._globalConfig.getCurrentEnv().getServerByName(myLoopStr)

            if (myServer):
                myServerNameList.append(myServer.getName())
                continue

            # Check for server group match, with and without attributes.
            myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName(myLoopStr)

            # Validate.
            if (myServerGroup):
                myServerGroupList.append(myLoopStr)

        #
        # Step 2: Make sure noone's trying to mix
        # server hostnames and server group names together.
        #
        if ( (len(myServerNameList) > 0) and (len(myServerGroupList) > 0) ):
            myError = "Mixing of server name(s) and server group(s) is unsupported."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        #
        # Step 3: If we found server name(s), then run with that.
        # Otherwise, do the same with the server group(s) given.
        #
        myPinger = engine.misc.HostPinger.HostPinger(self._globalConfig)

        # Server name(s)
        if ( len(myServerNameList) > 0 ):
            for myNameStr in myServerNameList:
                myServer = self._globalConfig.getCurrentEnv().getServerByName(myNameStr)

                if (myPinger.ping(myNameStr) == 0):
                    if ( self._globalConfig.isPrintUsername() ):
                        myOutput = myOutput + myServer.getUsername() + "@"

                    myOutput = myOutput + myServer.getName() + " "
                else:
                    myError = "Server '" + myServer.getName() + \
                              "' appears to be down.  Continuing..."
                    self._globalConfig.getMultiLogger().LogMsgWarn(myError)
                    self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

        # Server group(s)
        else:
            for myGroupStr in myServerGroupList:
                # Check for server group match, with and without attributes.
                myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName(myGroupStr)

                if (myLoopStr.find('[') == -1):
                    myServerList = myServerGroup.getServerList()
                else:
                    myServerList = myServerGroup.getAttribValueServerList(myGroupStr)

                for myServer in myServerList:
                    if (myPinger.ping( myServer.getName() ) == 0):
                        if ( self._globalConfig.isPrintUsername() ):
                            myOutput = myOutput + myServer.getUsername() + "@"

                        myOutput = myOutput + myServer.getName() + " "
                    else:
                        myError = "Server '" + myServer.getName() + \
                                  "' appears to be down.  Continuing..."
                        self._globalConfig.getMultiLogger().LogMsgWarn(myError)
                        self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

        myOutput = myOutput.strip()
        print myOutput

        return

######################################################################
