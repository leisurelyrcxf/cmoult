#include "listener.h"
#include "manager.h"
#include <stdio.h>

pthread_t * listener;


int main(){
  threaded_manager* man;
  puts("starting listener");
  start_threaded_listener();
  listener = access_threaded_listener();
  puts("starting threaded manager");
  man = start_threaded_manager();
  pthread_join(*listener,NULL);

  return 0;
}




