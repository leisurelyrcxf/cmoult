#ifndef ADD_MEMORY
#define ADD_MEMORY

#include "libc_includes.h"
#include "rwutils.h"

#define CODE_SIZE 5

//Linux-specific
//To have more portable code, we would need to add a syscall to open /dev/zero, pass this fd to mmap, and then close /dev/zero

/*
 * Bytes 1 to 3:          48 31 c0                 xor %rax, %rax           set rax to 0
 * Bytes 4 to 5:          b0 09                    movb $0x9, %al           set it to 9, smaller code that way
 *                                                                          RAX is the syscall ID, 0x9 is mmap
 * Bytes 6 to 8:          48 31 ff                 xor %rdi, %rdi           set rdi to 0*/
#define WORD1 0x4831c0b0094831ff
/*
 * Bytes 1 to 7:          48 c7 c7 00 00 40 00     movq $0x400000, %rdi     hint mmap to 0x400000 to be not too far away from the other code
 *                                                                          RDI is the address parameter
 * Byte 8:                90                       nop                      for readability*/
//#define WORD1 0x48c7c70000400090
/*
 * Bytes 1 to 7:          48 c7 c6 00 00 00 00     movq $0x0, %rsi          bytes 4 to 7 to be replaced by size
 *                                                                          RSI is the size parameter
 * Byte 8:                90                       nop                      for readability*/
#define WORD2 0x48c7c60000000090
/*
 * Bytes 1 to 3:          48 31 d2                 xor %rdx, %rdx           set rdx to 0
 * Bytes 4 to 5:          b2 05                    movb $0x5, %dl           set it to 5, same dirty hack
 *                                                                          RDX is the protection parameter, 0x5 is PROT_READ | PROT_EXEC
 * Bytes 6 to 8:          4d 31 d2                 xor %r10, %r10           set r10 to 0*/
#define WORD3 0x4831d2b2054d31d2
/*
 * Bytes 1 to 3:          41 b2 62                 movb $0x62, %r10b        set r10 to 0x62
 *                                                                          R10 is the flag parameter, 0x62 is MAP_32BIT | MAP_PRIVATE | MAP_ANONYMOUS
 * Bytes 4 to 7:          49 83 c8 ff              orq $-1, %r8             set R8 to -1
 *                                                                          R8 is the FD parameter
 * Byte 8:                90                       nop                      for readability*/
#define WORD4 0x41b2624983c8ff90
/*
 * Bytes 1 to 3:          4d 31 c9                 xor %r9, %r9             set r9 to 0
 *                                                                          R9 is the offset parameter
 * Bytes 4 to 5:          0f 05                    syscall                  Perform mmap(0, size, PROT_READ | PROT_EXEC, MAP_PRIVATE | MAP_ANONYMOUS, -1, 0)
 * Byte 6:                cc                       int3                     breakpoint, so that we can put things back to normal when we're done*/
#define WORD5 0x4d31c90f05cc9090
#define REVERT32(n) ((((n) & 0xff000000) >> 24) + (((n) & 0xff0000) >> 8) + (((n) & 0xff00) << 8) + (((n) & 0xff) << 24))
#define REVERT64(n) ((((n) & 0xff00000000000000) >> 56) + (((n) & 0xff000000000000) >> 40) + (((n) & 0xff0000000000) >> 24) + (((n) & 0xff00000000) >> 8) + \
        (((n) & 0xff000000) << 8) + (((n) & 0xff0000) << 24) + (((n) & 0xff00) << 40) + (((n) & 0xff) << 56))

uint64_t add_memory(pid_t pid, size_t size);

#endif
