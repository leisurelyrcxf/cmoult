#ifndef WAIT_ACCESS_H
#define WAIT_ACCESS_H

#include "data_structs.h"

#include "watch_access.h"
#include "add_watchpoint.h"
#include "rwutils.h"
#include "libc_includes.h"
#include "get_var_addr.h"
#include "get_var_size.h"

int um_wait_addr_access(um_data* dbg, uint64_t addr, size_t len);

int um_wait_addr_write(um_data* dbg, uint64_t addr, size_t len);

int um_wait_addr_execute(um_data* dbg, uint64_t addr, size_t len);

int um_wait_var_access(um_data* dbg, bool is_local, char* name, char* scope, size_t size);

int um_wait_var_write(um_data* dbg, bool is_local, char* name, char* scope, size_t size);

int um_watch_addr_access(um_data* dbg, uint64_t addr, size_t len,
    int (*callback)(um_data*, uint64_t, size_t, int (*callback_op)(um_data*, void*, size_t)),
    int (*callback_op)(um_data*, void*, size_t));

int um_watch_var_access(um_data* dbg, bool is_local, char* name, char* scope, size_t size,
    int (*callback)(um_data*, uint64_t, size_t, int (*callback_op)(um_data*, void*, size_t)),
    int (*callback_op)(um_data*, void*, size_t));

int cleanup_watchpoint(um_data* dbg, uint64_t addr, size_t len, uint8_t wait_cond);

#endif
