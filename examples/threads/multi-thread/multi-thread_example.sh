#!/bin/bash

hostname=`hostname`

echo "Starting Multi-Thread example"
./multi-thread.py &
prog=$?
sleep 10
echo "update update.py" | netcat $hostname 4242
sleep 20
kill $prog


