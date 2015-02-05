#include "get_function.h"

const char* um_get_function (um_data *dbg, um_frame* context)
  {
    if (!context || !dbg)
        return NULL;
    Dwarf_Attribute attr;
    char* pname = malloc(2);
    sprintf(pname, "*");

    um_search_first_args args =
      {
        .tag = DW_TAG_subprogram,
        .wanted_attribute = DW_AT_name,
        .name = NULL,
        .parent_name = (const char*) pname,
        .address = context->rip,
        .result = &attr
      };

    int r = um_parse(dbg, &um_search_first, &args);
    free(pname);
    if (!args.result || r == 0)
        return NULL;
    return dwarf_formstring(args.result);
  }
