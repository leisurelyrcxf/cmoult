#include "wait_out_of_stack.h"

int um_wait_out_of_stack(um_data* dbg, char* name){
    um_frame* cache = NULL;
    if (!name)
        return -1;
    if ((cache = um_unwind(dbg, name, &cache, UM_UNWIND_RETURNLAST))) {
        if (!(cache->next))
            return -2;

        printf("in stack!\n");
        //Set a breakpoint after the function's return
        uint64_t old_value = add_breakpoint(dbg->pid, cache->next->rip);
        //Let the function run
        um_cont(dbg->pid);
        waitpid(dbg->pid, 0, 0);
        //Delete the breakpoint and fix RIP
        _um_write_addr(dbg->pid, cache->next->rip, old_value, 1);
        struct user_regs_struct regs;
        _um_read_registers(dbg->pid, &regs);
        regs.rip = cache->next->rip;
        _um_write_registers(dbg->pid, &regs);
    }
    return 0;
}
