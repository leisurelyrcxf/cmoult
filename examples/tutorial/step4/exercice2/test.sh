#!/bin/bash

hostname=$(hostname)

if [ "$1" == "solution" ];
then
    python-dsu3 app_solution.py &
else
    python-dsu3 application.py &
fi
app=$! 
echo "WEB SERVER STARTED"
echo "HIT ENTER TO START UPDATE"

read -n 1 -s

if [ "$1" == "solution" ];
then
    echo "update solution.py" | netcat $hostname 4242
else
    echo "update update.py" | netcat $hostname 4242
fi    

echo "UPDATE SUMMONED"


control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app
