#!/bin/sh

SCRIPT=`realpath $0`
SCRIPTPATH=`dirname $SCRIPT`
cd $SCRIPTPATH
export NODE_PATH=/lib/node_modules/:$SCRIPTPATH
node --harmony main.js $1 $2
