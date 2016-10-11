#include "get_var_addr.h"

uint64_t um_get_var_addr(um_data* dbg, bool is_local, const char* name, const char* scope){
  if(!scope){
    return -1;
  }

  if(is_local){
    int derefs = 0;
    while (name[derefs] == '*')
        derefs++;
    uint64_t addr = um_get_local_var_addr (dbg, &(name[derefs]), scope);
    if (addr == 0xffffffffffffffff)
        return -1;
    //dereferencing as needed
    while (derefs > 0) {
        addr = _um_read_addr (dbg->pid, addr, 8);
        derefs --;
        if (addr == 0xffffffffffffffff)
            return -1;
    }
    return addr;
  }else{
    int derefs = 0;
    while (name[derefs] == '*')
      derefs++;

    Dwarf_Attribute attr;
    um_search_first_args args = {
      .tag = DW_TAG_variable,
      .wanted_attribute = DW_AT_location,
      .name = name+derefs,
      .parent_name = scope,
      .address = 0,
      .result = &attr
    };

    if (!um_parse(dbg, &um_search_first, &args))
      return -1;

    uint64_t addr = compute_location(args.result, NULL, dbg);
    if (!addr)
      return -1;

    //dereferencing as needed
    while (derefs > 0) {
      addr = _um_read_addr(dbg->pid, addr, 8);
      derefs --;
      if (addr == 0xffffffffffffffff)
        return -1;
    }

    return addr;
  }
}
