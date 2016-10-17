#ifndef SET_VARIABLE
#define SET_VARIABLE

#include "libc_includes.h"
#include "get_local_var_addr.h"
#include "rwutils.h"

#define AUTO_REALLOC 0x0
#define FORCE_REALLOC  0x1
#define NOT_REALLOC 0x2


#define MEMCPY_LOCAL_TO_LOCAL 0x0
#define MEMCPY_REMOTE_TO_LOCAL 0x1
#define MEMCPY_LOCAL_TO_REMOTE 0x2
#define MEMCPY_REMOTE_TO_REMOTE 0x3

int um_set_addr (um_data* dbg, uint64_t addr, uint64_t val, size_t size);

//Sets variable named name in pid, using debug data dbg, to the value specified by type and val
//If it is global, argument scope is the file name.
//The name of a variable can be dereferenced by preceding it with as many * as you need dereferencements.
//if scope is NULL, it's ignored
int um_set_variable (um_data* dbg, bool is_local, char* name, char* scope, uint64_t val, size_t size);

uint64_t um_get_addr_by_pointer_addr(um_data* dbg, uint64_t pointer_addr);

uint64_t um_malloc(um_data* dbg, size_t malloc_size);

uint64_t um_realloc(um_data* dbg, uint64_t old_addr, size_t old_size, size_t new_size);

int um_memcpy(um_data* dbg, uint64_t dest, uint64_t src, size_t n, int memcpy_flag);

uint64_t um_write_str(um_data* dbg, uint64_t str_addr, char* new_str, int flag);

uint64_t um_set_str_pointer(um_data* dbg, uint64_t str_pointer_addr, char* new_str, int flag);

uint64_t um_transform_struct(um_data* dbg, uint64_t pointer_addr, size_t old_size, size_t new_size, int (*transform)(um_data*, void*, void*, int flag), int flag);

uint64_t um_transform_struct_pointer(um_data* dbg, uint64_t pointer_addr, size_t old_size, size_t new_size, int (*transform)(um_data*, void*, void*, int flag), int flag);

uint64_t um_set_by_array_variable(um_data* dbg, bool is_local, char* name, char* scope, void* new_values, size_t new_size);


#endif
