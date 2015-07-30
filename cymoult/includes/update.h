#ifndef UPDATE_H
#define UPDATE_H

#include <stdlib.h>
#include "dsuthread.h"

typedef enum ra {
  yes,
  no,
  never
} req_ans;

typedef struct{
  char * name;
  dsuthread ** threads;
  size_t nthreads;
  int max_tries;
  req_ans (*check_requirements)();
  void (*preupdate_setup)();
  char (*check_alterability)();
  char (*wait_alterability)();
  void (*clean_failed_alterability)();
  void (*apply)();
  void (*preresume_setup)();
  char (*wait_over)();
  char (*check_over)();
  void (*cleanup)();
  char applied;
}update;

/* Empty default update function */

req_ans req_ans_empty_step();
void void_empty_step();
char char_empty_step();

/* Help for initializing updates */

update * create_empty_update(char* name, dsuthread ** threads, int nthreads);




#endif /* End ifndef UPDATE_H */
