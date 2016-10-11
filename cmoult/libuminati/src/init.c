#include "init.h"

int get_cfi (Dwfl_Module* mod, um_data* dbg)
  {
    //Trying to get .debug_frame
    dbg->cfi = dwfl_module_dwarf_cfi (mod, &(dbg->bias));
    if (dbg->cfi != NULL) {
        return DWARF_CB_OK;
    }


    dbg->cfi = dwfl_module_dwarf_cfi (mod, &(dbg->bias));
    if (dbg->cfi != NULL) {
        return DWARF_CB_OK;
    }
    //Trying to get .eh_frame
    dbg->cfi = dwfl_module_eh_cfi (mod, &(dbg->bias));
    if (dbg->cfi != NULL){
        return DWARF_CB_OK;
    }
    return DWARF_CB_ABORT;
  }

int um_init (um_data** dbg, pid_t pid, const char* fname)
  {
    if (!dbg)
        return -1;
    (*dbg) = (um_data*) malloc(sizeof(um_data));
    memset(*dbg, 0, sizeof(um_data));
    (*dbg)->pid = pid;
    (*dbg)->fname = fname;

    Dwfl_Module *mod;
    char* debuginfo_path;
    const Dwfl_Callbacks callbacks =
      {
        .find_elf = &dwfl_build_id_find_elf,
        .find_debuginfo = &dwfl_standard_find_debuginfo,
        .section_address = &dwfl_offline_section_address,
        .debuginfo_path = &debuginfo_path
      };
    (*dbg)->debug_raw = dwfl_begin(&callbacks);
    if (!(*dbg)->debug_raw)
        return 1;
    dwfl_report_begin((*dbg)->debug_raw);
    mod = dwfl_report_offline((*dbg)->debug_raw, "", fname, -1);
    if (mod == NULL)
        return 2;
    dwfl_report_end((*dbg)->debug_raw, NULL, NULL);
    if (get_cfi (mod, (*dbg)) != DWARF_CB_OK)
        return 3;
    return 0;
  }
