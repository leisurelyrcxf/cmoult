#include "read_str.h"
#include "get_var_addr.h"

size_t um_read_str_at_address(um_data* dbg, uint64_t addr, char* dest, size_t size){
  if(addr == 0 || addr == -1){
    return -1;
  }

  size_t number_read = 0;
  while(1){
    uint64_t result = um_read_addr(dbg, addr, 1);
    char c = result & 0xff;
    if(c == '\0'){
      number_read ++;
      *(dest + number_read) = c;
      return number_read - 1;
    }

    *(dest + number_read) = c;
    addr ++;
    number_read ++;
    if(number_read >= size){
      return number_read;
    }
  }
}

size_t um_read_str_of_pointer(um_data* dbg, uint64_t pointer_addr, char* dest, size_t size){
  uint64_t addr = um_read_addr(dbg, pointer_addr, 8);
  if(addr == 0 || addr == -1){
    fprintf(stderr, "failed to read address %p\n", (void*)pointer_addr);
    return -1;
  }
  return um_read_str_at_address(dbg, addr, dest, size);
}

size_t um_read_str_of_variable(um_data* dbg, bool is_local, char* name, char* scope, char* dest, size_t size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0 || addr == -1){
    fprintf(stderr, "failed to get address of variable %s in %s\n", name, scope);
    return -1;
  }
  return um_read_str_of_pointer(dbg, addr, dest, size);
}
