######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for loading the application's configuration data."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import os
import os.path
import string
import sys

# Custom modules
import engine.CommandLine
import engine.XMLFileParser
import engine.data.GlobalConfig

######################################################################

class ConfigLoader:
    """This class is responsible for loading the application's configuration data."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        self._globalConfig = PassedGlobalConfig

######################################################################

    def load(self, PassedCommLine):
        """
        This method is responsible for loading configuration data into the
        engine.data.GlobalConfig object.
        """

        # Load GNU Readline history.
        if (self._globalConfig.isBatchMode() == False):
            print('Loading configuration...')

        thisLinesLoaded = PassedCommLine.initHistory()
        #
        # Try to print status -after- actions so as to be
        # more accurate.
        #
        if (self._globalConfig.isBatchMode() == False):
            print("- GNU Readline history:        %d lines loaded." % \
                  (thisLinesLoaded))
        #
        # Step 1: Unix "pass through" commands.
        #
        thisPassThruList = []
        
        try:
            thisFilename = self._globalConfig.getPassThruFile()
            thisFile = open(thisFilename, 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.strip()
                thisPassThruList.append(thisLine)

            thisFile.close()

        except IOError, (errno, strerror):
            thisError = "ERROR: [Errno %s] %s: %s" % \
                        (errno, strerror, thisFilename)
            self._globalConfig.getMultiLogger().LogMsgError(thisError)
            sys.exit(True)

        self._globalConfig.setPassThruList(thisPassThruList)

        # Status.
        if (self._globalConfig.isBatchMode() == False):
            print( "- Unix pass-through commands:  %d lines loaded." \
                   % (len(thisPassThruList)) )

        #
        # Step 2: Load the main XML configuration file.
        #
        thisParser = engine.XMLFileParser.XMLFileParser()
        self._globalConfig = thisParser.parse(self._globalConfig)

        if (self._globalConfig.isBatchMode() == False):
            print( "- Global options and settings: %d lines loaded." %
                   (self._globalConfig.getConfigLines()) )

        self._globalConfig.setCurrentServerGroup(
            self._globalConfig.getServerGroupList()[0] )

        # Create our pretty output string.
        thisServerGroupStr = '- '
        thisTotalServerCount = 0
        thisColumnCount = 0

        for thisServerGroup in self._globalConfig.getServerGroupList():
            thisColumnCount = thisColumnCount + 1
            thisTotalServerCount = thisTotalServerCount + \
                                   thisServerGroup.getServerCount()
            thisServerGroupStr = thisServerGroupStr + '%10s (%3d) ' % \
                                 (thisServerGroup.getName(), thisServerGroup.getServerCount())

            if (thisColumnCount == 4):
                thisColumnCount = 0
                thisServerGroupStr = thisServerGroupStr + '\n- '

        if (self._globalConfig.isBatchMode() == False):
            print("- Available Server Groups:")
            print("-")
            print(thisServerGroupStr)        
            print
            print("Confused?  Need help?  Try typing 'help' and see what happens!")
            print

        return self._globalConfig

######################################################################
