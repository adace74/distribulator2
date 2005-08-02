######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for loading the application's configuration data."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import logging
import logging.config
import logging.handlers
import os
import stat

# Custom modules
import engine.conf.XMLFileChecker
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

        # Console Mode: Load GNU Readline history.
        if ( self._globalConfig.isConsoleMode() ):
            print('Loading configuration...')

            myLinesLoaded = PassedCommLine.initHistory()
            #
            # Try to print status -after- actions so as to be
            # more accurate.
            #
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
            myError = "[Errno %s] %s: %s" % \
                        (errno, strerror, myFilename)
            self._globalConfig.getMultiLogger().LogMsgCrit(myError)
            sys.exit(True)

        self._globalConfig.setPassThruList(myPassThruList)

        # Status.
        if ( self._globalConfig.isConsoleMode() ):
            print( "- Unix pass-through commands:  %d lines loaded." \
                   % (len(myPassThruList)) )

        #
        # Step 2: Load the logging configuration file.
        #
        myConfigLines = 0

        try:
            # Let's make sure the file we've been given is readable.
            if ( not stat.S_ISREG(os.stat(
                self._globalConfig.getLoggingConfigFile())[stat.ST_MODE]) ):
                myError = "File '" + \
                            self._globalConfig.getLoggingConfigFile() + \
                            "' is accessible, but not regular."
                self._globalConfig.getMultiLogger().LogMsgCrit(myError)
                self._globalConfig.setExitSuccess(False)
                return

            # We might as well count the lines as well.
            myFile = open(self._globalConfig.getLoggingConfigFile(), 'r')
            for myLine in myFile:
                myConfigLines = myConfigLines + 1
            myFile.close()

        except OSError, (errno, strerror):
            myError = "[Errno %s] %s: %s" % ( errno, strerror, \
                                                       self._globalConfig.getBatchFile() )
            self._globalConfig.getMultiLogger().LogMsgCrit(myError)
            self._globalConfig.setExitSuccess(False)
            return

        # Setup logging configuration.
        logging.config.fileConfig( self._globalConfig.getLoggingConfigFile() )

        # Override built-in text with something a little more brief.
        logging.addLevelName(logging.CRITICAL, 'CRIT')
        logging.addLevelName(logging.WARNING, 'WARN')

        # Override exception handling to silently swallow I/O exceptions.
        logging.raiseExceptions = False

        # Store loggers for later use.
        self._globalConfig.setAuditLogger( logging.getLogger('audit') )
        self._globalConfig.setStdoutLogger( logging.getLogger('stdout') )

        # If this is batch mode, we default to a higher log level.
        if ( self._globalConfig.isBatchMode() ):
            self._globalConfig.getStdoutLogger().setLevel(logging.DEBUG)

        # Override the logging.conf loglevel for STDOUT if specified.
        if ( self._globalConfig.getVerboseLevel() != None ):
            if (self._globalConfig.getVerboseLevel() == 'DEBUG'):
                self._globalConfig.getStdoutLogger().setLevel(logging.DEBUG)
            elif (self._globalConfig.getVerboseLevel() == 'INFO'):
                self._globalConfig.getStdoutLogger().setLevel(logging.INFO)
            elif (self._globalConfig.getVerboseLevel() == 'ERROR'):
                self._globalConfig.getStdoutLogger().setLevel(logging.ERROR)
            else:
                myError = "Standard output level setting '" + self._globalConfig.getVerboseLevel() + "' not supported.  Exiting..."
                self._globalConfig.getMultiLogger().LogMsgError(myError)
                self._globalConfig.setExitSuccess(False)
                return

        if ( self._globalConfig.isConsoleMode() ):
            print( "- Logging configuration:       %d lines loaded." % myConfigLines )

        #
        # Step 3: Pre-check the main XML configuration file.
        #
        myChecker = engine.conf.XMLFileChecker.XMLFileChecker()
        myChecker.check(self._globalConfig)

        #
        # Step 4: Load the main XML configuration file.
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
                self._globalConfig.getCurrentEnv().getServerGroupList()[0] )

        # Create our pretty output string.
        myServerGroupStr = '- '
        myTotalEnvironmentCount = 0
        myTotalServerCount = 0
        myColumnCount = 0

        for myEnvironment in self._globalConfig.getEnvironmentList():
            myTotalEnvironmentCount = myTotalEnvironmentCount + 1;
            for myServerGroup in myEnvironment.getServerGroupList():
                myTotalServerCount = myTotalServerCount + myServerGroup.getServerCount()

        for myServerGroup in self._globalConfig.getCurrentEnv().getServerGroupList():
            myColumnCount = myColumnCount + 1
            myServerGroupStr = myServerGroupStr + '%16s (%3d) ' % \
                               (myServerGroup.getName(), myServerGroup.getServerCount())

            if (myColumnCount == 4):
                myColumnCount = 0
                myServerGroupStr = myServerGroupStr + '\n- '

        if ( self._globalConfig.isConsoleMode() ):
            print("- Available Server Groups:")
            print("-")
            print(myServerGroupStr)        
            print("-")
            print("- Total: %d server(s) in %d environment(s) loaded." % (myTotalServerCount, myTotalEnvironmentCount))
            print
            print("Confused?  Need help?  Try typing 'help' and see what happens!")
            print

        return self._globalConfig

######################################################################
