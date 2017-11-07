#ifndef PARSE_DEBUG_INFO
#define PARSE_DEBUG_INFO

#include "libc_includes.h"
#include "elfutils_includes.h"
#include "data_structs.h"

/* Callback for um_parse and walk_tree.
 * This um_counts the DIEs matching the arg supplied, which should be of type um_count_arg.
 * If the tags, the names, the parent names and the addresses all match, it increments the result field.
 * In any case, it returns -1 to keep walking the trees.*/

typedef struct um_count_args{
    const int tag;
    const char* name;
    const char* parent_name;
    const uint64_t address;
    int result;
} um_count_args;

int um_count (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias);

/* Callback for um_parse and walk_tree.
 * This searchs for a DIE matching the arg supplied, which should be of type um_search_first_arg.
 * It checks first for the tags, the names, the parent names and the addresses. Please note that this is an AND, not an OR.
 * If any of these doesn't match, the function returns -1 to keep searching in the rest of the tree.
 * If they all match but there is no such attribute as you specified, it returns 1 to stop the search and sets the result field to NULL.
 * Otherwise, it returns 0 and sets the result field to the attribute it found.*/

typedef struct um_search_first_args{
    const int tag;
    const unsigned int wanted_attribute;
    const char* name;
    const char* parent_name;
    const uint64_t address;
    Dwarf_Attribute *result;
} um_search_first_args;

int um_search_first (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias);

/* Callback for um_parse and walk_tree.
 * Same as previous one, except it doesn't stop walking the tree and retrieves all valid results.
 * The argument supplied should be of type um_search_all_arg.*/

typedef struct um_search_all_args{
    const int tag;
    const unsigned int wanted_attribute;
    const char* name;
    const char* parent_name;
    const uint64_t address;
    int n_results;
    Dwarf_Attribute *result;
} um_search_all_args;

int um_search_all (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias);

/* You probably need parse_info_section more than this function.
 * This function recursively walks the DIE tree from a given CU and applies the callback to every DIE it enum_counters.
 * The parent_name argument is here to know one DIE's parent, you can and should set it to NULL when you call this function.
 * The callback's return value determines if the function continues to walk the tree:
 *  - a strictly negative value means that the function will go on,
 *  - a null or positive value means that the function will stop here.
 * See above for already defined callbacks.*/

int walk_tree (Dwarf_Die *cur_die, const char* parent_name, int (*callback) (Dwarf_Die*, const char*, void*, Dwarf_Addr), void* callback_args, Dwarf_Addr bias);

/* This function performs the callback on every DIE there is present anywhere.
 * The function stops when there are no more DIEs or when the callback returns a positive or null value.
 * See above for already defined callbacks.*/

int um_parse (um_data* dbg, int (*callback) (Dwarf_Die*, const char*, void*, Dwarf_Addr), void* callback_args);

#endif
