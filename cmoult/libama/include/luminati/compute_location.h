#ifndef PARSE_ATTRIBUTES
#define PARSE_ATTRIBUTES

#include "libc_includes.h"
#include "data_structs.h"
#include "dwarf_ops.h"
#include "parse.h"

/* DISCLAIMER: This file is not meant to wrap every function in libdw that gets a value from an attribute.
 * The libdw functions do their job quite well, the functions you should look into are mostly the dwarf_form* ones.
 * These functions help for the trickier parts, such as getting info on the type or getting a location. */

/* This function computes a location in a given context of execution */
uint64_t compute_location (Dwarf_Attribute* attr, um_frame* context, um_data* dbg);

#endif
