#include "set_variable.h"
#include "get_var_addr.h"
#include "add_memory.h"
#include "get_str_len.h"

int um_set_addr (um_data* dbg, uint64_t addr, uint64_t val, size_t size){
  if(addr == 0xffffffffffffffff){
    return -1;
  }

  return _um_write_addr (dbg->pid, addr, val, size);
}

int um_set_variable (um_data* dbg, bool is_local, char* name, char* scope, uint64_t val, size_t size){
  return um_set_addr(dbg, um_get_var_addr(dbg, is_local, name, scope), val, size);
}

uint64_t um_get_addr_by_pointer_addr(um_data* dbg, uint64_t pointer_addr){
  return um_read_addr(dbg, pointer_addr, 8);
}

int um_repoint_pointer_to_addr(um_data* dbg, uint64_t pointer_addr, uint64_t addr){
  return um_write_addr(dbg, pointer_addr, addr, 8);
}

uint64_t um_malloc(um_data* dbg, size_t malloc_size){
  uint64_t malloc_addr = add_memory(dbg->pid, malloc_size);
  if(malloc_addr == (uint64_t)-1 || malloc_addr == 0){
    fprintf(stderr, "can't malloc memory of %lu bytes\n", malloc_size);
    return 0;
  }
  return malloc_addr;
}

uint64_t um_realloc(um_data* dbg, uint64_t old_addr, size_t old_size, size_t new_size){
  if(old_addr == 0 || old_addr == -1 || new_size > old_size){
    return um_malloc(dbg, new_size);
  }
  return old_addr;
}

int um_memcpy(um_data* dbg, uint64_t dest, uint64_t src, size_t n, int memcpy_flag){
  if(dest == 0 || dest == -1 || src == 0 || src == -1){
    return -1;
  }

  switch(memcpy_flag){
    case MEMCPY_LOCAL_TO_LOCAL:
      memcpy((void*)dest, (void*)src, n);
      return 0;
    case MEMCPY_REMOTE_TO_LOCAL:
    {
      if(um_read_addr_n(dbg, src, (void*)dest, n, 1) != 0){
        return -1;
      }
      return 0;
    }
    case MEMCPY_LOCAL_TO_REMOTE:
    {
      if(um_write_addr_n(dbg, dest, (void*)src, n, 1) != 0){
        return -1;
      }
      return 0;
    }
    case MEMCPY_REMOTE_TO_REMOTE:
    {
      void* temp_buf = malloc(n);
      int result = um_memcpy(dbg, (uint64_t)temp_buf, src, n, MEMCPY_REMOTE_TO_LOCAL);
      if(result != 0){
        free(temp_buf);
        return result;
      }
      result = um_memcpy(dbg, dest, (uint64_t)temp_buf, n, MEMCPY_LOCAL_TO_REMOTE);
      if(result != 0){
        free(temp_buf);
        return result;
      }
      return 0;
    }
    default:
      return -1;
  }
}

uint64_t um_write_str(um_data* dbg, uint64_t str_addr, char* new_str, int flag){
  if(new_str == NULL){
    return -1;
  }
  size_t new_len = strlen(new_str);
  uint64_t new_size = new_len + 1;

  uint64_t addr;
  if(flag == FORCE_REALLOC){
    addr = um_malloc(dbg, new_size);
  }else if(flag == NOT_REALLOC){
    if(str_addr == 0 || str_addr == -1){
      return -1;
    }
    addr = str_addr;
  }else if(flag == AUTO_REALLOC){
    size_t old_len = um_get_str_len_at_address(dbg, str_addr);
    if(old_len == -1){
      addr = um_malloc(dbg, new_size);
    }else{
      uint64_t old_size = old_len + 1;
      addr = um_realloc(dbg, str_addr, old_size, new_size);
    }
  }else{
    return -1;
  }
  if(um_memcpy(dbg, addr, (uint64_t)new_str, new_size, MEMCPY_LOCAL_TO_REMOTE) != 0){
    return -1;
  }
  return addr;
}

uint64_t um_set_str_pointer(um_data* dbg, uint64_t str_pointer_addr, char* new_str, int flag){
  uint64_t str_addr = um_get_addr_by_pointer_addr(dbg, str_pointer_addr);
  if(str_addr == 0 || str_addr == -1){
    return -1;
  }

  uint64_t addr = um_write_str(dbg, str_addr, new_str, flag);
  if(addr == 0 || addr == -1){
    return -1;
  }

  if(um_repoint_pointer_to_addr(dbg, str_pointer_addr, addr) != 0){
    return -1;
  }
  return addr;
}

