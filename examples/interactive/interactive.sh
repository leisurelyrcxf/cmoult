#!/bin/bash

TITLE="Chose your own policy update!"
TPATH=/tmp/interactive
TMP=$TPATH/ans
MANAGER=""
STATIC=""
CLASS=""
ACCESS=""
ALTER=""

mkdir $TPATH

INTERPATH=$(realpath $(dirname $0))
cp $INTERPATH/application.py $TPATH/
cp $INTERPATH/update.py $TPATH/

dialog --msgbox "$TITLE\n\nHere, you will chose how to update your file server!\n\nLet's take a look at the code!" 10 80 

$EDITOR $TPATH/application.py

dialog --msgbox "$TITLE\n\nBefore starting the application, we need to decide a few things ..." 10 80

dialog --menu "$TITLE\n\nDo we add a manager to the application?" 30 80 3 "t" "add a threaded manager" "m" "add a non-threaded manager" "n" "do not add a manager" 2>$TMP

MANAGER=$(cat $TMP)

if [ "$MANAGER" == "t" ]
then
    #We decided to add a global threaded manager
    sed -i 's/import os/import os\nfrom pymoult.highlevel.managers import ThreadedManager/' $TPATH/application.py
    sed -i 's/listener.start()/listener.start()\n    manager = ThreadedManager(name="pymoult",threads=[])\n    manager.start()/' $TPATH/application.py

elif [ "$MANAGER" == "m" ]
then
    #We decided to add a non threaded manager
    sed -i 's/import os/import os\nfrom pymoult.highlevel.managers import Manager/' $TPATH/application.py
    sed -i 's/files = {}/manager = Manager(name="pymoult")\nfiles = {}/' $TPATH/application.py 

    #Decide where to make the manager run 

    dialog --msgbox "$TITLE\n\nThe manager will run when waiting for new connections" 8 80 
    sed -i 's/while True:/while True:\n        manager.apply_next_update()/' $TPATH/application.py

fi

$EDITOR $TPATH/application.py

dialog --menu "$TITLE\n\nDo we put static update points?" 30 80 3 "m" "put a static point in main's loop" "t" "put a static point in threads loop" "n" "do not put static points" 2>$TMP
    
STATIC=$(cat $TMP)
   
if [ "$STATIC" == "m" ]
then
    sed -i 's/import os/import os\nfrom pymoult.lowlevel.alterability import staticUpdatePoint\nfrom pymoult.threads import DSU_Thread/' $TPATH/application.py
    sed -i 's/  main()/  main_thread = DSU_Thread(target=main)\n    main_thread.start()/' $TPATH/application.py
    #place the point
    sed -i 's/conn,addr/staticUpdatePoint()\n            conn,addr/' $TPATH/application.py
    
elif [ "$STATIC" == "t" ]
then
    sed -i 's/import os/import os\nfrom pymoult.lowlevel.alterability import staticUpdatePoint\nfrom pymoult.threads import DSU_Thread/' $TPATH/application.py
    sed -i 's/threading.Thread/DSU_Thread/' $TPATH/application.py
    sed -i 's/run/main/' $TPATH/application.py
    #place the point
    sed -i 's/data = ""/staticUpdatePoint()\n                data = ""/' $TPATH/application.py    
fi
   
$EDITOR $TPATH/application.py

dialog --msgbox "$TITLE\n\nWe are now ready to start the application." 8 80

dialog --inputbox "$TITLE\n\nPlease enter paths of the folders to serve (separated by space)" 12 80 2> $TMP
folders=$(cat $TMP)

pypy-dsu $TPATH/application.py $folders &
app=$!

dialog --msgbox "$TITLE\n\nNow, it's time to launch the client." 8 80

dialog --msgbox "$TITLE\n\nReady for a Dynamic Update?\nLet's take a look at it." 10 80

$EDITOR $TPATH/update.py

if [ "$MANAGER" == "n" ]
then
    dialog --msgbox "Because we didn't started any manager before, we need to start one now." 8 80
    #Add threaded manager
    sed -i 's/import tempfile/import tempfile\nfrom pymoult.highlevel.managers import ThreadedManager/' $TPATH/update.py
    sed -i 's/\["__main__"\]/["__main__"]\nmanager = ThreadedManager(name="pymoult")\nmanager.start()/' $TPATH/update.py

    $EDITOR $TPATH/update.py
fi

dialog --msgbox "$TITLE\n\nNow, let's update the Picture class.\nBecause the new version of Picture class is backward compatible, we don't have to mind alterability.\n\nLet's see the skeleton of our update" 12 80

