#ifndef DATA_STRUCTS
#define DATA_STRUCTS
#include "registers.h"
#include "libc_includes.h"
#include "elfutils_includes.h"

typedef struct um_frame{
    uint64_t rip;
    uint64_t cfa;
    uint64_t regs[NREGS];
    struct um_frame *next;
} um_frame;

typedef struct function{
    char* name;
    uint64_t lowpc;
    uint64_t highpc;
    struct function *next;
} function;

typedef struct um_data{
    const char* fname;
    pid_t pid;
    Dwfl* debug_raw;
    Dwarf_CFI* cfi;
    Dwarf_Addr bias;
    Elf* elf;
    function* injected;
} um_data;

#endif
