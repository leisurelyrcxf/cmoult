#ifndef GENERATE_TRACE
#define GENERATE_TRACE
#include "libc_includes.h"
#include "data_structs.h"
#include "get_function.h"
#include "get_next_frame.h"

void um_generate_trace (um_data* dbg, um_frame* stack, char** functions, uint64_t* addresses);

#endif
