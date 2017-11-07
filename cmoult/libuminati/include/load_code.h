#ifndef LOAD_CODE
#define LOAD_CODE
//Because BFD wants us to use autotools
#define PACKAGE
#define PACKAGE_VERSION

#include "libc_includes.h"
#include "binutils_includes.h"
#include "add_memory.h"
#include "data_structs.h"

int um_load_code (um_data* dbg, const char* file_name);

#endif
