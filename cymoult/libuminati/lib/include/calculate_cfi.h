#ifndef CALCULATE_CFI
#define CALCULATE_CFI

#include "libc_includes.h"
#include "dwarf_ops.h"
#include "opcode_processors.h"

void calculate_cfi (unsigned char* code, size_t size, op_processors_t opcode_processors[], location** result);

#endif
