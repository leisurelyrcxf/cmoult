#ifndef GET_VAR_SIZE
#define GET_VAR_SIZE

#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"
#include "parse.h"

size_t um_get_var_size (um_data *dbg, const char* var_name, const char* scope_name);

#endif
