#include "get_frame_info.h"

int get_cfa_from_frame(um_frame* context, um_data* dbg)
  {
//    Dwarf_Frame tt;
//    memset(&tt, 0, sizeof(tt));
    Dwarf_Frame* um_frame;
    int result = dwarf_cfi_addrframe(dbg->cfi, context->rip - dbg->bias, &um_frame);
    if (result != 0){
        perror("dwarf_cfi_addrframe");
        return -1;
    }
    Dwarf_Op **ops = (Dwarf_Op**) malloc(1024*sizeof(Dwarf_Op*));
    size_t nops;
    dwarf_frame_cfa(um_frame, ops, &nops);
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
    Dwarf_Op **ops = (Dwarf_Op**) malloc(1024*sizeof(Dwarf_Op*));
    size_t nops;
    Dwarf_Op ops_mem[3];
    dwarf_frame_register (um_frame, reg, ops_mem, ops, &nops);
    if (nops < 4)
      {
        ops[0] = &(ops_mem[0]);
        ops[1] = &(ops_mem[1]);
        ops[2] = &(ops_mem[2]);
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
