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

    def run(self, PassedInternalCommand):
        self._commString = PassedInternalCommand.getCommand()
        self._commTokens = self._commString.split()

        #for thisToken in self._commTokens:
        #    print("DEBUG: Token |" + thisToken + "|")

        # Cheezy branching logic.  Works well, though.
        if (self._commTokens[0] == 'cd'):
            self.doChdir()
        elif (self._commTokens[0] == 'copy'):
            self.doCopy()
        elif (self._commTokens[0] == 'help'):
            self.doHelp()
        elif (self._commTokens[0] == 'login'):
            self.doLogin()
        elif (self._commTokens[0] == 'run'):
            self.doRun()
        elif (self._commTokens[0] == 'server-group'):
            self.doServerGroup()
        elif (self._commTokens[0] == 'server-list'):
            self.doServerList()
        else:
            print("ERROR: Unknown Command: '" + self._commTokens[0] + \
                  "'.")

######################################################################

    def doAreYouSure(self):
        try:
            thisInput = raw_input("Yes / No> ")

        except (EOFError, KeyboardInterrupt):
            print("INFO:  Caught CTRL-C / CTRL-D keystroke.")
            return False

        if (thisInput.lower() == 'yes'):
            return True
        else:
            return False

######################################################################

    def doChdir(self):
        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("INPUT: " + \
                                                     self._commString)

        try:
            if (self._commTokens[0] == 'cd'):
                os.chdir(self._commTokens[1])

        except OSError, (errno, strerror):
            print( "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                self._commTokens[1]) )

######################################################################

    def doCopy(self):
        thisServerGroupList = []

        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("INPUT: " + \
                                                     self._commString)
        
        # Sanity check.
        if (len(self._commTokens) != 3):
            print("ERROR:  Command Syntax Error.  Try 'help copy' for more information.")
            return False

        # copy /tmp/blah.txt /tmp/
        if ( self._commString.find(':') == -1 ):
            try:
                if ( stat.S_ISREG(os.stat(
                    self._commTokens[1])[stat.ST_MODE]) == False):
                    print("ERROR: File '" + self._commTokens[1] +
                    "' is accessible, but not regular.")
                    return False
            except OSError, (errno, strerror):
                print( "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                     self._commTokens[1]) )
                return False

            thisGroupStr = self._globalConfig.getCurrentServerGroup().getName()
            print("Copy local file '" + self._commTokens[1] +
            "' to remote directory '" + self._commTokens[2] + "'")
            print("on server group " + thisGroupStr + "?")

            if (self.doAreYouSure() == False):
                print("INFO:  Aborting command.")
                return False
            else:
                thisServerGroupList.append( thisGroupStr )
        else:
            print("ERROR: Syntax not yet implemented!")
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
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                        thisExternalCommand.setCommand( \
                            self._globalConfig.getScpBinary() + " " + \
                            self._commTokens[1] + " " + \
                            thisServer.getUsername() + "@" + \
                            thisServer.getName() + ":" + \
                            self._commTokens[2] )
                        # Log It.
                        self._globalConfig.getSysLogger().LogMsgInfo("EXEC: " + \
                                                                     thisExternalCommand.getCommand())
                        # Run It.
                        thisExternalCommand.run()
                    else:
                        print("ERROR: Server '" + thisServer.getName() + \
                              "' appears to be down.  Continuing...")
                        self._globalConfig.getSysLogger().LogMsgInfo(
                            "ERROR: Server '" + thisServer.getName() + \
                            "' appears to be down.  Continuing.." )

            except EOFError:
                noop
            except KeyboardInterrupt:
                print("INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt...")
                return False

        return True

######################################################################

    def doHelp(self):
        if ( len(self._commTokens) > 1 ):
            thisFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        self._commTokens[1] + '-desc.txt')
        else:
            thisFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        'help.txt')

        thisFilePrinter = generic.FilePrinter.FilePrinter()

        if (thisFilePrinter.printFile(thisFileName) == False):
            print("ERROR: Cannot find help for specified command '" + \
            self._commTokens[1] + "'.")

