#!/bin/bash

hostname=`hostname`

echo "Starting Recaml example"
./recaml.py &
prog=$?
sleep 10
echo "update update.py" | netcat $hostname 4242
sleep 5
kill $prog


