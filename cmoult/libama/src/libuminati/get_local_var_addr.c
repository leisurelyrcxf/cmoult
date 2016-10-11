#include "get_local_var_addr.h"

uint64_t um_get_local_var_addr(um_data* dbg, const char* name, const char* scope) {
    if (!name)
        return -1;

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

        if (!args.result || !r)
            return -1;

        //um_unwind until we find scope
        um_frame* scope_um_frame;
        scope_um_frame = um_unwind(dbg, scope, &scope_um_frame, UM_UNWIND_STOPWHENFOUND);
        if (!scope_um_frame)
            return 0;

        uint64_t addr = compute_location(args.result, scope_um_frame, dbg);
        return addr;
    }

    return -1;
}
