#include "listener.h"
#include <stdio.h>

pthread_t * listener;


int main(){
  puts("starting listener");
  start_threaded_listener();
  listener = access_threaded_listener();
  pthread_join(*listener,NULL);

  return 0;
}




