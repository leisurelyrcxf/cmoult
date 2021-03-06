#!/bin/bash

hostname=$(hostname)

cmoult_home="$CMOULT_PROJECT_HOME"
if [ $? -ne 0 ]; then
  exit -1
fi

make clean && make

if [ $? -ne 0 ]; then
  exit -1
fi

./test &
last_app_pid=$!

echo "pid is $last_app_pid"

sleep 2


echo "#include \"update.h\"
#include \"lowlevel.h\"


#define PROGRAM_PROC_MAXLENGTH 24
#define PROGRAM_NAME_MAXLENGTH 128
#define PROGRAM_DIRECTORY_MAXLENGTH 512
#define FUNCTION_NAME_MAXLENGTH 128


#define \$thread_array_elements\$ $last_app_pid
#define \$update_process_pid\$ $last_app_pid
#define \$program_name\$ \"test\"
#define \$program_directory\$ \"`pwd`\"
#define \$new_code_path\$ \"`pwd`/update/lib/libupdate.so\"





" > update/include/variables.h

if [ $? -ne 0 ]; then
  exit -1
fi

cd update
make clean && make

if [ $? -ne 0 ]; then
  exit -1
fi

cd ..


sleep 1

echo "scripts = ( 
			{ 
			  name  = \"lazy_update\";
              script = \"`pwd`/update/lib/libupdate.so\";
              manager  = \"manager\";
            }
          );" > update/update.cfg

if [ $? -ne 0 ]; then
  exit -1
fi

echo "BEGINING UPDATE"
echo "update $last_app_pid `pwd`/update/update.cfg"

echo -n "update $last_app_pid `pwd`/update/update.cfg"  | netcat $hostname 4242 

if [ $? -ne 0 ]; then
  exit -1
fi

control_c()
{
    kill $last_app_pid
    exit 0
}

trap control_c SIGINT
wait $last_app_pid
