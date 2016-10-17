#include "get_var_size.h"

size_t um_get_var_size (um_data *dbg, const char* var_name, const char* scope_name)
  {
    um_search_first_args args =
      {
        .tag = DW_TAG_variable,
        .wanted_attribute = DW_AT_type,
        .name = var_name,
        .parent_name = scope_name,
        .address = 0,
        .result = NULL
      };

    int r = um_parse(dbg, &um_search_first, &args);

    if(!args.result){
      return 0;
    }

    if (r == 0){
      free(args.result);
      return 0;
    }

    Dwarf_Die type_die;
    if (dwarf_formref_die(args.result, &type_die))
      {
        size_t size = dwarf_bytesize(&type_die);
        free(args.result);
        return size;
      }
    free(args.result);
    return 0;
  }
