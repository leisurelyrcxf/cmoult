#include <manager.h>
#include <stdio.h>
#include <signal.h>
#include <pthread.h>
#include <dsuthread.h>

extern pthread_t main_thread;


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
  pthread_kill(main_thread,SIGUSR1);
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


