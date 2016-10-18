#include "get_frame_info.h"
#include "common_utils.h"
#include "init.h"

int get_cfa_from_frame(um_frame* context, um_data* dbg)
  {
//    Dwarf_Frame tt;
//    memset(&tt, 0, sizeof(tt));
    Dwarf_Frame* um_frame;
    int result = dwarf_cfi_addrframe(dbg->cfi, context->rip - dbg->bias, &um_frame);
    if (result != 0){
        dwarf_error("dwarf_cfi_addrframe");
        return -1;
    }
    Dwarf_Op *ops;
    size_t nops;
    dwarf_frame_cfa(um_frame, &ops, &nops);
    content c = compute_ops(ops, nops, context, dbg);
    if (c.is_loc)
        context->cfa = c.loc.addr;
    else
        context->cfa = c.val.u;
    if (!context->cfa)
        return 1;
    else
        return 0;
  }

int get_register_from_frame(unsigned int reg, um_frame* context, um_data* dbg)
  {
    Dwarf_Frame* um_frame;
    int result = dwarf_cfi_addrframe(dbg->cfi, context->rip - dbg->bias, &um_frame);
    if (result != 0)
        return -1;
    Dwarf_Op *ops;
    size_t nops;
    Dwarf_Op ops_mem[3];
    dwarf_frame_register (um_frame, reg, ops_mem, &ops, &nops);

    if(nops < 4){
        Dwarf_Op convert[3];
        convert[0] = ops_mem[0];
        convert[1] = ops_mem[1];
        convert[2] = ops_mem[2];
        ops = &convert[0];
    }
    content c = compute_ops(ops, nops, context, dbg);
    if (c.is_loc)
        context->regs[reg] = c.loc.addr;
    else
        context->regs[reg] = c.val.u;
    if (!context->regs[reg])
        return 1;
    else
        return 0;
  }




int get_cfa_from_dwfl_module(Dwfl_Module* mod, Dwarf_Addr pc, um_frame* context, um_data* dbg){
  Dwarf_CFI* cfi;
  Dwarf_Addr bias;
  if(get_cfi_of_module(mod, &cfi, &bias) != DWARF_CB_OK){
    dwarf_error("failed in get_cfi_of_module()");
    return 1;
  }

  Dwarf_Frame* dwarf_frame;
  int result = dwarf_cfi_addrframe(cfi, pc - bias, &dwarf_frame);
  if (result != 0){
//    dwarf_error("failed in dwarf_cfi_addrframe()");
    return 1;
  }

  Dwarf_Op *ops;
  size_t nops;
  dwarf_frame_cfa(dwarf_frame, &ops, &nops);
  content c = compute_ops(ops, nops, context, dbg);
  if (c.is_loc)
      context->cfa = c.loc.addr;
  else
      context->cfa = c.val.u;

  if (!context->cfa)
      return 1;
  else
      return 0;
}

int get_register_from_dwfl_module(unsigned int reg, Dwfl_Module* mod, Dwarf_Addr pc, um_frame* context, um_data* dbg){
  Dwarf_CFI* cfi;
  Dwarf_Addr bias = 0;
  if(get_cfi_of_module(mod, &cfi, &bias) != DWARF_CB_OK){
    dwarf_error("failed in get_cfi_of_module()");
    return 1;
  }

  Dwarf_Frame* dwarf_frame;
  int result = dwarf_cfi_addrframe(cfi, pc - bias, &dwarf_frame);
  if (result != 0){
//    dwarf_error("failed in dwarf_cfi_addrframe()");
    return 1;
  }

  Dwarf_Op *ops;
  size_t nops;
  Dwarf_Op ops_mem[3];

  if(dwarf_frame_register (dwarf_frame, reg, ops_mem, &ops, &nops) != 0){
    dwarf_error("failed in dwarf_frame_register()");
    return 1;
  }

//  if(nops == 0){
////    if(ops == NULL){
////      printf("%p", (void*)state->regs[regno]);
////    }else{
////      return 1;
////    }
//    context->regs[reg] = 0;
//    return 0;
//  }

  if(nops < 4){
    Dwarf_Op convert[3];
    convert[0] = ops_mem[0];
    convert[1] = ops_mem[1];
    convert[2] = ops_mem[2];
    ops = &convert[0];
  }
  content c = compute_ops(ops, nops, context, dbg);
  if (c.is_loc)
      context->regs[reg] = c.loc.addr;
  else
      context->regs[reg] = c.val.u;

  if (!context->regs[reg])
      return 1;
  else
      return 0;
}
