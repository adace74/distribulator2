######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
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
import sys

# Custom modules
import engine.data.ExternalCommand
import generic.FilePrinter
import generic.HostPinger

######################################################################

class CommandRunner:
    """
    This class is responsible for doing the actual work of
    expanding a given distribulator command into a set of 
    SSH commands and running them.
    """

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def run(self, PassedInternalCommand):
        """This method is the main entry point into the expansion engine."""

        self._commString = PassedInternalCommand.getCommand()

        # Verify there's something to process.
        if (len(self._commString) == 0):
             return False

        self._commTokens = self._commString.split()
        myCommandCount = 0

        if (self._commTokens[0] != 'cd'):
            # Log it.
            self._globalConfig.getSysLogger().LogMsgInfo("CMD:   " + \
                                                         self._commString)
            # If we're not being quiet, print it.
            if ( self._globalConfig.isQuietMode() == False ):
                print("CMD:   " + self._commString)

        # Cheezy branching logic.  Works well, though.
        if (self._commTokens[0] == 'cd'):
            myCommandCount = self.doChdir()
        elif (self._commTokens[0] == 'copy'):
            myCommandCount = self.doCopy()
        elif (self._commTokens[0] == 'exit'):
            myCommandCount = self.doExit()
        elif (self._commTokens[0] == 'help'):
            myCommandCount = self.doHelp()
        elif (self._commTokens[0] == 'login'):
            myCommandCount = self.doLogin()
        elif (self._commTokens[0] == 'run'):
            myCommandCount = self.doRun()
        elif (self._commTokens[0] == 'server-group'):
            myCommandCount = self.doServerGroup()
        elif (self._commTokens[0] == 'server-list'):
            myCommandCount = self.doServerList()
        else:
            myError = "ERROR: Unknown Command: '" + \
                            self._commTokens[0] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        return myCommandCount

######################################################################

    def doAreYouSure(self):
        """This method simply asks the never-ending question: Are You Sure?"""

        try:
            sys.stdout.write("Yes / No> ")
            myInput = sys.stdin.readline()
            myInput = myInput.strip()

        except (EOFError, KeyboardInterrupt):
            myInfo = "INFO:  Caught CTRL-C / CTRL-D keystroke."
            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
            return False

        if (myInput.lower() == 'yes'):
            return True
        else:
            return False

######################################################################

    def doChdir(self):
        """This method is responsible for the processing of the 'cd' command."""

        # If the user just types 'cd', do what most shells would do.
        if (len(self._commTokens) == 1):
            myDirStr = os.environ.get('HOME')
        else:
            myDirStr = self._commTokens[1]

        try:
            if (self._commTokens[0] == 'cd'):
                os.chdir(myDirStr)

        except OSError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                      self._commTokens[1])
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        return True

######################################################################

    def doCopy(self):
        """This method is responsible for the processing of the 'copy' command."""

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
                    myPinger = generic.HostPinger.HostPinger(
                        self._globalConfig.getPingBinary() )

                    if (myPinger.ping(myNameStr) == 0):
                        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
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
                        myError = "ERROR: Server '" + \
                                    myServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self._globalConfig.getMultiLogger().LogMsgError(myError)

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
                        myPinger = generic.HostPinger.HostPinger(
                            self._globalConfig.getPingBinary() )

                        if (myPinger.ping(myServer.getName()) == 0):
                            myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
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
                            myError = "ERROR: Server '" + \
                                        myServer.getName() + \
                                        "' appears to be down.  Continuing..."
                            self._globalConfig.getMultiLogger().LogMsgError(myError)

                except EOFError:
                    pass
                except KeyboardInterrupt:
                    myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return myCommandCount

######################################################################

    def doExit(self):
        """This method is responsible for the processing of the 'exit' command."""

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        myInfo = "INFO:  Received exit command.  Wrote history.  Dying..."

        self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return True

######################################################################

    def doHelp(self):
        """This method is responsible for the processing of the 'help' command."""

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        if ( len(self._commTokens) > 1 ):
            myFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        self._commTokens[1] + '-desc.txt')
        else:
            myFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        'help.txt')

        myFilePrinter = generic.FilePrinter.FilePrinter()

        if (myFilePrinter.printFile(myFileName) == False):
            myError = "ERROR: Cannot find help for specified command '" + \
                        self._commTokens[1] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        return True

######################################################################

    def doLogin(self):
        """This method is responsible for the processing of the 'login' command."""

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # Check for server name.
        if ( len(self._commTokens) > 1):
            if ( self._globalConfig.getServerByName(self._commTokens[1]) ):
                myServer = self._globalConfig.getServerByName(self._commTokens[1])
            else:
                myError = "ERROR: No matching server '" + \
                            self._commTokens[1] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
        else:
            myError = "ERROR: No server name given."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # Run the expanded shell command.
        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
        myExternalCommand.setCommand( \
            self._globalConfig.getSshBinary() + " -l " + \
            myServer.getUsername() + " " + myServer.getName() )
        try:
            myExternalCommand.runConsole(True)
        except (EOFError, KeyboardInterrupt):
            myInfo = "INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt..."
            self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

        return True

