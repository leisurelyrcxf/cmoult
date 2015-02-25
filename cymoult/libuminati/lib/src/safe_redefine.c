#include "safe_redefine.h"

int um_safe_redefine(um_data* dbg, char* name1, char* name2)
  {
    uint64_t f1, f2;
    f1 = um_get_function_addr(dbg, name1);
    f2 = um_get_function_addr(dbg, name2);
    if (f1 == 0 || f2 == 0)
        return -1;

    insert_jump(dbg->pid, f1, f2);
    return 0;
  }
