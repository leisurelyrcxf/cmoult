#!/bin/bash

echo "Begining tests for Pymoult"

#Getting the path of the tests
testPath=$(realpath $(dirname $0))
managersPath="$testPath/managers"
updatesPath="$testPath/updates"
listenersPath="$testPath/listeners"

if [ -f "$testPath/results.txt" ];
then
    rm "$testPath/results.txt"
fi

managerTests=$(find "$managersPath" -type d -not -name "__pycache__" -printf '%P\n')
updateTests=$(find "$updatesPath" -type d -not -name "__pycache__" -printf '%P\n')
listenersTests=$(find "$listenersPath" -type d -not -name "__pycache__" -printf '%P\n')

echo "Testing managers" | tee -a "$testPath/results.txt"

for folder in $managerTests
do
    cd "$managersPath/$folder"
    ./test.sh "$testPath/oracle.py" | tee -a "$testPath/results.txt"
done

echo "Testing updates" | tee -a "$testPath/results.txt" 

for folder in $updateTests
do
    cd "$updatesPath/$folder"
    ./test.sh "$testPath/oracle.py" | tee -a "$testPath/results.txt"
done

for folder in $listenersTests
do
    cd "$listenersPath/$folder"
    ./test.sh "$testPath/oracle.py" | tee -a "$testPath/results.txt"
done

echo "Finished. Results are in $testPath/results.txt"

passed=$(grep -o passed "$testPath/results.txt" | wc -l)
failed=$(grep -o failed "$testPath/results.txt" | wc -l)
skipped=$(grep -o skipped "$testPath/results.txt" | wc -l)

echo "$passed tests passed"
echo "$failed tests failed"
echo "$skipped tests were skipped"
