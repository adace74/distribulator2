######################################################################
#
# $Id$
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is responsible for pre-checking XML configuration file well-formedness."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules
import logging
import os
import os.path

# XML Well-formedness recipe modules.
import xml.parsers.expat
from glob import glob
import sys

# Custom modules
import engine.data.GlobalConfig

######################################################################

class XMLFileChecker:
    """This class is responsible for pre-checking XML configuration file well-formedness."""

    def __init__(self):
        """Constructor."""

        pass

######################################################################

    def check(self, PassedGlobalConfig):
        """This method represents the main entry point into the XML check logic."""

        self._globalConfig = PassedGlobalConfig

        myFilename = self._globalConfig.getAppConfigFile()

        try:
            parser = xml.parsers.expat.ParserCreate()
            parser.ParseFile(open(myFilename, "r"))

        except IOError, (errno, strerror):
            print("ERROR: [Errno %s] %s: %s" % (errno, strerror, myFilename))
            sys.exit(True)

        except Exception, myException:
            print("ERROR: XML configuration file is not well-formed!")
            print("ERROR: %s" % myException)
            sys.exit(True)

######################################################################
