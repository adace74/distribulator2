######################################################################
#
# $Id$
#
# Name: CommandRunner.py
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
        if ( self._globalConfig.isBatchMode() ):
            self._globalConfig.getSysLogger().LogMsgError(
                PassedError)
        else:
            print(PassedError)
            self._globalConfig.getSysLogger().LogMsgError(
                PassedError)

######################################################################

    def handleInfo(self, PassedInfo):
        if ( self._globalConfig.isBatchMode() ):
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

        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("CMD:   " + \
                                                     self._commString)

        #for thisToken in self._commTokens:
        #    print("DEBUG: Token |" + thisToken + "|")

        # Cheezy branching logic.  Works well, though.
        if (self._commTokens[0] == 'cd'):
            thisStatus = self.doChdir()
        elif (self._commTokens[0] == 'copy'):
            thisStatus = self.doCopy()
        elif (self._commTokens[0] == 'help'):
            thisStatus = self.doHelp()
        elif (self._commTokens[0] == 'login'):
            thisStatus = self.doLogin()
        elif (self._commTokens[0] == 'run'):
            thisStatus = self.doRun()
        elif (self._commTokens[0] == 'server-group'):
            thisStatus = self.doServerGroup()
        elif (self._commTokens[0] == 'server-list'):
            thisStatus = self.doServerList()
        else:
            thisError = "ERROR: Unknown Command: '" + \
                            self._commTokens[0] + "'."
            self.handleError(thisError)
            return False

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
        thisServerGroupList = []

        # Sanity check.
        if (len(self._commTokens) != 3):
            thisError = "ERROR: Command Syntax Error.  Try 'help copy' for more information."
            self.handleError(thisError)
            return False

        # copy /tmp/blah.txt /tmp/
        if ( self._commString.find(':') == -1 ):
            try:
                if ( stat.S_ISREG(os.stat(
                    self._commTokens[1])[stat.ST_MODE]) == False):
                    thisError = "ERROR: File '" + self._commTokens[1] + \
                                "' is accessible, but not regular."
                    self.handleError(thisError)
                    return False
            except OSError, (errno, strerror):
                thisError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                         self._commTokens[1])
                self.handleError(thisError)
                return False

            thisGroupStr = self._globalConfig.getCurrentServerGroup().getName()
            print("Copy local file '" + self._commTokens[1] +
            "' to remote directory '" + self._commTokens[2] + "'")
            print("on server group " + thisGroupStr + "?")

            if (self.doAreYouSure() == False):
                thisInfo = "INFO:  Aborting command."
                self.handleInfo(thisInfo)
                return False
            else:
                thisServerGroupList.append( thisGroupStr )
        else:
            thisError = "ERROR: Syntax not yet implemented!"
            self.handleError(thisError)
            return False

        # Just Do It.
        for thisGroupStr in thisServerGroupList:
            thisServerGroup = self._globalConfig.getServerGroupByName(
                thisGroupStr)

            try:
                for thisServer in thisServerGroup.getServerList():
                    thisPinger = generic.HostPinger.HostPinger(
                        self._globalConfig.getPingBinary() )

                    if (thisPinger.ping(thisServer.getName()) == 0):
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                        thisExternalCommand.setCommand( \
                            self._globalConfig.getScpBinary() + " " + \
                            self._commTokens[1] + " " + \
                            thisServer.getUsername() + "@" + \
                            thisServer.getName() + ":" + \
                            self._commTokens[2] )
                        # Run It.
                        if ( self._globalConfig.isBatchMode() ):
                            thisExternalCommand.runAtomic()
                        else:
                            thisExternalCommand.run(True)
                    else:
                        thisError = "ERROR: Server '" + thisServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self.handleError(thisError)

            except EOFError:
                noop
            except KeyboardInterrupt:
                thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
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
        thisFoundIt = False

        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        if ( len(self._commTokens) > 1):
            thisServerGroupList = self._globalConfig.getServerGroupList()

            for thisServerGroup in thisServerGroupList:
                if ( thisServerGroup.getServerByName(self._commTokens[1]) ):
                    thisServer = thisServerGroup.getServerByName(self._commTokens[1])
                    thisFoundIt = True

            if (thisFoundIt):
                thisExternalCommand = engine.data.ExternalCommand.ExternalCommand(self._globalConfig)
                thisExternalCommand.setCommand( \
                    self._globalConfig.getSshBinary() + " -l " + \
                    thisServer.getUsername() + " " + thisServer.getName() )
                try:
                    thisExternalCommand.run(True)
                except (EOFError, KeyboardInterrupt):
                    thisInfo = "INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt..."
                    self.handleInfo(thisInfo)
            else:
                thisError = "ERROR: No matching server '" + \
                            self._commTokens[1] + "'."
                self.handleError(thisError)
                return False
        else:
            thisError = "ERROR: No server name given."
            self.handleError(thisError)
            return False

        return True

