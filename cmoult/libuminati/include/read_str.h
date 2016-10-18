#ifndef READ_STR_H
#define READ_STR_H

#include "rwutils.h"
#include "stdlib.h"

size_t um_read_str_at_address(um_data* dbg, uint64_t addr, char* dest);

size_t um_read_str_of_pointer(um_data* dbg, uint64_t pointer_addr, char* dest);

size_t um_read_str_of_variable(um_data* dbg, bool is_local, char* name, char* scope, char* dest);


#endif
