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
import engine.conf.XMLFileParser
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
        if ( self._globalConfig.isConsoleMode() ):
            print('Loading configuration...')

        myLinesLoaded = PassedCommLine.initHistory()
        #
        # Try to print status -after- actions so as to be
        # more accurate.
        #
        if ( self._globalConfig.isConsoleMode() ):
            print("- GNU Readline history:        %d lines loaded." % \
                  (myLinesLoaded))
        #
        # Step 1: Unix "pass through" commands.
        #
        myPassThruList = []
        
        try:
            myFilename = self._globalConfig.getPassThruFile()
            myFile = open(myFilename, 'r')
            
            for myLine in myFile:
                myLine = myLine.strip()
                myPassThruList.append(myLine)

            myFile.close()

        except IOError, (errno, strerror):
            myError = "ERROR: [Errno %s] %s: %s" % \
                        (errno, strerror, myFilename)
            self._globalConfig.getMultiLogger().LogMsgError(myError)
            sys.exit(True)

        self._globalConfig.setPassThruList(myPassThruList)

        # Status.
        if ( self._globalConfig.isConsoleMode() ):
            print( "- Unix pass-through commands:  %d lines loaded." \
                   % (len(myPassThruList)) )

        #
        # Step 2: Load the main XML configuration file.
        #
        myParser = engine.conf.XMLFileParser.XMLFileParser()
        self._globalConfig.setCurrentServerGroup(False)
        self._globalConfig = myParser.parse(self._globalConfig)

        if ( self._globalConfig.isConsoleMode() ):
            print( "- Global options and settings: %d lines loaded." %
                   (self._globalConfig.getConfigLines()) )

        # If the current server group isn't set, set it.
        if (self._globalConfig.getCurrentServerGroup() == False):
            self._globalConfig.setCurrentServerGroup(
                self._globalConfig.getServerGroupList()[0] )

        # Create our pretty output string.
        myServerGroupStr = '- '
        myTotalServerCount = 0
        myColumnCount = 0

        for myServerGroup in self._globalConfig.getServerGroupList():
            myColumnCount = myColumnCount + 1
            myTotalServerCount = myTotalServerCount + \
                                   myServerGroup.getServerCount()
            myServerGroupStr = myServerGroupStr + '%10s (%3d) ' % \
                                 (myServerGroup.getName(), myServerGroup.getServerCount())

            if (myColumnCount == 4):
                myColumnCount = 0
                myServerGroupStr = myServerGroupStr + '\n- '

        if ( self._globalConfig.isConsoleMode() ):
            print("- Available Server Groups:")
            print("-")
            print(myServerGroupStr)        
            print
            print("Confused?  Need help?  Try typing 'help' and see what happens!")
            print

        return self._globalConfig

######################################################################
