######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for handling the list mode of the application."""

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
import engine.data.ExternalCommand
import engine.data.InternalCommand
import engine.mode.Mode

######################################################################

class ListMode(engine.mode.Mode.Mode):
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
        # If my works, back-patch me into AllCommand.py
        if (self._listString.find(',') == -1):
            myGroupList.append(self._listString)
        else:
            myGroupList = self._listString.split(',')

        for myLoopStr in myGroupList:
            myLoopStr = myLoopStr.strip()
            # Check for server name match.
            myServer = self._globalConfig.getServerByName(myLoopStr)

            if (myServer):
                myServerNameList.append(myServer.getName())
                continue

            # Check for server group match.
            myServerGroup = self._globalConfig.getServerGroupByName(myLoopStr)
            if (myServerGroup):
                myServerGroupList.append(myLoopStr)
            else:
                myError = "ERROR: No matching server name or group '" + \
                            myLoopStr + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False

        #
        # Step 2: Make sure noone's trying to mix
        # server hostnames and server group names together.
        #
        if ( (len(myServerNameList) > 0) & (len(myServerGroupList) > 0) ):
            myError = "ERROR: Mixing of server name(s) and server group(s) is unsupported."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        #
        # Step 3: If we found server name(s), then run with that.
        # Otherwise, do the same with the server group(s) given.
        #
        if ( len(myServerNameList) > 0 ):
            for myNameStr in myServerNameList:
                myServer = self._globalConfig.getServerByName(myNameStr)

                myOutput = myOutput + myServer.getUsername() + "@" + \
                    myServer.getName() + " "
        else:
            # If we found server group names, then run with that.
            #
            for myGroupStr in myServerGroupList:
                myServerGroup = self._globalConfig.getServerGroupByName(
                    myGroupStr)

                myServerList = myServerGroup.getServerList()

                for myServer in myServerList:
                    myOutput = myOutput + myServer.getUsername() + "@" + \
                        myServer.getName() + " "

        myOutput = myOutput.strip()
        print myOutput

        return

######################################################################
