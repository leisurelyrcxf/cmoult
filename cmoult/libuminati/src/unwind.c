#include "unwind.h"
#include "common_utils.h"

um_frame* um_unwind_old (um_data* dbg, const char* target, um_frame** cache, int flags) {

    if (!cache)
        return NULL;

    //Flag processing
    bool stop_when_found = flags & 01;
    bool return_last = flags & 02;

    um_frame* res = NULL;

    //Getting registers
    struct user_regs_struct regs = {0};
    if (_um_read_registers(dbg->pid, &regs) != 0)
        return NULL;

    //Creating useful variables
    um_frame* stack = (um_frame*) malloc (sizeof(um_frame));
    um_frame* current_stack_pointer = stack;

    //Initializing
    current_stack_pointer->rip = regs.rip;
    current_stack_pointer->regs[REG_RSP] = regs.rsp;
    current_stack_pointer->regs[REG_RBP] = regs.rbp;
    get_cfa_from_frame(current_stack_pointer, dbg);
    get_register_from_frame(REG_RA, current_stack_pointer, dbg);

    //Iterating
    while (1) {
        //Actualizing pointers
        um_frame* previous_stack_pointer = current_stack_pointer;
        current_stack_pointer->next = (um_frame*) malloc (sizeof(um_frame));
        current_stack_pointer = current_stack_pointer->next;

        current_stack_pointer->rip = 0;
        current_stack_pointer->cfa = 0;
        current_stack_pointer->regs[REG_RBP] = 0;
        current_stack_pointer->regs[REG_RSP] = 0;
        current_stack_pointer->regs[REG_RA] = 0;
        current_stack_pointer->rip = _um_read_addr(dbg->pid, previous_stack_pointer->regs[REG_RA], 8);
        //Check if we have finished um_unwinding
        if (current_stack_pointer->rip == 0 || current_stack_pointer->rip == 0xffffffffffffffff)
            break;

        current_stack_pointer->regs[REG_RSP] = previous_stack_pointer->cfa;
        if (get_cfa_from_frame(current_stack_pointer, dbg) == 0) {
            if (get_register_from_frame(REG_RBP, current_stack_pointer, dbg) > 0)
                current_stack_pointer->regs[REG_RBP] = _um_read_addr(dbg->pid, previous_stack_pointer->regs[REG_RBP], 8);
        }
        else {
            current_stack_pointer->regs[REG_RBP] = _um_read_addr(dbg->pid, previous_stack_pointer->regs[REG_RBP], 8);
            if (get_cfa_from_frame(current_stack_pointer, dbg) != 0)
                break;
        }
        if (get_register_from_frame(REG_RA, current_stack_pointer, dbg) != 0)
            break;

        //if this um_frame corresponds to the wanted scope, we set res
        if (target) {
            const char* function = um_get_function(dbg, current_stack_pointer);
            if (function) {
                if (strcmp(target, function) == 0) {
                    if (!res || return_last)
                        res = current_stack_pointer;
                    if (stop_when_found)
                        break;
                }
            }
        }
    }

    //Terminating
    current_stack_pointer->next = NULL;

    *cache = stack;
    return res;
}


//static int
//module_callback (Dwfl_Module *mod, void **userdata __attribute__ ((unused)),
//        const char *name, Dwarf_Addr start,
//        void *arg __attribute__ ((unused)))
//{
////  Dwarf_Addr end;
////  dwfl_module_info (mod, NULL, NULL, &end, NULL, NULL, NULL, NULL);
////  printf ("%p\t%p\t%s\n", (void*)(uint64_t) start, (void*)(uint64_t) end, name);
//  return DWARF_CB_OK;
//}

typedef struct _frame_callback_struc {
  um_data* dbg;
  um_frame* stack;
  um_frame* current;
  um_frame* result;
  bool found;
  bool finished;
  bool has_error;
  const char* target;
  const bool stop_when_found;
  const bool return_last;
  const bool print;
}frame_callback_struc;



