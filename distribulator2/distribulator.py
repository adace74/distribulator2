#!/usr/local/bin/python
######################################################################
#
# $Id$
#
# Description: The Distribulator.
# A detailed description can be found in the README file.
#
# (c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
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
__appversion__ = 'The Distribulator v0.7.1'

# Standard modules
import commands
import getopt
import getpass
import os
import os.path
import socket
import sys

# Custom modules
import engine.conf.ConfigLoader
import engine.data.GlobalConfig
import engine.misc.MultiLogger
import engine.mode.BatchMode
import engine.mode.ConsoleMode
import engine.mode.ListMode
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

    --list=[host1, host2, ...] | [servergroup1, servergroup2, ...]
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

    myBatchFile = ''
    myConfigFile = ''
    myInstallDir = '/tmp'
    myQuietMode = False
    myRequestedList = ''
    myServerEnv = 'demo'
    myVar1 = ''
    myVar2 = ''
    myVar3 = ''
    myVerboseMode = False

    try:
        if len(argv) < 2:
            print("ERROR: I need to know which environment I am to use!")
            raise "CommandLineError"

        optlist, args = getopt.getopt(sys.argv[1:], short_options, long_options)

        if len(optlist) > 0:
            for opt in optlist:
                if (opt[0] == '--batch'):
                    myBatchFile = opt[1]
                elif (opt[0] == '--config'):
                    myConfigFile = opt[1]
                elif (opt[0] == '--directory'):
                    myInstallDir = opt[1]
                elif (opt[0] == '--env'):
                    myServerEnv = opt[1]
                elif (opt[0] == '--help'):
                    print(usage)
                    sys.exit(False)
                elif (opt[0] == '--?'):
                    print(usage)
                    sys.exit(False)
                elif (opt[0] == '--list'):
                    myRequestedList = opt[1]
                elif (opt[0] == '--quiet'):
                    myQuietMode = True
                elif (opt[0] == '--var1'):
                    myVar1 = opt[1]
                elif (opt[0] == '--var2'):
                    myVar2 = opt[1]
                elif (opt[0] == '--var3'):
                    myVar3 = opt[1]
                elif (opt[0] == '--version'):
                    print(__appversion__)
                    print("(c) Copyright 2004 Adam W. Dace <adam@turing.com>  All Rights Reserved.")
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
        myGlobalConfig = engine.data.GlobalConfig.GlobalConfig()

        if ( len(myBatchFile) > 0 ):
            myGlobalConfig.setBatchMode(True)
            myGlobalConfig.setBatchFile(myBatchFile)
        else:
            myGlobalConfig.setBatchMode(False)

        if ( len(myRequestedList) > 0 ):
            myGlobalConfig.setListMode(True)
            myGlobalConfig.setRequestedList(myRequestedList)
        else:
            myGlobalConfig.setListMode(False)

        if ( (len(myBatchFile) == 0) & \
             (len(myRequestedList) == 0) ):
            myGlobalConfig.setConsoleMode(True)
        else:
            myGlobalConfig.setConsoleMode(False)

        if ( len(myConfigFile) > 0 ):
            myGlobalConfig.setConfigFile(myConfigFile)
        else:
            myGlobalConfig.setConfigFile( os.path.join(myInstallDir, 'conf/config.xml') )

        myGlobalConfig.setExitSuccess(True)
        myGlobalConfig.setHelpDir( os.path.join(myInstallDir, 'doc') )
        myGlobalConfig.setPassThruFile( os.path.join(myInstallDir, 'conf/pass_through_cmds.txt') )

        if ( myGlobalConfig.isBatchMode() ):
            myGlobalConfig.setQuietMode(myQuietMode)
        else:
            myGlobalConfig.setQuietMode(False)

        myGlobalConfig.setServerEnv(myServerEnv)
        myGlobalConfig.setUsername( getpass.getuser() )
        myGlobalConfig.setVar1(myVar1)
        myGlobalConfig.setVar2(myVar2)
        myGlobalConfig.setVar3(myVar3)
    
        if ( myGlobalConfig.isConsoleMode() ):
            printTitleHeader()
            printInfoHeader(myServerEnv, myGlobalConfig.getConfigFile())

        # These three really should be pinned to an interface.
        myBatchMode = engine.mode.BatchMode.BatchMode(myGlobalConfig)
        myCommLine = engine.mode.ConsoleMode.ConsoleMode(myGlobalConfig)
        myListModeer = engine.mode.ListMode.ListMode(myGlobalConfig)

        myLoader = engine.conf.ConfigLoader.ConfigLoader(myGlobalConfig)
        myGlobalConfig = myLoader.load(myCommLine)

        # Currently not using the MultiLogger here as we log based on a different set of criteria
        # than it is aware of.
        if ( myGlobalConfig.isBatchMode() & \
             (myGlobalConfig.isQuietMode() == False) ):
            myVerboseMode = True

        # Setup syslog and console output handle.
        mySysLogger = generic.SysLogger.SysLogger(myGlobalConfig.getSyslogFacility(), 'distribulator.py')
        myGlobalConfig.setSysLogger(mySysLogger)
        myMultiLogger = engine.misc.MultiLogger.MultiLogger(myGlobalConfig)
        myGlobalConfig.setMultiLogger(myMultiLogger)

        # Log our startup.
        myStatus, myOutput = commands.getstatusoutput( \
            myGlobalConfig.getLognameBinary())

        if ( myStatus == 0 ):
            myGlobalConfig.setRealUsername(myOutput)
        else:
            myGlobalConfig.setRealUsername( getpass.getuser() )

        # Define a pretty seperator.
        mySeperator = '----------------------------------------------------------------------'
        mySysLogger.LogMsgInfo(mySeperator)
        if (myVerboseMode):
            print(mySeperator)

        if (myGlobalConfig.isBatchMode()):
            myInfo = "INFO:  " + __appversion__ + " (batch mode) START"
            if (myVerboseMode):
                print(myInfo)
        elif (myGlobalConfig.isListMode()):
            myInfo = "INFO:  " + __appversion__ + " (list mode) START"
        else:
            myInfo = "INFO:  " + __appversion__ + " (console mode) START"
        mySysLogger.LogMsgInfo(myInfo)

        myInfo = "INFO:  Real UID: " + myGlobalConfig.getRealUsername() + \
                   " | " + \
                   "Effective UID: " + myGlobalConfig.getUsername() + \
                   " | " + \
                   "Environment: " + myServerEnv

        mySysLogger.LogMsgInfo(myInfo)
        if (myVerboseMode):
            print(myInfo)

    except (EOFError, KeyboardInterrupt):
            myError = "ERROR: Caught CTRL-C / CTRL-D keystroke.  Exiting..."
            mySysLogger.LogMsgError(myError)
            if (myVerboseMode):
                print(myError)

            sys.exit(True)

    # Batch mode.
    if ( myGlobalConfig.isBatchMode() ):
        myBatchMode.invoke()

        myInfo = "INFO:  " + __appversion__ + " (batch mode) EXIT"
        mySysLogger.LogMsgInfo(myInfo)
        if (myVerboseMode):
            print(myInfo)

        mySysLogger.LogMsgInfo(mySeperator)
        if (myVerboseMode):
            print(mySeperator)
    # List mode.
    elif ( myGlobalConfig.isListMode() ):
        myListModeer.invoke()

        myInfo = "INFO:  " + __appversion__ + " (list mode) EXIT"
        mySysLogger.LogMsgInfo(myInfo)
    # Console mode.
    else:
        myCommLine.invoke()

        myInfo = "INFO:  " + __appversion__ + " (console mode) EXIT"
        mySysLogger.LogMsgInfo(myInfo)
        if (myVerboseMode):
            print(myInfo)

        mySysLogger.LogMsgInfo(mySeperator)
        if (myVerboseMode):
            print(mySeperator)

    if ( myGlobalConfig.isExitSuccess() ):
        sys.exit(False)
    else:
        sys.exit(True)

######################################################################
# If called from the command line, invoke thyself!
######################################################################

if __name__=='__main__': main(sys.argv)

######################################################################
