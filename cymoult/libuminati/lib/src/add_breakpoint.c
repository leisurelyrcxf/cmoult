#include "add_breakpoint.h"

uint64_t add_breakpoint(pid_t pid, uint64_t addr) {
    uint64_t old_value = _um_read_addr (pid, addr, 1);
    _um_write_addr (pid, addr, (uint64_t) BREAKPOINT, 1);
    return old_value;
}
