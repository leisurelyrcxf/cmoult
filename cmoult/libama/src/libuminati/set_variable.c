#include "set_variable.h"
#include "get_var_addr.h"
#include "add_memory.h"

int um_set_variable (um_data* dbg, bool is_local, char* name, char* scope, uint64_t val, size_t size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0xffffffffffffffff){
    return -1;
  }

  return _um_write_addr (dbg->pid, addr, val, size);
}

uint64_t um_realloc_variable_in_heap(um_data* dbg, bool is_local, char* name, char* scope, size_t realloc_size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);

//  uint64_t addr = um_get_var_addr(dbg, false, "*obj", "src/test.c");
  if(addr == (uint64_t)-1 || addr == 0){
    fprintf(stderr, "failed to get address of variable %s\n", name);
    return 0xffffffffffffffff;
  }
  printf("variable %s at %p\n", name, (void*)addr);

  uint64_t realloc_addr = add_memory(dbg->pid, realloc_size);
  if(realloc_addr == (uint64_t)-1){
    fprintf(stderr, "can't realloc\n");
    return 0xffffffffffffffff;
  }

  if(_um_write_addr(dbg->pid, addr, realloc_addr, sizeof(uint64_t)) != 0){
    fprintf(stderr, "failed to write to address %p\n", (void*)addr);
    return 0xffffffffffffffff;
  };

  return realloc_addr;
}

int um_realloc_and_set_variable_in_heap(um_data* dbg, bool is_local, char* name, char* scope, size_t realloc_size, void* new_values, size_t copy_size){
  if(copy_size > realloc_size){
    fprintf(stderr, "the size of the reallocated memory must not be smaller than the copy size\n");
    return -1;
  }
  uint64_t realloc_addr = um_realloc_variable_in_heap(dbg, is_local, name, scope, realloc_size);
  if(realloc_addr == 0xffffffffffffffff){
    return -1;
  }

  um_write_addr_n(dbg, realloc_addr, new_values, copy_size, 1);

//  void* new_empty = malloc(realloc_size - copy_size);
//  memset(new_empty, 0, realloc_size - copy_size);
//  um_write_addr_n(dbg, realloc_addr + copy_size, new_empty, realloc_size - copy_size, 1);
//  free(new_empty);
}
