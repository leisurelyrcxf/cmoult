#!/bin/bash

hostname=$(hostname)

pypy-dsu application.py &
app=$! 

sleep 2
echo "BEGINING UPDATE"
echo "update update.py" | netcat $hostname 4242 


control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app
