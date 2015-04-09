#ifndef DWARF_OPS
#define DWARF_OPS
#include "elfutils_includes.h"
#include "data_structs.h"
#include "get_function.h"
#include "compute_location.h"
#include "rwutils.h"

typedef struct location{
    uint64_t addr;
    uint64_t reg;
    int64_t offset;
} location;

typedef union value{
    uint64_t u;
    int64_t s;
} value;

typedef struct content{
    bool is_signed;
    bool is_loc;
    location loc;
    value val;
} content;

typedef struct op_stack{
    content c;
    struct op_stack *down;
} op_stack;

void process_op(op_stack **s, Dwarf_Op *op, um_frame *context, um_data* dbg);

content compute_ops (Dwarf_Op **ops, size_t nops, um_frame *context, um_data* dbg);

#endif
