######################################################################
#
# $Id$
#
# Name: CommandRunner.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
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
import engine.data.ExternalCommand
import generic.FilePrinter
import generic.HostPinger

######################################################################

class CommandRunner:
    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig

######################################################################

    def handleError(self, PassedError):
        if ( self._globalConfig.isQuietMode() ):
            self._globalConfig.getSysLogger().LogMsgError(
                PassedError)
        else:
            print(PassedError)
            self._globalConfig.getSysLogger().LogMsgError(
                PassedError)

######################################################################

    def handleInfo(self, PassedInfo):
        if ( self._globalConfig.isQuietMode() ):
            self._globalConfig.getSysLogger().LogMsgInfo(
                PassedInfo)
        else:
            print(PassedInfo)
            self._globalConfig.getSysLogger().LogMsgInfo(
                PassedInfo)

######################################################################

    def run(self, PassedInternalCommand):
        self._commString = PassedInternalCommand.getCommand()
        self._commTokens = self._commString.split()
        thisCommandCount = 0

        if (self._commTokens[0] != 'cd'):
            # Log it.
            self._globalConfig.getSysLogger().LogMsgInfo("CMD:   " + \
                                                         self._commString)
            # If we're not being quiet, print it.
            if ( self._globalConfig.isQuietMode() == False ):
                print("CMD:   " + self._commString)

        # Cheezy branching logic.  Works well, though.
        if (self._commTokens[0] == 'cd'):
            thisCommandCount = self.doChdir()
        elif (self._commTokens[0] == 'copy'):
            thisCommandCount = self.doCopy()
        elif (self._commTokens[0] == 'exit'):
            thisCommandCount = self.doExit()
        elif (self._commTokens[0] == 'help'):
            thisCommandCount = self.doHelp()
        elif (self._commTokens[0] == 'login'):
            thisCommandCount = self.doLogin()
        elif (self._commTokens[0] == 'run'):
            thisCommandCount = self.doRun()
        elif (self._commTokens[0] == 'server-group'):
            thisCommandCount = self.doServerGroup()
        elif (self._commTokens[0] == 'server-list'):
            thisCommandCount = self.doServerList()
        else:
            thisError = "ERROR: Unknown Command: '" + \
                            self._commTokens[0] + "'."
            self.handleError(thisError)
            return False

        return thisCommandCount

######################################################################

    def doAreYouSure(self):
        try:
            sys.stdout.write("Yes / No> ")
            thisInput = sys.stdin.readline()
            thisInput = thisInput.strip()

        except (EOFError, KeyboardInterrupt):
            thisInfo = "INFO:  Caught CTRL-C / CTRL-D keystroke."
            self.handleInfo(thisInfo)
            return False

        if (thisInput.lower() == 'yes'):
            return True
        else:
            return False

######################################################################

    def doChdir(self):
        # If the user just types 'cd', do what most shells would do.
        if (len(self._commTokens) == 1):
            thisDirStr = os.environ.get('HOME')
        else:
            thisDirStr = self._commTokens[1]

        try:
            if (self._commTokens[0] == 'cd'):
                os.chdir(thisDirStr)

        except OSError, (errno, strerror):
            thisError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                      self._commTokens[1])
            self.handleError(thisError)
            return False

        return True

