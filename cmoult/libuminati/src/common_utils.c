#include "common_utils.h"
#include "libdw.h"


const char* REG_NAMES[] = {"r15", "r14", "r13", "r12", "rbp", "rbx", "r11", "r10", "r9", "r8", "rax", "rcx", "rdx", "rsi", "rdi", "orig_rax", "rip", "cs", "eflags", "rsp", "ss", "fs_base", "gs_base", "ds", "es", "fs", "gs"};

const char* get_reg_name_of_user_regs_struct_by_reg_idx(int i){
  return REG_NAMES[i];
}



void dwarf_error(const char *msg)
{
  printf("%s: %s\n", msg, dwarf_errmsg(-1));
}
