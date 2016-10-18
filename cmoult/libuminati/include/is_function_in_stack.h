#ifndef SAFE_REDEFINE_WAIT
#define SAFE_REDEFINE_WAIT

#include "libc_includes.h"
#include "data_structs.h"
#include "rwutils.h"
#include "unwind.h"

bool is_function_in_stack(um_data* dbg, char* name);
#endif
