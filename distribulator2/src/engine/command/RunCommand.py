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
This class is responsible for doing the actual work of
expanding a given distribulator command into a set of
SSH commands and running them.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import re
import os
import os.path
import stat
import string
import sys

# Custom modules
import Command
import engine.data.ExternalCommand
import engine.misc.HostPinger

######################################################################

class RunCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doRun(self, PassedCommString):
        """This method is responsible for the processing of the 'run' command."""

        # Tokenize!
        self._commString = PassedCommString
        self._commTokens = PassedCommString.split()

        myCommandCount = 0
        myServerGroupList = []
        myServerNameList = []
        myRunTarget = '';

        myIsNow = False
        myIsReverse = False
        myIsSingle = False

        #
        # Step 1:  Create our own tokens, and check for SSH flags and
        #          the special-case keywords. (i.e. now, reverse, single)
        #
        if ( self._commString.find('"') == -1 ):
            myError = "Command Syntax Error.  Try 'help run' for more information."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # Get substr indexes.
        myFirstQuoteIndex = self._commString.find('"')
        myLastQuoteIndex = self._commString.rfind('"')
        myPrefixStr = self._commString[0:myFirstQuoteIndex]
        myBodyStr = self._commString[myFirstQuoteIndex:(myLastQuoteIndex + 1)]
        mySuffixStr = self._commString[myLastQuoteIndex + 1:]

        # Check for pass-through SSH flags
        if (myPrefixStr.find('-') != -1):
            myFlagStr = ' ' + myPrefixStr[myPrefixStr.find('-'):]
            myFlagStr = myFlagStr.rstrip()
        else:
            myFlagStr = ''

        # Check for special-case keywords.
        if (mySuffixStr.find(' now') != -1):
            myIsNow = True
            mySuffixStr = string.replace(mySuffixStr, ' now' , '')

        if (mySuffixStr.find(' reverse') != -1):
            myIsReverse = True
            mySuffixStr = string.replace(mySuffixStr, ' reverse' , '')

        if (mySuffixStr.find(' single') != -1):
            myIsSingle = True
            mySuffixStr = string.replace(mySuffixStr, ' single' , '') 

        #
        # Step 2: Try to determine what the target of the command is
        #         and set a state-tracking variable accordingly.
        # 
        if (len(mySuffixStr) == 0):
            # run "uptime"
            # run -t "uptime"
            myRunTarget = 'current_server_group';
        # Check for syntax errors.
        elif (mySuffixStr.find(' on ') == -1):
            myError = "Command Syntax Error.  Try 'help run' for more information."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False
        elif (mySuffixStr.find(',') == -1):
            # run "uptime" on app
            # run -t "uptime" on app
            # run "uptime" on app01
            # run -t "uptime" on app01
            myRunTarget = 'single_server_group';
        else:
            # run "uptime" on app, www
            # run -t "uptime" on app, www
            # run "uptime" on app01, www01
            # run -t "uptime" on app01, www01
            myRunTarget = 'multiple_server_group';

        # Assuming no error up until my point we can now
        # throw out the " on " part of our command.
        myGroupStr = mySuffixStr[mySuffixStr.find(' on ') + 4:]
        myGroupStr = myGroupStr.strip()

        #
        # Step 3: Assemble two lists based on command syntax.
        #
        # myServerNameList will contain a list of server names.
        # -or-
        # myServerGroupList will contain a list of server groups.
        #
        if (myRunTarget == 'current_server_group'):
            myGroupStr = self._globalConfig.getCurrentServerGroup().getName()
            myServerGroupList.append(myGroupStr)
        #
        elif (myRunTarget == 'single_server_group'):
            # Check for server name match.
            myServer = self._globalConfig.getCurrentEnv().getServerByName(myGroupStr)

            if (myServer):
                myServerNameList.append(myServer.getName())
            else:
                # Check for server group match.
                myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName(myGroupStr)
                # Validate.
                if (not myServerGroup):
                    myError = "No matching server name or group '" + \
                                myGroupStr + "'."
                    self._globalConfig.getMultiLogger().LogMsgError(myError)
                    return False
                else:
                    myServerGroupList.append(myGroupStr)
        #
        elif (myRunTarget == 'multiple_server_group'):
            myGroupList = myGroupStr.split(',')

            for myLoopStr in myGroupList:
                myLoopStr = myLoopStr.strip()
                # Check for server name match.
                myServer = self._globalConfig.getCurrentEnv().getServerByName(myLoopStr)

                if (myServer):
                    myServerNameList.append(myServer.getName())
                    continue

                # Check for server group match.
                myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName(myLoopStr)
                if (myServerGroup):
                    myServerGroupList.append(myLoopStr)
                else:
                    myError = "No matching server name or group '" + \
                                myLoopStr + "'."
                    self._globalConfig.getMultiLogger().LogMsgError(myError)
                    return False

        #
        # Step 4: Make sure noone's trying to mix
        # server hostnames and server group names together.
        #
        if ( (len(myServerNameList) > 0) and (len(myServerGroupList) > 0) ):
            myError = "Mixing of server name(s) and server group(s) is unsupported."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        #
        # Step 5: Must make sure...are you sure you're sure?
        #
        if ( (not self._globalConfig.isBatchMode()) and (not myIsNow) ):
            myDisplayStr = ''

            if ( len(myServerNameList) > 0):
                for myNameStr in myServerNameList:
                    myDisplayStr = myDisplayStr + myNameStr + ','

                myDisplayStr = myDisplayStr.rstrip(',')

                # Are you sure?
                myInfo = "Run command " + myBodyStr + " on server(s) " + \
                      myDisplayStr + "?"
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

                if (not self.doAreYouSure()):
                    myInfo = "Aborting command."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                    return False
            else:
                for myGroupStr in myServerGroupList:
                    myDisplayStr = myDisplayStr + myGroupStr + ','

                myDisplayStr = myDisplayStr.rstrip(',')

                # Are you sure?
                myInfo = "Run command " + myBodyStr + " on server group(s) " + \
                      myDisplayStr + "?"
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

                if (not self.doAreYouSure()):
                    myInfo = "Aborting command."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                    return False

        #
        # Step 6: If we found server name(s), then run with that.
        # Otherwise, do the same with the server group(s) given.
        #
        # Slightly nasty hack.  Since lists can only be sorted in-place,
        # and copying objects in Python isn't super-easy, we do the
        # following:
        #
        # 1) Reverse sort the list
        # 2) Run the commands
        #
        if ( len(myServerNameList) > 0 ):
            if (myIsReverse):
                myServerNameList.reverse()

            try:
                for myNameStr in myServerNameList:
                    myServer = self._globalConfig.getCurrentEnv().getServerByName(myNameStr)
                    myPinger = engine.misc.HostPinger.HostPinger(self._globalConfig)

                    if (myPinger.ping(myNameStr) == 0):
                        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)

                        # Build It.
                        if ( myServer.getVersion() != None ):
                            myExternalCommand.setCommand( \
                                self._globalConfig.getSshBinary() + myFlagStr + \
                                " -" + myServer.getVersion() + \
                                " -l " + myServer.getUsername() + " " + \
                                myServer.getName() + " " + \
                                myBodyStr )
                        else:
                            myExternalCommand.setCommand( \
                                self._globalConfig.getSshBinary() + myFlagStr + \
                                " -l " + myServer.getUsername() + " " + \
                                myServer.getName() + " " + \
                                myBodyStr )

                        # Run It.
                        if ( self._globalConfig.isBatchMode() ):
                            myExternalCommand.run()
                        elif ( len(myFlagStr) > 0 ):
                            myExternalCommand.run(True)
                        else:
                            myExternalCommand.run()

                        myCommandCount = myCommandCount + 1

                        if (myIsSingle):
                            break
                    else:
                        myError = "Server '" + myServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self._globalConfig.getMultiLogger().LogMsgError(myError)
                        self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

            except EOFError:
                pass
            except KeyboardInterrupt:
                myInfo = "Caught CTRL-C keystroke.  Attempting to abort..."
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                self._globalConifg.setBreakState(True)
                return False

            return True
        else:
            # If we found server group names, then run with that.
            #
            # Slightly nasty hack.  Since lists can only be sorted in-place,
            # and copying objects in Python isn't super-easy, we do the
            # following:
            #
            # 1) Reverse sort the list
            # 2) Run the commands
            # 3) Forward-sort the list, hopefully back to its original state.
            #
            for myGroupStr in myServerGroupList:
                myServerGroup = self._globalConfig.getCurrentEnv().getServerGroupByName(myGroupStr)

                reggie=re.compile(r'(.*):r\'(.*)\'')
                maggie=reggie.match(myGroupStr)
                if (maggie != None):
                    myServerList = myServerGroup.getRegExServerList(maggie.group(2))

                    if ( (not self._globalConfig.isBatchMode()) and (not myIsNow) ):
                        myDisplayStr = ''
                        for servlist in myServerList:
                            myDisplayStr = myDisplayStr + servlist.getName() + ','
                            myDisplayStr = myDisplayStr.rstrip(',')

                            # Are you sure?
                            myInfo = "Run command " + myBodyStr + " on server(s) " + \
                                myDisplayStr + "?"
                            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

                            if (not self.doAreYouSure()):
                                myInfo = "Aborting command."
                                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                                continue
                else:
                    myServerList = myServerGroup.getServerList()

                if (myIsReverse):
                    myServerList.reverse()

                try:
                    for myServer in myServerList:
                        myPinger = engine.misc.HostPinger.HostPinger(self._globalConfig)

                        if (myPinger.ping(myServer.getName()) == 0):
                            myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)

                            # Build It.
                            if ( myServer.getVersion() != None ):
                                myExternalCommand.setCommand( \
                                self._globalConfig.getSshBinary() + myFlagStr + \
                                " -" + myServer.getVersion() + \
                                " -l " + myServer.getUsername() + " " + \
                                myServer.getName() + " " + \
                                myBodyStr )
                            else:
                                myExternalCommand.setCommand( \
                                self._globalConfig.getSshBinary() + myFlagStr + \
                                " -l " + myServer.getUsername() + " " + \
                                myServer.getName() + " " + \
                                myBodyStr )

                            # Run It.
                            if ( self._globalConfig.isBatchMode() ):
                                myExternalCommand.run()
                            elif ( len(myFlagStr) > 0 ):
                                myExternalCommand.run(True)
                            else:
                                myExternalCommand.run()

                            myCommandCount = myCommandCount + 1

                            if (myIsSingle):
                                break
                        else:
                            myError = "Server '" + myServer.getName() + \
                                        "' appears to be down.  Continuing..."
                            self._globalConfig.getMultiLogger().LogMsgError(myError)
                            self._globalConfig.getMultiLogger().LogMsgDebugSeperator()

                except EOFError:
                    pass
                except KeyboardInterrupt:
                    myInfo = "Caught CTRL-C keystroke.  Attempting to abort..."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                    self._globalConfig.setBreakState(True)
                    return False

                if (myIsReverse):
                    myServerList.sort()

            return myCommandCount

######################################################################
