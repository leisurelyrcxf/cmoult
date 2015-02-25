#include "add_memory.h"

uint64_t add_memory(pid_t pid, size_t size)
{
    struct user_regs_struct regs;
    uint64_t old_code[CODE_SIZE], new_code[CODE_SIZE];
    memset(&regs, 0, sizeof(struct user_regs_struct));
    //Save registers
    if (_um_read_registers(pid, &regs) != 0)
        return 0;
    //Save present code
    int i;
    for (i = 0; i < CODE_SIZE; i++)
    {
        old_code[i] = _um_read_addr(pid, regs.rip + 8*i, 8);
        if (old_code[i] == 0xffffffffffffffff)
            return 0;
    }
    //Form new code
    new_code[0] = REVERT64(WORD1);
    new_code[1] = REVERT64(WORD2 + (REVERT32(size) << 8));
    new_code[2] = REVERT64(WORD3);
    new_code[3] = REVERT64(WORD4);
    new_code[4] = REVERT64(WORD5);
    //Write new code
    for (i = 0; i < CODE_SIZE; i++)
        if (_um_write_addr(pid, regs.rip + 8*i, new_code[i], 8) == -1)
            return 0xffffffffffffffff;
    //Unpause the program and wait for the SIGTRAP
    um_cont(pid);
    waitpid(pid, 0, 0);
    //Get the address
    struct user_regs_struct new_regs;
    memset(&new_regs, 0, sizeof(struct user_regs_struct));
    if (_um_read_registers(pid, &new_regs) != 0)
        return 0xffffffffffffffff;
    uint64_t address = new_regs.rax;
    //Restore old code and registers
    for (i = 0; i < CODE_SIZE; i++)
        if (_um_write_addr(pid, regs.rip + 8*i, old_code[i], 8) == -1)
            return 0xffffffffffffffff;
    if (_um_write_registers(pid, &regs) != 0)
        return 0xffffffffffffffff;
    return address;
}
