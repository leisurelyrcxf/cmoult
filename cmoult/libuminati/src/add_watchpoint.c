#include "add_watchpoint.h"


bool wp_dr_used[4] = {0, 0, 0, 0};
uint64_t wp_dr_mem_addr[4] = {(uint64_t)-1, (uint64_t)-1, (uint64_t)-1, (uint64_t)-1};
uint8_t wp_dr_mem_len[4] = {0, 0, 0, 0};
uint8_t wp_dr_cond[4] = {0xff, 0xff, 0xff, 0xff};
uint8_t wp_dr_ctrl[4] = {0xff, 0xff, 0xff, 0xff};

static uint8_t um_get_len_bits(uint8_t len){
  switch(len){
    case 1:
      return WATCH_LENGTH_1;
    case 2:
      return WATCH_LENGTH_2;
    case 4:
      return WATCH_LENGTH_4;
    case 8:
      return WATCH_LENGTH_8;
    default:
      return 0b11111111;
  }
}

static const char* um_get_str_of_break_cond(uint8_t break_cond){
  switch(break_cond){
    case WP_TRAP_COND_EXECUTION:
      return "WP_TRAP_COND_EXECUTION";
    case WP_TRAP_COND_DATA_WRITE:
      return "WP_TRAP_COND_DATA_WRITE";
    case WP_TRAP_COND_IO_ACCESS:
      return "WP_TRAP_COND_IO_ACCESS";
    case WP_TRAP_COND_DATA_ACCESS:
      return "WP_TRAP_COND_DATA_ACCESS";
    default:
      return "invalid break condition";
  }
}

static const char* um_get_str_of_break_ctrl(uint8_t break_ctrl){
  switch(break_ctrl){
    case WATCH_LOCAL:
      return "WATCH_LOCAL";
    case WATCH_GLOBAL:
      return "WATCH_GLOBAL";
    default:
      return "invalid break control";
  }
}

static bool um_is_dr_available(int i){
  return wp_dr_used[i] == 0;
}

static int um_find_dr(int64_t addr_to_watch, uint8_t len,
    uint8_t break_cond, bool break_ctrl){
  for(int i = 0; i < DR_NUM; i++){
    if(wp_dr_used[i] == 1 && wp_dr_mem_addr[i] == addr_to_watch && wp_dr_mem_len[i] == len
        && wp_dr_cond[i] == break_cond && wp_dr_ctrl[i] == break_ctrl){
      return i;
    }
  }
  return -1;
}

static uint64_t um_read_dr(um_data* dbg, int i){
  return ptrace(PTRACE_PEEKUSER, dbg->pid, offsetof (struct user, u_debugreg[i]), 0);
}

static int um_write_dr(um_data* dbg, int i, uint64_t val){
  return ptrace(PTRACE_POKEUSER, dbg->pid, offsetof (struct user, u_debugreg[i]), val);
}

static int um_add_aligned_watchpoint(um_data* dbg, uint64_t addr_to_watch, uint8_t len,
    uint8_t break_cond, uint8_t break_ctrl){
  if(addr_to_watch == 0 || addr_to_watch == (uint64_t)-1){
    return -1;
  }

  if(len != 1 && len != 2 && len != 4 && len != 8){
    fprintf(stderr, "len must be 1, 2, 4 or 8\n");
    return -1;
  }

  if(addr_to_watch % len != 0){
    fprintf(stderr, "not aligned\n");
    return -1;
  }

  if(break_cond < 0 || break_cond > 3){
    fprintf(stderr, "break condition invalid\n");
    return -1;
  }

  if(break_ctrl < 0 || break_ctrl > 1){
    fprintf(stderr, "break control invalid\n");
    return -1;
  }

  int i = 0;
  for(; i < DR_NUM; i++){
    if(um_is_dr_available(i)){
      break;
    }
  }
  if(i >= DR_NUM){
    fprintf(stderr, "no debug register available\n");
    return -1;
  }

  uint64_t dri = addr_to_watch;
  uint64_t break_len_bits_mask = (((uint64_t)break_cond) | ((uint64_t)um_get_len_bits(len))) << (16 + i * 4);
  uint64_t local_global_bits_mask = (1 << (break_ctrl ? 1 : 0) ) << (i * 2);
  uint64_t dr7 = um_read_dr(dbg, 7);
  uint64_t clear_bits_mask = ~((0b1111 << (16 + i * 4)) | (0b11 << (i * 2)));

  dr7 = ((dr7 & clear_bits_mask ) | break_len_bits_mask ) | local_global_bits_mask;
  if(um_write_dr(dbg, i, dri) != 0){
    char buff[1024];
    sprintf(buff, "write dr%d", i);
    perror(buff);
    return -1;
  }

  if(um_write_dr(dbg, 7, dr7) != 0){
    perror("write dr7");
    return -1;
  }
  wp_dr_used[i] = 1;
  wp_dr_mem_addr[i] = dri;
  wp_dr_mem_len[i] = len;
  wp_dr_cond[i] = break_cond;
  wp_dr_ctrl[i] = break_ctrl;
  return 0;
}

