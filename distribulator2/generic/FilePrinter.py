######################################################################
#
# $Id$
#
# Name: FilePrinter.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import sys

except ImportError:
    print("An error occured while loading Python modules, exiting...")
    sys.exit(1)

######################################################################

class FilePrinter:

    def printFile(self, PassedFilename):
        try:
            thisFile = open(PassedFilename, 'r')
            
            for thisLine in thisFile:
                thisLine = thisLine.strip()
                print(thisLine)

            thisFile.close()

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, PassedFilename))
            return False

        return True

######################################################################
