// From http://www.x86-64.org/documentation/abi-0.98.pdf, page 56
#ifndef REGS
#define REGS
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
#endif