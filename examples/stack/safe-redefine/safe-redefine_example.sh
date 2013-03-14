#!/bin/bash

hostname=`hostname`

echo "Starting Safe-Redefine example"
./safe-redefine.py &
prog=$?
sleep 5
echo "update update.py" | netcat $hostname 4242
sleep 7
kill $prog