######################################################################
            
    def doRun(self):
        thisServerGroupList = []

        #
        # Attempt to retokenize our command based on appropriate syntax.
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

        # run "uptime"
        # run -t "uptime"
        if (len(thisSuffixStr) == 0):
            thisGroupStr = self._globalConfig.getCurrentServerGroup().getName()
            thisServerGroupList.append( thisGroupStr.strip() )
        else:
            # Sanity syntax check.
            if (thisSuffixStr.find(' on ') == -1):
                thisError = "ERROR: Command Syntax Error.  Try 'help run' for more information."
                self.handleErorr(thisError)
                return False

            thisSuffixStr = thisSuffixStr[thisSuffixStr.find(' on ') + 4:]

            if (thisSuffixStr.find(',') == -1):
                # run "uptime" on app
                # run -t "uptime" on app
                thisSpaceIndex = thisSuffixStr.rfind(' ')
                thisGroupStr = thisSuffixStr[thisSpaceIndex + 1:]
                
                thisServerGroup = self._globalConfig.getServerGroupByName(thisGroupStr)

                # Validate.
                if (thisServerGroup == False):
                    thisError = "ERROR: No matching server group '" + \
                                thisGroupStr + "'."
                    self.handleError(thisError)
                    return False
                else:
                    thisServerGroupList.append( thisGroupStr.strip() )
            else:
                # run "uptime" on app, www
                # run -t "uptime" on app, www
                thisGroupList = thisSuffixStr.split(',')

                for thisGroupStr in thisGroupList:
                    if (self._globalConfig.getServerGroupByName(thisGroupStr.strip())
                        == False):
                        thisError = "ERROR: No matching server group '" + \
                              thisGroupStr.strip() + "'."
                        self.handleError(thisError)
                        return False
                    else:
                        thisServerGroupList.append( thisGroupStr.strip() )

        if (self._globalConfig.isBatchMode() == False):
            # Verify.
            thisDisplayStr = ''
            for thisGroupStr in thisServerGroupList:
                thisDisplayStr = thisDisplayStr + thisGroupStr + ','
            thisDisplayStr = thisDisplayStr.rstrip(',')

            print("Run command " + thisBodyStr + " on server group(s) " + \
                  thisDisplayStr + "?")
            if (self.doAreYouSure() == False):
                thisInfo = "INFO:  Aborting command."
                self.handleInfo(thisInfo)
                return False

        # Just Do It.
        for thisGroupStr in thisServerGroupList:
            thisServerGroup = self._globalConfig.getServerGroupByName(
                thisGroupStr)

            thisServerList = thisServerGroup.getServerList()

            #
            # Slightly nasty hack.  Since lists can only be sorted in-place,
            # and Python doesn't support object copying, we do the following:
            # 1) Reverse sort the list
            # 2) Run the commands
            # 3) Forward-sort the list, hopefully back to its original state.
            #
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
                    else:
                        thisError = "ERROR: Server '" + \
                                    thisServer.getName() + \
                                    "' appears to be down.  Continuing..."
                        self.handleError(thisError)

            except EOFError:
                noop
            except KeyboardInterrupt:
                thisInfo = "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."
                self.handleInfo(thisInfo)

            if (isReverse):
                thisServerList.sort()

        return True

######################################################################
    
    def doServerGroup(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        if ( len(self._commTokens) > 1 ):
            thisServerGroup = self._globalConfig.getServerGroupByName( self._commTokens[1] )

            if (thisServerGroup == False):
                thisError = "ERROR: No matching server group '" + \
                            self._commTokens[1] + "'."
                self.handleError(thisError)
                return False
            else:
                self._globalConfig.setCurrentServerGroup(thisServerGroup)
                print("Current server group is now '" + self._commTokens[1] + "'.")
                return True
        else:
            thisError = "ERROR: No server group name given."
            self.handleError(thisError)
            return False

    def doServerList(self):
        # Check for batch mode.
        if ( self._globalConfig.isBatchMode() ):
            thisError = "ERROR: Invalid command for batch mode."
            self.handleError(thisError)
            return False

        if ( len(self._commTokens) > 1 ):
            thisServerGroup = self._globalConfig.getServerGroupByName( \
                self._commTokens[1] )
        else:
            thisServerGroup = self._globalConfig.getCurrentServerGroup()

        if (thisServerGroup == False):
            thisError = "ERROR: No matching server group '" + \
                        self._commTokens[1] + "'."
            self.handleError(thisError)
            return False
        else:
            print("Known servers for group '" + thisServerGroup.getName() + "'")
            print("----------------------------------------")
            # Actual server list goes here.
            thisTempStr = ''

            for thisServer in \
                    thisServerGroup.getServerList():
                if ( len(thisTempStr) > 0 ):
                    print (thisTempStr + "\t" + thisServer.getName())
                    thisTempStr = ''
                else:
                    thisTempStr = thisServer.getName()

            if ( len(thisTempStr) > 0 ):
                print(thisTempStr)

            return True

######################################################################
