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

# Import modules we'll need.
try:
    import getopt
    import os
    import os.path
    import socket
    import sys

except ImportError:
    print "An error occured while loading Python modules, exiting..."
    exit(1)

# Define global variables(how global are they?)
install_dir = os.getcwd()
install_conf = os.path.join(os.getcwd(), 'conf')
server_shell = 'ssh'

# Display a nice pretty header.
def title_header():
    print
    print "The Distribulator v0.10"
    print "-----------------------"
    print

def info_header(server_env):
    print "Python Version:      " + sys.version.split()[0]
    print "Local Install Dir:   " + install_dir
    print "Local Config Dir:    " + install_conf
    print "Local Hostname:      " + socket.gethostname()
    print "Current Environment: " + server_env
    print
    print "Internal Commands: 0"
    print "External Commands: 0"
    print "Server Groups: all"

# Good old main...
def main(argv):
    short_options = ':e:s:'
    long_options = ['env=',
                    'shell=']

    usage = """Usage: %s [options] --env=environment

The available options are:

    -b / --batch=filename
    Enables batch mode processing, requires a readable input file.
    Not yet implemented.  OPTIONAL

    -e / --env=
    Set the server environment we wish to operate in.

    -s / --shell=
    Sets the remote shell type we wish to use.  Defaults to ssh.
    Not yet implemented.  OPTIONAL

""" % argv[0]

    title_header()

    try:
        if len(argv) < 2:
            print "ERROR: I need to know which environment I am to use!"
            print
            raise "CommandLineError"

        optlist, args = getopt.getopt(sys.argv[1:], short_options, long_options)

        if len(optlist) > 0:
            for opt in optlist:
                if (opt[0] == '-e') or (opt[0] == '--env'):
                    server_env = opt[1]
                elif (opt[0] == '-s') or (opt[0] == '--shell'):
                    server_shell = opt[1]

            # Verify that we got what we need
            if not server_env:
                print "ERROR: I need to know which environment I am to use!"
                print
                raise "CommandLineError"

        else:
            print "ERROR: getopt failure!  This shouldn't even happen!"
            print
            raise "CommandLineError"

    except "CommandLineError":
        sys.stderr.write(usage)
        sys.exit(1)

    info_header(server_env)
#
# If called from the command line, invoke thyself!
#
if __name__=='__main__': main(sys.argv)