#Skeleton

sed -i 's/import tempfile/import tempfile\nfrom pymoult.highlevel.updates import Update/' $TPATH/update.py

sed -i 's/helptext =/class PictureUpd(Update):\n    def preupdate_setup(self):\n        self.threads=getAllThreads()\n    def wait_alterability(self):\n        return True\n    def check_alterability(self):\n        return True\n    def apply(self):\n        #Updating the Pictures\n\n\nhelptext =/' $TPATH/update.py 

$EDITOR $TPATH/update.py 

dialog --menu "$TITLE\n\nFirst, how do we update the class?" 30 80 3 "r" "redefine the class" "i" "just add it along the old one" 2>$TMP
    
CLASS=$(cat $TMP)

dialog --menu "$TITLE\n\nHow should we access the pictures in order to update them?" 30 80 3 "e" "eagerly" "l" "lazyly" 2>$TMP

ACCESS=$(cat $TMP)

sed -i 's/import tempfile/import tempfile\nfrom pymoult.lowlevel.data_update import updateToClass/' $TPATH/update.py


if [ "$ACCESS" == "e" ]
then
    #Eager access
    sed -i 's/import tempfile/import tempfile\nfrom pymoult.lowlevel.data_access import startEagerUpdate/' $TPATH/update.py
    if [ "$CLASS" == "i" ]
    then
        sed -i 's/helptext =/def pic_upd(pic):\n    updateToClass(pic,main.Picture,Picture_V2,pic_transformer)\n\nhelptext =/' $TPATH/update.py
        sed -i 's/#Updating the Pictures/#Updating the Pictures\n        startEagerUpdate(main.Picture,pic_upd)/' $TPATH/update.py
    else
        sed -i 's/helptext =/old_Pic = main.Picture\ndef pic_upd(pic):\n    updateToClass(pic,old_Pic,Picture_V2,pic_transformer)\n\nhelptext =/' $TPATH/update.py
        sed -i 's/import updateToClass/import updateToClass, redefineClass/' $TPATH/update.py
        sed -i 's/#Updating the Pictures/#Updating the Pictures\n        redefineClass(main,main.Picture,Picture_V2)\n        startEagerUpdate(old_Pic,pic_upd)/' $TPATH/update.py
    fi
else
    #Lazy access
    sed -i 's/import tempfile/import tempfile\nfrom pymoult.lowlevel.data_access import startLazyUpdate/' $TPATH/update.py
    if [ "$CLASS" == "i" ]
    then
        sed -i 's/helptext =/def pic_upd(pic):\n    updateToClass(pic,main.Picture,Picture_V2,pic_transformer)\n\nhelptext =/' $TPATH/update.py
        sed -i 's/#Updating the Pictures/#Updating the Pictures\n        startLazyUpdate(main.Picture,pic_upd)/' $TPATH/update.py
    else
        sed -i 's/helptext =/old_Pic = main.Picture\ndef pic_upd(pic):\n    updateToClass(pic,old_Pic,Picture_V2,pic_transformer)\n\nhelptext =/' $TPATH/update.py
        sed -i 's/import updateToClass/import updateToClass, redefineClass/' $TPATH/update.py
        sed -i 's/#Updating the Pictures/#Updating the Pictures\n        redefineClass(main,main.Picture,Picture_V2)\n        startLazyUpdate(old_Pic,pic_upd)/' $TPATH/update.py
    fi
fi

if [ "$MANAGER" == "n" ]
then
    #Add update to the new manager
    sed -i 's/helptext =/picture_update = PictureUpd(name="picupd")\nmanager.add_update(picture_update)\n\nhelptext =/' $TPATH/update.py
else
    #Add update to app manager
    sed -i 's/helptext =/picture_update = PictureUpd(name="picupd")\nmain.manager.add_update(picture_update)\n\nhelptext =/' $TPATH/update.py
fi

$EDITOR $TPATH/update.py

dialog --msgbox "$TITLE\n\nNow, let's update the connection handling threads\nFirst, let's consider the alterability criteria" 8 80

#Skeleton

sed -i 's/import Update/import Update, isApplied/' $TPATH/update.py
sed -i 's/#end of update/class ConnUpd(Update):\n    def __init__(self,old_method,new_method,name=None):\n        self.old_method = old_method\n        self.new_method=new_method\n        super(ConnUpd,self).__init__(name=name,threads=[])\n\n    def check_requirements(self):\n        if isApplied("picupd"):\n            return "yes"\n        return "no"\n\n    def preupdate_setup(self):\n        #preupdate setup\n        pass\n\n    def wait_alterability(self):\n        #wait for alterability\n\n    def check_alterability(self):\n        #check for alterability\n\n    def clean_failed_alterability(self):\n        #clean failed alt\n        pass\n\n    def apply(self):\n        #Updating the connection threads\n\n    def resume_hook(self):\n        #resume hook\n        pass\n\n\n#end of update/' $TPATH/update.py 


