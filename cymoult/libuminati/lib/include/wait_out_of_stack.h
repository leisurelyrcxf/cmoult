#ifndef SAFE_REDEFINE_WAIT
#define SAFE_REDEFINE_WAIT

#include "libc_includes.h"
#include "add_breakpoint.h"
#include "data_structs.h"
#include "rwutils.h"
#include "unwind.h"

int um_wait_out_of_stack(um_data* dbg, char* name);
#endif
