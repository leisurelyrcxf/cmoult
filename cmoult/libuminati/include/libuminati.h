/*****libuminati.h*****/
#ifndef LIBUMINATI
#define LIBUMINATI
#include <stdint.h>
#include <sys/user.h>
#include <libdw.h>

#define NREGS 67
#define REG_RAX 0
#define REG_RDX 1
#define REG_RCX 2
#define REG_RBX 3
#define REG_RSI 4
#define REG_RDI 5
#define REG_RBP 6
#define REG_RSP 7
#define REG_R8 8
#define REG_R9 9
#define REG_R10 10
#define REG_R11 11
#define REG_R12 12
#define REG_R13 13
#define REG_R14 14
#define REG_R15 15
#define REG_RA 16
#define REG_XMM0 17
#define REG_XMM1 18
#define REG_XMM2 19
#define REG_XMM3 20
#define REG_XMM4 21
#define REG_XMM5 22
#define REG_XMM6 23
#define REG_XMM7 24
#define REG_XMM8 25
#define REG_XMM9 26
#define REG_XMM10 27
#define REG_XMM11 28
#define REG_XMM12 29
#define REG_XMM13 30
#define REG_XMM14 31
#define REG_XMM15 32
#define REG_ST0 33
#define REG_ST1 34
#define REG_ST2 35
#define REG_ST3 36
#define REG_ST4 37
#define REG_ST5 38
#define REG_ST6 39
#define REG_ST7 40
#define REG_MM0 41
#define REG_MM1 42
#define REG_MM2 43
#define REG_MM3 44
#define REG_MM4 45
#define REG_MM5 46
#define REG_MM6 47
#define REG_MM7 48
#define REG_RFLAGS 49
#define REG_ES 50
#define REG_CS 51
#define REG_SS 52
#define REG_DS 53
#define REG_FS 54
#define REG_GS 55
#define REG_FS_BASE 58
#define REG_GS_BASE 59
#define REG_TR 62
#define REG_LDTR 63
#define REG_MXCSR 64
#define REG_FCW 65
#define REG_FSW 66

/*****Flags*****/
#define UM_UNWIND_STOPWHENFOUND 1
#define UM_UNWIND_RETURNLAST 2

#include "compute_location.h"
#include "elfutils_includes.h"
#include "init.h"
#include "rwutils.h"
#include "data_structs.h"
#include "generate_trace.h"
#include "get_local_var_addr.h"
#include "get_var_size.h"
#include "opcode_processors.h"
#include "binutils_includes.h"
#include "load_code.h"
#include "libc_includes.h"
#include "get_function_addr.h"
#include "wait_out_of_stack.h"
#include "registers.h"
#include "get_next_frame.h"
#include "unwind.h"
#include "parse.h"
#include "add_breakpoint.h"
#include "add_memory.h"
#include "set_variable.h"
#include "destroy.h"
#include "get_frame_info.h"
#include "redefine.h"
#include "get_stack_size.h"
#include "dwarf_ops.h"
#include "insert_jump.h"
#include "get_function.h"


///*****Opaque data types*****/
//typedef struct um_frame um_frame;
//
//typedef struct um_data um_data;
//
///*****Initialization*****/
//int um_init (um_data** dbg, pid_t pid, const char* fname);
//
///*****Functions to free the above types*****/
//void um_destroy_stack(um_frame* list);
//void um_end (um_data* dbg);
//
///*****Thread control*****/
///*****Attach to a thread*****/
//int um_attach (pid_t pid);
///*****Unpause a traced thread*****/
//int um_cont (pid_t pid);
///*****Detach from a thread*****/
//int um_detach (pid_t pid);
//
///*****Read/Write in a thread's memory or registers*****/
//int um_write_addr (um_data* dbg, uint64_t addr, uint64_t value, size_t size);
//int um_write_registers(um_data* dbg, struct user_regs_struct* regs);
//uint64_t um_read_addr (um_data* dbg, uint64_t addr, size_t size);
//int um_read_registers(um_data* dbg, struct user_regs_struct* regs);
//
///*****Stack and frame manipulation*****/
///*Unwind the stack until target is found.
// * If target is NULL or cannot be found, um_unwind returns NULL.
// * If target is found, um_unwind returns the corresponding um_frame.
// * um_unwind sets cache to the full stack.*/
//um_frame* um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags);
///* Get the frame that is further down in the stack*/
//um_frame* um_get_next_frame (um_frame* cur);
///* Get the size of the stack*/
//int um_get_stack_size (um_data* dbg, um_frame* stack);
///* Get the function "owning" a frame*/
//const char* um_get_function (um_data *dbg, um_frame* context);
///* Generate a stack trace (list of pairs (function name, address)) from a stack
// * functions and addresses must be non-null and point to a pre-allocated array of the stack's size*/
//void um_generate_trace (um_data* dbg, um_frame* stack, char** functions, uint64_t* addresses);
//
///*****Parsing functions*****/
///*Callbacks for the parsing*/
//typedef struct um_count_args{
//    const int tag;
//    const char* name;
//    const char* parent_name;
//    const uint64_t address;
//    int result;
//} um_count_args;
//int um_count (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias);
//
//typedef struct um_search_first_args{
//    const int tag;
//    const unsigned int wanted_attribute;
//    const char* name;
//    const char* parent_name;
//    const uint64_t address;
//    Dwarf_Attribute *result;
//} um_search_first_args;
//int um_search_first (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias);
//
//typedef struct um_search_all_args{
//    const int tag;
//    const unsigned int wanted_attribute;
//    const char* name;
//    const char* parent_name;
//    const uint64_t address;
//    int n_results;
//    Dwarf_Attribute *result;
//} um_search_all_args;
//int um_search_all (Dwarf_Die* die, const char* parent_name, void* vargs, Dwarf_Addr bias);
//
///*Parsing function. The callback is applied to every node in the debug info*/
//int um_parse (um_data* dbg, int (*callback) (Dwarf_Die*, const char*, void*, Dwarf_Addr), void* callback_args);
//
///*More specific parsing functions*/
//uint64_t um_get_function_addr (um_data *dbg, char* name);
//uint64_t um_get_local_var_addr(um_data* dbg, const char* name, const char* scope);
//size_t um_get_var_size (um_data *dbg, const char* var_name, const char* scope_name);
//
///*****High-level helpers*****/
///* Wait until function is out of stack*/
//int um_wait_out_of_stack(um_data* dbg, char* name);
///* Redefinition of a function by another*/
//int um_redefine(um_data* dbg, char* name1, char* name2);
///*Set a variable of a given size to a given value*/
//int um_set_variable (um_data* dbg, char* name, bool is_local, char* scope, uint64_t val, size_t size);
//
//
//int um_load_code (um_data* dbg, const char* file_name);
#endif
