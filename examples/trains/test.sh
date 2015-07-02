#!/bin/bash

typ=$1
hostname=$(hostname)

if [ "$typ" == "gui" ];
then
    python guiserver.py &
    gui=$!
    python-dsu applicationgui.py &
    app=$!
    
    sleep 15
    echo "update update.py" | netcat $hostname 4242 
    
    control_c()
    {
        kill $app
        kill $gui
        exit 0
    }

    trap control_c SIGINT
    wait $app

else
    python-dsu application.py &
    app=$! 

    sleep 15
    echo "update update.py" | netcat $hostname 4242 
    
    control_c()
    {
        kill $app
        exit 0
    }
    
    trap control_c SIGINT
    wait $app

fi

