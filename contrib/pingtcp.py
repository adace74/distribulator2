#!/usr/local/bin/python
######################################################################
#
# $Id$
#
# Description:  Small script that will connect to a given TCP port
# on a given host and return success or failure status.
#
# (c) Copyright 2003 Orbitz, Inc.  All rights reserved.
#
######################################################################

# Pydoc comments
"""Application entry point for pingtcp."""

# File version tag
__version__ = '$Revision$'[11:-2]

# Standard modules
import getopt
import os
import os.path
import sys
import socket

######################################################################
# Good old main...
######################################################################

def main(argv):
    """Good old main."""

    short_options = ['']
    long_options = ['banner=',
                    'port=',
                    'help',
                    'quiet',
                    'timeout=',
                    'version',
                    '?']

    usage = """Usage: %s [OPTION] HOSTNAME

This script attempts to contact a given HOSTNAME at a given TCP/IP port.
Using a specified second timeout, it attempts to connect to the remote
HOSTNAME and TCP_PORT.  Optionally, it will read a "banner" from the
remote service and return error conditions based on whether it considers
the transaction a success or failure.

The available options are:

    --banner=MATCH_STRING
    Specifies that in order to achieve success, the remote service
    must return a banner containing the string we specify.
    OPTIONAL

    --help
    Prints the usage statement.
    OPTIONAL

    --port=TCP_PORT
    Specifies which port on the remote host we're to test.
    Default: 22
    OPTIONAL

    --quiet
    Specifies that we want only an exit code, and no STDOUT output.
    OPTIONAL

    --timeout=TIMEOUT
    Specifies the socket-level timeout in seconds.
    Default: 10
    OPTIONAL

    --version
    Prints the version banner.
    OPTIONAL

Exit Status Codes:
------------------
0 = Success
1 = Socket error type 1.
2 = Socket error type 2.
3 = Socket error type 3.
4 = Socket timeout during connect() / recv().
5 = Unknown exception caught.
6 = Received non-matching or zero-length service banner.

Examples:
---------
pingtcp.py --banner=OpenSSH --timeout=20 egg02.eg.orbitz.com
pingtcp.py --banner=ESMTP --port=25 mailgw01st.eg.orbitz.com
""" % argv[0]

    version = """pingtcp.py v%s
Application Layer-based TCP Ping Script
(c) Copyright 2004 Orbitz, Inc.  All rights reserved.
-----------------------------------------------------
""" % __version__

######################################################################
# Variable initialization.
######################################################################

    # Default to SSH service.
    myBannerMode=0
    myBannerString=''
    myHostname=''
    myPortNum=22
    myTimeout=10
    myQuietMode=0

######################################################################
# Main logic flow.
######################################################################

    try:
        if len(argv) < 2:
            raise "CommandLineError"

        optlist, args = \
                 getopt.getopt(sys.argv[1:], short_options, long_options)

        if len(optlist) > 0:
            for opt in optlist:
                if (opt[0] == '--banner'):
                    myBannerMode=1
                    myBannerString=opt[1]
                elif (opt[0] == '--help'):
                    print(version)
                    print(usage)
                    sys.exit(0)
                elif (opt[0] == '--port'):
                    myPortNum = int(opt[1])
                elif (opt[0] == '--quiet'):
                    myQuietMode=1
                elif (opt[0] == '--timeout'):
                    myTimeout = int(opt[1])
                elif (opt[0] == '--version'):
                    print(version)
                    sys.exit(0)
                elif (opt[0] == '--?'):
                    print(version)
                    print(usage)
                    sys.exit(0)

        if len(args) > 0:
            myHostname = args[0]

    except "CommandLineError":
        print(version)
        print("ERROR: Invalid argument or flag found.  Please check your syntax.")
        print("ERROR: Please run again with the --help flag for more information.")
        sys.exit(1)

    except getopt.GetoptError:
        print(version)
        print("ERROR: Invalid argument or flag found.  Please check your syntax.")
        print("ERROR: Please run again with the --help flag for more information.")
        sys.exit(1)

    if (myQuietMode == 0):
        print(version)

    try:
        mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        mySocket.settimeout(myTimeout)
        mySocket.connect( (myHostname, myPortNum) )

        # Check for a banner if specified.
        if (myBannerMode == 1):
            myString = mySocket.recv(1024)

            if (myQuietMode == 0):
                sys.stdout.write("INFO:  Received remote service header: %d bytes.\n" % len(myString))

            if (len(myString) < 1):
                if (myQuietMode == 0):
                    sys.stderr.write("ERROR: Received zero-length remote service header!\n")
                    sys.exit(6)

            if (myString.find(myBannerString) == -1):
                sys.stderr.write("ERROR: Received non-matching service banner!\n")
                sys.exit(6)

        mySocket.close()

        if (myQuietMode == 0):
            sys.stdout.write("INFO:  Success!\n")

        sys.exit(0)

    except socket.error, myErrorInfo:
        if (myQuietMode == 0):
            sys.stderr.write("ERROR: OS Reports: [%s] while connecting to remote host.\n" % (myErrorInfo))
            sys.stderr.write("ERROR: Server '" + myHostname + "' appears to be down.\n")
        sys.exit(1)

    except socket.herror, (errno, strerror):
        if (myQuietMode == 0):
            sys.stderr.write("ERROR: OS Reports: [Errno %s, %s]\n" % (errno, strerror))
            sys.stderr.write("ERROR: Server '" + myHostname + "' appears to be down.\n")
        sys.exit(2)

    except socket.gaierror, (errno, strerror):
        if (myQuietMode == 0):
            sys.stderr.write("ERROR: OS Reports: [Errno %s, %s]\n" % (errno, strerror))
            sys.stderr.write("ERROR: Server '" + myHostname + "' appears to be down.\n")
        sys.exit(3)

    except socket.timeout:
        if (myQuietMode == 0):
            sys.stderr.write("ERROR: Socket timed out while connecting to server.\n")
            sys.stderr.write("ERROR: Server '" + myHostname + "' appears to be down.\n")
        sys.exit(4)

    except SystemExit:
        sys.exit(0)

    except:
        if (myQuietMode == 0):
            sys.stderr.write("ERROR: %s\n" % sys.exc_info()[0])
            sys.stderr.write("ERROR: Server '" + myHostname + "' appears to be down.\n")
        sys.exit(5)

######################################################################
# If called from the command line, invoke thyself!
######################################################################

if __name__=='__main__': main(sys.argv)

######################################################################
