#include "insert_jump.h"

void insert_jump (pid_t pid, uint64_t from, uint64_t to)
{
    int64_t diff = to-(from+2);
    if (diff >= NEAR_JUMP_MINVAL && diff <= NEAR_JUMP_MAXVAL) { //near jump
        long data = (NEAR_JUMP_OPCODE + ((diff&0xff) << 8)) & 0xffff;
        _um_write_addr(pid, from, data, 8);
    } else if (diff >= LONG_JUMP_MINVAL && diff <= LONG_JUMP_MAXVAL) { //long jump
        diff = to-(from+5);
        long data = (LONG_JUMP_OPCODE + ((diff&0xffffffff) << 8)) & 0xffffffffff;
        _um_write_addr(pid, from, data, 8);
    }
}
