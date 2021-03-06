#!/bin/bash

hostname=$(hostname)

python-dsu3 application.py &
app=$! 

sleep 6
echo "SUMMONING UPDATE"

if [ "$1" == "solution" ];
then
    echo "update solution.py" | netcat $hostname 4242
else 
    echo "update update.py" | netcat $hostname 4242 
fi

control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app
