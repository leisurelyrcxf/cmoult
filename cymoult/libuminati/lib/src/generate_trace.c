#include "generate_trace.h"

void um_generate_trace (um_data* dbg, um_frame* stack, char** functions, uint64_t* addresses) {
    if (!dbg || !stack || !functions || !addresses)
        return;
    do {
        *functions = (char*) um_get_function(dbg, stack);
        *addresses = stack->rip;
        functions++;
        addresses++;
    } while ((stack = um_get_next_frame(stack)))
}
