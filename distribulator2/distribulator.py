#!/usr/local/bin/python
######################################################################
#
# $Id$
#
# Description: The Distribulator.
# A detailed description can be found in the README file.
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
# Notes: Unfortunately, Python, like other shell-oriented langauges,
# requires that methods be defined before calling them.
# As such, main() will always be at the -bottom- of a file.
#
######################################################################

# Pydoc comments
"""Application entry point for The Distribulator."""

# File version tag
__version__ = '$Revision$'[11:-2]
# Application version tag
__appversion__ = 'The Distribulator v0.61'

# Standard modules
import commands
import getopt
import getpass
import os
import os.path
import socket
import sys

# Custom modules
import engine.BatchRunner
import engine.CommandLine
import engine.ConfigLoader
import engine.data.GlobalConfig
import generic.SysLogger

######################################################################
# Display a nice pretty header.
######################################################################

def printTitleHeader():
    """Print the title header."""

    print
    print(__appversion__ + " (Python v" + \
          sys.version.split()[0] + " / " + sys.platform + ")")
    print("--------------------------------------------------")
    print

######################################################################

def printInfoHeader(PassedServerEnv, PassedConfigDir):
    """Print the informational header."""

    print("Local Hostname:      " + socket.gethostname())
    print("Current Environment: " + PassedServerEnv)
    print("Config Directory:    " + PassedConfigDir)
    print

######################################################################
# Good old main...
######################################################################

