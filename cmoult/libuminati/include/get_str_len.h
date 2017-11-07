#ifndef GET_STR_LEN_H
#define GET_STR_LEN_H

#include "rwutils.h"
#include "stdlib.h"

size_t um_get_str_len_at_address(um_data* dbg, uint64_t addr);

size_t um_get_str_len_of_pointer(um_data* dbg, uint64_t pointer_addr);

size_t um_get_str_len_of_variable(um_data* dbg, bool is_local, char* name, char* scope);


#endif