######################################################################
            
    def doLogin(self):
        thisFoundIt = False

        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("INPUT: " + \
                                                     self._commString)

        if ( len(self._commTokens) > 1):
            thisServerGroupList = self._globalConfig.getServerGroupList()

            for thisServerGroup in thisServerGroupList:
                if ( thisServerGroup.getServerByName(self._commTokens[1]) ):
                    thisServer = thisServerGroup.getServerByName(self._commTokens[1])
                    thisFoundIt = True

            if (thisFoundIt):
                thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                thisExternalCommand.setCommand( \
                    self._globalConfig.getSshBinary() + " -l " + \
                    thisServer.getUsername() + " " + thisServer.getName() )
                self._globalConfig.getSysLogger().LogMsgInfo("EXEC: " + \
                                                             thisExternalCommand.getCommand())
                try:
                    thisExternalCommand.run()
                except (EOFError, KeyboardInterrupt):
                    print("INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt...")
            else:
                print("ERROR: No matching server '" + \
                      self._commTokens[1] + "'.")
        else:
            print("ERROR: No server name given.")

######################################################################
            
    def doRun(self):
        thisServerGroupList = []

        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("INPUT: " + \
                                                     self._commString)

        #
        # Attempt to retokenize our command based on appropriate syntax.
        #
        if ( self._commString.find('"') == -1 ):
            print("ERROR:  Command Syntax Error.  Try 'help run' for more information.")
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

        # run "uptime"
        # run -t "uptime"
        if (len(thisSuffixStr) == 0):
            thisGroupStr = self._globalConfig.getCurrentServerGroup().getName()
            thisServerGroupList.append( thisGroupStr.strip() )
        else:
            # Sanity syntax check.
            if (thisSuffixStr.find(' on ') == -1):
                print("ERROR:  Command Syntax Error.  Try 'help run' for more information.")
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
                    print("ERROR: No matching server group '" + \
                          thisGroupStr + "'.")
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
                        print("ERROR: No matching server group '" + \
                              thisGroupStr.strip() + "'.")
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
                print("INFO:  Aborting command.")
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
                        thisExternalCommand = engine.data.ExternalCommand.ExternalCommand()
                        thisExternalCommand.setCommand( \
                            self._globalConfig.getSshBinary() + thisFlagStr + \
                            " -l " + thisServer.getUsername() + " " + \
                            thisServer.getName() + " " + \
                            thisBodyStr )
                        # Log It.
                        self._globalConfig.getSysLogger().LogMsgInfo("EXEC: " + \
                                                                     thisExternalCommand.getCommand())
                        # Run It.
                        thisExternalCommand.run()
                    else:
                        print("ERROR: Server '" + thisServer.getName() + \
                              "' appears to be down.  Continuing...")
                        self._globalConfig.getSysLogger().LogMsgInfo(
                            "ERROR: Server '" + thisServer.getName() + \
                            "' appears to be down.  Continuing.." )

            except EOFError:
                noop
            except KeyboardInterrupt:
                print("INFO:  Caught CTRL-C / CTRL-D keystroke.  Returning to command prompt...")

        return True

######################################################################
    
    def doServerGroup(self):
        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("INPUT: " + \
                                                     self._commString)

        if ( len(self._commTokens) > 1 ):
            thisServerGroup = self._globalConfig.getServerGroupByName( self._commTokens[1] )

            if (thisServerGroup == False):
                print("ERROR: No matching server group '" + self._commTokens[1] + "'.")
                return
            else:
                self._globalConfig.setCurrentServerGroup(thisServerGroup)
                print("Current server group is now '" + self._commTokens[1] + "'.")
        else:
            print("ERROR: No server group name given.")

    def doServerList(self):
        # Log It.
        self._globalConfig.getSysLogger().LogMsgInfo("INPUT: " + \
                                                     self._commString)

        if ( len(self._commTokens) > 1 ):
            thisServerGroup = self._globalConfig.getServerGroupByName( \
                self._commTokens[1] )
        else:
            thisServerGroup = self._globalConfig.getCurrentServerGroup()

        if (thisServerGroup == False):
            print("ERROR: No matching server group '" + self._commTokens[1] + "'.")
            return
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

######################################################################
