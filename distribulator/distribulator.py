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
######################################################################

# Import modules we'll need.
try:
    import getopt
    import socket
    import sys

except ImportError:
    print "An error occured while loading Python modules, exiting..."
    exit(1)

# Display a nice pretty header.
def title_header():
    print "The Distribulator v0.10"
    print "-----------------------"
    print

def info_header():
    print "Python Version: " + sys.version
    print "Local Hostname: " + socket.gethostname()

# Good old main...
def main(argv):
    short_options = ':e:s:'
    long_options = ['env=',
                    'shell=']

    usage = """Usage: %s [options] --env=environment

The available options are:

    -e / --env=
    Set the server environment we wish to operate in.

    -s / --shell=
    Sets the remote shell type we wish to use.  Defaults to ssh.
    Not fully implemented.  OPTIONAL

""" % argv[0]

    title_header()

    try:
        if len(argv) < 2:
            print "ERROR: I need to know which environment I am to use!"
            print
            raise "CommandLineError"

        optlist, args = getopt.getopt(sys.argv[1:], short_options, long_options)

        if len(optlist) > 0:
            # Set the sane defaults
            server_env=''
            server_shell='ssh'

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

    info_header()
#
# If called from the command line, invoke thyself!
#
if __name__=='__main__': main(sys.argv)
