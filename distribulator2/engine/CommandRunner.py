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
import string
import sys

# Custom modules
import engine.data.ExternalCommand
import generic.FilePrinter

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

    def doAreYouSure(self):
        try:
            thisInput = raw_input("Yes / No> ")

        except KeyboardInterrupt:
            print "INFO:  Caught CTRL-C keystroke."
            return False

        if (thisInput.lower() == 'yes'):
            return True
        else:
            return False

    def doChdir(self):
        try:
            if (self._commTokens[0] == 'cd'):
                os.chdir(self._commTokens[1])

        except OSError, (errno, strerror):
            print( "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                self._commTokens[1]) )

    def doCopy(self):
        print("ERROR: This command not yet implemented.")

    def doHelp(self):
        if ( len(self._commTokens) > 1 ):
            thisFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        self._commTokens[1] + '-desc.txt')
        else:
            thisFileName = os.path.join(self._globalConfig.getHelpDir(), \
                                        'help.txt')

        thisFilePrinter = generic.FilePrinter.FilePrinter()

        if (thisFilePrinter.printFile(thisFileName) == False):
            print "ERROR: Cannot find help for specified command '" + \
            self._commTokens[1] + "'."

    def doLogin(self):
        thisFoundIt = False

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
                except KeyboardInterrupt:
                    print("INFO:  Caught CTRL-C keystroke.  Returning to command prompt...")
            else:
                print("ERROR: No matching server '" + \
                      self._commTokens[1] + "'.")
        else:
            print("ERROR: No server name given.")

    def doRun(self):
        thisFoundIt = False

        #
        # Attempt to retokenize our command based on appropriate syntax.
        #
        # Examples: run "uptime" on app
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

        #print("DEBUG: Prefix |" + thisPrefixStr + '|')
        #print("DEBUG: Body: |" + thisBodyStr + '|')
        #print("DEBUG: Suffix: |" + thisSuffixStr + '|')

        # Check for pass-through SSH flags
        if (thisPrefixStr.find('-') != -1):
            thisFlagStr = ' ' + thisPrefixStr[thisPrefixStr.find('-'):]
            thisFlagStr = thisFlagStr.rstrip()
        else:
            thisFlagStr = ''

        # run "uptime"
        # run -t "uptime"
        if (len(thisSuffixStr) == 0):
            # Verify.
            print "Run command " + thisBodyStr + " on server group " + \
                  self._globalConfig.getCurrentServerGroup().getName() + "?"
            if (self.doAreYouSure() == False):
                print("INFO:  Aborting command.")
                return False

            thisServerGroup = self._globalConfig.getCurrentServerGroup()

            # Just Do It.
            try:
                for thisServer in thisServerGroup.getServerList():
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
            except KeyboardInterrupt:
                print "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."

            return True

        # Sanity check.
        if (thisSuffixStr.find(' on ') == -1):
            print("ERROR:  Command Syntax Error.  Try 'help run' for more information.")
            return False

        # run "uptime" on www, app
        if (thisSuffixStr.find(',') != -1):
            print("ERROR: Multiple groups not implemented yet!")
            return False

        # run "uptime" on www
        thisSpaceIndex = thisSuffixStr.rfind(' ')
        thisGroupStr = thisSuffixStr[thisSpaceIndex + 1:]

        thisServerGroup = self._globalConfig.getServerGroupByName(thisGroupStr)

        # Validate.
        if (thisServerGroup == False):
            print("ERROR: No matching server group '" + thisGroupStr + "'.")
            return False

        # Verify.
        print "Run command " + thisBodyStr + " on server group " + \
              thisGroupStr + "?"
        if (self.doAreYouSure() == False):
            print("INFO:  Aborting command.")
            return False

        # Just Do It.
        try:
            for thisServer in thisServerGroup.getServerList():
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
        except KeyboardInterrupt:
            print "INFO:  Caught CTRL-C keystroke.  Returning to command prompt..."

        return True

    def doServerGroup(self):
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
