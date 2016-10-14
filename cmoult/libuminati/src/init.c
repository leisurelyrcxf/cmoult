#include "init.h"
#include "common_utils.h"

int get_cfi (Dwfl_Module* mod, um_data* dbg){
  //Trying to get .eh_frame
  dbg->cfi = dwfl_module_eh_cfi (mod, &(dbg->bias));
  if (dbg->cfi != NULL){
      return DWARF_CB_OK;
  }

  dbg->cfi = dwfl_module_dwarf_cfi (mod, &(dbg->bias));
  if (dbg->cfi != NULL) {
      return DWARF_CB_OK;
  }
  return DWARF_CB_ABORT;
}

int get_cfi_of_module(Dwfl_Module* mod, Dwarf_CFI** cfi, Dwarf_Addr* bias){
  //Trying to get .eh_frame
  *cfi = dwfl_module_eh_cfi(mod, bias);
  if (*cfi != NULL){
      return DWARF_CB_OK;
  }

  *cfi = dwfl_module_dwarf_cfi(mod, bias);
  if (*cfi != NULL) {
      return DWARF_CB_OK;
  }
  return DWARF_CB_ABORT;
}

void report_pid (Dwfl *dwfl, pid_t pid){
  dwfl_report_begin(dwfl);

  if(dwfl_linux_proc_report (dwfl, pid) != 0)
    dwarf_error("dwfl_linux_proc_report()");

  if(dwfl_report_end(dwfl, NULL, NULL) != 0)
    dwarf_error("dwfl_report_end()");

  if(dwfl_linux_proc_attach(dwfl, pid, true) != 0)
    dwarf_error("dwfl_linux_proc_attach()");
}

Dwfl *pid_to_dwfl (pid_t pid){
  static char *debuginfo_path;
  static const Dwfl_Callbacks proc_callbacks = {
    .find_debuginfo = dwfl_standard_find_debuginfo,
    .debuginfo_path = &debuginfo_path,
    .section_address = &dwfl_offline_section_address, //mark
    .find_elf = dwfl_linux_proc_find_elf,
  };

//  .find_elf = &dwfl_build_id_find_elf,
//  .find_debuginfo = &dwfl_standard_find_debuginfo,
//  .section_address = &dwfl_offline_section_address,
//  .debuginfo_path = &debuginfo_path
  Dwfl *dwfl = dwfl_begin (&proc_callbacks);
  if (dwfl == NULL)
    dwarf_error("dwfl_begin()");
  report_pid(dwfl, pid);
  return dwfl;
}

int um_init (um_data** dbg, pid_t pid, const char* fname){
  if (!dbg || !fname){
      fprintf(stderr, "arguments shouldn't be NULL\n");
      return -1;
  }
  (*dbg) = (um_data*) malloc(sizeof(um_data));
  memset(*dbg, 0, sizeof(um_data));
  (*dbg)->pid = pid;
  (*dbg)->fname = fname;
  (*dbg)->debug_raw = pid_to_dwfl((*dbg)->pid);
  if (!(*dbg)->debug_raw)
      return 1;


  Dwfl_Module* mod = dwfl_report_offline((*dbg)->debug_raw, "", fname, -1);
  if (mod == NULL)
      return 2;
  if (get_cfi (mod, (*dbg)) != DWARF_CB_OK)
      return 3;
  return 0;
}