######################################################################

    def doCopy(self):
        thisCommandCount = 0
        thisCopyTarget = '';
        thisServerGroupList = []
        thisServerNameList = []

        #
        # Step 1: Common validation and variable-setting.
        #
        # Validate token count.
        if (len(self._commTokens) < 3):
            thisError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self.handleError(thisError)
            return False
        elif (self._commTokens[2].find('/') == -1):
            thisError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self.handleError(thisError)
            return False            
        if (self._commString.find(' reverse') > 0):
            thisError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self.handleError(thisError)
            return False
        else:
            thisLocalPath = self._commTokens[1]
            thisRemotePath = self._commTokens[2]

        # Validate local file.
        try:
            if ( stat.S_ISREG(os.stat(
                thisLocalPath)[stat.ST_MODE]) == False):
                thisError = "ERROR: File '" + thisLocalPath + \
                            "' is accessible, but not regular."
                self.handleError(thisError)
                return False
        except OSError, (errno, strerror):
            thisError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                      thisLocalPath)
            self.handleError(thisError)
            return False

        #
        # Step 2: Try to determine what the target of the command is,
        #         and set a state-tracking variable accordingly.
        # 
        if (self._commString.find(':') == -1):
            # copy /tmp/blah /tmp/
            thisCopyTarget = 'current_server_group'
        elif (self._commTokens[1].find(':') > 0):
            # copy app:/tmp/blah /tmp/
            thisError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self.handleError(thisError)
            return False
        elif (self._commString.find(',') == -1):
            # copy /tmp/blah.txt app:/tmp/
            thisCopyTarget = 'single_server_group'
        else:
            # copy /tmp/blah.txt app,www:/tmp/
            thisCopyTarget = 'multiple_server_group'

        #
        # Step 3: Assemble two lists based on command syntax.
        #
        # thisServerNameList will contain a list of server names.
        # -or-
        # thisServerGroupList will contain a list of server groups.
        #
        if (thisCopyTarget == 'current_server_group'):
            # copy /tmp/blah /tmp/
            thisGroupStr = self._globalConfig.getCurrentServerGroup().getName()

            # Validate remote path.
            if (thisRemotePath[len(thisRemotePath) - 1] != '/'):
                thisError = "ERROR: Remote path '" + thisRemotePath + \
                            "' must end with a slash."
                self.handleError(thisError)
                return False

            thisServerGroupList.append(thisGroupStr)

        elif (thisCopyTarget == 'single_server_group'):
            # copy /tmp/blah app:/tmp/
            thisGroupStr = self._commTokens[2]
            thisGroupStr = thisGroupStr[:thisGroupStr.find(':')]
            thisRemotePath = self._commTokens[2]
            thisRemotePath = thisRemotePath[thisRemotePath.find(':') + 1:]

            # Validate remote path.
            if (thisRemotePath[len(thisRemotePath) - 1] != '/'):
                thisError = "ERROR: Remote path '" + thisRemotePath + \
                            "' must end with a slash."
                self.handleError(thisError)
                return False

            # Check for server name match.
            thisServer = self._globalConfig.getServerByName(thisGroupStr)

            if (thisServer):
                thisServerNameList.append(thisServer.getName())
            else:
                # Check for server group match.
                thisServerGroup = self._globalConfig.getServerGroupByName(thisGroupStr)
                # Validate.
                if (thisServerGroup == False):
                    thisError = "ERROR: No matching server name or group '" + \
                                thisGroupStr + "'."
                    self.handleError(thisError)
                    return False
                else:
                    thisServerGroupList.append(thisGroupStr)
        elif (thisCopyTarget == 'multiple_server_group'):
            # copy /tmp/blah app,www:/tmp/
            thisGroupStr = self._commTokens[2]
            thisGroupStr = thisGroupStr[:thisGroupStr.find(':')]
            thisGroupList = thisGroupStr.split(',')
            thisRemotePath = self._commTokens[2]
            thisRemotePath = thisRemotePath[thisRemotePath.find(':') + 1:]

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
                    self.handleError(thisError)
                    return False

        #
        # Step 4: Make sure noone's trying to mix
        #         server hostnames and server group names together.
        #
        if ( (len(thisServerNameList) > 0) & (len(thisServerGroupList) > 0) ):
            thisError = "ERROR: Mixing of server name(s) and server group(s) is unsupported."
            self.handleError(thisError)
            return False

        #
        # Step 5: Must make sure...are you sure you're sure?
        #
        if (self._globalConfig.isBatchMode() == False):
            thisDisplayStr = ''

            if ( len(thisServerNameList) > 0):
                for thisNameStr in thisServerNameList:
                    thisDisplayStr = thisDisplayStr + thisNameStr + ','

                thisDisplayStr = thisDisplayStr.rstrip(',')

                # Are you sure?
                print("Copy local file '" + thisLocalPath + \
                      "' to remote directory '" + thisRemotePath + "'")
                print("on server(s) " + thisDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    thisInfo = "INFO:  Aborting command."
                    self.handleInfo(thisInfo)
                    return False
            else:
                for thisGroupStr in thisServerGroupList:
                    thisDisplayStr = thisDisplayStr + thisGroupStr + ','

                thisDisplayStr = thisDisplayStr.rstrip(',')

                # Are you sure?
                print("Copy local file '" + thisLocalPath + \
                      "' to remote directory '" + thisRemotePath + "'")
                print("on server group(s) " + thisDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    thisInfo = "INFO:  Aborting command."
                    self.handleInfo(thisInfo)
                    return False

        #
        # Step 6: If we found server name(s), then run with that.
        #         Otherwise, do the same with the server group(s) given.
        #
        if ( len(thisServerNameList) > 0 ):
            try:
                for thisNameStr in thisServerNameList:
                    thisServer = self._globalConfig.getServerByName(thisNameStr)
                    thisPinger = generic.HostPinger.HostPinger(
                        self._globalConfig.getPingBinary() )

                    if (thisPinger.ping(thisNameStr) == 0):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                        thisExternalCommand.setCommand( \
                            self._globalConfig.getScpBinary() + " " + \
                            thisLocalPath + " " + \
                            thisServer.getUsername() + "@" + \
                            thisServer.getName() + ":" + \
                            thisRemotePath )
                        # Run It.
                        if ( self._globalConfig.isBatchMode() ):
                            thisExternalCommand.runAtomic()
                        else:
                            thisExternalCommand.run(True)
                        thisCommandCount = thisCommandCount + 1
                    else:
                        thisError = "ERROR: Server '" + \
                                    thisServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self.handleError(thisError)

            except EOFError:
                pass
            except KeyboardInterrupt:
                thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                self.handleInfo(thisInfo)
        else:
            #
            # Server group version of the above.
            #
            for thisGroupStr in thisServerGroupList:
                thisServerGroup = self._globalConfig.getServerGroupByName(
                    thisGroupStr)
                thisServerList = thisServerGroup.getServerList()

                try:
                    for thisServer in thisServerList:
                        thisPinger = generic.HostPinger.HostPinger(
                            self._globalConfig.getPingBinary() )

                        if (thisPinger.ping(thisServer.getName()) == 0):
                            thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                            thisExternalCommand.setCommand( \
                            self._globalConfig.getScpBinary() + " " + \
                            thisLocalPath + " " + \
                            thisServer.getUsername() + "@" + \
                            thisServer.getName() + ":" + \
                            thisRemotePath )
                            # Run It.
                            if ( self._globalConfig.isBatchMode() ):
                                thisExternalCommand.runAtomic()
                            else:
                                thisExternalCommand.run(True)
                            thisCommandCount = thisCommandCount + 1
                        else:
                            thisError = "ERROR: Server '" + \
                                        thisServer.getName() + \
                                        "' appears to be down.  Continuing..."
                            self.handleError(thisError)

                except EOFError:
                    pass
                except KeyboardInterrupt:
                    thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                    self.handleInfo(thisInfo)

        return thisCommandCount

######################################################################

    def doExit(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        thisInfo = "INFO:  Received exit command.  Wrote history.  Dying..."

        self.handleInfo(thisInfo)

        return True

######################################################################

    def doHelp(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        if ( len(self._commTokens) > 1 ):
            thisFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        self._commTokens[1] + '-desc.txt')
        else:
            thisFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        'help.txt')

        thisFilePrinter = generic.FilePrinter.FilePrinter()

        if (thisFilePrinter.printFile(thisFileName) == False):
            thisError = "ERROR: Cannot find help for specified command '" + \
                        self._commTokens[1] + "'."
            self.handleError(thisError)
            return False

        return True

######################################################################

    def doLogin(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        # Check for server name.
        if ( len(self._commTokens) > 1):
            if ( self._globalConfig.getServerByName(self._commTokens[1]) ):
                thisServer = self._globalConfig.getServerByName(self._commTokens[1])
            else:
                thisError = "ERROR: No matching server '" + \
                            self._commTokens[1] + "'."
                self.handleError(thisError)
                return False
        else:
            thisError = "ERROR: No server name given."
            self.handleError(thisError)
            return False

        # Run the expanded shell command.
        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
        thisExternalCommand.setCommand( \
            self._globalConfig.getSshBinary() + " -l " + \
            thisServer.getUsername() + " " + thisServer.getName() )
        try:
            thisExternalCommand.run(True)
        except (EOFError, KeyboardInterrupt):
            thisInfo = "INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt..."
            self.handleInfo(thisInfo)

        return True

######################################################################

    def doRun(self):
        thisCommandCount = 0
        thisServerGroupList = []
        thisServerNameList = []
        thisRunTarget = '';

        #
        # Step 1:  Create our own tokens, and check for SSH flags and
        #          the 'reverse' keyword.
        #
        if ( self._commString.find('"') == -1 ):
            thisError = "ERROR: Command Syntax Error.  Try 'help run' for more information."
            self.handleError(thisError)
            return False

        # Get substr indexes.
        thisFirstQuoteIndex = self._commString.find('"')
        thisLastQuoteIndex = self._commString.rfind('"')
        thisPrefixStr = self._commString[0:thisFirstQuoteIndex]
        thisBodyStr = self._commString[thisFirstQuoteIndex:(thisLastQuoteIndex + 1)]
        thisSuffixStr = self._commString[thisLastQuoteIndex + 1:]

        # Check for pass-through SSH flags
        if (thisPrefixStr.find('-') != -1):
            thisFlagStr = ' ' + thisPrefixStr[thisPrefixStr.find('-'):]
            thisFlagStr = thisFlagStr.rstrip()
        else:
            thisFlagStr = ''

        # Check for the 'reverse' keyword.
        if (thisSuffixStr.find(' reverse') != -1):
            isReverse = True
            thisSuffixStr = thisSuffixStr[:thisSuffixStr.find(' reverse')]
        else:
            isReverse = False

        #
        # Step 2: Try to determine what the target of the command is
        #         and set a state-tracking variable accordingly.
        # 
        if (len(thisSuffixStr) == 0):
            # run "uptime"
            # run -t "uptime"
            thisRunTarget = 'current_server_group';
        # Check for syntax errors.
        elif (thisSuffixStr.find(' on ') == -1):
            thisError = "ERROR: Command Syntax Error.  Try 'help run' for more information."
            self.handleError(thisError)
            return False
        elif (thisSuffixStr.find(',') == -1):
            # run "uptime" on app
            # run -t "uptime" on app
            # run "uptime" on app01
            # run -t "uptime" on app01
            thisRunTarget = 'single_server_group';
        else:
            # run "uptime" on app, www
            # run -t "uptime" on app, www
            # run "uptime" on app01, www01
            # run -t "uptime" on app01, www01
            thisRunTarget = 'multiple_server_group';

        # Assuming no error up until this point we can now
        # throw out the " on " part of our command.
        thisGroupStr = thisSuffixStr[thisSuffixStr.find(' on ') + 4:]
        thisGroupStr = thisGroupStr.strip()

        #
        # Step 3: Assemble two lists based on command syntax.
        #
        # thisServerNameList will contain a list of server names.
        # -or-
        # thisServerGroupList will contain a list of server groups.
        #
        if (thisRunTarget == 'current_server_group'):
            thisGroupStr = self._globalConfig.getCurrentServerGroup().getName()
            thisServerGroupList.append(thisGroupStr)
        #
        elif (thisRunTarget == 'single_server_group'):
            # Check for server name match.
            thisServer = self._globalConfig.getServerByName(thisGroupStr)

            if (thisServer):
                thisServerNameList.append(thisServer.getName())
            else:
                # Check for server group match.
                thisServerGroup = self._globalConfig.getServerGroupByName(thisGroupStr)
                # Validate.
                if (thisServerGroup == False):
                    thisError = "ERROR: No matching server name or group '" + \
                                thisGroupStr + "'."
                    self.handleError(thisError)
                    return False
                else:
                    thisServerGroupList.append(thisGroupStr)
        #
        elif (thisRunTarget == 'multiple_server_group'):
            thisGroupList = thisGroupStr.split(',')

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
                    self.handleError(thisError)
                    return False

        #
        # Step 4: Make sure noone's trying to mix
        # server hostnames and server group names together.
        #
        if ( (len(thisServerNameList) > 0) & (len(thisServerGroupList) > 0) ):
            thisError = "ERROR: Mixing of server name(s) and server group(s) is unsupported."
            self.handleError(thisError)
            return False

        #
        # Step 5: Must make sure...are you sure you're sure?
        #
        if (self._globalConfig.isBatchMode() == False):
            thisDisplayStr = ''

            if ( len(thisServerNameList) > 0):
                for thisNameStr in thisServerNameList:
                    thisDisplayStr = thisDisplayStr + thisNameStr + ','

                thisDisplayStr = thisDisplayStr.rstrip(',')

                # Are you sure?
                print("Run command " + thisBodyStr + " on server(s) " + \
                      thisDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    thisInfo = "INFO:  Aborting command."
                    self.handleInfo(thisInfo)
                    return False
            else:
                for thisGroupStr in thisServerGroupList:
                    thisDisplayStr = thisDisplayStr + thisGroupStr + ','

                thisDisplayStr = thisDisplayStr.rstrip(',')

                # Are you sure?
                print("Run command " + thisBodyStr + " on server group(s) " + \
                      thisDisplayStr + "?")

                if (self.doAreYouSure() == False):
                    thisInfo = "INFO:  Aborting command."
                    self.handleInfo(thisInfo)
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
        if ( len(thisServerNameList) > 0 ):
            if (isReverse):
                thisServerNameList.reverse()

            try:
                for thisNameStr in thisServerNameList:
                    thisServer = self._globalConfig.getServerByName(thisNameStr)
                    thisPinger = generic.HostPinger.HostPinger(
                        self._globalConfig.getPingBinary() )

                    if (thisPinger.ping(thisNameStr) == 0):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                        thisExternalCommand.setCommand( \
                            self._globalConfig.getSshBinary() + thisFlagStr + \
                            " -l " + thisServer.getUsername() + " " + \
                            thisServer.getName() + " " + \
                            thisBodyStr )
                        # Run It.
                        if ( self._globalConfig.isBatchMode() ):
                            thisExternalCommand.runAtomic()
                        else:
                            thisExternalCommand.run(True)
                        thisCommandCount = thisCommandCount + 1
                    else:
                        thisError = "ERROR: Server '" + \
                                    thisServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self.handleError(thisError)

            except EOFError:
                pass
            except KeyboardInterrupt:
                thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                self.handleInfo(thisInfo)

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
            for thisGroupStr in thisServerGroupList:
                thisServerGroup = self._globalConfig.getServerGroupByName(
                    thisGroupStr)

                thisServerList = thisServerGroup.getServerList()

                if (isReverse):
                    thisServerList.reverse()

                try:
                    for thisServer in thisServerList:
                        thisPinger = generic.HostPinger.HostPinger(
                            self._globalConfig.getPingBinary() )

                        if (thisPinger.ping(thisServer.getName()) == 0):
                            thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                            thisExternalCommand.setCommand( \
                            self._globalConfig.getSshBinary() + thisFlagStr + \
                            " -l " + thisServer.getUsername() + " " + \
                            thisServer.getName() + " " + \
                            thisBodyStr )
                            # Run It.
                            if ( self._globalConfig.isBatchMode() ):
                                thisExternalCommand.runAtomic()
                            else:
                                thisExternalCommand.run(True)
                            thisCommandCount = thisCommandCount + 1
                        else:
                            thisError = "ERROR: Server '" + \
                                        thisServer.getName() + \
                                        "' appears to be down.  Continuing..."
                            self.handleError(thisError)

                except EOFError:
                    pass
                except KeyboardInterrupt:
                    thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                    self.handleInfo(thisInfo)

                if (isReverse):
                    thisServerList.sort()

            return thisCommandCount

######################################################################

    def doServerGroup(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        # If given a group name, set it.
        if ( len(self._commTokens) > 1 ):
            thisServerGroup = self._globalConfig.getServerGroupByName( self._commTokens[1] )

            if (thisServerGroup == False):
                thisError = "ERROR: No matching server group '" + \
                            self._commTokens[1] + "'."
                self.handleError(thisError)
                return False
            else:
                self._globalConfig.setCurrentServerGroup(thisServerGroup)
                print("INFO:  Current server group is now '" + self._commTokens[1] + "'.")
                return True
        else:
            # Otherwise, display the server group list given at startup.
            thisServerGroupStr = "Known server groups for environment '" + \
                                 self._globalConfig.getServerEnv() + "'\n"
            thisServerGroupStr = thisServerGroupStr + \
                                 "--------------------------------------------------\n"
            thisTotalServerCount = 0
            thisColumnCount = 0

            for thisServerGroup in self._globalConfig.getServerGroupList():
                thisColumnCount = thisColumnCount + 1
                thisTotalServerCount = thisTotalServerCount + \
                                       thisServerGroup.getServerCount()
                thisServerGroupStr = thisServerGroupStr + '%10s (%2d) ' % \
                                     (thisServerGroup.getName(), thisServerGroup.getServerCount())

                if (thisColumnCount == 4):
                    thisColumnCount = 0
                    thisServerGroupStr = thisServerGroupStr + '\n'

            print(thisServerGroupStr)

            return True

######################################################################

    def doServerList(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        # If given a server group name, display servers in that group.
        if ( len(self._commTokens) > 1 ):
            thisServerGroup = self._globalConfig.getServerGroupByName( \
                self._commTokens[1] )
        else:
            # Otherwise, display servers in the current working server group.
            thisServerGroup = self._globalConfig.getCurrentServerGroup()

        # Check for errors.
        if (thisServerGroup == False):
            thisError = "ERROR: No matching server group '" + \
                        self._commTokens[1] + "'."
            self.handleError(thisError)

            return False
        else:
            print("Known servers for group '" + thisServerGroup.getName() + "'")
            print("--------------------------------------------------")
            # Actual server list goes here.
            thisTempStr = ''

            for thisServer in thisServerGroup.getServerList():
                if ( len(thisTempStr) > 0 ):
                    print (thisTempStr + "\t" + thisServer.getName())
                    thisTempStr = ''
                else:
                    thisTempStr = thisServer.getName()

            if ( len(thisTempStr) > 0 ):
                print(thisTempStr)

            return True

######################################################################
