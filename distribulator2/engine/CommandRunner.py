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
        self.thisGlobalConfig = PassedGlobalConfig

    def run(self, PassedInternalCommand):
        self.thisCommTokens = PassedInternalCommand.getCommand().split()

        for thisToken in self.thisCommTokens:
            print("DEBUG: Token |" + thisToken + "|")

        # Cheezy branching logic.  Works well, though.
        if (self.thisCommTokens[0] == 'cd'):
            self.doChdir()
        elif (self.thisCommTokens[0] == 'copy'):
            self.doCopy()
        elif (self.thisCommTokens[0] == 'help'):
            self.doHelp()
        elif (self.thisCommTokens[0] == 'login'):
            self.doLogin()
        elif (self.thisCommTokens[0] == 'run'):
            self.doRun()
        elif (self.thisCommTokens[0] == 'server-group'):
            self.doServerGroup()
        elif (self.thisCommTokens[0] == 'server-list'):
            self.doServerList()
        else:
            print("ERROR: Unknown Command: '" + self.thisCommTokens[0] + \
                  "'")

    def doChdir(self):
        try:
            if (self.thisCommTokens[0] == 'cd'):
                os.chdir(self.thisCommTokens[1])

        except OSError, (errno, strerror):
            print( "ERROR: [Errno %s] %s: %s" % (errno, strerror, \
                                                self.thisCommTokens[1]) )

    def doCopy(self):
        print("Copy")

    def doHelp(self):
        if ( len(self.thisCommTokens) > 1 ):
            thisFileName = os.path.join(self.thisGlobalConfig.getHelpDir(), \
                                        self.thisCommTokens[1] + '-desc.txt')
        else:
            thisFileName = os.path.join(self.thisGlobalConfig.getHelpDir(), \
                                        'help.txt')

        thisFilePrinter = generic.FilePrinter.FilePrinter()

        if (thisFilePrinter.printFile(thisFileName) == False):
            print "ERROR: Cannot find help for specified command '" + \
            self.thisCommTokens[1] + "'"

    def doLogin(self):
        print("ERROR: No Matching Server '" + self.thisCommTokens[1] + "'")

    def doRun(self):
        print("Run")

    def doServerGroup(self):
        print("Server-Group")

    def doServerList(self):
        print("Known servers for group '" +
              self.thisGlobalConfig.getCurrentServerGroup().getName() + "'")
        print("----------------------------------------")
        # Actual server list goes here.

######################################################################