static int um_remove_aligned_watchpoint(um_data* dbg, uint64_t addr_to_watch, uint8_t len,
    uint8_t break_cond, bool break_ctrl){
  if(addr_to_watch == 0 || addr_to_watch == (uint64_t)-1){
    return -1;
  }

  if(len != 1 && len != 2 && len != 4 && len != 8){
    fprintf(stderr, "len must be 1, 2, 4 or 8\n");
    return -1;
  }

  if(addr_to_watch % len != 0){
    fprintf(stderr, "not aligned\n");
    return -1;
  }

  if(break_cond < 0 || break_cond > 3){
    fprintf(stderr, "break condition invalid\n");
    return -1;
  }

  if(break_ctrl < 0 || break_ctrl > 1){
    fprintf(stderr, "break control invalid\n");
    return -1;
  }

  int i = um_find_dr(addr_to_watch, len, break_cond, break_ctrl);
  if(i == -1){
    fprintf(stdout, "no debug register found\n");
    return -1;
  }

  uint64_t dr7 = um_read_dr(dbg, 7);
  uint64_t clear_bits_mask = ~((0b1111 << (16 + i * 4)) | (0b11 << (i * 2)));

  dr7 = (dr7 & clear_bits_mask );
  if(um_write_dr(dbg, i, 0) != 0){
    char buff[1024];
    sprintf(buff, "write dr%d", i);
    perror(buff);
  }

  if(um_write_dr(dbg, 7, dr7) != 0){
    perror("write dr7");
    return -1;
  }
  wp_dr_used[i] = 0;
  wp_dr_mem_addr[i] = (uint64_t)-1;
  wp_dr_mem_len[i] = 0;
  wp_dr_cond[i] = 0xff;
  wp_dr_ctrl[i] = 0xff;
  return 0;
}

