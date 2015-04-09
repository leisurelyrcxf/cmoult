#ifndef GET_FRAME_INFO_FROM_ADDR
#define GET_FRAME_INFO_FROM_ADDR
#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"
#include "dwarf_ops.h"

/**/
int get_cfa_from_frame(um_frame* context, um_data* dbg);

/**/
int get_register_from_frame(unsigned int reg, um_frame* context, um_data* dbg);
#endif
