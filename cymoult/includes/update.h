#ifndef UPDATE_H
#define UPDATE_H

#include <stdlib.h>

typedef enum ra {
  yes,
  no,
  never
} req_ans;

typedef struct{
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
}update_functions;

/* Empty default update function */

req_ans req_ans_empty_step();
void void_empty_step();
char char_empty_step();

/* Help for initializing updates */


#endif /* End ifndef UPDATE_H */
