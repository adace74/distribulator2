######################################################################
#
# $Id$
#
# Name: ConfigLoader.py
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
    import engine.CommandLine
    import engine.XMLFileParser
    import engine.data.GlobalConfig

except ImportError:
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

class ConfigLoader:

    def __init__(self, PassedGlobalConfig):
        self.thisGlobalConfig = PassedGlobalConfig

    def loadGlobalConfig(self, PassedCommLine):
        # Load GNU Readline history.
        print('Loading configuration...')

        thisLinesLoaded = PassedCommLine.initHistory()
        #
        # Try to print status -after- actions so as to be
        # more accurate.
        #
        print("- GNU Readline history:        %d lines loaded." % thisLinesLoaded)
        #
        # Unix "pass through" commands.
        #
        thisPassThruList = []
        
        try:
            thisFilename = os.path.join(self.thisGlobalConfig.getConfigDir(), \
                                        'pass_through_cmds.txt')
            thisFile = open(thisFilename, 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.strip()
                thisPassThruList.append(thisLine)

            thisFile.close()

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename))
            sys.exit(1)

        self.thisGlobalConfig.setPassThruList(thisPassThruList)

        # Status.
        print( "- Unix pass-through commands:  %d lines loaded." \
               % len(thisPassThruList) )

        # Parse XML...ouchies.
        thisParser = engine.XMLFileParser.XMLFileParser()
        self.thisGlobalConfig = thisParser.parse(self.thisGlobalConfig)

        print("- Global options and settings: %d lines loaded." % self.thisGlobalConfig.getConfigLines())

        self.thisGlobalConfig.setCurrentServerGroup( self.thisGlobalConfig.getServerGroupList()[0] )

        thisServerGroupStr = ''
        for thisServerGroup in self.thisGlobalConfig.getServerGroupList():
            thisServerGroupStr = thisServerGroupStr + \
                                 thisServerGroup.getName() + ' '

        print("- Available Server Groups:     all " + thisServerGroupStr)
        print
        print("Confused?  Need help?  Try typing 'help' and see what happens!")
        print

        return self.thisGlobalConfig

######################################################################
