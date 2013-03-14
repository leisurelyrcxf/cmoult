#!/bin/bash

hostname=`hostname`

echo "Starting Lazy example"
./lazy.py &
prog=$?
sleep 10
echo "update update.py" | netcat $hostname 4242
sleep 20
kill $prog