if [ "$STATIC" == "m" ]
then
    #Static point in main : we cannot use it
    dialog --menu "$TITLE\n\nWhen will we update the connection threads?\n\nUfortunately, we cannot use our static update point : the application will not be alterable here." 16 80 1 "q" "when the functions to update are not active (i.e. quiescent)"  2>$TMP
elif [ "$STATIC" == "t" ]
then
    #Static point in threads : we can use it!
    dialog --menu "$TITLE\n\nWhen will we update the connection threads?" 16 80 2 "q" "when the functions to update are not active (i.e. quiescent)" "s" "when static points are reached" 2>$TMP
    
else
    #Just asap available
    dialog --menu "$TITLE\n\nWhen will we update the connection threads?" 16 80 1 "q" "when the functions to update are not active (i.e. quiescent)" 2>$TMP
fi

ALTER=$(cat $TMP)

sed -i 's/import tempfile/import tempfile\nfrom pymoult.lowlevel.alterability import */' $TPATH/update.py

if [ "$ALTER" == "q" ]
then
    #function quiescence
    sed -i 's/#wait for alterability/return waitQuiescenceOfFunction(self.old_method)/' $TPATH/update.py
    sed -i 's/#check for alterability/return checkQuiescenceOfFunction(self.old_method)/' $TPATH/update.py
    sed -i 's/#resume hook/resumeSuspendedThreads()/' $TPATH/update.py
    
else

    #static point in threads
    sed -i 's/#preupdate setup/self.connThreads = getAllConnThreads()\n        setupWaitStaticPoints(self.connThreads)/' $TPATH/update.py
    sed -i 's/#check for alterability/return checkStaticPointsReached(self.connThreads)/' $TPATH/update.py
    sed -i 's/#wait for alterability/return waitStaticPoints(self.connThreads)/' $TPATH/update.py
    sed -i 's/#clean failed alt/cleanFailedStaticPoints(self.connThreads)/' $TPATH/update.py
    sed -i 's/#resume hook/resumeSuspendedThreads(self.connThreads)/' $TPATH/update.py
fi

$EDITOR $TPATH/update.py

dialog --msgbox "$TITLE\n\nNow we modify the 'apply' part of the update" 8 80

sed -i 's/from pymoult.lowlevel.data_update import/from pymoult.lowlevel.data_update import addMethodToClass,/' $TPATH/update.py

sed -i 's/#Updating the connection threads/addMethodToClass(main.ConnThread,self.old_method.__name__,self.new_method)/' $TPATH/update.py

$EDITOR $TPATH/update.py

dialog --msgbox "$TITLE\n\nWe now create the updates for serve_folder ad do_command" 8 80

if [ "$MANAGER" == "n" ]
then
    #Add update to the new manager
    sed -i 's/#end of update/serve_update = ConnUpd(main.ConnThread.serve_folder,serve_folder_v2,name="serve_folder")\nserve_update.set_sleep_time(0.5)\nmanager.add_update(serve_update)\ncommand_update = ConnUpd(main.ConnThread.do_command,do_command_v2,name="do_command")\ncommand_update.set_sleep_time(0.5)\nmanager.add_update(command_update)\n/' $TPATH/update.py
else
    sed -i 's/#end of update/serve_update = ConnUpd(main.ConnThread.serve_folder,serve_folder_v2,name="serve_folder")\nserve_update.set_sleep_time(0.5)\nmain.manager.add_update(serve_update)\ncommand_update = ConnUpd(main.ConnThread.do_command,do_command_v2,name="do_command")\ncommand_update.set_sleep_time(0.5)\nmain.manager.add_update(command_update)\n/' $TPATH/update.py
fi

$EDITOR $TPATH/update.py

dialog --msgbox "$TITLE\n\nThe update is ready to be applied!" 10 80

echo "set loglevel 2" | netcat $(hostname) 4242
echo "update $TPATH/update.py" | netcat $(hostname) 4242

dialog --msgbox "$TITLE\n\nThe update has been started.\nDo you see the new feature?" 10 80


dialog --msgbox "$TITLE\n\nThe demo is now finished!\nGood bye!" 10 80


kill $app

rm -r $TPATH
