#!/bin/bash

hostname=`hostname`

echo "Starting Reboot example"
./reboot.py &
prog=$?
sleep 5
echo "update update.py" | netcat $hostname 4242
sleep 5
echo "update update2.py" | netcat $hostname 4242
sleep 5
kill $prog


