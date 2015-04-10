#ifndef DESTROY
#define DESTROY

#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"

/*Frees the whole stack state list, starting from the end*/
void um_destroy_stack(um_frame* list);

/*Frees the whole struct um_data*/
void um_end (um_data* dbg);

#endif
