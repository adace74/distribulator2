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
        self._globalConfig = PassedGlobalConfig

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
            thisFilename = os.path.join(self._globalConfig.getConfigDir(), \
                                        'pass_through_cmds.txt')
            thisFile = open(thisFilename, 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.strip()
                thisPassThruList.append(thisLine)

            thisFile.close()

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename))
            sys.exit(1)

        self._globalConfig.setPassThruList(thisPassThruList)

        # Status.
        print( "- Unix pass-through commands:  %d lines loaded." \
               % len(thisPassThruList) )

        # Parse XML...ouchies.
        thisParser = engine.XMLFileParser.XMLFileParser()
        self._globalConfig = thisParser.parse(self._globalConfig)

        print("- Global options and settings: %d lines loaded." % self._globalConfig.getConfigLines())

        self._globalConfig.setCurrentServerGroup( self._globalConfig.getServerGroupList()[0] )

        thisServerGroupStr = ''
        thisTotalServerCount = 0
        for thisServerGroup in self._globalConfig.getServerGroupList():
            thisTotalServerCount = thisTotalServerCount + thisServerGroup.getServerCount()
            thisServerGroupStr = thisServerGroupStr + \
                                 thisServerGroup.getName() + '(%d) ' % \
                                 thisServerGroup.getServerCount()

        print("- Available Server Groups:     " + \
              thisServerGroupStr)
        # Implement the "all" group sometime!
        #+ "all(%d)" % thisTotalServerCount)
        print
        print("Confused?  Need help?  Try typing 'help' and see what happens!")
        print

        return self._globalConfig

######################################################################
