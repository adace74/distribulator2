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
This class is responsible for doing the actual work of
expanding a given distribulator command into a set of
SSH commands and running them.
"""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import stat
import string

# Custom modules
import Command
import engine.data.ExternalCommand
import engine.misc.HostPinger

######################################################################

class CopyCommand(Command.Command):
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def doCopy(self, PassedCommString):
        """This method is responsible for the processing of the 'copy' command."""

        # Tokenize!
        self._commString = PassedCommString
        self._commTokens = PassedCommString.split()

        myCommandCount = 0
        myCopyTarget = '';
        myServerGroupList = []
        myServerNameList = []

        #
        # Step 1: Common validation and variable-setting.
        #
        # Validate token count.
        if (len(self._commTokens) < 3):
            myError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False
        elif (self._commTokens[2].find('/') == -1):
            myError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False            
        if (self._commString.find(' reverse') > 0):
            myError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False
        else:
            myLocalPath = self._commTokens[1]
            myRemotePath = self._commTokens[2]

        # Validate local file.
        try:
            if ( stat.S_ISREG(os.stat(
                myLocalPath)[stat.ST_MODE]) == False):
                myError = "ERROR: File '" + myLocalPath + \
                            "' is accessible, but not regular."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
        except OSError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                      myLocalPath)
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        #
        # Step 2: Try to determine what the target of the command is,
        #         and set a state-tracking variable accordingly.
        # 
        if (self._commString.find(':') == -1):
            # copy /tmp/blah /tmp/
            myCopyTarget = 'current_server_group'
        elif (self._commTokens[1].find(':') > 0):
            # copy app:/tmp/blah /tmp/
            myError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False
        elif (self._commString.find(',') == -1):
            # copy /tmp/blah.txt app:/tmp/
            myCopyTarget = 'single_server_group'
        else:
            # copy /tmp/blah.txt app,www:/tmp/
            myCopyTarget = 'multiple_server_group'

        #
        # Step 3: Assemble two lists based on command syntax.
        #
        # myServerNameList will contain a list of server names.
        # -or-
        # myServerGroupList will contain a list of server groups.
        #
        if (myCopyTarget == 'current_server_group'):
            # copy /tmp/blah /tmp/
            myGroupStr = self._globalConfig.getCurrentServerGroup().getName()

            # Validate remote path.
            if (myRemotePath[len(myRemotePath) - 1] != '/'):
                myError = "ERROR: Remote path '" + myRemotePath + \
                            "' must end with a slash."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False

            myServerGroupList.append(myGroupStr)

        elif (myCopyTarget == 'single_server_group'):
            # copy /tmp/blah app:/tmp/
            myGroupStr = self._commTokens[2]
            myGroupStr = myGroupStr[:myGroupStr.find(':')]
            myRemotePath = self._commTokens[2]
            myRemotePath = myRemotePath[myRemotePath.find(':') + 1:]

            # Validate remote path.
            if (myRemotePath[len(myRemotePath) - 1] != '/'):
                myError = "ERROR: Remote path '" + myRemotePath + \
                            "' must end with a slash."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False

            # Check for server name match.
            myServer = self._globalConfig.getServerByName(myGroupStr)

            if (myServer):
                myServerNameList.append(myServer.getName())
            else:
                # Check for server group match.
                myServerGroup = self._globalConfig.getServerGroupByName(myGroupStr)
                # Validate.
                if (myServerGroup == False):
                    myError = "ERROR: No matching server name or group '" + \
                                myGroupStr + "'."
                    self._globalConfig.getMultiLogger().LogMsgError(myError)
                    return False
                else:
                    myServerGroupList.append(myGroupStr)
        elif (myCopyTarget == 'multiple_server_group'):
            # copy /tmp/blah app,www:/tmp/
            myGroupStr = self._commTokens[2]
            myGroupStr = myGroupStr[:myGroupStr.find(':')]
            myGroupList = myGroupStr.split(',')
            myRemotePath = self._commTokens[2]
            myRemotePath = myRemotePath[myRemotePath.find(':') + 1:]

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
        # Step 4: Make sure noone's trying to mix
        #         server hostnames and server group names together.
        #
        if ( (len(myServerNameList) > 0) & (len(myServerGroupList) > 0) ):
            myError = "ERROR: Mixing of server name(s) and server group(s) is unsupported."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        #
        # Step 5: Must make sure...are you sure you're sure?
        #
        if (self._globalConfig.isBatchMode() == False):
            myDisplayStr = ''

            if ( len(myServerNameList) > 0):
                for myNameStr in myServerNameList:
                    myDisplayStr = myDisplayStr + myNameStr + ','

                myDisplayStr = myDisplayStr.rstrip(',')

                # Are you sure?
                print("Copy local file '" + myLocalPath + \
                      "' to remote directory '" + myRemotePath + "'")
                print("on server(s) " + myDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    myInfo = "INFO:  Aborting command."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                    return False
            else:
                for myGroupStr in myServerGroupList:
                    myDisplayStr = myDisplayStr + myGroupStr + ','

                myDisplayStr = myDisplayStr.rstrip(',')

                # Are you sure?
                print("Copy local file '" + myLocalPath + \
                      "' to remote directory '" + myRemotePath + "'")
                print("on server group(s) " + myDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    myInfo = "INFO:  Aborting command."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                    return False

        #
        # Step 6: If we found server name(s), then run with that.
        #         Otherwise, do the same with the server group(s) given.
        #
        if ( len(myServerNameList) > 0 ):
            try:
                for myNameStr in myServerNameList:
                    myServer = self._globalConfig.getServerByName(myNameStr)
                    myPinger = engine.misc.HostPinger.HostPinger(self._globalConfig)

                    if (myPinger.ping(myNameStr) == 0):
                        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)

                        # Build It.
                        if ( myServer.getVersion() != None ):
                            myExternalCommand.setCommand( \
                                self._globalConfig.getScpBinary() + " " + \
                                "-oProtocol=" + myServer.getVersion() + " " + \
                                myLocalPath + " " + \
                                myServer.getUsername() + "@" + \
                                myServer.getName() + ":" + \
                                myRemotePath )
                        else:
                            myExternalCommand.setCommand( \
                                self._globalConfig.getScpBinary() + " " + \
                                myLocalPath + " " + \
                                myServer.getUsername() + "@" + \
                                myServer.getName() + ":" + \
                                myRemotePath )

                        # Run It.
                        if ( self._globalConfig.isBatchMode() ):
                            myExternalCommand.runBatch()
                        else:
                            myExternalCommand.runConsole(True)
                        myCommandCount = myCommandCount + 1
                    else:
                        myError = "ERROR: Server '" + myServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self._globalConfig.getMultiLogger().LogMsgError(myError)
                        if (self._globalConfig.isQuietMode() == False):
                            print( self._globalConfig.getSeperator() )

            except EOFError:
                pass
            except KeyboardInterrupt:
                myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
        else:
            #
            # Server group version of the above.
            #
            for myGroupStr in myServerGroupList:
                myServerGroup = self._globalConfig.getServerGroupByName(
                    myGroupStr)
                myServerList = myServerGroup.getServerList()

                try:
                    for myServer in myServerList:
                        myPinger = engine.misc.HostPinger.HostPinger(self._globalConfig)

                        if (myPinger.ping(myServer.getName()) == 0):
                            myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)

                            # Build It.
                            if ( myServer.getVersion() != None ):
                                myExternalCommand.setCommand( \
                                self._globalConfig.getScpBinary() + " " + \
                                myLocalPath + " " + \
                                myServer.getUsername() + "@" + \
                                myServer.getName() + ":" + \
                                myRemotePath )
                            else:
                                myExternalCommand.setCommand( \
                                self._globalConfig.getScpBinary() + " " + \
                                "-oProtocol=" + myServer.getVersion() + " " + \
                                myLocalPath + " " + \
                                myServer.getUsername() + "@" + \
                                myServer.getName() + ":" + \
                                myRemotePath )

                            # Run It.
                            if ( self._globalConfig.isBatchMode() ):
                                myExternalCommand.runBatch()
                            else:
                                myExternalCommand.runConsole(True)
                            myCommandCount = myCommandCount + 1
                        else:
                            myError = "ERROR: Server '" + myServer.getName() + \
                                        "' appears to be down.  Continuing..."
                            self._globalConfig.getMultiLogger().LogMsgError(myError)
                            if (self._globalConfig.isQuietMode() == False):
                                print( self._globalConfig.getSeperator() )

                except EOFError:
                    pass
                except KeyboardInterrupt:
                    myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return myCommandCount

######################################################################
