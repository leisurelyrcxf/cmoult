#!/bin/bash

#path of the test
testPath=$(realpath $(dirname $0))
hostname=$(hostname)

pushd $testPath

if [ -f pymoult.log ]
then
    rm pymoult.log
fi


echo "Starting server"
echo "==============="

#./start.py > /dev/null 2>&1 &
./testsite/server.py &
app=$!

control_c()
{
    kill $app
    echo "Interrupted!"
    popd
    exit 0
}

trap control_c SIGINT
sleep 2
echo "set loglevel 2" | netcat $hostname 4242
echo "You can now connect on localhost:8080"
echo "The server is running version 1.8.0"
#Update to 1.2.0
echo "Press any key to update to version 1.8.1"
read
echo "Submitting update"
echo "update update1.8.0-1.8.1.py" | netcat $hostname 4242
sleep 1
echo "The server should run in version 1.8.1 shortly"



# #update to 1.3.0
# echo "Press any key to update to version 1.3.0"
# read
# echo "Submitting update"
# echo "update update1.2.0-1.3.0.py" | netcat $hostname 4242
# sleep 1
# echo "The server should run in version 1.3.0 shortly"
# #update to 1.3.1
# echo "Press any key to update to version 1.3.1"
# read
# echo "Submitting update"
# echo "update update1.3.0-1.3.1.py" | netcat $hostname 4242
# sleep 1
# echo "The server should run in version 1.3.1 shortly"
# #update to 1.4.0
# echo "Press any key to update to version 1.4.0"
# read
# echo "Submitting update"
# echo "update update1.3.1-1.4.0.py" | netcat $hostname 4242
# sleep 1
# echo "The server should run in version 1.4.0 shortly"


echo "Press any key to end the server and terminate this example"
read

kill $app
popd 

