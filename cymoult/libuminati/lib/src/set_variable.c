#include "set_variable.h"

int um_set_variable (um_data* dbg, char* name, bool is_local, char* scope, uint64_t val, size_t size)
  {
    if (is_local)
      {
        int derefs = 0;
        while (name[derefs] == '*')
            derefs++;
        uint64_t addr = um_get_local_var_addr (dbg, &(name[derefs]), scope);
        //dereferencing as needed
        while (derefs > 0)
          {
            addr = _um_read_addr (dbg->pid, addr, 8);
            derefs --;
          }
        return _um_write_addr (dbg->pid, addr, val, size);
      }
    //TODO : variables globales
    else
      {
        Dwarf_Attribute attr;

        um_search_first_args args =
          {
            .tag = DW_TAG_variable,
            .wanted_attribute = DW_AT_location,
            .name = name,
            .parent_name = NULL,
            .address = 0,
            .result = &attr
          };

        if (!um_parse(dbg, &um_search_first, &args))
            return -1;

        int derefs = 0;
        while (name[derefs] == '*')
            derefs++;

        uint64_t addr = compute_location(args.result, NULL, dbg);

        //dereferencing as needed
        while (derefs > 0)
        {
            addr = _um_read_addr(dbg->pid, addr, 8);
            derefs --;
        }

        return _um_write_addr (dbg->pid, addr, val, size);
      }
    return -1;
  }
