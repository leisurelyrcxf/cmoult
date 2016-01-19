#include "data_structs.h"

void um_destroy_stack(um_frame* list)
  {
    um_frame *previous_sp, *current_sp;
    current_sp = list;
    while (current_sp != NULL)
      {
        previous_sp = current_sp;
        current_sp = current_sp->next;
        free(previous_sp);
      }
  }

void free_all_injected (function* list)
  {
    function *previous, *current;
    current = list;
    while (current != NULL)
      {
        previous = current;
        current = current->next;
        free(previous->name);
        free(previous);
      }
  }

void um_end (um_data* dbg)
  {
    if (dbg->elf)
      {
        dwarf_cfi_end(dbg->cfi);
        elf_end(dbg->elf);
      }
    dwfl_end(dbg->debug_raw);
    free_all_injected(dbg->injected);
    free(dbg);
  }
