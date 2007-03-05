#!/bin/bash

Usage () {
cat << LIM
Usage: dwrap.sh [OPTIONS]
  -e ENVIRONMENT	the distribulator environment in which to perform the action
  -s SERVERGROUPS 	comma-seperated server groups

Use one of -b and -c
  -b BATCHCOMMAND	the "run" command
  -c COPYCOMMAND	the "copy" command

OPTIONAL
  --var1 		var1 for distribulator
  --var2 		var2 for distribulator
  --var3 		var3 for distribulator

EXAMPLES
  \$dwrap.sh -e demo1 -s www -b "uptime"
  run uptime on all the demo1 webservers

  \$dwrap.sh -e demo2 -s app -c "tmpf /tmp/"
  copy tmpf to all the demo2 app machines
LIM
}

DIST=/opt/orbitz/distribulator2/bin/distribulator

# if invokes using full path, only take the script name
scriptname=`basename $0`

# create tempfile
TMPFILE=`mktemp -q /tmp/$scriptname.XXXXXX`
if [ $? -ne 0 ]; then
    echo "$0: Can't create temp file, exiting..."
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
    -s)     shift;  sgroups=$1 ;;
    -s*)    sgroups=`echo $1 | cut -c3-`;;
    -1)     shift;  var1=$1 ;;
    -1*)    var1=`echo $1 | cut -c3-`;;
    -2)     shift;  var2=$1 ;;
    -2*)    var2=`echo $1 | cut -c3-`;;
    -3)     shift;  var3=$1 ;;
    -3*)    var3=`echo $1 | cut -c3-`;;
    -*)     Usage; exit 1 ;;
    esac
    shift
done

# construct distribulator command
if [ -z "$batch" ]; then
    filename=`echo $copy | cut -d" " -f1`
    remoteDirectory=`echo $copy | cut -d" " -f2`
    echo "copy \"$filename\" $sgroups:$remoteDirectory now" >> $TMPFILE
else
    echo "run \"$batch\" on $sgroups now" >> $TMPFILE
fi

# run distribulator with batch file
$DIST --env=$environment --batch=$TMPFILE --var1=$var1 --var2=$var2 --var3=$var3

# remove tempfile
rm $TMPFILE
