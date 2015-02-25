#ifndef GET_LOCAL_VAR_ADDR
#define GET_LOCAL_VAR_ADDR

#include "libc_includes.h"
#include "data_structs.h"
#include "get_function.h"
#include "parse.h"
#include "unwind.h"

//Get the adress of variable named name in scope scope in process pid, using debug data dbg
//scope is optional, if NULL the function returns the last definition of the identifier
uint64_t um_get_local_var_addr(um_data* dbg, const char* name, const char* scope);
#endif
