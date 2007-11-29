######################################################################
#
# $Id: Parser.py 23 2005-10-14 21:20:52Z awd $
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved.
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is the base abstract class for all parser subclasses."""

# Version tag
__version__= '$Revision: 23 $'[11:-2]

# Standard modules

# Custom modules

######################################################################

class Parser:
    """This class is the base abstract class for all runtime modes."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        pass

######################################################################

    def test(self, PassedString):
        """Unit testing function call."""

        pass

######################################################################

    def getParseTree(self, PassedString):
        """This method is responsible for parsing the given string and returning a parse tree to the caller."""

        pass

######################################################################
