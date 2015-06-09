#include <manager.h>
#include <stdio.h>
#include <signal.h>
#include <pthread.h>
#include <update.h>



extern dsuthread * main_dsu_thread;


void * new_main(void* arg){
  puts("new main!");
  while(1){
    sleep(2);
    puts("lama!");
  }
}

void apply(){
  puts("apply!");
  main_dsu_thread->tsignal = reboot;
  main_dsu_thread->main = &new_main; 
  // pthread_kill(*(main_dsu_thread->thread),SIGUSR1);
  puts("applied!");
}

__attribute__ ((__constructor__))
void update_func(){
  puts("update received!");
  update * upd = create_empty_update("update 1",NULL,0);
  upd->apply = &apply;
  threaded_manager * man = request_threaded_manager();
  puts("sending update!");
  manager_add_update(AS_BASE(man),upd);

}


