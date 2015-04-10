#include "debug.h"

void print_variables (um_frame *stack, um_data *dbg)
  {
    um_frame* current_stack_pointer = stack;

    while (current_stack_pointer)
      {

        const char* current_function = um_get_function(dbg, current_stack_pointer);

        if (!current_function) {
            current_stack_pointer = um_get_next_frame(current_stack_pointer);
            continue;
        }

        um_search_all_args args =
          {
            .tag = DW_TAG_variable,
            .wanted_attribute = DW_AT_name,
            .name = NULL,
            .parent_name = current_function,
            .address = 0,
            .n_results = 0,
            .result = NULL
          };

        int r = um_parse(dbg, &um_search_all, &args);

        if (args.n_results && r > 0)
            printf("Variables in function %s:\n", current_function);
        else {
            printf("No variable in function %s.\n", current_function);
            current_stack_pointer = um_get_next_frame(current_stack_pointer);
            continue;
        }

        //now, let's loop through the variables
        for (int i = 0; i < args.n_results; i++)
          {
            const char* name = dwarf_formstring(&(args.result[i]));
            uint64_t addr = um_get_local_var_addr(dbg, name, current_function);
            uint64_t value = um_read_addr(dbg, addr, um_get_var_size(dbg, name, current_function));
            printf("[%d]Variable %s is located at address 0x%lx and is equal to 0x%lx.\n", i, name, addr, value);
          }

        current_stack_pointer = um_get_next_frame(current_stack_pointer);

      }
  }
