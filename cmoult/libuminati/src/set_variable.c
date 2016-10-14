#include "set_variable.h"
#include "get_var_addr.h"

int um_set_variable (um_data* dbg, bool is_local, char* name, char* scope, uint64_t val, size_t size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0xffffffffffffffff){
    return -1;
  }

  return _um_write_addr (dbg->pid, addr, val, size);
}
