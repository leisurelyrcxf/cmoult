#!/bin/bash

hostname=$(hostname)

python-dsu3 server.py &
app=$! 
echo "SERVER STARTED"
echo "HIT ENTER TO START UPDATE"

read -n 1 -s
echo "update update.py" | netcat $hostname 4242 

echo "UPDATE BEGAN"


control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app
