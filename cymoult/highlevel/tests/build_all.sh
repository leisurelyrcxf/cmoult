#!/bin/bash

#Common Program
gcc -std=c11 -g -O0 -I ../../includes -lconfig -pthread -rdynamic -ldl -o test basic_test.c ../src/listeners/socket_listener.c ../src/listeners/common.c ../../common.c ../src/codeloader.c ../src/managers/common.c ../src/managers/extern_manager.c

#Extern manager
gcc -std=c11 -g -O0 -I ../../includes -lconfig -pthread -rdynamic -ldl -o manager manager_test.c ../src/listeners/socket_listener.c ../src/listeners/common.c ../../common.c ../src/codeloader.c ../src/managers/common.c ../src/managers/extern_manager.c




