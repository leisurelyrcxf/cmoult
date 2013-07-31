#!/bin/bash

hostname=`hostname`

echo "Products example : Starting example 'products'"
./products_v1.py &
prog=$?
sleep 2
echo "Products example :  Ordering apples from Paris" 
echo "order 3 apple Paris" | netcat $hostname 5678
sleep 2
echo "Products example :  Starting first update" 
echo "update products_update_v2.py" | netcat $hostname 4242
sleep 5
echo "Products example :  Ordering lychees from Lyon" 
echo "order 2 lychee Lyon" | netcat $hostname 5678
sleep 2
echo "Products example :  Rating mango from Brest" 
echo "rate 3 mango Brest" | netcat $hostname 5678
sleep 2
echo "Products example :  Starting second update" 
echo "update products_update_v3.py" | netcat $hostname 4242
sleep 15
echo "Products example : Ending the program"
kill $prog


