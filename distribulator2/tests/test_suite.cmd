#
# $Id$
#
######################################################################
#
# Name: The Distribulator Batch Test Suite
#
# Description: Quick'n'dirty batch file to test various ways things can fail.
#
######################################################################
run "uptime" on app
run "uptime" on db
run "uptime" on www
######################################################################
#
# Run / multi group
#
######################################################################
run "uptime" on app,db,www
######################################################################
#
# The following should produce errors and not execute at all.
#
######################################################################
