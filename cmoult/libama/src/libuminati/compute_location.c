#include "compute_location.h"
#include "common_utils.h"

uint64_t compute_location (Dwarf_Attribute* attr, um_frame* context, um_data* dbg)
  {
    Dwarf_Op *ops;
    size_t nops = 0;

    if (dwarf_getlocation (attr, &ops, &nops) != 0){
      dwarf_error("dwarf_getlocation()");

      Dwarf_Addr base, begin, end;
      ptrdiff_t offset = 0;
      while ((offset = dwarf_getlocations (attr, offset,
                   &base, &begin, &end,
                   &ops, &nops)) > 0){
        if (begin >= end){
          printf (" %p , %p) <empty range>\n", (void*)begin, (void*)end); // XXX report?
        }else
          {
//      print_expr_block_addrs (&attr, begin, end,
//            expr, exprlen);
          }
      }

    }

    if(nops == 0 || ops == NULL){
      return 0;
    }
    content c = compute_ops(ops, nops, context, dbg);
//    free(ops);
    if (c.is_loc)
        if (c.loc.addr)
            return c.loc.addr;
        else
            return 0;
    else
        return c.val.u;
  }

