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
__appversion__ = 'The Distribulator v0.6.3'

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
import engine.MultiLogger
import engine.ServerLister
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
    print("---------------------------------------------------")
    print

######################################################################

def printInfoHeader(PassedServerEnv, PassedConfigFile):
    """Print the informational header."""

    print("Local Hostname:      " + socket.gethostname())
    print("Current Environment: " + PassedServerEnv)
    print("Config File:         " + PassedConfigFile)
    print

######################################################################
# Good old main...
######################################################################

def main(argv):
    """Good old main."""

    short_options = ['']
    long_options = ['batch=',
                    'config=',
                    'directory=',
                    'env=',
                    'help',
                    'list=',
                    'quiet',
                    'var1=',
                    'var2=',
                    'var3=',
                    'version',
                    '?']

    usage = """
Usage: %s [options] --env=environment

The available options are:

    --batch=batch_filename
    Enables batch mode processing, requires a readable input file.
    OPTIONAL

    --config=config_filename
    Specifies the location of the global XML-based configuraiton file.
    OPTIONAL

    --directory=install_dir
    Allows the wrapper script to pass in the install location.
    This is a simple workaround to avoid installing our application
    into the Python system class path.
    REQUIRED

    --env=env_name
    The server environment we wish to operate in.
    REQUIRED

    --help
    This usage statement.
    OPTIONAL

    --list=[host1,host2,...] | [servergroup1,servergroup2,...]
    Enables serer "listing", outputs all given username@hostname pairs
    for a given set of hosts or server groups.
    OPTIONAL

    --quiet
    Batch Mode Only: Disable STDOUT, particularly useful when run from cron.
    OPTIONAL

    --var1=some_string
    --var2=some_other_string
    --var3=you_get_the_idea
    Batch Mode Only: Enables simple string substitution.
    Up to 3 variables may be defined then referenced in a given batch file
    as $var1, $var2, and $var3.
    OPTIONAL

    --version
    Print version information.
""" % argv[0]

    thisBatchFile = ''
    thisConfigFile = ''
    thisInstallDir = '/tmp'
    thisQuietMode = False
    thisRequestedList = ''
    thisServerEnv = 'demo'
    thisVar1 = ''
    thisVar2 = ''
    thisVar3 = ''
    thisVerboseMode = False

    try:
        if len(argv) < 2:
            print("ERROR: I need to know which environment I am to use!")
            raise "CommandLineError"

        optlist, args = getopt.getopt(sys.argv[1:], short_options, long_options)

        if len(optlist) > 0:
            for opt in optlist:
                if (opt[0] == '--batch'):
                    thisBatchFile = opt[1]
                elif (opt[0] == '--config'):
                    thisConfigFile = opt[1]
                elif (opt[0] == '--directory'):
                    thisInstallDir = opt[1]
                elif (opt[0] == '--env'):
                    thisServerEnv = opt[1]
                elif (opt[0] == '--help'):
                    print(usage)
                    sys.exit(False)
                elif (opt[0] == '--?'):
                    print(usage)
                    sys.exit(False)
                elif (opt[0] == '--list'):
                    thisRequestedList = opt[1]
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
                    print("(c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved.")
                    print
                    print("Please see the LICENSE file for accompanying legalese.")
                    print
                    sys.exit(False)
        else:
            print("ERROR: getopt failure!  This shouldn't ever happen!")
            print
            raise "CommandLineError"

    except "CommandLineError":
        print(usage)
        sys.exit(True)

    except getopt.GetoptError:
        print("ERROR: Erroneous flag(s) given.  Please check your syntax.")
        print(usage)
        sys.exit(True)

    try:
        # Load up our GlobalConfig object.
        thisGlobalConfig = engine.data.GlobalConfig.GlobalConfig()

        if ( len(thisBatchFile) > 0 ):
            thisGlobalConfig.setBatchMode(True)
            thisGlobalConfig.setBatchFile(thisBatchFile)
        else:
            thisGlobalConfig.setBatchMode(False)

        if ( len(thisRequestedList) > 0 ):
            thisGlobalConfig.setListMode(True)
            thisGlobalConfig.setRequestedList(thisRequestedList)
        else:
            thisGlobalConfig.setListMode(False)

        if ( (len(thisBatchFile) == 0) & \
             (len(thisRequestedList) == 0) ):
            thisGlobalConfig.setConsoleMode(True)
        else:
            thisGlobalConfig.setConsoleMode(False)

        if ( len(thisConfigFile) > 0 ):
            thisGlobalConfig.setConfigFile(thisConfigFile)
        else:
            thisGlobalConfig.setConfigFile( os.path.join(thisInstallDir, 'conf/config.xml') )

        thisGlobalConfig.setExitSuccess(True)
        thisGlobalConfig.setHelpDir( os.path.join(thisInstallDir, 'doc') )
        thisGlobalConfig.setPassThruFile( os.path.join(thisInstallDir, 'conf/pass_through_cmds.txt') )

        if ( thisGlobalConfig.isBatchMode() ):
            thisGlobalConfig.setQuietMode(thisQuietMode)
        else:
            thisGlobalConfig.setQuietMode(False)

        thisGlobalConfig.setServerEnv(thisServerEnv)
        thisGlobalConfig.setUsername( getpass.getuser() )
        thisGlobalConfig.setVar1(thisVar1)
        thisGlobalConfig.setVar2(thisVar2)
        thisGlobalConfig.setVar3(thisVar3)
    
        if ( thisGlobalConfig.isConsoleMode() ):
            printTitleHeader()
            printInfoHeader(thisServerEnv, thisGlobalConfig.getConfigFile())

        # These three really should be pinned to an interface.
        thisBatchRunner = engine.BatchRunner.BatchRunner(thisGlobalConfig)
        thisCommLine = engine.CommandLine.CommandLine(thisGlobalConfig)
        thisServerLister = engine.ServerLister.ServerLister(thisGlobalConfig)

        thisLoader = engine.ConfigLoader.ConfigLoader(thisGlobalConfig)
        thisGlobalConfig = thisLoader.load(thisCommLine)

        # Currently not using the MultiLogger here as we log based on a different set of criteria
        # than it is aware of.
        if ( thisGlobalConfig.isBatchMode() & \
             (thisGlobalConfig.isQuietMode() == False) ):
            thisVerboseMode = True

        # Setup syslog and console output handle.
        thisSysLogger = generic.SysLogger.SysLogger(thisGlobalConfig.getSyslogFacility(), 'distribulator.py')
        thisGlobalConfig.setSysLogger(thisSysLogger)
        thisMultiLogger = engine.MultiLogger.MultiLogger(thisGlobalConfig)
        thisGlobalConfig.setMultiLogger(thisMultiLogger)

        # Log our startup.
        thisStatus, thisOutput = commands.getstatusoutput( \
            thisGlobalConfig.getLognameBinary())

        if ( thisStatus == 0 ):
            thisGlobalConfig.setRealUsername(thisOutput)
        else:
            thisGlobalConfig.setRealUsername( getpass.getuser() )

        # Define a pretty seperator.
        thisSeperator = '----------------------------------------------------------------------'
        thisSysLogger.LogMsgInfo(thisSeperator)
        if (thisVerboseMode):
            print(thisSeperator)

        if (thisGlobalConfig.isBatchMode()):
            thisInfo = "INFO:  " + __appversion__ + " (batch mode) START"
            if (thisVerboseMode):
                print(thisInfo)
        elif (thisGlobalConfig.isListMode()):
            thisInfo = "INFO:  " + __appversion__ + " (list mode) START"
        else:
            thisInfo = "INFO:  " + __appversion__ + " (console mode) START"
        thisSysLogger.LogMsgInfo(thisInfo)

        thisInfo = "INFO:  Real UID: " + thisGlobalConfig.getRealUsername() + \
                   " | " + \
                   "Effective UID: " + thisGlobalConfig.getUsername() + \
                   " | " + \
                   "Environment: " + thisServerEnv

        thisSysLogger.LogMsgInfo(thisInfo)
        if (thisVerboseMode):
            print(thisInfo)

    except (EOFError, KeyboardInterrupt):
            thisError = "ERROR: Caught CTRL-C / CTRL-D keystroke.  Exiting..."
            thisSysLogger.LogMsgError(thisError)
            if (thisVerboseMode):
                print(thisError)

            sys.exit(True)

    # Batch mode.
    if ( thisGlobalConfig.isBatchMode() ):
        thisBatchRunner.invoke()

        thisInfo = "INFO:  " + __appversion__ + " (batch mode) EXIT"
        thisSysLogger.LogMsgInfo(thisInfo)
        if (thisVerboseMode):
            print(thisInfo)

        thisSysLogger.LogMsgInfo(thisSeperator)
        if (thisVerboseMode):
            print(thisSeperator)
    # List mode.
    elif ( thisGlobalConfig.isListMode() ):
        thisServerLister.invoke()

        thisInfo = "INFO:  " + __appversion__ + " (list mode) EXIT"
        thisSysLogger.LogMsgInfo(thisInfo)
    # Console mode.
    else:
        thisCommLine.invoke()

        thisInfo = "INFO:  " + __appversion__ + " (console mode) EXIT"
        thisSysLogger.LogMsgInfo(thisInfo)
        if (thisVerboseMode):
            print(thisInfo)

        thisSysLogger.LogMsgInfo(thisSeperator)
        if (thisVerboseMode):
            print(thisSeperator)

    if ( thisGlobalConfig.isExitSuccess() ):
        sys.exit(False)
    else:
        sys.exit(True)

######################################################################
# If called from the command line, invoke thyself!
######################################################################

if __name__=='__main__': main(sys.argv)

######################################################################
