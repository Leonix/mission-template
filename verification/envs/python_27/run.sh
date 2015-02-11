#!/bin/sh
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`

python2 $SCRIPTPATH/main.py $1 $2