######################################################################

    def doRun(self):
        """This method is responsible for the processing of the 'run' command."""

        myCommandCount = 0
        myServerGroupList = []
        myServerNameList = []
        myRunTarget = '';

        #
        # Step 1:  Create our own tokens, and check for SSH flags and
        #          the 'reverse' keyword.
        #
        if ( self._commString.find('"') == -1 ):
            myError = "ERROR: Command Syntax Error.  Try 'help run' for more information."
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

        # Check for the 'reverse' keyword.
        if (mySuffixStr.find(' reverse') != -1):
            isReverse = True
            mySuffixStr = mySuffixStr[:mySuffixStr.find(' reverse')]
        else:
            isReverse = False

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
            myError = "ERROR: Command Syntax Error.  Try 'help run' for more information."
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
        #
        elif (myRunTarget == 'multiple_server_group'):
            myGroupList = myGroupStr.split(',')

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
        # server hostnames and server group names together.
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
                print("Run command " + myBodyStr + " on server(s) " + \
                      myDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    myInfo = "INFO:  Aborting command."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)
                    return False
            else:
                for myGroupStr in myServerGroupList:
                    myDisplayStr = myDisplayStr + myGroupStr + ','

                myDisplayStr = myDisplayStr.rstrip(',')

                # Are you sure?
                print("Run command " + myBodyStr + " on server group(s) " + \
                      myDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    myInfo = "INFO:  Aborting command."
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
            if (isReverse):
                myServerNameList.reverse()

            try:
                for myNameStr in myServerNameList:
                    myServer = self._globalConfig.getServerByName(myNameStr)
                    myPinger = generic.HostPinger.HostPinger(
                        self._globalConfig.getPingBinary() )

                    if (myPinger.ping(myNameStr) == 0):
                        myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                        myExternalCommand.setCommand( \
                            self._globalConfig.getSshBinary() + myFlagStr + \
                            " -l " + myServer.getUsername() + " " + \
                            myServer.getName() + " " + \
                            myBodyStr )
                        # Run It.
                        if ( self._globalConfig.isBatchMode() ):
                            myExternalCommand.runBatch()
                        else:
                            myExternalCommand.runConsole(True)
                        myCommandCount = myCommandCount + 1
                    else:
                        myError = "ERROR: Server '" + \
                                    myServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self._globalConfig.getMultiLogger().LogMsgError(myError)

            except EOFError:
                pass
            except KeyboardInterrupt:
                myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

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
                myServerGroup = self._globalConfig.getServerGroupByName(
                    myGroupStr)

                myServerList = myServerGroup.getServerList()

                if (isReverse):
                    myServerList.reverse()

                try:
                    for myServer in myServerList:
                        myPinger = generic.HostPinger.HostPinger(
                            self._globalConfig.getPingBinary() )

                        if (myPinger.ping(myServer.getName()) == 0):
                            myExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                            myExternalCommand.setCommand( \
                            self._globalConfig.getSshBinary() + myFlagStr + \
                            " -l " + myServer.getUsername() + " " + \
                            myServer.getName() + " " + \
                            myBodyStr )
                            # Run It.
                            if ( self._globalConfig.isBatchMode() ):
                                myExternalCommand.runBatch()
                            else:
                                myExternalCommand.runConsole(True)
                            myCommandCount = myCommandCount + 1
                        else:
                            myError = "ERROR: Server '" + \
                                        myServer.getName() + \
                                        "' appears to be down.  Continuing..."
                            self._globalConfig.getMultiLogger().LogMsgError(myError)

                except EOFError:
                    pass
                except KeyboardInterrupt:
                    myInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                    self._globalConfig.getMultiLogger().LogMsgInfo(myInfo)

                if (isReverse):
                    myServerList.sort()

            return myCommandCount

######################################################################

    def doServerGroup(self):
        """This method is responsible for the processing of the 'server-group' command."""

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a group name, set it.
        if ( len(self._commTokens) > 1 ):
            myServerGroup = self._globalConfig.getServerGroupByName( self._commTokens[1] )

            if (myServerGroup == False):
                myError = "ERROR: No matching server group '" + \
                            self._commTokens[1] + "'."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                return False
            else:
                self._globalConfig.setCurrentServerGroup(myServerGroup)
                print("INFO:  Current server group is now '" + self._commTokens[1] + "'.")
                return True
        else:
            # Otherwise, display the server group list given at startup.
            myServerGroupStr = "Known server groups for environment '" + \
                                 self._globalConfig.getServerEnv() + "'\n"
            myServerGroupStr = myServerGroupStr + \
                                 "--------------------------------------------------\n"
            myTotalServerCount = 0
            myColumnCount = 0

            for myServerGroup in self._globalConfig.getServerGroupList():
                myColumnCount = myColumnCount + 1
                myTotalServerCount = myTotalServerCount + \
                                       myServerGroup.getServerCount()
                myServerGroupStr = myServerGroupStr + '%10s (%2d) ' % \
                                     (myServerGroup.getName(), myServerGroup.getServerCount())

                if (myColumnCount == 4):
                    myColumnCount = 0
                    myServerGroupStr = myServerGroupStr + '\n'

            print(myServerGroupStr)

            return True

######################################################################

    def doServerList(self):
        """This method is responsible for the processing of the 'server-list' command."""

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            myError = "ERROR: Invalid command for batch mode."
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            return False

        # If given a server group name, display servers in that group.
        if ( len(self._commTokens) > 1 ):
            myServerGroup = self._globalConfig.getServerGroupByName( \
                self._commTokens[1] )
        else:
            # Otherwise, display servers in the current working server group.
            myServerGroup = self._globalConfig.getCurrentServerGroup()

        # Check for errors.
        if (myServerGroup == False):
            myError = "ERROR: No matching server group '" + \
                        self._commTokens[1] + "'."
            self._globalConfig.getMultiLogger().LogMsgError(myError)

            return False
        else:
            print("Known servers for group '" + myServerGroup.getName() + "'")
            print("--------------------------------------------------")
            # Actual server list goes here.
            myTempStr = ''

            for myServer in myServerGroup.getServerList():
                if ( len(myTempStr) > 0 ):
                    print (myTempStr + "\t" + myServer.getName())
                    myTempStr = ''
                else:
                    myTempStr = myServer.getName()

            if ( len(myTempStr) > 0 ):
                print(myTempStr)

            return True

######################################################################
