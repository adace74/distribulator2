######################################################################
#
# $Id$
#
# (c) Copyright 2003 Adam W. Dace <adam@turing.com>  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################

# Pydoc comments
"""This class is the base abstract class for all runtime modes."""

# Version tag
__version__= '$Revision$'[11:-2]

# Standard modules

# Custom modules

######################################################################

class Mode:
    """This class is the base abstract class for all runtime modes."""

    def __init__(self, PassedGlobalConfig):
        """Constructor."""

        pass

######################################################################

    def invoke(self):
        """This method is the main entry point into tons of custom logic."""
        
        pass

######################################################################
