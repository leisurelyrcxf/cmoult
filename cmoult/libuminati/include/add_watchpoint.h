#ifndef ADD_WATCHPOINT_H
#define ADD_WATCHPOINT_H

#include "stdlib.h"
#include "data_structs.h"

#define DR_NUM 4
#define DR_STATUS 6
#define DR_CTRL 7

#define WP_TRAP_COND_EXECUTION 0b00
#define WP_TRAP_COND_DATA_WRITE 0b01
#define WP_TRAP_COND_IO_ACCESS 0b10
#define WP_TRAP_COND_DATA_ACCESS 0b11

#define WATCH_LENGTH_1 (0b00 << 2)
#define WATCH_LENGTH_2 (0b01 << 2)
#define WATCH_LENGTH_4 (0b11 << 2)
#define WATCH_LENGTH_8 (0b10 << 2)

#define WATCH_LOCAL 0
#define WATCH_GLOBAL 1

typedef enum _wp_op_t{
  WP_COUNT,
  WP_ADD,
  WP_REMOVE,
  WP_PRINT_ADD,
  WP_PRINT_REMOVE
}wp_op_t;


int um_add_watchpoint(um_data* dbg, uint64_t addr, int len, uint8_t break_cond, bool break_ctrl);

int um_remove_watchpoint(um_data* dbg, uint64_t addr, int len, uint8_t break_cond, bool break_ctrl);

int um_clear_all_dr(um_data* dbg);

int um_clear_dr_status(um_data* dbg);

#endif
