#include "redefine.h"
#include "is_function_in_stack.h"
#include "rwutils.h"
#include "unwind.h"
#include "time.h"

int um_redefine(um_data* dbg, char* name1, char* name2){
  uint64_t f1, f2;
  f1 = um_get_function_addr(dbg, name1);
  f2 = um_get_function_addr(dbg, name2);
  if(f1 == 0)
    printf("can't get address of function \"%s\"\n", name1);
  if(f2 == 0){
    printf("can't get address of function \"%s\"\n", name2);
  }
  if (f1 == 0 || f2 == 0)
      return -1;
  insert_jump(dbg->pid, f1, f2);
  return 0;
}

int um_wait_safe_redefine_update_point(um_data* dbg, char* func_name, unsigned long mseconds){
  while(is_function_in_stack(dbg, func_name)){
//    um_print_stack(dbg);
    um_cont(dbg->pid);

    struct timespec spec = {.tv_sec = mseconds/1000, .tv_nsec = (mseconds%1000)*1000000};
    nanosleep(&spec, NULL);
    um_stop(dbg->pid);
    int res = waitpid(dbg->pid,NULL,0);
    if(res != dbg->pid){
      return -1;
    }
  }
  return 0;
}

int um_safe_redefine(um_data* dbg, char* name1, char* name2, unsigned long mseconds){
  if(um_wait_safe_redefine_update_point(dbg, name1, mseconds) == 0)
    return um_redefine(dbg, name1, name2);
}
