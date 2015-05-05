#!/bin/bash

TITLE="Chose your own policy update!"
TPATH=/tmp/interactive
TMP=$TPATH/ans
MANAGER=""
STATIC=""
CLASS=""
ACCESS=""

mkdir $TPATH

INTERPATH=$(realpath $(dirname $0))
cp $INTERPATH/application.py $TPATH/
cp $INTERPATH/update.py $TPATH/

dialog --msgbox "$TITLE\n\nHere, you will chose how to update your file server!\n\nLet's take a look at the code!" 10 80 

dialog --textbox $TPATH/application.py 120 150

dialog --msgbox "$TITLE\n\nBefore starting the application, we need to decide a few things ..." 10 80

dialog --menu "$TITLE\n\nDo we add a manager to the application?" 30 80 3 "t" "add a threaded manager" "m" "add a non-threaded manager" "n" "do not add a manager" 2>$TMP

MANAGER=$(cat $TMP)

if [ "$MANAGER" == "t" ]
then
    #We decided to add a global threaded manager
    sed -i 's/import os/import os\nfrom pymoult.highlevel.managers import ThreadedManager/' $TPATH/application.py
    sed -i 's/listener.start()/listener.start()\n    manager = ThreadedManager(name="pymoult",threads=[])\n    manager.start()/' $TPATH/application.py

    dialog --textbox $TPATH/application.py 120 150
    
elif [ "$MANAGER" == "m" ]
then
    #We decided to add a non threaded manager
    sed -i 's/import os/import os\nfrom pymoult.highlevel.managers import Manager/' $TPATH/application.py
    sed -i 's/files = {}/manager = Manager(name="pymoult")\nfiles = {}/' $TPATH/application.py 

    #Decide where to make the manager run 

    dialog --menu "$TITLE\n\nWhere do we run the manager?" 30 80 2 "m" "in main's loop" "t" "in threads loop" 2>$TMP
    STATIC=$(cat $TMP)
   
    if [ "$STATIC" == "m" ]
    then
        sed -i 's/while True:/while True:\n        manager.apply_next_update()/' $TPATH/application.py
    else
        sed -i 's/while self.connection:/while self.connection:\n            manager.apply_next_update()/' $TPATH/application.py    
    fi

fi

if [ "$MANAGER" != "m" ]
then
    dialog --menu "$TITLE\n\nDo we put static update points?" 30 80 3 "m" "put a static point in main's loop" "t" "put a static point in threads loop" "n" "do not put static points" 2>$TMP
    
   STATIC=$(cat $TMP)
   
   if [ "$STATIC" == "m" ]
   then
       sed -i 's/import os/import os\nfrom pymoult.lowlevel.alterability import staticUpdatePoint\nfrom pymoult.threads import DSU_Thread/' $TPATH/application.py
       sed -i 's/  main()/  main_thread = DSU_Thread(target=main)\n    main_thread.start()/' $TPATH/application.py
       #place the point
       sed -i 's/while True:/while True:\n        staticUpdatePoint()/' $TPATH/application.py
       
   elif [ "$STATIC" == "t" ]
   then
        sed -i 's/import os/import os\nfrom pymoult.lowlevel.alterability import staticUpdatePoint\nfrom pymoult.threads import DSU_Thread/' $TPATH/application.py
        sed -i 's/threading.Thread/DSU_Thread/' $TPATH/application.py
        sed -i 's/run/main/' $TPATH/application.py
        #place the point
        sed -i 's/while self.connection:/while self.connection:\n            staticUpdatePoint()/' $TPATH/application.py    
   fi
   
fi

dialog --textbox $TPATH/application.py 120 150

dialog --msgbox "$TITLE\n\nWe are now ready to start the application." 8 80

dialog --inputbox "$TITLE\n\nPlease enter paths of the folders to serve (separated by space)" 12 80 2> $TMP
folders=$(cat $TMP)

pypy-dsu $TPATH/application.py $folders &
app=$!

dialog --msgbox "$TITLE\n\nNow, it's time to launch the client." 8 80

dialog --msgbox "$TITLE\n\nReady for a Dynamic Update?\nLet's take a look at it." 10 80

dialog --textbox $TPATH/update.py 120 150

#Managers, static points, skeleton of update




dialog --menu "$TITLE\n\nNow, let's update the Picture class.\nHow do we update the class?" 30 80 3 "r" "redefine the class" "i" "just add it along the old one (and relink instances later)" 2>$TMP
    
CLASS=$(cat $TMP)

dialog --menu "$TITLE\n\nHow should we access the pictures in order to update them?" 30 80 3 "e" "eagerly" "l" "lazyly" 2>$TMP

ACCESS=$(cat $TMP)

#Modify the update

dialog --textbox $TPATH/update.py 120 150

#Then update the thread
#- update by redefining class (only new connection will use new version)
#- Redef the methods with alterability (static points of safe redef)






echo "update update.py" | netcat localhost 4242

dialog --msgbox "$TITLE\n\nThe update has been started.\nDo you see the new feature?" 10 80


dialog --msgbox "$TITLE\n\nThe demo is now finished!\nGood bye!" 10 80


kill $app

rm -r $TPATH
