#include "dwarf_ops.h"

void pop (op_stack** s, content* c)
  {
    *c = (*s)->c;
    op_stack* ns = (*s)->down;
    free(*s);
    *s = ns;
  }

void push (op_stack** s, content c)
  {
    op_stack* ns = (op_stack*) malloc (sizeof(op_stack));
    ns->c = c;
    ns->down = *s;
    *s = ns;
  }

void pick (op_stack* s, content* c, char index)
  {
    char i;
    op_stack* pointer = s;
    for (i = 0; i < index; i++)
        pointer = pointer->down;
    *c = pointer->c;
  }

void destroy (op_stack* s)
  {
    if (!s)
        return;
    destroy(s->down);
    free(s);
  }

int compare (content c1, content c2)
  {
    uint64_t val1 = (c1.is_loc)?(c1.loc.addr):(c1.val.u);
    uint64_t val2 = (c2.is_loc)?(c2.loc.addr):(c2.val.u);
    if (c1.is_loc && !c1.loc.addr)
      {
        if (c1.loc.reg != c2.loc.reg)
            return 2;
        if (c1.loc.offset != c2.loc.offset)
            return 2;
      }
    if (val1 == val2)
        return 0;
    if (val1 < val2)
        return -1;
    return 1;
  }

void process_op(op_stack **s, Dwarf_Op *op, um_frame *context, um_data* dbg)
  {
    Dwarf_Attribute attr;
    uint64_t v;
    int comp;
    content c, c2, c3;
    c.loc.addr = 0;
    c.loc.reg = 0;
    c.loc.offset = 0;
    c.val.u = 0;
    c2.loc.addr = 0;
    c2.loc.reg = 0;
    c2.loc.offset = 0;
    c2.val.u = 0;
    c3.loc.addr = 0;
    c3.loc.reg = 0;
    c3.loc.offset = 0;
    c3.val.u = 0;
    if (!op)
        return;
    //Processing ops as specified as in the DWARFv4 specification, 2.5 & 2.6
    switch (op->atom)
      {
      //2.5.1
        //2.5.1.1.
        case DW_OP_lit0:
        case DW_OP_lit1:
        case DW_OP_lit2:
        case DW_OP_lit3:
        case DW_OP_lit4:
        case DW_OP_lit5:
        case DW_OP_lit6:
        case DW_OP_lit7:
        case DW_OP_lit8:
        case DW_OP_lit9:
        case DW_OP_lit10:
        case DW_OP_lit11:
        case DW_OP_lit12:
        case DW_OP_lit13:
        case DW_OP_lit14:
        case DW_OP_lit15:
        case DW_OP_lit16:
        case DW_OP_lit17:
        case DW_OP_lit18:
        case DW_OP_lit19:
        case DW_OP_lit20:
        case DW_OP_lit21:
        case DW_OP_lit22:
        case DW_OP_lit23:
        case DW_OP_lit24:
        case DW_OP_lit25:
        case DW_OP_lit26:
        case DW_OP_lit27:
        case DW_OP_lit28:
        case DW_OP_lit29:
        case DW_OP_lit30:
        case DW_OP_lit31:
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = op->atom - 0x30;
            push(s, c);
            break;
        case DW_OP_addr:
            c.is_signed = false;
            c.is_loc = true;
            c.loc.addr = op->number;
            push(s, c);
            break;
        case DW_OP_const1u:
        case DW_OP_const2u:
        case DW_OP_const4u:
        case DW_OP_const8u:
        case DW_OP_constu:
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = op->number;
            push(s, c);
            break;
        case DW_OP_const1s:
        case DW_OP_const2s:
        case DW_OP_const4s:
        case DW_OP_const8s:
        case DW_OP_consts:
            c.is_signed = true;
            c.is_loc = false;
            c.val.s = op->number;
            push(s, c);
            break;
        //2.5.1.2.
        case DW_OP_fbreg:
            c.is_signed = false;
            c.is_loc = true;
            char* pname = malloc(2);
            sprintf(pname, "*");

            um_search_first_args args =
              {
                .tag = DW_TAG_subprogram,
                .wanted_attribute = DW_AT_frame_base,
                .parent_name = pname,
                .name = um_get_function(dbg, context),
                .address = 0,
                .result = &attr
              };
            int r = um_parse(dbg, &um_search_first, &args);
            c.loc.addr = (r > 0 && args.result)?compute_location(args.result, context, dbg)+op->number:0;
            free(pname);
            push(s, c);
            break;
        case DW_OP_breg0:
        case DW_OP_breg1:
        case DW_OP_breg2:
        case DW_OP_breg3:
        case DW_OP_breg4:
        case DW_OP_breg5:
        case DW_OP_breg6:
        case DW_OP_breg7:
        case DW_OP_breg8:
        case DW_OP_breg9:
        case DW_OP_breg10:
        case DW_OP_breg11:
        case DW_OP_breg12:
        case DW_OP_breg13:
        case DW_OP_breg14:
        case DW_OP_breg15:
        case DW_OP_breg16:
        case DW_OP_breg17:
        case DW_OP_breg18:
        case DW_OP_breg19:
        case DW_OP_breg20:
        case DW_OP_breg21:
        case DW_OP_breg22:
        case DW_OP_breg23:
        case DW_OP_breg24:
        case DW_OP_breg25:
        case DW_OP_breg26:
        case DW_OP_breg27:
        case DW_OP_breg28:
        case DW_OP_breg29:
        case DW_OP_breg30:
        case DW_OP_breg31:
            c.is_signed = false;
            if (context)
              {
                if (context->regs[op->atom - 0x70])
                  {
                    c.is_loc = false;
                    c.val.u = context->regs[op->atom - 0x70] + op->number;
                  }
              }
            else
              {
                c.is_loc = true;
                c.loc.offset = op->number;
                c.loc.reg = op->atom - 0x70;
              }
            push(s, c);
            break;
        case DW_OP_bregx:
            c.is_signed = false;
            if (context)
              {
                if (context->regs[op->number])
                  {
                    c.is_loc = false;
                    c.val.u = context->regs[op->number] + op->number2;
                  }
              }
            else
              {
                c.is_loc = true;
                c.loc.offset = op->number2;
                c.loc.reg = op->number;
              }
            push(s, c);
            break;
        //2.5.1.3.
        case DW_OP_dup:
            pop(s, &c);
            push(s, c);
            push(s, c);
            break;
        case DW_OP_drop:
            pop(s, &c);
            break;
        case DW_OP_over:
            pick(*s, &c, 1);
            push(s, c);
            break;
        case DW_OP_pick:		/* 1-byte stack index.  */
            pick(*s, &c, op->number);
            push(s, c);
            break;
        case DW_OP_swap:
            pop(s, &c);
            pop(s, &c2);
            push(s, c);
            push(s, c2);
            break;
        case DW_OP_rot:
            pop(s, &c);
            pop(s, &c2);
            pop(s, &c3);
            push(s, c);
            push(s, c3);
            push(s, c2);
            break;
        case DW_OP_deref:
            pop (s, &c);
            if (c.is_loc)
                v = c.loc.addr;
            else
                v = c.val.u;
            c.val.u = _um_read_addr(dbg->pid, v, 8);
            c.is_loc = false;
            c.is_signed = false;
            push(s, c);
            break;
        case DW_OP_deref_size:
            pop(s, &c);
            if (c.is_loc)
                v = c.loc.addr;
            else
                v = c.val.u;
            c.val.u = _um_read_addr(dbg->pid, v, op->number);
            c.is_loc = false;
            c.is_signed = false;
            push(s, c);
            break;
        case DW_OP_xderef:
        case DW_OP_xderef_size:
            //NOT IMPLEMENTED: that means no support for multiple address spaces
            break;
        case DW_OP_push_object_address:
            //NOT IMPLEMENTED: is not used for anything in C
            break;
        case DW_OP_form_tls_address:
            //NOT IMPLEMENTED: used for C implementations where there is a thread-local storage block FIXME
            break;
        case DW_OP_call_frame_cfa:
            c.is_signed = false;
            c.is_loc = true;
            if (context)
                c.loc.addr = context->cfa;
            else
                c.loc.addr = 0;
            push(s, c);
            break;
        //2.5.1.4.
        case DW_OP_abs:
            pop(s, &c);
            c.val.u = (c.val.s < 0)?(-c.val.s):c.val.s;
            c.is_signed = false;
            push(s, c);
            break;
        case DW_OP_and:
            pop(s, &c);
            pop(s, &c2);
            if (!c.is_loc)
                c.val.u &= (c2.is_loc)?c2.loc.addr:c2.val.u;
            else
                c.loc.addr &= (c2.is_loc)?c2.loc.addr:c2.val.u;
            push(s, c);
            break;
        case DW_OP_div:
            pop(s, &c);
            pop(s, &c2);
            c2.val.s /= c.val.s;
            push(s, c2);
            break;
        case DW_OP_minus:
            pop(s, &c);
            pop(s, &c2);
            if (c2.is_loc)
                if (c2.loc.addr)
                    c2.loc.addr -= c.val.u;
                else
                    c2.loc.offset -= c.val.u;
            else
                c2.val.u -= c.val.u;
            push(s, c2);
            break;
        case DW_OP_mod:
            pop(s, &c);
            pop(s, &c2);
            c2.val.u %= c.val.u;
            push(s, c2);
            break;
        case DW_OP_mul:
            pop(s, &c);
            pop(s, &c2);
            c2.val.u *= c.val.u;
            push(s, c2);
            break;
        case DW_OP_neg:
            pop(s, &c);
            c.val.s = -c.val.s;
            push(s, c);
            break;
        case DW_OP_not:
            pop(s, &c);
            c.val.s = ~c.val.s;
            push(s, c);
            break;
        case DW_OP_or:
            pop(s, &c);
            pop(s, &c2);
            if (!c.is_loc)
                c.val.u |= (c2.is_loc)?c2.loc.addr:c2.val.u;
            else
                c.loc.addr |= (c2.is_loc)?c2.loc.addr:c2.val.u;
            push(s, c);
            break;
        case DW_OP_plus:
            pop(s, &c);
            pop(s, &c2);
            if (c2.is_loc)
                if (c2.loc.addr)
                    c2.loc.addr += c.val.u;
                else
                    c2.loc.offset += c.val.u;
            else
                c2.val.u += c.val.u;
            push(s, c2);
            break;
        case DW_OP_plus_uconst:	/* Unsigned LEB128 addend.  */
            pop(s, &c);
            if (c.is_loc)
                if (c.loc.addr)
                    c.loc.addr += op->number;
                else
                    c.loc.offset += op->number;
            else
                c.val.u += op->number;
            push(s, c);
            break;
        case DW_OP_shl:
            pop(s, &c);
            pop(s, &c2);
            c2.val.u <<= c.val.u;
            push(s, c2);
            break;
        case DW_OP_shr:
            pop(s, &c);
            pop(s, &c2);
            c2.val.u >>= c.val.u;
            push(s, c2);
            break;
        case DW_OP_shra:
            pop(s, &c);
            pop(s, &c2);
            c2.val.s >>= c.val.u;
            push(s, c2);
            break;
        case DW_OP_xor:
            pop(s, &c);
            pop(s, &c2);
            if (!c.is_loc)
                c.val.u ^= (c2.is_loc)?c2.loc.addr:c2.val.u;
            else
                c.loc.addr ^= (c2.is_loc)?c2.loc.addr:c2.val.u;
            push(s, c);
            break;
        //2.5.1.5.
        case DW_OP_eq:
            pop(s, &c);
            pop(s, &c2);
            comp = compare(c,c2);
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = (comp==0)?0:1;
            push(s, c);
            break;
        case DW_OP_ge:
            pop(s, &c);
            pop(s, &c2);
            comp = compare(c,c2);
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = (comp==0 || comp==1)?0:1;
            push(s, c);
            break;
        case DW_OP_gt:
            pop(s, &c);
            pop(s, &c2);
            comp = compare(c,c2);
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = (comp==1)?0:1;
            push(s, c);
            break;
        case DW_OP_le:
            pop(s, &c);
            pop(s, &c2);
            comp = compare(c,c2);
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = (comp==0 || comp==-1)?0:1;
            push(s, c);
            break;
        case DW_OP_lt:
            pop(s, &c);
            pop(s, &c2);
            comp = compare(c,c2);
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = (comp==-1)?0:1;
            push(s, c);
            break;
        case DW_OP_ne:
            pop(s, &c);
            pop(s, &c2);
            comp = compare(c,c2);
            c.is_signed = false;
            c.is_loc = false;
            c.val.u = (comp!=0)?0:1;
            push(s, c);
            break;
        //NOT IMPLEMENTED: Control flow operations are a HUGE pain. As long as they're not needed, it's ok.
        case DW_OP_skip:		/* Signed 2-byte constant.  */
        case DW_OP_bra:		/* Signed 2-byte constant.  */
        case DW_OP_call2:
        case DW_OP_call4:
        case DW_OP_call_ref:
            break;
        //2.5.1.6.
        case DW_OP_nop:
            break; //That is its definition
        //2.6.1.1.2.
        case DW_OP_reg0:
        case DW_OP_reg1:
        case DW_OP_reg2:
        case DW_OP_reg3:
        case DW_OP_reg4:
        case DW_OP_reg5:
        case DW_OP_reg6:
        case DW_OP_reg7:
        case DW_OP_reg8:
        case DW_OP_reg9:
        case DW_OP_reg10:
        case DW_OP_reg11:
        case DW_OP_reg12:
        case DW_OP_reg13:
        case DW_OP_reg14:
        case DW_OP_reg15:
        case DW_OP_reg16:
        case DW_OP_reg17:
        case DW_OP_reg18:
        case DW_OP_reg19:
        case DW_OP_reg20:
        case DW_OP_reg21:
        case DW_OP_reg22:
        case DW_OP_reg23:
        case DW_OP_reg24:
        case DW_OP_reg25:
        case DW_OP_reg26:
        case DW_OP_reg27:
        case DW_OP_reg28:
        case DW_OP_reg29:
        case DW_OP_reg30:
        case DW_OP_reg31:
            c.is_signed = false;
            if (context)
              {
                if (context->regs[op->atom - 0x50])
                  {
                    c.is_loc = false;
                    c.val.u = context->regs[op->atom - 0x50];
                  }
              }
            else
              {
                c.is_loc = true;
                c.loc.reg = op->atom - 0x50;
              }
            break;
        case DW_OP_regx:
            c.is_signed = false;
            if (context)
              {
                if (context->regs[op->number])
                  {
                    c.is_loc = false;
                    c.val.u = context->regs[op->number];
                  }
              }
            else
              {
                c.is_loc = true;
                c.loc.reg = op->number;
              }
            break;
        //2.6.1.1.3.
        //NOT IMPLEMENTED: libdw functions skip the DW_OP_stack_value, it's up to the caller of this function to get the value from the top of the stack
        //2.6.1.2.
        //NOT IMPLEMENTED: not needed yet
        case DW_OP_implicit_value:
        case DW_OP_stack_value:
        case DW_OP_piece:
        case DW_OP_bit_piece:
            break;
      }
  }

void free_op_stack (op_stack* s) {
    if (!s)
        return;
    free_op_stack(s->down);
    free(s);
}

content compute_ops (Dwarf_Op **ops, size_t nops, um_frame *context, um_data* dbg)
  {
    op_stack *s = (op_stack*) malloc(sizeof(op_stack));
    int i;
    s->down = NULL;
    for (i = 0; i < (int)nops; i++)
        process_op(&s, ops[i], context, dbg);
    content ret = s->c;
    free_op_stack(s);
    return ret;
  }
