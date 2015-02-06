#include "get_var_size.h"

size_t um_get_var_size (um_data *dbg, const char* var_name, const char* scope_name)
  {
    Dwarf_Attribute attr;

    um_search_first_args args =
      {
        .tag = DW_TAG_variable,
        .wanted_attribute = DW_AT_type,
        .name = var_name,
        .parent_name = scope_name,
        .address = 0,
        .result = &attr
      };

    int r = um_parse(dbg, &um_search_first, &args);
    if (r == 0)
        return 0;

    Dwarf_Die type_die;
    if (dwarf_formref_die(&attr, &type_die))
      {
        size_t size = dwarf_bytesize(&type_die);
        return size;
      }
    return 0;
  }
