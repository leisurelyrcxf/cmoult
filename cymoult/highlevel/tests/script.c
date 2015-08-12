#include <stdio.h>
#include <pthread.h>
#include "update.h"

char * name = "toto";
pthread_t * threads = NULL;
int nthreads = 0;
int max_tries = 3;

req_ans check_requirements(){
  puts("coucou");
  return never;
}


