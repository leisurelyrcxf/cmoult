#!/bin/bash

#Path to oracle is first argument
oracle=$1

hostname=$(hostname)

if [ -f pymoult.log ];
then
    rm pymoult.log
fi

currentTest="$(basename "$PWD") ... "
echo -n $currentTest

python-dsu application.py &
app=$!
sleep 1
echo "set loglevel 2" | netcat $hostname 4242

sleep 2 
echo "update update.py" | netcat $hostname 4242 

control_c()
{
    kill $app
    exit 0
}

trap control_c SIGINT
wait $app

#result=$(cat pymoult.log | cut -f2)
#answer=$(cat answer.txt)

#if [ "$result" == "$answer" ];
#then
#    echo " passed"
#else
#    echo " failed"
#fi

$oracle .
res=$?
if [ $res ]
then
    echo " passed"
else
    echo " failed"
fi
