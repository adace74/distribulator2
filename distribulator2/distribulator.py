#!/usr/bin/env python
######################################################################
#
# $Id$
#
# Name: distribulator.py
#
# Description: The Distribulator.
# A detailed description can be found in the README file.
#
# Notes: Unfortunately, Python, like other shell-oriented langauges,
# requires that methods be defined before calling them.
# As such, main() will always be at the -bottom- of a file.
#
# Flow:
# 1) Fire up / validation
# 2) Load up Server / ServerGroup objectsets.
# 3) Report Load Summary
# 4) Interactive Mode (Parser object, Command objects?)
#
# Server object -- contains server hostname, username
# ServerGroup object -- contains many Server objects
######################################################################

# Version tag
__version__ = '$Revision$'[11:-2]

# Standard modules
import commands
import getopt
import getpass
import os
import os.path
import socket
import sys
import syslog

# Custom modules
import engine.BatchRunner
import engine.CommandLine
import engine.ConfigLoader
import engine.data.GlobalConfig
import generic.SysLogger

######################################################################

# Display a nice pretty header.
def printTitleHeader():
    print
    print("The Distribulator v0.50 (Python v" + \
          sys.version.split()[0] + " / " + sys.platform + ")")
    print("--------------------------------------------------")
    print

def printInfoHeader(PassedServerEnv, PassedConfigDir):
    print("Local Hostname:      " + socket.gethostname())
    print("Current Environment: " + PassedServerEnv)
    print("Config Directory:    " + PassedConfigDir)
    print

# Good old main...
def main(argv):
    short_options = ':b:d:e:h:s:v:'
    long_options = ['batch=',
                    'directory=',
                    'env=',
                    'help',
                    'shell=',
                    'version']

    usage = """Usage: %s [options] --env=environment

The available options are:

    -b / --batch=filename
    Enables batch mode processing, requires a readable input file.
    OPTIONAL

    -d / --directory=start_dir
    Allows the wrapper script to pass in the user's real cwd.
    OPTIONAL

    -e / --env=
    Set the server environment we wish to operate in.
    REQUIRED

    -h / --help
    This usage statement.

    -v / --version
    Print version information.

""" % argv[0]

    thisBatchFile = ''
    thisServerEnv = 'demo'
    thisStartDir = '/tmp'

    try:
        if len(argv) < 2:
            print("ERROR: I need to know which environment I am to use!")
            print
            raise "CommandLineError"

        optlist, args = getopt.getopt(sys.argv[1:], short_options, long_options)

        if len(optlist) > 0:
            for opt in optlist:
                if (opt[0] == '-b') or (opt[0] == '--batch'):
                    thisBatchFile = opt[1]
                elif (opt[0] == '-d') or (opt[0] == '--directory'):
                    thisStartDir = opt[1]
                elif (opt[0] == '-e') or (opt[0] == '--env'):
                    thisServerEnv = opt[1]
                elif (opt[0] == '-h') or (opt[0] == '--help'):
                    sys.stdout.write(usage)
                    sys.exit(0)
                elif (opt[0] == '-v') or (opt[0] == '--version'):
                    print("The Distribulator v0.50")
                    print("Please see the LICENSE file for accompanying legalese.")
                    sys.exit(0)
        else:
            print("ERROR: getopt failure!  This shouldn't ever happen!")
            print
            raise "CommandLineError"

    except "CommandLineError":
        sys.stderr.write(usage)
        sys.exit(1)

    except getopt.GetoptError:
        print("ERROR: Erroneous flag(s) given.  Please check your syntax.")
        print
        sys.stderr.write(usage)
        sys.exit(1)

    try:
        thisConfigDir = os.path.join(os.getcwd(), 'conf')
        thisHelpDir = os.path.join(os.getcwd(), 'doc')

        # Load up our GlobalConfig object.
        thisGlobalConfig = engine.data.GlobalConfig.GlobalConfig()
        thisLogger = generic.SysLogger.SysLogger(syslog.LOG_LOCAL1)
        thisGlobalConfig.setSysLogger(thisLogger)

        if ( len(thisBatchFile) > 0 ):
            thisGlobalConfig.setBatchMode(True)
            thisGlobalConfig.setBatchFile(thisBatchFile)
        else:
            thisGlobalConfig.setBatchMode(False)

        thisGlobalConfig.setConfigDir(thisConfigDir)
        thisGlobalConfig.setHelpDir(thisHelpDir)
        thisGlobalConfig.setServerEnv(thisServerEnv)

        if ( thisGlobalConfig.isBatchMode() == False):
            printTitleHeader()
            printInfoHeader(thisServerEnv, thisConfigDir)

        thisBatchRunner = engine.BatchRunner.BatchRunner(thisGlobalConfig)
        thisCommLine = engine.CommandLine.CommandLine(thisGlobalConfig)
        thisLoader = engine.ConfigLoader.ConfigLoader(thisGlobalConfig)
        thisGlobalConfig = thisLoader.loadGlobalConfig(thisCommLine)

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

        if (thisGlobalConfig.isBatchMode()):
            thisLogger.LogMsgInfo("INFO:  Starting The Distribulator v0.50 -- batch mode.")
        else:
            thisLogger.LogMsgInfo("INFO:  Starting The Distribulator v0.50 -- console mode.")

        thisLogger.LogMsgInfo("INFO:  Real UID:      " +
                              thisGlobalConfig.getRealUsername())
        thisLogger.LogMsgInfo("INFO:  Effective UID: " + \
                              thisGlobalConfig.getUsername())
        thisLogger.LogMsgInfo("INFO:  Environment:   " + \
                              thisServerEnv)

        thisLogger.LogMsgInfo(thisSeperator)

    except (EOFError, KeyboardInterrupt):
            thisError = "ERROR: Caught CTRL-C / CTRL-D keystroke.  Exiting..."
            print(thisError)
            thisLogger.LogMsgError(thisError)
            sys.exit(1)

    # Try to chdir() to thisStartDir if possible.
    try:
        os.chdir(thisStartDir)

    except OSError, (errno, strerror):
        thisError = "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisTokens[1])
        print(thisError)
        thisLogger.LogMsgError(thisError)

    # The main readline loop.
    if ( thisGlobalConfig.isBatchMode() ):
        if ( thisBatchRunner.invoke() ):
            thisLogger.LogMsgInfo(
                "INFO:  Batch command set completed successfully.  Shutting down.")
            sys.exit(0)
        else:
            thisLogger.LogMsgError(
                "ERROR: Shutting down as a result of a previous error.")
            sys.exit(1)
    else:
        if ( thisCommLine.invoke() ):
            thisLogger.LogMsgInfo("INFO:  Console user requested exit.  Shutting down.")
            sys.exit(0)
        else:
            thisLogger.LogMsgError(
                "ERROR: Shutting down as a result of a previous error.")
            sys.exit(1)

######################################################################
#
# If called from the command line, invoke thyself!
#
######################################################################
if __name__=='__main__': main(sys.argv)
