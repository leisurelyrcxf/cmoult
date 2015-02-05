#include "get_function_addr.h"

uint64_t um_get_function_addr (um_data* dbg, char* name)
{
    if (!name || !dbg)
        return 0;
    //First check if we have loaded the function into memory earlier
    function* current = dbg->injected;
    while (current)
    {
        if (strcmp(current->name, name) == 0)
            return current->lowpc;
        current = current->next;
    }
    //Then, search in the debug info
    Dwarf_Attribute attr;
    uint64_t addr;
    char* pname = malloc(2);
    sprintf(pname, "*");

    um_search_first_args args =
      {
        .tag = DW_TAG_subprogram,
        .wanted_attribute = DW_AT_low_pc,
        .name = name,
        .parent_name = (const char*) pname,
        .address = 0,
        .result = &attr
      };

    int r = um_parse(dbg, &um_search_first, &args);

    free(pname);
    if (r == 0)
        return 0;
    dwarf_formaddr(args.result, &addr);
    return addr;
}
