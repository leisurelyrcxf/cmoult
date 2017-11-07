#ifndef SAFE_REDEFINE
#define SAFE_REDEFINE

#include "libc_includes.h"
#include "data_structs.h"
#include "get_function_addr.h"
#include "insert_jump.h"

int um_redefine(um_data* dbg, char* name1, char* name2);

int um_wait_safe_redefine_update_point(um_data* dbg, char* func_name, unsigned long mseconds);

int um_safe_redefine(um_data* dbg, char* name1, char* name2, unsigned long mseconds);

#endif
