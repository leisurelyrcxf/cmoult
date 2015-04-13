#include "calculate_cfi.h"

//bool check_if_all_unknown (location** result) {
//}

void calculate_cfi (unsigned char* code, size_t size, op_processors_t opcode_processors[], location** result) {
    if (!code || !result)
        return;
    if (!opcode_processors)
        opcode_processors = standard_opcode_processors;
    for (unsigned int i = 0; i < size; i += (opcode_processors[code[i]])(code+i+1, result)); //TODO: check that some registers are still known at this point (arch-specific)
}
