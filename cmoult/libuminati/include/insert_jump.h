#ifndef INSERT_JUMP
#define INSERT_JUMP

#include "libc_includes.h"
#include "rwutils.h"

#define NEAR_JUMP_OPCODE 0xeb
#define NEAR_JUMP_MAXVAL INT8_MAX
#define NEAR_JUMP_MINVAL INT8_MIN

#define LONG_JUMP_OPCODE 0xe9
#define LONG_JUMP_MAXVAL INT32_MAX
#define LONG_JUMP_MINVAL INT32_MIN

#define REVERT16(n) ((((n) & 0xff00) >> 8) + (((n) & 0xff) << 8))
#define REVERT32(n) ((((n) & 0xff000000) >> 24) + (((n) & 0xff0000) >> 8) + (((n) & 0xff00) << 8) + (((n) & 0xff) << 24))
#define REVERT64(n) ((((n) & 0xff00000000000000) >> 56) + (((n) & 0xff000000000000) >> 40) + (((n) & 0xff0000000000) >> 24) + (((n) & 0xff00000000) >> 8) + \
        (((n) & 0xff000000) << 8) + (((n) & 0xff0000) << 24) + (((n) & 0xff00) << 40) + (((n) & 0xff) << 56))

void insert_jump (pid_t pid, uint64_t from, uint64_t to);
#endif
