#include "unwind.h"

um_frame* um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags) {

    if (!cache)
        return NULL;

    //Flag processing
    bool stop_when_found = flags & 01;
    bool return_last = flags & 02;

    um_frame* res = NULL;

    //Getting registers
    struct user_regs_struct regs = {0};
    if (_um_read_registers(dbg->pid, &regs) != 0)
        return NULL;

    //Creating useful variables
    um_frame* stack = (um_frame*) malloc (sizeof(um_frame));
    um_frame* current_stack_pointer = stack;

    //Initializing
    current_stack_pointer->rip = regs.rip;
    current_stack_pointer->regs[REG_RSP] = regs.rsp;
    current_stack_pointer->regs[REG_RBP] = regs.rbp;
    get_cfa_from_frame(current_stack_pointer, dbg);
    get_register_from_frame(REG_RA, current_stack_pointer, dbg);

    //Iterating
    while (1) {
        //Actualizing pointers
        um_frame* previous_stack_pointer = current_stack_pointer;
        current_stack_pointer->next = (um_frame*) malloc (sizeof(um_frame));
        current_stack_pointer = current_stack_pointer->next;

        current_stack_pointer->rip = 0;
        current_stack_pointer->cfa = 0;
        current_stack_pointer->regs[REG_RBP] = 0;
        current_stack_pointer->regs[REG_RSP] = 0;
        current_stack_pointer->regs[REG_RA] = 0;
        current_stack_pointer->rip = _um_read_addr(dbg->pid, previous_stack_pointer->regs[REG_RA], 8);
        //Check if we have finished um_unwinding
        if (current_stack_pointer->rip == 0 || current_stack_pointer->rip == 0xffffffffffffffff)
            break;

        current_stack_pointer->regs[REG_RSP] = previous_stack_pointer->cfa;
        if (get_cfa_from_frame(current_stack_pointer, dbg) == 0) {
            if (get_register_from_frame(REG_RBP, current_stack_pointer, dbg) > 0)
                current_stack_pointer->regs[REG_RBP] = _um_read_addr(dbg->pid, previous_stack_pointer->regs[REG_RBP], 8);
        }
        else {
            current_stack_pointer->regs[REG_RBP] = _um_read_addr(dbg->pid, previous_stack_pointer->regs[REG_RBP], 8);
            if (get_cfa_from_frame(current_stack_pointer, dbg) != 0)
                break;
        }
        if (get_register_from_frame(REG_RA, current_stack_pointer, dbg) != 0)
            break;

        //if this um_frame corresponds to the wanted scope, we set res
        if (target) {
            const char* function = um_get_function(dbg, current_stack_pointer);
            if (function) {
                if (strcmp(target, function) == 0) {
                    if (!res || return_last)
                        res = current_stack_pointer;
                    if (stop_when_found)
                        break;
                }
            }
        }
    }

    //Terminating
    current_stack_pointer->next = NULL;

    *cache = stack;
    return res;
}
