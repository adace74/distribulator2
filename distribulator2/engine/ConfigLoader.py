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
    print "An error occured while loading Python modules, exiting..."
    sys.exit(1)

######################################################################

class ConfigLoader:

    def getGlobalConfig(self, PassedCommLine, PassedConfigDir):
        # Load GNU Readline history.
        print('Loading configuration...')

        thisLinesLoaded = PassedCommLine.initHistory()
        #
        # Try to print status -after- actions so as to be
        # more accurate.
        #
        print("- Readline history: %d lines loaded." % thisLinesLoaded)
        
        #
        # Create GlobalConfig object.
        #
        thisGlobalConfig = engine.data.GlobalConfig.GlobalConfig()
        thisGlobalConfig.setConfigDir(PassedConfigDir)

        #
        # Unix "pass through" commands.
        #
        thisPassThruList = []
        
        try:
            thisFilename = os.path.join(thisGlobalConfig.getConfigDir(), \
                                        'pass_through_cmds.txt')
            thisFile = open(thisFilename, 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.strip()
                thisPassThruList.append(thisLine)

            thisFile.close()

        except IOError, (errno, strerror):
            print "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename)
            sys.exit(1)

        thisGlobalConfig.setPassThruList(thisPassThruList)

        # Status.
        print( "- Pass-through Unix commands: %d lines loaded." \
               % len(thisPassThruList) )

        # Parse XML...ouchies.
        thisParser = engine.XMLFileParser.XMLFileParser()
        thisParser.parse(thisGlobalConfig)
        print("- Global options and settings.")
        print("- Entering interactive mode...")
        print

        return thisGlobalConfig

######################################################################
