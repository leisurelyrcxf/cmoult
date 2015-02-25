#ifndef ADD_BREAKPOINT
#define ADD_BREAKPOINT

#include "libc_includes.h"
#include "rwutils.h"

#define BREAKPOINT 0xcc //int3

#define REVERT32(n) ((((n) & 0xff000000) >> 24) + (((n) & 0xff0000) >> 8) + (((n) & 0xff00) << 8) + (((n) & 0xff) << 24))
#define REVERT64(n) ((((n) & 0xff00000000000000) >> 56) + (((n) & 0xff000000000000) >> 40) + (((n) & 0xff0000000000) >> 24) + (((n) & 0xff00000000) >> 8) + \
        (((n) & 0xff000000) << 8) + (((n) & 0xff0000) << 24) + (((n) & 0xff00) << 40) + (((n) & 0xff) << 56))

uint64_t add_breakpoint(pid_t pid, uint64_t addr);

#endif
