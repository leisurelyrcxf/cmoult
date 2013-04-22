#!/bin/bash

hostname=`hostname`

echo "Starting Dynamic-Thread example"
./dynamic_threads.py &
prog=$?
sleep 10
echo "applying update 1"
echo "update update1.py" | netcat $hostname 4242
sleep 10
echo "applying update 2"
echo "update update2.py" | netcat $hostname 4242
sleep 10
kill $prog