uint64_t um_write_values(um_data* dbg, uint64_t exisiting_addr, size_t old_size, void* new_values, size_t new_size, int flag){
  if(new_values == NULL){
    return -1;
  }

  uint64_t addr;
  if(flag == FORCE_REALLOC){
    addr = um_malloc(dbg, new_size);
  }else if(flag == NOT_REALLOC){
    if(exisiting_addr == 0 || exisiting_addr == -1){
      return -1;
    }
    addr = exisiting_addr;
  }else if(flag == AUTO_REALLOC){
    addr = um_realloc(dbg, exisiting_addr, old_size, new_size);
  }else{
    return -1;
  }
  if(um_memcpy(dbg, addr, (uint64_t)new_values, new_size, MEMCPY_LOCAL_TO_REMOTE) != 0){
    return -1;
  }
  return addr;
}

uint64_t um_set_pointer_to_values(um_data* dbg, uint64_t pointer_addr, size_t old_size, void* new_values, size_t new_size, int flag){
  uint64_t target_addr = um_get_addr_by_pointer_addr(dbg, pointer_addr);
  if(target_addr == 0 || target_addr == -1){
    return -1;
  }

  uint64_t addr = um_write_values(dbg, target_addr, old_size, new_values, new_size, flag);
  if(addr == 0 || addr == -1){
    return -1;
  }

  if(um_repoint_pointer_to_addr(dbg, pointer_addr, addr) != 0){
    return -1;
  }
  return addr;
}

uint64_t um_transform_struct(um_data* dbg, uint64_t obj_addr, size_t old_size, size_t new_size, int (*transform)(um_data*, void*, void*, int flag), int flag){
  if(obj_addr == -1 || obj_addr == 0){
    return -1;
  }

  void* old_values = malloc(old_size);
  memset(old_values, 0, old_size);
  if(um_memcpy(dbg, (uint64_t)old_values, obj_addr, old_size, MEMCPY_REMOTE_TO_LOCAL) != 0){
    free(old_values);
    return -1;
  }

  void* new_values = malloc(new_size);
  memset(new_values, 0, new_size);
  if(transform(dbg, old_values, new_values, flag) != 0){
    fprintf(stderr, "Failed to transform\n");
    free(old_values);
    free(new_values);
    return -1;
  }

  uint64_t addr;
  if(flag == FORCE_REALLOC){
    addr = um_malloc(dbg, new_size);
  }else if(flag == NOT_REALLOC){
    if(new_size > old_size){
      fprintf(stderr, "new struct size bigger than old, must realloc\n");
      addr = -1;
    }else{
      addr = obj_addr;
    }
  }else if(flag == AUTO_REALLOC){
    addr = um_realloc(dbg, obj_addr, old_size, new_size);
  }else{
    return -1;
  }
  if(addr == 0 || addr == -1){
    free(old_values);
    free(new_values);
    return -1;
  }


  if(um_memcpy(dbg, addr, (uint64_t)new_values, new_size, MEMCPY_LOCAL_TO_REMOTE) != 0){
    return -1;
  }

  return addr;
}

uint64_t um_transform_struct_pointer(um_data* dbg, uint64_t pointer_addr, size_t old_size, size_t new_size, int (*transform)(um_data*, void*, void*, int flag), int flag){
  uint64_t obj_addr = um_get_addr_by_pointer_addr(dbg, pointer_addr);
  if(obj_addr == 0 || obj_addr == -1){
    return -1;
  }

  uint64_t addr = um_transform_struct(dbg, obj_addr, old_size, new_size, transform, flag);
  if(addr == 0 || addr == -1){
    return -1;
  }

  if(um_repoint_pointer_to_addr(dbg, pointer_addr, addr) != 0){
    return -1;
  }
  return addr;
}



uint64_t um_set_by_array_variable(um_data* dbg, bool is_local, char* name, char* scope, void* new_values, size_t new_size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == -1 || addr == 0){
    fprintf(stderr, "failed to get address of variable %s in %s\n", name, scope);
    return -1;
  }

  if(um_write_addr_n(dbg, addr, new_values, new_size, 1) != 0){
    return -1;
  }
  return 0;
}
