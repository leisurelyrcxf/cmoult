#!/bin/bash

#Path to oracle is first argument
oracle=$1

hostname=$(hostname)

if [ -f pymoult.log ];
then
    rm pymoult.log
fi

if [ -p fifopipe ];
then
    rm fifopipe
fi

currentTest="$(basename "$PWD") ... "
echo -n $currentTest

python-dsu3 application.py &
app=$! 
sleep 1
echo "set loglevel 2" > fifopipe

sleep 2 
echo "update update.py" > fifopipe

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
if [ "$res" == "0" ]
then
    echo " passed"
else
    echo " failed"
fi
