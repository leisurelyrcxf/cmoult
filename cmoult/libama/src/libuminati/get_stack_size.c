#include "get_stack_size.h"

int um_get_stack_size (um_data* dbg, um_frame* stack){
    int i = 0;
    while (stack) {
        i++;
        stack = um_get_next_frame(stack);
    }
    return i;
}
