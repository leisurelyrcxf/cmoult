#include <stdio.h>
#include <pthread.h>
#include "codeloader.h"

void main(){
  pthread_t * loader = access_code_loader();
  start_code_loader();
  load_code("script.so");
  pthread_join(*loader,NULL);
}
