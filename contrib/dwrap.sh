#!/bin/bash
######################################################################
#
# $Id: dwrap.sh 8807 2007-04-25 22:42:10Z adace $
#
# Description:  A small wrapper script to present a more command-line
#               oriented inteface to The Distribulator.
#
######################################################################

Usage () {
cat << LIM

Usage: dwrap.sh [OPTIONS]

REQUIRED
    -e ENVIRONMENT
    Specifies the environment in which to perform a given action.

    -s SERVERGROUPS
    Specifies the target server group(s) which we wish to perform actions upon.
    upon which to perform a given action.

    -k CONFIGFILE
    Specifies which distribulator config file one wishes to use.
    Would have probably been -c if it wasn\'t already taken.

USE ONE OF THE FOLLOWING
    -b BATCHCOMMAND
    Specifies that we wish to run a command.  (i.e. the "run" command)
    
    -c COPYCOMMAND
    Specifies that we wish to copy a file.  (i.e. the "copy" command)

OPTIONAL
    -1 VARIABLE
    Allows passing of variables into distribulator.
    
    -2 VARIABLE
    Allows passing of variables into distribulator.
    
    -3 VARIABLE
    Allows passing of variables into distribulator.

EXAMPLES
    \$ dwrap.sh -e staging -s admin_www -b "uptime"
    Runs "uptime" on all the staging admin webservers.

    \$ dwrap.sh -e production -s dconeg -c "tmpf /tmp/"
    Copies tmpf to all the production dconeg machines.

LIM
}

######################################################################

DIST=/opt/orbitz/distribulator2/bin/distribulator

# if invokes using full path, only take the script name
scriptname=`basename $0`

# create tempfile
TMPFILE=`mktemp -q /tmp/$scriptname.XXXXXX`
config=""
if [ $? -ne 0 ]; then
    echo "ERROR: Can't create temp file, exiting..."
    exit 1
fi

# must give at least 3 arguments: batch commands, environment, and server group(s)
if [ $# -lt 4 ]; then
    Usage
    exit 127
fi

# parse args
while [ $# -ge 1 ]; do
    case $1 in
    -e)     shift;  environment=$1 ;;
    -e*)    environment=`echo $1 | cut -c3-`;;
    -b)     shift;  batch=$1 ;;
    -b*)    batch=`echo $1 | cut -c3-`;;
    -c)     shift;  copy=$1 ;;
    -c*)    copy=`echo $1 | cut -c3-`;;
    -k)     shift;  konfig=$1 ;;
    -k*)    konfig=`echo $1 | cut -c3-`;;
    -s)     shift;  sgroups=$1 ;;
    -s*)    sgroups=`echo $1 | cut -c3-`;;
    -1)     shift;  var1=$1 ;;
    -1*)    var1=`echo $1 | cut -c3-`;;
    -2)     shift;  var2=$1 ;;
    -2*)    var2=`echo $1 | cut -c3-`;;
    -3)     shift;  var3=$1 ;;
    -3*)    var3=`echo $1 | cut -c3-`;;
    --config*) config=`echo $1`;;
    esac
    shift
done

######################################################################

# If neither batch or copy were specified, error out.
if [ -z "$batch" ] && [ -z "$copy" ]; then
    echo "ERROR: Please specify either -b or -c flags.  Exiting..."
    Usage
    exit 1
fi

# construct distribulator command
if [ -z "$batch" ]; then
    filename=`echo $copy | cut -d" " -f1`
    remoteDirectory=`echo $copy | cut -d" " -f2`
    echo "copy \"$filename\" $sgroups:$remoteDirectory now" >> $TMPFILE
else
    echo "run \"$batch\" on $sgroups now" >> $TMPFILE
fi

# run distribulator with batch file
if [ -z "$konfig" ]; then
    $DIST $config --env=$environment --batch=$TMPFILE --var1=$var1 --var2=$var2 --var3=$var3
else
    $DIST $config --config=$konfig --env=$environment --batch=$TMPFILE --var1=$var1 --var2=$var2 --var3=$var3
fi

# remove tempfile
rm $TMPFILE
