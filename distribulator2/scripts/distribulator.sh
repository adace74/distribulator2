#!/bin/sh
#
# $Id$
#
# Description:  This script acts as a wrapper for calling the python program proper.
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
INSTALL_DIR="/usr/local/distribulator2"

$INSTALL_DIR/distribulator.py --directory=$INSTALL_DIR $1 $2 $3 $4 $5 $6 $7 $8
