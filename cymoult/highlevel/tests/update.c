#include <manager.h>
#include <stdio.h>
#include <signal.h>
#include <pthread.h>
#include <dsuthread.h>


extern dsuthreadarg * main_dsu_thread;

void * new_main(void* arg){
  puts("lama!");
  while(1){
    puts("toto");
    sleep(2);
  }

}



char requirements(){
  puts("requirements");
  return 1;
}
char alterability(){
  puts("alterability");
  return 1;
}
char over(){
  puts("over");
  return 1;
}
void apply(){
  puts("apply!");
  main_dsu_thread->signal = REBOOT;
  main_dsu_thread->start_routine = &new_main; 
  pthread_kill(*(main_dsu_thread->thread),SIGUSR1);
  sleep(6);
  main_dsu_thread->signal = NONE;
  puts("applied!");
}

__attribute__((__constructor__)) void update_func(){
  update * upd = malloc(sizeof(update));
  upd->requirements = &requirements;
  upd->alterability = &alterability;
  upd->apply = &apply;
  upd->over = &over;
  upd->applied = 0;
  threaded_manager * man = request_threaded_manager();
  add_update_threaded_manager(man,upd);

}


