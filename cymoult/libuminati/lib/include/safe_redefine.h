#ifndef SAFE_REDEFINE
#define SAFE_REDEFINE

#include "libc_includes.h"
#include "data_structs.h"
#include "get_function_addr.h"
#include "insert_jump.h"

int um_safe_redefine(um_data* dbg, char* name1, char* name2);
#endif
