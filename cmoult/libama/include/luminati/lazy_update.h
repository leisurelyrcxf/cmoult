#ifndef LAZY_UPDATE_H
#define LAZY_UPDATE_H

#include "add_watchpoint.h"
#include "watch_access.h"

int lazy_update_watch_access_callback(um_data* dbg, uint64_t addr, size_t len, int (*update)(um_data*, void*, size_t));

int um_lazy_update_address(um_data* dbg, uint64_t addr, size_t len, int (*update)(um_data*, void*, size_t));

int um_lazy_update_variable(um_data* dbg, bool is_local, char* name, char* scope, size_t size, int (*update)(um_data*, void*, size_t));


#endif