/* The following function is inspired by the i386-nat.c  i386_handle_nonaligned_watchpoint() proc*/
static int um_handle_unaligned_watchpoint (um_data* dbg, wp_op_t op, uint64_t addr, int len,
    uint8_t break_cond, bool break_ctrl)
{
  int align;
  int size;
  int rv = 0, status = 0;
  int max_wp_len = 8; //for x86-64, maxim monitored bytes are 8

  static int size_try_array[8][8] =
  {
    {1, 1, 1, 1, 1, 1, 1, 1}, /* trying size one */
    {2, 1, 2, 1, 2, 1, 2, 1}, /* trying size two */
    {2, 1, 2, 1, 2, 1, 2, 1}, /* trying size three */
    {4, 1, 2, 1, 4, 1, 2, 1}, /* trying size four */
    {4, 1, 2, 1, 4, 1, 2, 1}, /* trying size five */
    {4, 1, 2, 1, 4, 1, 2, 1}, /* trying size six */
    {4, 1, 2, 1, 4, 1, 2, 1}, /* trying size seven */
    {8, 1, 2, 1, 4, 1, 2, 1}, /* trying size eight */
  };

  while (len > 0){
      align = addr % max_wp_len;
      /* Four(eigth on x86_64) is the maximum length an x86 debug register
   can watch.  */
      size = size_try_array[len > max_wp_len ? (max_wp_len - 1) : len - 1][align];
      if (op == WP_COUNT){
  /* size_try_array[] is defined so that each iteration through
     the loop is guaranteed to produce an address and a size
     that can be watched with a single debug register.  Thus,
     for counting the registers required to watch a region, we
     simply need to increment the count on each iteration.  */
        rv++;
      }else if(op == WP_PRINT_ADD){
        printf("add debug register for watchpoint for address %p, length %d, type \"%s\", control \"%s\"\n",
            (void*)addr,
            size,
            um_get_str_of_break_cond(break_cond),
            um_get_str_of_break_ctrl(break_ctrl));
      }else if(op == WP_PRINT_REMOVE){
        printf("remove debug register for watchpoint for address %p, length %d, type \"%s\", control \"%s\"\n",
            (void*)addr,
            size,
            um_get_str_of_break_cond(break_cond),
            um_get_str_of_break_ctrl(break_ctrl));
      }else{
        if (op == WP_ADD)
          status = um_add_aligned_watchpoint(dbg, addr, size, break_cond, break_ctrl);
        else if (op == WP_REMOVE)
          status = um_remove_aligned_watchpoint (dbg, addr, size, break_cond, break_ctrl);
        else
          fprintf(stderr, "invalid operation\n");
        /* We keep the loop going even after a failure, because some
           of the other aligned watchpoints might still succeed
           (e.g. if they watch addresses that are already watched,
           in which case we just increment the reference counts of
           occupied debug registers).  If we break out of the loop
           too early, we could cause those addresses watched by
           other watchpoints to be disabled when breakpoint.c reacts
           to our failure to insert this watchpoint and tries to
           remove it.  */
        if (status)
          rv += status;
      }
      addr += size;
      len -= size;
  }
  return rv;
}

int um_add_watchpoint(um_data* dbg, uint64_t addr, int len, uint8_t break_cond, bool break_ctrl){
  int ret;

  if ((len != 1 && len !=2 && len !=4 && len != 8) || addr % len != 0){
    um_handle_unaligned_watchpoint(dbg, WP_PRINT_ADD, addr, len, break_cond, break_ctrl);
    ret = um_handle_unaligned_watchpoint(dbg, WP_ADD, addr, len, break_cond, break_ctrl);
    if(ret == -1 * um_handle_unaligned_watchpoint(dbg, WP_COUNT, addr, len, break_cond, break_ctrl)){
      return -1;
    }
    return 0;
  }else{
    ret = um_add_aligned_watchpoint(dbg, addr, len, break_cond, break_ctrl);
  }

  return ret;
}

int um_remove_watchpoint(um_data* dbg, uint64_t addr, int len, uint8_t break_cond, bool break_ctrl){
  int ret;

  if ((len != 1 && len !=2 && len !=4 && len != 8) || addr % len != 0){
    um_handle_unaligned_watchpoint(dbg, WP_PRINT_REMOVE, addr, len, break_cond, break_ctrl);
    ret = um_handle_unaligned_watchpoint(dbg, WP_REMOVE, addr, len, break_cond, break_ctrl);
  }else{
    ret = um_remove_aligned_watchpoint(dbg, addr, len, break_cond, break_ctrl);
  }

  return ret;
}

int um_clear_all(um_data* dbg){
  int err;
  for(int i = 0; i < 4; i++){
    err+=um_write_dr(dbg, i, 0);
  }
  err+=um_write_dr(dbg, 6, 0);
  err+=um_write_dr(dbg, 7, 0);
  if(err == 0)
    return 0;
  return -1;
}

int um_clear_status(um_data* dbg){
  if(um_write_dr(dbg, 6, 0) != 0){
    perror("write dr6");
    return -1;
  }
}
