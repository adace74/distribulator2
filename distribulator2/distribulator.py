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

# Import modules
try:
    # Standard modules
    import getopt
    import getpass
    import os
    import os.path
    import socket
    import sys
    import syslog

    # Custom modules
    import engine.CommandLine
    import engine.ConfigLoader
    import engine.data.GlobalConfig
    import generic.SysLogger

except ImportError:
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

# Display a nice pretty header.
def printTitleHeader():
    print
    print("The Distribulator v0.50")
    print("-----------------------")
    print

def printInfoHeader(PassedServerEnv, PassedConfigDir):
    print("Python Version:      " + sys.version.split()[0])
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
    Not yet implemented.
    OPTIONAL

    -d / --directory=start_dir
    Allows the wrapper script to pass in the user's real cwd.
    OPTIONAL

    -e / --env=
    Set the server environment we wish to operate in.
    REQUIRED

    -h / --help
    This usage statement.

    -s / --shell=
    Sets the remote shell type we wish to use.  Defaults to ssh.
    Not yet implemented.
    OPTIONAL

    -v / --version
    Print version information.

""" % argv[0]

    thisServerEnv = 'sample'
    thisServerShell = 'ssh'
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
                elif (opt[0] == '-s') or (opt[0] == '--shell'):
                    thisServerShell = opt[1]
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

    # Future batch check goes here.
    printTitleHeader()

    thisConfigDir = os.path.join(os.getcwd(), 'conf')
    thisHelpDir = os.path.join(os.getcwd(), 'doc')

    printInfoHeader(thisServerEnv, thisConfigDir)

    # Load up our GlobalConfig object.
    thisGlobalConfig = engine.data.GlobalConfig.GlobalConfig()
    thisGlobalConfig.setConfigDir(thisConfigDir)
    thisGlobalConfig.setHelpDir(thisHelpDir)
    thisGlobalConfig.setServerEnv(thisServerEnv)

    thisCommLine = engine.CommandLine.CommandLine(thisGlobalConfig)
    thisLoader = engine.ConfigLoader.ConfigLoader(thisGlobalConfig)
    thisGlobalConfig = thisLoader.loadGlobalConfig(thisCommLine)

    # Log our startup.
    thisLogger = generic.SysLogger.SysLogger(syslog.LOG_LOCAL1)
    thisLogger.LogMsgInfo("Started by user " + getpass.getuser() + '.')

    # Try to chdir() to thisStartDir if possible.
    try:
        os.chdir(thisStartDir)

    except OSError, (errno, strerror):
        print("ERROR: [Errno %s] %s: %s" % (errno, strerror, thisTokens[1]))

    # The main readline loop.
    thisCommLine.invoke()

    # Once it returns, we're done!
    thisLogger.LogMsgInfo("Shutting down...")
    sys.exit(0)

######################################################################
#
# If called from the command line, invoke thyself!
#
######################################################################
if __name__=='__main__': main(sys.argv)
