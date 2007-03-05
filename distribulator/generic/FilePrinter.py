######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved.
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""
Simple generic class whose funciton is to take a given file and
print it out to STDOUT.
"""

# Version tag
__version__= '$Revision$'[11:-2]

######################################################################

class FilePrinter:
    """
    Simple generic class whose funciton is to take a given file and
    print it out to STDOUT.
    """

    def printFile(self, PassedFilename):
        """Prints a given file."""

        try:
            myFile = open(PassedFilename, 'r')

            for myLine in myFile:
                myLine = myLine.rstrip()
                print(myLine)

            myFile.close()

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, PassedFilename))
            return False

        return True

######################################################################
