#!/bin/bash

# tape-pl_invent_mgmt.sh
# Created by Sam Delfino, template as of October 2019
# Driving script for Pulling Inventory Item Data

if [ $# -ne 2 ]; then
  echo 1>&2 "Arguments Needed: (dev/prod/both) (ohio/local/both)"
  echo 1>&2 "Did not execute query or modify databases."
  exit 3
fi

echo -e "Routing to [ \e[1m$1\e[0m ] DB(s). Routing to [ \e[1m$2\e[0m ] machine(s)."
d=$(date +%m%d%Y-%H%M%S)

# Per-script variable definition
setname="pl_invent_mgmt"
querybasename="PL_INV_ITEM"
newquerybasename=$querybasename
scriptname="pl_invent_mgmt"

cd $RUBIXTAPEBASEPATH
mkdir $RUBIXTAPEDATAPATH/$setname/$d

python3 $RUBIXTAPEBASEPATH/selenium-$setname.py $d

mv $RUBIXTAPEDATAPATH/$setname/$d/$querybasename\_*.xlsx $RUBIXTAPEDATAPATH/$setname/$d/$newquerybasename-$d.xlsx

python3 $RUBIXTAPEBASEPATH/'rm_head'.py $RUBIXTAPEDATAPATH/$setname/$d/$newquerybasename-$d.xlsx $RUBIXTAPEITEMSPATH/$newquerybasename.xlsx

# $1 is the db type (dev/prod/both), $2 is the location (ohio/local/both)
if [ "$2" = "ohio" ] || [ "$2" = "both" ]; then
remotedatapath=$(ssh prodbash 'printf $RUBIXTAPEDATAPATH')
remotescriptpath=$(ssh prodbash 'printf $RUBIXTAPESCRIPTPATH')
ssh prodbash "mkdir -p $remotedatapath/$setname/$d"
scp -i /home/rubix/.ssh/rubixprodbash.pem -r \
    $RUBIXTAPEDATAPATH/$setname/$d/ \
    ubuntu@rubikdata3.com:$remotedatapath/$setname/
ssh prodbash "cd $remotescriptpath; python3 ./$scriptname.py \"$d\" \"$1\""
fi

if [ "$2" = "local" ] || [ "$2" = "both" ]; then
python3 $RUBIXTAPESCRIPTPATH/$scriptname.py $d $1
fi
