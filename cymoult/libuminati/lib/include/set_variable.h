#ifndef SET_VARIABLE
#define SET_VARIABLE

#include "libc_includes.h"
#include "get_local_var_addr.h"
#include "rwutils.h"

//Sets variable named name in pid, using debug data dbg, to the value specified by type and val
//You have to say whether the variable is local. If it is global, argument scope is ignored.
//The name of a variable can be dereferenced by preceding it with as many * as you need dereferencements.
int um_set_variable (um_data* dbg, char* name, bool is_local, char* scope, uint64_t val, size_t size);
#endif
