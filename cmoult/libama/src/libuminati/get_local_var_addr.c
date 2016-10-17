#include "get_local_var_addr.h"

uint64_t um_get_local_var_addr(um_data* dbg, const char* name, const char* scope) {
    if (!name)
        return -1;

    int r = 0;

    if (scope) {
//        Dwarf_Attribute* attr;

        um_search_first_args args = {
            .tag = DW_TAG_variable,
            .wanted_attribute = DW_AT_location,
            .name = name,
            .parent_name = scope,
            .address = 0,
            .result = NULL
        };

        r = um_parse(dbg, &um_search_first, &args);

        if (!args.result)
          return -1;

        if(!r){
          free(args.result);
          return -1;
        }

        //um_unwind until we find scope
        um_frame* scope_um_frame;
        scope_um_frame = um_unwind(dbg, scope, &scope_um_frame, UM_UNWIND_STOPWHENFOUND);
        if (!scope_um_frame){
          free(args.result);
          return -1;
        }

        uint64_t addr = compute_location(args.result, scope_um_frame, dbg);
        free(args.result);

        if(addr == 0){
          return -1;
        }
        return addr;
    }

    return -1;
}


static Dwarf_Op * get_location(Dwarf_Attribute *location, Dwarf_Addr addr, size_t *len);
static uint64_t fetch_register(um_data* dbg, int reg);
static uint64_t fetch_register_x86_64(um_data* dbg, int reg);
static uint64_t translate(um_data* dbg, Dwarf_Op *locexpr, size_t len, uint64_t *value ,bool *need_fb);

static uint64_t variable_address(um_data* dbg, Dwarf_Die *fun_die, Dwarf_Die *var_die, uint64_t *value)
{
  size_t len;
  Dwarf_Op *locexpr;
  bool need_fb;
  Dwarf_Attribute fb_attr, loc_attr;

  struct user_regs_struct regs = {0};
  if (_um_read_registers(dbg->pid, &regs) != 0)
      return-1;
  Dwarf_Addr addr = regs.rip;
  uint64_t var_addr = 0x0;
  if(!dwarf_attr_integrate(var_die, DW_AT_location, &loc_attr))
    goto out;

  locexpr = get_location(&loc_attr, addr, &len);
  if (!locexpr)
    goto out;

  var_addr = translate(dbg, locexpr, len, value, &need_fb);
  if (need_fb) {
    if(!dwarf_attr_integrate(fun_die, DW_AT_frame_base, &fb_attr))
      goto out;

  locexpr = get_location(&fb_attr, addr, &len);
  if (!locexpr)
    goto out;

    var_addr += translate(dbg, locexpr, len, value, 0);
  }
  return var_addr;
  out:
  return 0;
}

static uint64_t translate(um_data* dbg, Dwarf_Op *locexpr, size_t len, uint64_t *value ,bool *need_fb)
{
  int i;
  unsigned int reg;
  unsigned long loc = 0;
  unsigned long offset = 0;
  for (i=0; i<len; i++) {
    switch (locexpr[i].atom) {
      case DW_OP_reg0 ... DW_OP_reg31:
          reg = locexpr[i].atom - DW_OP_reg0;
        goto op_reg;
      case DW_OP_regx:
        reg = locexpr[i].number;
      op_reg:
        *value = fetch_register(dbg, reg);
        break;
      case DW_OP_fbreg:
        *need_fb = true;
        loc = locexpr[i].number;
        break;
      case DW_OP_addr:
        loc = locexpr[i].number;
        break;
      case DW_OP_breg0 ... DW_OP_breg31:
        reg = locexpr[i].atom - DW_OP_breg0;
        offset = locexpr[i].number;
        loc = fetch_register(dbg, reg) + offset;
        break;
      case DW_OP_bregx:
        reg = locexpr[i].number;
        offset = locexpr[i].number2;
        loc = fetch_register(dbg, reg) + offset;
        break;
      default:
        fprintf(stderr,
         "unprocessed OpCode in translate()");
        break;
    }
  }
  return loc;
}

static uint64_t fetch_register(um_data* dbg, int reg){
  return fetch_register_x86_64(dbg, reg);
}

static uint64_t fetch_register_x86_64(um_data* dbg, int reg)
{
//  struct pt_regs_x86_64 *pt_regs;
//  pt_regs = (struct pt_regs_x86_64 *)local->regs;


  struct user_regs_struct regs = {0};
  if (_um_read_registers(dbg->pid, &regs) != 0)
      return-1;

  switch(reg){
    case 0: return regs.rax;
    case 1: return regs.rdx;
    case 2: return regs.rcx;
    case 3: return regs.rbx;
    case 4: return regs.rsi;
    case 5: return regs.rdi;
    case 6: return regs.rbp;
    case 7: return regs.rsp;
    case 8: return regs.r8;
    case 9: return regs.r9;
    case 10: return regs.r10;
    case 11: return regs.r11;
    case 12: return regs.r12;
    case 13: return regs.r13;
    case 14: return regs.r14;
    case 15: return regs.r15;
    default:
      fprintf(stderr,
        "fetch_register_x86_64: unhandled x86_64 register %d", reg);
  }
  return 0;
}

static Dwarf_Op * get_location(Dwarf_Attribute *location, Dwarf_Addr addr, size_t *len)
{
  Dwarf_Op *expr;
  switch(dwarf_getlocation_addr(location, addr, &expr,len,1))
  {
  case 1:
    if( len > 0)
    break;
  case 0:
    return NULL;
    break;
  default:
    return NULL;
  }
  return expr;
}