static int frame_callback (Dwfl_Frame *dwfl_frame, void *callback_arg){
  frame_callback_struc *args = (frame_callback_struc*)callback_arg;
  if(args->has_error){
    return DWARF_CB_ABORT;
  }

  if(args->finished){
    return DWARF_CB_OK;
  }

  Dwarf_Addr pc;
  bool isactivation;
  um_frame* previous;

  if (!dwfl_frame_pc(dwfl_frame, &pc, &isactivation)){
    args->has_error = true;
    dwarf_error("failed to get pc in dwfl_frame_pc()");
    return DWARF_CB_ABORT;
  }
  Dwarf_Addr pc_adjusted = pc - (isactivation ? 0 : 1);

  /* Get PC->SYMNAME.  */
//  Dwfl_Thread *thread = dwfl_frame_thread (dwfl_frame);
//  Dwfl *dwfl = dwfl_thread_dwfl (thread);
  Dwfl_Module *mod = dwfl_addrmodule (args->dbg->debug_raw, pc_adjusted);

  if(mod == NULL){
    dwarf_error("Failed in dwfl_addrmodule()");
    args->has_error = true;
    return DWARF_CB_ABORT;
  }


  Dwarf_Addr start, end; const char* name;
  name = dwfl_module_info (mod, NULL, &start, &end, NULL, NULL, NULL, NULL);
//  printf ("%p\t%p\t%s\n", (void*)(uint64_t) start, (void*)(uint64_t) end, name);
  const char *symname = NULL;
  if(mod){
    symname = dwfl_module_addrname (mod, pc_adjusted);
  }


  if(args->print){
    printf("#%p\t%4s\t%s\n", (void*)((uint64_t) pc),
      ! isactivation ? "-1" : "top", symname);
  }



  if(args->stack == NULL){
    args->stack = (um_frame*)malloc(sizeof(um_frame));
    memset(args->stack, 0, sizeof(um_frame));
    args->current = args->stack;
    previous = NULL;
  }else{
    args->current->next = (um_frame*)malloc(sizeof(um_frame));
    memset(args->current->next, 0, sizeof(um_frame));
    previous = args->current;
    args->current = args->current->next;
  }

  if(args->current == args->stack){
    struct user_regs_struct regs = {0};
    if (_um_read_registers(args->dbg->pid, &regs) != 0){
      fprintf(stderr, "can't read registers\n");
      args->has_error = true;
      goto ppp;
    }else{
      args->current->rip = regs.rip;
      args->current->regs[REG_RSP] = regs.rsp;
      args->current->regs[REG_RBP] = regs.rbp;
      if(get_cfa_from_dwfl_module(mod, args->current->rip, args->current, args->dbg) != 0){
//        dwarf_error("Failed in get_cfa_from_dwfl_frame()");
        args->finished = true;
        goto ppp;
      }else{
        if(get_register_from_dwfl_module(REG_RA, mod, args->current->rip, args->current, args->dbg) != 0){
//          dwarf_error("Failed in get_register_from_dwfl_frame()");
          args->finished = true;
          goto ppp;
        }
      }
    }
  }else{
    args->current->rip = _um_read_addr(args->dbg->pid, previous->regs[REG_RA], 8);
    if(args->current->rip == 0 || args->current->rip == 0xffffffffffffffff){
      args->finished = true;
      goto ppp;
    }

    args->current->regs[REG_RSP] = previous->cfa;
    if (get_cfa_from_dwfl_module(mod, args->current->rip, args->current, args->dbg) == 0) {
      int temp_result;
      if ((temp_result = get_register_from_dwfl_module(REG_RBP, mod, args->current->rip, args->current, args->dbg)) > 0){
        args->current->regs[REG_RBP] = _um_read_addr(args->dbg->pid, previous->regs[REG_RBP], 8);
      }else if(temp_result < 0){
//        dwarf_error("Failed in get_register_from_dwfl_frame()");
        args->finished = true;
        goto ppp;
      }
    }else{
      args->current->regs[REG_RBP] = _um_read_addr(args->dbg->pid, previous->regs[REG_RBP], 8);
      if (get_cfa_from_dwfl_module(mod, args->current->rip, args->current, args->dbg) != 0){
//        dwarf_error("Failed in get_cfa_from_dwfl_frame()");
        args->finished = true;
        goto ppp;
      }
    }

    if (get_register_from_dwfl_module(REG_RA, mod, args->current->rip, args->current, args->dbg) != 0){
//      dwarf_error("Failed in get_register_from_dwfl_frame()");
      args->finished = true;
      goto ppp;
    }

  }

ppp:
  //if this um_frame corresponds to the wanted scope, we set res
  if(args->target){
    if (symname) {
      if (strcmp(args->target, symname) == 0){
        args->found = true;
        if (!args->result || args->return_last)
          args->result = args->current;
        if (args->stop_when_found){
          args->finished = true;
        }
      }
    }
  }
  return DWARF_CB_OK;
}

um_frame* um_unwind_print (um_data* dbg, const char* target, um_frame** cache, int flags, bool print) {
//  ptrdiff_t ptrdiff = dwfl_getmodules (dbg->debug_raw, module_callback, NULL, 0);
//  if(ptrdiff != 0){
//    dwarf_error("error in dwfl_getmodules()");
//    return NULL;
//  }

  frame_callback_struc args = {
      .dbg = dbg,
      .stack = NULL,
      .current = NULL,
      .result = NULL,
      .target = target,
      .stop_when_found = flags & 0x01,
      .return_last = flags & 0x02,
      .found = 0,
      .finished = false,
      .print = print,
      .has_error = false
  };

  if(dwfl_getthread_frames(dbg->debug_raw, dbg->pid, &frame_callback, (void*)(&args)) != 0){
      dwarf_error("dwfl_getthread_frames");
      return NULL;
  }

  *cache = args.stack;

  if(args.has_error || (target && !args.found)){
    return NULL;
  }

  return args.result;
}

void um_print_stack(um_data* dbg){
  frame_callback_struc args = {
      .dbg = dbg,
      .stack = NULL,
      .current = NULL,
      .result = NULL,
      .target = NULL,
      .stop_when_found = false,
      .return_last = false,
      .found = false,
      .finished = false,
      .print = true,
      .has_error = false
  };

  if(dwfl_getthread_frames(dbg->debug_raw, dbg->pid, &frame_callback, (void*)(&args)) != 0){
      dwarf_error("dwfl_getthread_frames");
      return;
  }
}

um_frame* um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags) {
  um_unwind_print(dbg, target, cache, flags, 0);
}
