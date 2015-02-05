#include "compute_location.h"

uint64_t compute_location (Dwarf_Attribute* attr, um_frame* context, um_data* dbg)
  {
    Dwarf_Op **ops = (Dwarf_Op**) malloc(1024*sizeof(Dwarf_Op*));
    size_t nops;

    dwarf_getlocation(attr, ops, &nops);
    content c = compute_ops(ops, nops, context, dbg);
    free(ops);
    if (c.is_loc)
        if (c.loc.addr)
            return c.loc.addr;
        else
            return 0;
    else
        return c.val.u;
  }

