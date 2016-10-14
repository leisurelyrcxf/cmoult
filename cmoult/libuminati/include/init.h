#ifndef POPULATE_DEBUG_DATA
#define POPULATE_DEBUG_DATA

#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"


Dwfl *pid_to_dwfl (pid_t pid);

/* This function retrieves the CFI from mod and place it into dbg */
int get_cfi (Dwfl_Module* mod, um_data* dbg);

int um_init (um_data** dbg, pid_t pid, const char* fname);

#endif
