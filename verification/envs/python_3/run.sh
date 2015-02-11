#!/bin/sh
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`

python3 $SCRIPTPATH/main.py $1 $2
