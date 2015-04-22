#!/bin/bash

hostname=$(hostname)

if [ -f pymoult.log ];
then
    rm pymoult.log
fi

currentTest="$(basename "$PWD") ... "
echo -n $currentTest

pypy-dsu application.py &
app=$! 
sleep 0.5
echo "set loglevel 2" | netcat $hostname 4242

sleep 1 
echo "update update.py" | netcat $hostname 4242 

control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app

result=$(cat pymoult.log | cut -f2)
answer=$(cat answer.txt)

if [ "$result" == "$answer" ];
then
    echo " passed"
else
    echo " failed"
fi

