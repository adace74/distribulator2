######################################################################
#
# $Id$
#
# Name: XMLParser.py
#
######################################################################

# Version tag
__version__= '$Revision$'[11:-2]

try:
    # Standard modules
    import os
    import os.path
    import string
    import sys
    import xml.dom.minidom

    # Custom modules
    import engine.data.GlobalConfig

except ImportError:
    print "An error occured while loading Python modules, exiting..."
    sys.exit(1)

######################################################################

class XMLFileParser:

    def parse(self, PassedGlobalConfig):

        thisFilename = os.path.join(PassedGlobalConfig.getConfigDir(), \
                                    'config.xml')

        try:
            thisDom = xml.dom.minidom.parse(thisFilename)

        except IOError, (errno, strerror):
            print "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename)
            sys.exit(1)

        #handleConfig(thisDom)

    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                return rc

    def handleConfig(self, PassedConfig):
        handleBinaries(PassedConfig.getElementsByTagName("binaries")[0])

    def handleBinaries(self, PassedBinaries):
        print "Blah"

######################################################################
