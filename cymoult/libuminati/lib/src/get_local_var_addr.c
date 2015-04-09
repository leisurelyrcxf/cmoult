#include "get_local_var_addr.h"

uint64_t um_get_local_var_addr(um_data* dbg, const char* name, const char* scope) {
    if (!name)
        return 0;

    int r = 0;

    if (scope) {
        Dwarf_Attribute attr;

        um_search_first_args args = {
            .tag = DW_TAG_variable,
            .wanted_attribute = DW_AT_location,
            .name = name,
            .parent_name = scope,
            .address = 0,
            .result = &attr
        };

        r = um_parse(dbg, &um_search_first, &args);

        if (!args.result || r == 0)
            return 0;

        //um_unwind until we find scope
        um_frame* scope_um_frame;
        scope_um_frame = um_unwind(dbg, scope, &scope_um_frame, UM_UNWIND_STOPWHENFOUND);

        //if the scope function is not there, neither is the variable
        if (!scope_um_frame)
            return 0;

        return compute_location(args.result, scope_um_frame, dbg);
    } else {
        //um_unwind all the stack
        um_frame* stack;
        um_unwind(dbg, NULL, &stack, 0);

        um_frame* current_stack_pointer = stack;

        //walk the stack
        while (current_stack_pointer) {
            const char* function = um_get_function(dbg, current_stack_pointer);
            if (!function) {
                current_stack_pointer = current_stack_pointer->next;
                continue;
            }

            Dwarf_Attribute attr;

            um_search_first_args args = {
                .tag = DW_TAG_variable,
                .wanted_attribute = DW_AT_location,
                .name = name,
                .parent_name = function,
                .address = 0,
                .result = &attr
            };

            r = um_parse(dbg, &um_search_first, &args);

            if (!args.result || r == 0) {
                current_stack_pointer = current_stack_pointer->next;
                continue;
            }

            return compute_location(args.result, current_stack_pointer, dbg);

            current_stack_pointer = current_stack_pointer->next;
        }
    }

    return 0;
}
