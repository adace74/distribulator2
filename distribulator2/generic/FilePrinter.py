######################################################################
#
# $Id$
#
# Name: FilePrinter.py
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import sys

######################################################################

class FilePrinter:

    def printFile(self, PassedFilename):
        try:
            thisFile = open(PassedFilename, 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.rstrip()
                print(thisLine)

            thisFile.close()

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, PassedFilename))
            return False

        return True

######################################################################