def main(argv):
    """Good old main."""

    long_options = ['batch=',
                    'directory=',
                    'env=',
                    'help',
                    'quiet',
                    'var1=',
                    'var2=',
                    'var3=',
                    'version']

    usage = """
Usage: %s [options] --env=environment

The available options are:

    --batch=filename
    Enables batch mode processing, requires a readable input file.
    OPTIONAL

    --directory=start_dir
    Allows the wrapper script to pass in the user's real cwd.
    OPTIONAL

    --env=env_name
    The server environment we wish to operate in.
    REQUIRED

    --help
    This usage statement.

    --quiet
    Batch Mode Only: Disable STDOUT, particularly useful when run from cron.
    OPTIONAL

    --var1=some_string
    --var2=some_other_string
    --var3=you_get_the_idea
    Batch Mode Only: Enables simple string substitution.
    Up to 3 variables may be defined then referenced in a given batch file
    as $var1, $var2, and $var3.

    --version
    Print version information.
""" % argv[0]

    thisBatchFile = ''
    thisQuietMode = False
    thisServerEnv = 'demo'
    thisStartDir = '/tmp'
    thisVar1 = ''
    thisVar2 = ''
    thisVar3 = ''
    thisVerboseMode = False

    try:
        if len(argv) < 2:
            print("ERROR: I need to know which environment I am to use!")
            raise "CommandLineError"

        optlist, args = getopt.getopt(sys.argv[1:], None, long_options)

        if len(optlist) > 0:
            for opt in optlist:
                if (opt[0] == '--batch'):
                    thisBatchFile = opt[1]
                elif (opt[0] == '--directory'):
                    thisStartDir = opt[1]
                elif (opt[0] == '--env'):
                    thisServerEnv = opt[1]
                elif (opt[0] == '--help'):
                    print(usage)
                    sys.exit(0)
                elif (opt[0] == '--quiet'):
                    thisQuietMode = True
                elif (opt[0] == '--var1'):
                    thisVar1 = opt[1]
                elif (opt[0] == '--var2'):
                    thisVar2 = opt[1]
                elif (opt[0] == '--var3'):
                    thisVar3 = opt[1]
                elif (opt[0] == '--version'):
                    print(__appversion__)
                    print("Please see the LICENSE file for accompanying legalese.")
                    sys.exit(0)
        else:
            print("ERROR: getopt failure!  This shouldn't ever happen!")
            print
            raise "CommandLineError"

    except "CommandLineError":
        print(usage)
        sys.exit(1)

    except getopt.GetoptError:
        print("ERROR: Erroneous flag(s) given.  Please check your syntax.")
        print(usage)
        sys.exit(1)

    try:
        thisConfigDir = os.path.join(os.getcwd(), 'conf')
        thisHelpDir = os.path.join(os.getcwd(), 'doc')

        # Load up our GlobalConfig object.
        thisGlobalConfig = engine.data.GlobalConfig.GlobalConfig()

        if ( len(thisBatchFile) > 0 ):
            thisGlobalConfig.setBatchMode(True)
            thisGlobalConfig.setBatchFile(thisBatchFile)
        else:
            thisGlobalConfig.setBatchMode(False)

        thisGlobalConfig.setConfigDir(thisConfigDir)
        thisGlobalConfig.setExitSuccess(True)
        thisGlobalConfig.setHelpDir(thisHelpDir)
        thisGlobalConfig.setQuietMode(thisQuietMode)
        thisGlobalConfig.setServerEnv(thisServerEnv)
        thisGlobalConfig.setVar1(thisVar1)
        thisGlobalConfig.setVar2(thisVar2)
        thisGlobalConfig.setVar3(thisVar3)
    
        if ( thisGlobalConfig.isBatchMode() == False ):
            printTitleHeader()
            printInfoHeader(thisServerEnv, thisConfigDir)

        thisBatchRunner = engine.BatchRunner.BatchRunner(thisGlobalConfig)
        thisCommLine = engine.CommandLine.CommandLine(thisGlobalConfig)
        thisLoader = engine.ConfigLoader.ConfigLoader(thisGlobalConfig)
        thisGlobalConfig = thisLoader.load(thisCommLine)

        # Set our silly output flag
        if ( thisGlobalConfig.isBatchMode() & \
             (thisGlobalConfig.isQuietMode() == False) ):
            thisVerboseMode = True

        # Setup syslog.
        thisLogger = generic.SysLogger.SysLogger(thisGlobalConfig.getSyslogFacility(), 'distribulator.py')
        thisGlobalConfig.setSysLogger(thisLogger)

        # Log our startup.
        thisStatus, thisOutput = commands.getstatusoutput( \
            thisGlobalConfig.getLognameBinary())

        if ( thisStatus == 0 ):
            thisGlobalConfig.setRealUsername(thisOutput)
            thisGlobalConfig.setUsername( getpass.getuser() )
        else:
            thisGlobalConfig.setRealUsername( getpass.getuser() )
            thisGlobalConfig.setUsername( getpass.getuser() )

        # Define a pretty seperator.
        thisSeperator = '----------------------------------------------------------------------'
        thisLogger.LogMsgInfo(thisSeperator)
        if (thisVerboseMode):
            print(thisSeperator)

        if (thisGlobalConfig.isBatchMode()):
            thisInfo = "INFO:  " + __appversion__ + " (batch mode) START"
            if (thisVerboseMode):
                print(thisInfo)
        else:
            thisInfo = "INFO:  " + __appversion__ + " (console mode) START"
        thisLogger.LogMsgInfo(thisInfo)

        thisInfo = "INFO:  Real UID: " + thisGlobalConfig.getRealUsername() + \
                   " | " + \
                   "Effective UID: " + thisGlobalConfig.getUsername() + \
                   " | " + \
                   "Environment: " + thisServerEnv

        thisLogger.LogMsgInfo(thisInfo)
        if (thisVerboseMode):
            print(thisInfo)

    except (EOFError, KeyboardInterrupt):
            thisError = "ERROR: Caught CTRL-C / CTRL-D keystroke.  Exiting..."
            thisLogger.LogMsgError(thisError)
            if (thisVerboseMode):
                print(thisError)

            sys.exit(-1)

    # Try to chdir() to thisStartDir if possible.
    try:
        os.chdir(thisStartDir)

    except OSError, (errno, strerror):
        thisError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisTokens[1])
        print(thisError)
        thisLogger.LogMsgError(thisError)

    # Batch mode.
    if ( thisGlobalConfig.isBatchMode() ):
        thisBatchRunner.invoke()

        thisInfo = "INFO:  " + __appversion__ + " (batch mode) EXIT"
        thisLogger.LogMsgInfo(thisInfo)
        if (thisVerboseMode):
            print(thisInfo)

        thisLogger.LogMsgInfo(thisSeperator)
        if (thisVerboseMode):
            print(thisSeperator)
    # Console mode.
    else:
        thisCommLine.invoke()

        thisInfo = "INFO:  " + __appversion__ + " (console mode) EXIT"
        thisLogger.LogMsgInfo(thisInfo)
        if (thisVerboseMode):
            print(thisInfo)

        thisLogger.LogMsgInfo(thisSeperator)
        if (thisVerboseMode):
            print(thisSeperator)

    if ( thisGlobalConfig.isExitSuccess() ):
        sys.exit(0)
    else:
        sys.exit(-1)

######################################################################
# If called from the command line, invoke thyself!
######################################################################

if __name__=='__main__': main(sys.argv)

######################################################################
