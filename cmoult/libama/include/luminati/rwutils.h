#ifndef RWUTILS
#define RWUTILS

#include "libc_includes.h"
#include "data_structs.h"

#define LITTLEENDIAN

int um_attach (pid_t pid);
int _um_write_addr (pid_t pid, uint64_t addr, uint64_t value, size_t size);
int um_write_addr (um_data* dbg, uint64_t addr, uint64_t value, size_t size);
int um_write_addr_n (um_data* dbg, uint64_t addr, void* values, int n, size_t size);
int _um_write_registers(pid_t pid, struct user_regs_struct* regs);
int um_write_registers(um_data* dbg, struct user_regs_struct* regs);
uint64_t _um_read_addr (pid_t pid, uint64_t addr, size_t size);
uint64_t um_read_addr (um_data* dbg, uint64_t addr, size_t size);
int _um_read_registers(pid_t pid, struct user_regs_struct* regs);
int um_read_registers(um_data* dbg, struct user_regs_struct* regs);
int um_cont (pid_t pid);
int um_detach (pid_t pid);

#endif
