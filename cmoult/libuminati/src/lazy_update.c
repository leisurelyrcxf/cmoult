#include "lazy_update.h"
#include "set_variable.h"
#include "get_var_addr.h"


int lazy_update_watch_access_callback(um_data* dbg, uint64_t addr, size_t len, int (*update)(um_data*, void*, size_t)){
  void* buffer = malloc(len);
  if(um_memcpy(dbg, (uint64_t)buffer, addr, len, MEMCPY_REMOTE_TO_LOCAL) != 0){
    free(buffer);
    return -1;
  }
  if(update(dbg, buffer, len) != 0){
    free(buffer);
    return -1;
  }
  if(um_memcpy(dbg, addr, (uint64_t)buffer, len, MEMCPY_LOCAL_TO_REMOTE) != 0){
    free(buffer);
    return -1;
  }
  free(buffer);
  return 0;
}

int um_lazy_update_address(um_data* dbg, uint64_t addr, size_t len, int (*update)(um_data*, void*, size_t)){
  return um_watch_addr_access(dbg, addr, len, lazy_update_watch_access_callback, update);
}


int um_lazy_update_variable(um_data* dbg, bool is_local, char* name, char* scope, size_t size, int (*update)(um_data*, void*, size_t)){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0 || addr == -1){
    fprintf(stderr, "can't find addr of variable %s in scope %s\n", name, scope);
    return -1;
  }
  return um_lazy_update_address(dbg, addr, size, update);
}
