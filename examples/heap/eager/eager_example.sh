#!/bin/bash

hostname=`hostname`

echo "Starting Eager example"
./eager.py &
prog=$?
sleep 10
echo "update update.py" | netcat $hostname 4242
sleep 20
kill $prog


