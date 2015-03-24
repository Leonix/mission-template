#!/bin/sh
SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`

# TODO: find right way, that will work in docker/linux/mac os
#SCRIPTPATH=$( cd "$( dirname "$BASH_SOURCE" )" && pwd )  # for macos

python2 $SCRIPTPATH/main.py $1 $2
