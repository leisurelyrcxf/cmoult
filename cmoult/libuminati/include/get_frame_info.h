#ifndef GET_FRAME_INFO_FROM_ADDR
#define GET_FRAME_INFO_FROM_ADDR
#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"
#include "dwarf_ops.h"


int get_cfa_from_frame(um_frame* context, um_data* dbg);

int get_register_from_frame(unsigned int reg, um_frame* context, um_data* dbg);

int get_cfa_from_dwfl_module(Dwfl_Module* mod, Dwarf_Addr pc, um_frame* context, um_data* dbg);

int get_register_from_dwfl_module(unsigned int reg, Dwfl_Module* mod, Dwarf_Addr pc, um_frame* context, um_data* dbg);

#endif
