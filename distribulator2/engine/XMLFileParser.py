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
        self.thisGlobalConfig = PassedGlobalConfig

        thisFilename = os.path.join(self.thisGlobalConfig.getConfigDir(), \
                                    'config.xml')

        try:
            thisDom = xml.dom.minidom.parse(thisFilename)

        except IOError, (errno, strerror):
            print "ERROR: [Errno %s] %s: %s" % (errno, strerror, thisFilename)
            sys.exit(1)

        self.handleConfig(thisDom)

        return self.thisGlobalConfig

    # Gotta clean this up some day...
    def getText(self, nodelist):
        rc = ""
        for node in nodelist:
            if node.nodeType == node.TEXT_NODE:
                rc = rc + node.data
                return rc

    def handleConfig(self, PassedConfig):
        self.handleBinary(PassedConfig.getElementsByTagName("binary")[0])
        self.handleLogging(PassedConfig.getElementsByTagName("logging")[0])

    # Binary locations.
    def handleBinary(self, PassedBinary):
        self.handleScp(PassedBinary.getElementsByTagName("scp")[0])
        self.handleSsh(PassedBinary.getElementsByTagName("ssh")[0])

    def handleScp(self, PassedScp):
        self.thisGlobalConfig.setScpBinary( self.getText(PassedScp.childNodes) )

    def handleSsh(self, PassedSsh):
        self.thisGlobalConfig.setSshBinary( self.getText(PassedSsh.childNodes) )

    # Logging options.
    def handleLogging(self, PassedLogging):
        self.handleFacility(PassedLogging.getElementsByTagName("facility")[0])

    def handleFacility(self, PassedFacility):
        self.thisGlobalConfig.setSyslogFacility( self.getText(PassedFacility.childNodes) )

######################################################################
