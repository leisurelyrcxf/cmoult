#define _POSIX_C_SOURCE 100

#include "rwutils.h"

int um_attach (pid_t pid) {
    return ptrace(PTRACE_ATTACH, pid, NULL, NULL);
}

int write_char (pid_t pid, uint64_t addr, uint8_t val) {
    uint64_t old_val = _um_read_addr(pid, addr, 8);
    return ptrace(PTRACE_POKEDATA,pid,addr,(old_val&0xffffffffffffff00)+val);
}

int write_int (pid_t pid, uint64_t addr, uint32_t val) {
  uint64_t upper_bits = (uint64_t)val;
  uint64_t lower_bits;
  uint64_t value;
  errno = 0;
  lower_bits = ptrace(PTRACE_PEEKDATA,pid,addr+4,NULL);
  int error = errno;
  if (lower_bits == 0xffffffffffffffff && error != 0)
      return -2;
#ifdef LITTLEENDIAN
  lower_bits = (lower_bits << (8*4));
#endif
#ifdef BIGENDIAN
  upper_bits = (upper_bits << (8*4));
#endif
  value = upper_bits + lower_bits;
  return ptrace(PTRACE_POKEDATA,pid,addr,value);
}

int write_long (pid_t pid, uint64_t addr, uint64_t val) {
    return ptrace(PTRACE_POKEDATA, pid, addr, val);
}

int _um_write_addr (pid_t pid, uint64_t addr, uint64_t value, size_t size) {
    if (size == 4)
        return write_int (pid, addr, value & 0xffffffff);
    else if (size == 8)
        return write_long (pid, addr, value);
    else if (size == 1)
        return write_char (pid, addr, value&0xff);
    else
        return -1;
}

int um_write_addr (um_data* dbg, uint64_t addr, uint64_t value, size_t size) {
    return _um_write_addr(dbg->pid, addr, value, size);
}

static int um_write_addr_n_basic (um_data* dbg, uint64_t addr, void* values, int n, size_t size){
    if(size == 4){
      uint32_t *int_values = (uint32_t*)values;
      for(int i = 0; i < n; i++){
        if(um_write_addr(dbg, addr + (i << 2), (uint64_t)(*(int_values + i)), size) != 0){
          return -1;
        }
      }
    }else if(size == 8){
      uint64_t *int64_values = (uint64_t*)values;
      for(int i = 0; i < n; i++){
        if(um_write_addr(dbg, addr + (i << 3), (*(int64_values + i)), size) != 0){
          return -1;
        }
      }
    }else if(size == 1){
      uint8_t *char_values = (uint8_t*)values;
      for(int i = 0; i < n; i++){
        if(um_write_addr(dbg, addr + i, (uint64_t)(*(char_values + i)), size) != 0){
          return -1;
        }
      }
    }else{
      return -1;
    }
    return 0;
}


int um_write_addr_n (um_data* dbg, uint64_t addr, void* values, int n, size_t size){
  if(size == 1){
    size_t n8 = n / 8;
    if(n8 > 0){
      if(um_write_addr_n_basic(dbg, addr, values, n8, 8) != 0){
        return -1;
      }
    }
    size_t remain8 = n % 8;

    size_t n4 = remain8 / 4;
    if(n4 > 0){
      if(um_write_addr_n_basic(dbg, addr + (n8 << 3), (void*)((char*)values + (n8 << 3)), n4, 4) != 0 ){
        return -1;
      }
    }
    size_t remain4 = remain8 % 4;

    size_t n1 = remain4;
    if(n1 > 0){
      if(um_write_addr_n_basic(dbg, addr + (n8 << 3) + (n4 << 2), (void*)((char*)values + (n8 << 3) + (n4 << 2)), n1, 1) != 0){
        return -1;
      }
    }
  }else{
    if(um_write_addr_n_basic(dbg, addr, values, n, size) != 0){
      return -1;
    }
  }
  return 0;
}

int _um_write_registers(pid_t pid, struct user_regs_struct* regs) {
    struct iovec iov;
    iov.iov_len = sizeof(*regs);
    iov.iov_base = regs;
    return ptrace(PTRACE_SETREGSET, pid, NT_PRSTATUS, &iov);
}

int um_write_registers(um_data* dbg, struct user_regs_struct* regs) {
    struct iovec iov;
    iov.iov_len = sizeof(*regs);
    iov.iov_base = regs;
    return ptrace(PTRACE_SETREGSET, dbg->pid, NT_PRSTATUS, &iov);
}

uint64_t _um_read_addr (pid_t pid, uint64_t addr, size_t size) {
    uint64_t mask = 0xffffffffffffffff;
    for (int i = 0; i < 8 - (int)size; i++)
        mask >>= 8;
    return (ptrace(PTRACE_PEEKDATA, pid, addr, 0) & mask);
}

uint64_t um_read_addr (um_data* dbg, uint64_t addr, size_t size) {
    return _um_read_addr(dbg->pid, addr, size);
}

int _um_read_registers(pid_t pid, struct user_regs_struct* regs) {
//    struct iovec iov;
//    iov.iov_len = sizeof(*regs);
//    iov.iov_base = regs;
//    return ptrace(PTRACE_GETREGSET, pid, NT_PRSTATUS, &iov);
    return ptrace(PTRACE_GETREGS, pid, 0, regs);
}

int um_read_registers(um_data* dbg, struct user_regs_struct* regs) {
    return _um_read_registers(dbg->pid, regs);
}

int um_cont (pid_t pid) {
    return ptrace(PTRACE_CONT, pid, NULL, NULL);
}

int um_stop (pid_t pid) {
    return kill(pid, 3);
}

int um_detach (pid_t pid) {
    return ptrace(PTRACE_DETACH, pid, NULL, NULL);
}
