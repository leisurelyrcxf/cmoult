#!/bin/bash

hostname=`hostname`

echo "Starting DynamicML example"
./dynamicml.py &
prog=$?
sleep 10
echo "update update.py" | netcat $hostname 4242
sleep 15
kill $prog


