######################################################################
#
# $Id$
#
# Name: CommandRunner.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import os
    import os.path
    import string
    import sys

    # Custom modules
    import generic.FilePrinter

except ImportError:
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

class CommandRunner:
    def __init__(self, PassedGlobalConfig):
        self._globalConfig = PassedGlobalConfig

    def run(self, PassedInternalCommand):
        self._commTokens = PassedInternalCommand.getCommand().split()

        for thisToken in self._commTokens:
            print("DEBUG: Token |" + thisToken + "|")

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

    def doChdir(self):
        try:
            if (self._commTokens[0] == 'cd'):
                os.chdir(self._commTokens[1])

        except OSError, (errno, strerror):
            print( "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                self._commTokens[1]) )

    def doCopy(self):
        print("Copy")

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
        print("ERROR: No Matching Server '" + self._commTokens[1] + "'.")

    def doRun(self):
        print("Run")

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
