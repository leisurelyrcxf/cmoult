#ifndef UNWIND
#define UNWIND

#include "libc_includes.h"
#include "data_structs.h"
#include "rwutils.h"
#include "get_frame_info.h"
#include "get_function.h"


#define UM_UNWIND_STOPWHENFOUND 1
#define UM_UNWIND_RETURNLAST 2


//Unwinds the stack in thread pid, using the debug info in dbg, until a um_frame corresponding to function target.
//Updates the cache to reflect the new stack state and returns a pointer to the um_frame associated to function "target"
//If target is not present in the stack, or if it is NULL, the function just performs a full um_unwinding and returns NULL after having updated cache
//Flags : see below
um_frame* um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags);

void um_print_stack(um_data* dbg);

#endif
