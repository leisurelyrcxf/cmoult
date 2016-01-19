#ifndef GET_FUNCTION_ADDR_FROM_NAME
#define GET_FUNCTION_ADDR_FROM_NAME

#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"
#include "parse.h"

//Looks in .debug_info for the function named name, and returns its first address
uint64_t um_get_function_addr (um_data *dbg, char* name);
#endif
