#!/bin/sh
#pushd `dirname $0` > /dev/null
#SCRIPTPATH=`pwd`
#popd > /dev/null

SCRIPT=`realpath -s $0`
SCRIPTPATH=`dirname $SCRIPT`

/bin/sh $SCRIPTPATH/{{env}}/run.sh $1 $2
