#include "is_function_in_stack.h"

bool is_function_in_stack(um_data* dbg, char* name){
    um_frame* cache = NULL;
    if (!name)
        return false;
    if(um_unwind(dbg, name, &cache, UM_UNWIND_STOPWHENFOUND) == NULL){
      return false;
    }
    return true;
}
