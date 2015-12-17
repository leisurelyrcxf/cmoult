#!/bin/bash

hostname=$(hostname)

python-dsu3 application.py &
app=$! 

sleep 5
echo "BEGINING UPDATE"

echo "update solution.py" | netcat $hostname 4242

control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app
