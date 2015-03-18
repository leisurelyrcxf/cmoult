#include "listener.h"
#include "manager.h"
#include "dsuthread.h"
#include <stdio.h>
#include <unistd.h>


pthread_t * listener;



pthread_t main_thread;
dsuthreadarg * main_dsu_thread;

void * main_thread_main(void* arg){
  while(1){
    sleep(2);
    puts("hello!");
  }
}


int main(){
  threaded_manager* man;
  puts("starting listener");
  start_threaded_listener();
  listener = access_threaded_listener();
  puts("starting threaded manager");
  man = start_threaded_manager();
  main_dsu_thread = dsuthread_create(&main_thread,NULL,&main_thread_main,NULL);
  pthread_join(*listener,NULL);
  return 0;
}




