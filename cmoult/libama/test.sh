#!/bin/bash

hostname=$(hostname)

cd test
make clean && make

./test &
last_app_pid=$!
echo "pid is $last_app_pid"

cd ..


#echo "#ifndef FORCE_QUIESCENCE_UPDATE_H
#define FORCE_QUIESCENCE_UPDATE_H




#define PROGRAM_PROC_MAXLENGTH 24
#define PROGRAM_NAME_MAXLENGTH 128
#define PROGRAM_DIRECTORY_MAXLENGTH 512
#define FUNCTION_NAME_MAXLENGTH 128


#define \$old_function_name\$  \"func1\"
#define \$new_function_name\$  \"func2\"
#define \$update_process_pid\$ $last_app_pid
#define \$program_name\$ \"test\"
#define \$program_directory\$ \"`pwd`/test\"
#define \$new_code_path\$ \"`pwd`/lib/libama.so\"






#endif" > include/variables.h

echo $last_app_pid > pid

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
