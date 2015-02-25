#gcc -std=c11 -g -O0 -I ../../includes -rdynamic -pthread -o threaded_listener threaded_listener.c -ldl 
gcc -std=c11 -g -O0 -I ../../includes -rdynamic -pthread -o test test.c threaded_listener.c common.c -ldl 

gcc -std=c11 -g -O0 -c -fPIC lama.c -o lama.o
gcc -std=c11 -g -O0 -shared -Wl,-soname,lama.so.1 -o lama lama.o


