#ifndef OPCODE_PROCESSORS
#define OPCODE_PROCESSORS

#include "libc_includes.h"
#include "dwarf_ops.h"

typedef void (*op_processors_t)(void*[], unsigned char[], size_t, location*[]);

void opcode_processor_00 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_01 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_02 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_03 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_04 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_05 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_06 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_07 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_08 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_09 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_0a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_0b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_0c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_0d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_0e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_0f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_10 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_11 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_12 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_13 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_14 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_15 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_16 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_17 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_18 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_19 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_1a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_1b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_1c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_1d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_1e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_1f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_20 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_21 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_22 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_23 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_24 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_25 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_26 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_27 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_28 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_29 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_2a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_2b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_2c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_2d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_2e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_2f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_30 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_31 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_32 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_33 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_34 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_35 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_36 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_37 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_38 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_39 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_3a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_3b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_3c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_3d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_3e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_3f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_40 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_41 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_42 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_43 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_44 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_45 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_46 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_47 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_48 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_49 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_4a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_4b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_4c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_4d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_4e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_4f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_50 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_51 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_52 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_53 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_54 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_55 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_56 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_57 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_58 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_59 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_5a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_5b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_5c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_5d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_5e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_5f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_60 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_61 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_62 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_63 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_64 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_65 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_66 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_67 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_68 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_69 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_6a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_6b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_6c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_6d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_6e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_6f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_70 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_71 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_72 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_73 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_74 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_75 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_76 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_77 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_78 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_79 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_7a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_7b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_7c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_7d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_7e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_7f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_80 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_81 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_82 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_83 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_84 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_85 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_86 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_87 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_88 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_89 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_8a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_8b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_8c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_8d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_8e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_8f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_90 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_91 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_92 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_93 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_94 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_95 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_96 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_97 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_98 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_99 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_9a (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_9b (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_9c (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_9d (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_9e (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_9f (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a0 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a1 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a2 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a3 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a4 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a5 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a6 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a7 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a8 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_a9 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_aa (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ab (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ac (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ad (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ae (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_af (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b0 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b1 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b2 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b3 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b4 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b5 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b6 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b7 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b8 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_b9 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ba (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_bb (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_bc (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_bd (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_be (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_bf (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c0 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c1 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c2 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c3 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c4 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c5 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c6 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c7 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c8 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_c9 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ca (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_cb (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_cc (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_cd (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ce (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_cf (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d0 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d1 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d2 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d3 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d4 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d5 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d6 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d7 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d8 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_d9 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_da (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_db (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_dc (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_dd (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_de (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_df (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e0 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e1 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e2 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e3 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e4 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e5 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e6 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e7 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e8 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_e9 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ea (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_eb (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ec (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ed (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ee (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ef (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f0 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f1 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f2 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f3 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f4 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f5 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f6 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f7 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f8 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_f9 (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_fa (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_fb (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_fc (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_fd (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_fe (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);
void opcode_processor_ff (void* opcode_processors[static 256], unsigned char code[static 1], size_t size_to_read, location* result[static NREGS]);

op_processors_t standard_opcode_processors[256];

#endif
