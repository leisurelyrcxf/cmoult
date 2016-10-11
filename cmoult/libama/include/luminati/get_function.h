#ifndef GET_FUNCTION_FROM_ADDR
#define GET_FUNCTION_FROM_ADDR

#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"
#include "parse.h"

//Looks in .debug_info for the function owning addr, and returns its name
const char* um_get_function (um_data *dbg, um_frame* context);
#endif
