#include "watch_access.h"
#include "add_watchpoint.h"
#include "rwutils.h"
#include "libc_includes.h"
#include "get_var_addr.h"
#include "get_var_size.h"


static int um_wait_addr(um_data* dbg, uint64_t addr, size_t len, uint8_t wait_cond){
  if(um_add_watchpoint(dbg, addr, len, wait_cond, WATCH_LOCAL) != 0){
    fprintf(stderr, "failed to add any watch point\n");
    return -1;
  }
  um_cont(dbg->pid);
  int ret, status;
  do{
    ret = waitpid(dbg->pid, &status, 0);
    if(ret != dbg->pid){
      fprintf(stderr, "error waitpid\n");
      if(um_remove_watchpoint(dbg, addr, len, wait_cond, WATCH_LOCAL) != 0){
        fprintf(stderr, "failed to remove all watch point\n");
      }
      return -1;
    }
  }while(!WIFEXITED(status) && !(WIFSTOPPED(status) && WSTOPSIG(status) == SIGTRAP));

  return 0;
}

int um_wait_addr_access(um_data* dbg, uint64_t addr, size_t len){
  return um_wait_addr(dbg, addr, len, WP_TRAP_COND_DATA_ACCESS);
}

int um_wait_addr_write(um_data* dbg, uint64_t addr, size_t len){
  return um_wait_addr(dbg, addr, len, WP_TRAP_COND_DATA_WRITE);
}

int um_wait_addr_execute(um_data* dbg, uint64_t addr, size_t len){
  return um_wait_addr(dbg, addr, len, WP_TRAP_COND_EXECUTION);
}

int um_wait_var_access(um_data* dbg, bool is_local, char* name, char* scope, size_t size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0 || addr == (uint64_t)-1){
    return -1;
  }
  printf("var %s in scope %s at addr %p", name, scope, (void*)addr);
  um_wait_addr_access(dbg, addr, size);
}

int um_wait_var_write(um_data* dbg, bool is_local, char* name, char* scope, size_t size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0 || addr == (uint64_t)-1){
    return -1;
  }
  um_wait_addr_write(dbg, addr, size);
}

int um_watch_addr_access(um_data* dbg, uint64_t addr, size_t len,
    int (*callback)(um_data*, uint64_t, size_t, int (*callback_op)(um_data*, void*, size_t)),
    int (*callback_op)(um_data*, void*, size_t)){
  if(um_add_watchpoint(dbg, addr, len, WP_TRAP_COND_DATA_ACCESS, WATCH_LOCAL) != 0){
    fprintf(stderr, "failed to add all watch point\n");
  }
  um_cont(dbg->pid);
  int ret, status;
  do{
    ret = waitpid(dbg->pid, &status, 0);
    if(ret != dbg->pid){
      fprintf(stderr, "error waitpid\n");
      if(um_remove_watchpoint(dbg, addr, len, WP_TRAP_COND_DATA_ACCESS, WATCH_LOCAL) != 0){
        fprintf(stderr, "failed to remove all watch point\n");
      }
      return -1;
    }
  }while(!WIFEXITED(status) && !(WIFSTOPPED(status) && WSTOPSIG(status) == SIGTRAP));

  if(callback){
    if(callback(dbg, addr, len, callback_op) != 0){
      fprintf(stderr, "failed in callback in um_watch_addr_access\n");
      if(um_remove_watchpoint(dbg, addr, len, WP_TRAP_COND_DATA_ACCESS, WATCH_LOCAL) != 0){
        fprintf(stderr, "failed to remove all watch point\n");
      }
      return -1;
    }
  }

  if(um_remove_watchpoint(dbg, addr, len, WP_TRAP_COND_DATA_ACCESS, WATCH_LOCAL) != 0){
    fprintf(stderr, "failed to remove all watch point\n");
  }
  return 0;
}

int um_watch_var_access(um_data* dbg, bool is_local, char* name, char* scope, size_t size,
    int (*callback)(um_data*, uint64_t, size_t, int (*callback_op)(um_data*, void*, size_t)),
    int (*callback_op)(um_data*, void*, size_t)){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == 0 || addr == (uint64_t)-1){
    return -1;
  }
//  size_t size = um_get_var_size(dbg, name, scope);
  um_watch_addr_access(dbg, addr, size, callback, callback_op);
}

int cleanup_watchpoint(um_data* dbg, uint64_t addr, size_t len, uint8_t wait_cond){
  if(um_remove_watchpoint(dbg, addr, len, wait_cond, WATCH_LOCAL) != 0){
    fprintf(stderr, "failed to remove all watch point\n");
  }
  um_clear_all_dr(dbg);
  return 0;
}
