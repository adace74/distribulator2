#!/bin/sh
######################################################################
#
# $Id$
#
# Description:  Creates distribution tar/gzip archives.
#
# (c) Copyright 2004 Orbitz, Inc.  All Rights Reserved. 
# Please see the accompanying LICENSE file for license information.
#
######################################################################
#
# Sourcecode location.
#
CVSWORK_DIR="."
PROJECT_DIR="distribulator2"
PROJECT_NAME="distribulator"
#
# Binary locations.
#
FIND_BIN="/usr/bin/find"
RM_BIN="/bin/rm"
TAR_BIN="/usr/bin/tar"
XARGS_BIN="/usr/bin/xargs"
#
# Make sure the user passed in a version to package.
#
if [ $# -lt 1 ]; then
	echo "ERROR: Please specify a version to package."

	exit 1
else
	echo "INFO:  Starting to archive..."
fi
#
# Step 1: Clean up any compiled python objects.
#
$FIND_BIN $CVSWORK_DIR/$PROJECT_DIR -name '*.pyc' | $XARGS_BIN $RM_BIN > /dev/null 2>&1
#
# Step 2: Clean up any emacs temp files.
#
$FIND_BIN $CVSWORK_DIR/$PROJECT_DIR -name '*~' | $XARGS_BIN $RM_BIN > /dev/null 2>&1
#
# Step 3: Clean up the config.xml symlink.
#
if [ -f $CVSWORK_DIR/$PROJECT_DIR/conf/config.xml ]; then
	$RM_BIN $CVSWORK_DIR/$PROJECT_DIR/conf/config.xml
fi
#
# Step 4: Create the distribution tar/gzip archive.
#
cd $CVSWORK_DIR
$TAR_BIN --create --gzip --exclude CVS* --exclude .cvsignore \
	--file $CVSWORK_DIR/archive/$PROJECT_NAME-$1.tar.gz \
	$PROJECT_DIR

echo "INFO:  All done!"
