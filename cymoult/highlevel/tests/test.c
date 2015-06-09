#include "listener.h"
#include "manager.h"
#include "dsuthread.h"
#include <stdio.h>
#include <unistd.h>


pthread_t * listener;
dsuthread * main_dsu_thread, * lamathread;

void * main_thread_main(void* arg){
  puts("start main");
  while(1){
    sleep(2);
    puts("hello!");
  }
}


void * lama_main(void * arg){
  while(1){
    sleep(2);
    puts("lama!");
  }
}


  

int main(){
  threaded_manager* man;
  puts("starting listener");
  start_threaded_listener();
  listener = access_threaded_listener();
  puts("starting threaded manager");
  main_dsu_thread = dsuthread_create(NULL,&main_thread_main,NULL);
  lamathread = dsuthread_create(NULL,&lama_main,NULL);
  dsuthread * threads[1] = {main_dsu_thread,};
  man = start_threaded_manager("manager",threads,1);
  pthread_join(*listener,NULL);
  return 0;
}




