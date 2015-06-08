#!/bin/bash
#gcc -std=c11 -g -O0 -I ../../includes -rdynamic -pthread -o threaded_listener threaded_listener.c -ldl 
#gcc -std=c11 -g -O0 -I ../../includes -rdynamic -pthread -o test test.c threaded_listener.c common.c -ldl 

#gcc -std=c11 -g -O0 -I ../includes -D_XOPEN_SOURCE=500 -pthread -fPIC -c ../src/managers/threaded_manager.c ../src/managers/common.c ../src/managers/manager.c update.c 
#gcc -std=c11 -g -O0 -shared -Wl,-soname,update.so.1 -o update update.o threaded_manager.o common.o manager.o

gcc -std=c11 -g -O0 -I ../includes -rdynamic -pthread -o test test.c ../src/listeners/threaded_listener.c ../src/listeners/common.c ../src/managers/threaded_manager.c ../src/managers/common.c ../src/managers/manager.c ../src/threads/dsuthread.c -ldl



