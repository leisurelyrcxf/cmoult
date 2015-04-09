#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/user.h>
#include <sys/wait.h>
#include <unistd.h>
#include <syscall.h>
#include <string.h>
#include "libuminati.h"
#include "debug.h"

int main(int argc, const char* argv[])
  {
    if (argc < 3)
      {
        printf("Usage: %s pid binary_file\n", argv[0]);
        exit(EXIT_FAILURE);
      }
    int fail = 0;
    pid_t pid = atoi(argv[1]);
    //Prise de controle
    fail = um_attach(pid);
    if (fail != 0)
      {
        perror("ptrace");
        exit(EXIT_FAILURE);
      }
    waitpid(pid, NULL, 0);
    printf("Attached to PID %d!\n", pid);

    /***** ALLOCATING DEBUG DATA *****/

    um_data* dbg;
    if ((fail = um_init(&dbg, pid, argv[2])))
      {
        fprintf(stderr, "Could not fill out debug info for %s, error code %d\n", argv[2], fail);
        exit(EXIT_FAILURE);
      }

    /***** STACK UNWINDING *****/

    um_frame* stack = NULL;
    um_unwind (dbg, NULL, &stack, 0);

    /***** VARIABLE PRINTING *****/

    if (stack)
        print_variables (stack, dbg);

    /***** CHECKING FOR FUNCTIONS IN STACK *****/

    if (um_unwind (dbg, "ancien_main", &stack, UM_UNWIND_STOPWHENFOUND))
        printf("Found ancien_main on the stack!\n");
    else
        printf("Did not find ancien_main on the stack!\n");
    if (um_unwind (dbg, "lol", &stack, UM_UNWIND_STOPWHENFOUND | UM_UNWIND_RETURNLAST))
        printf("Found lol on the stack!\n");
    else
        printf("Did not find lol on the stack!\n");

    /***** MODIFYING VARIABLES *****/
    int i;
    for (i = 3; i < argc; i++)
      {
        char* buf = strtok((char*)argv[i], "=");
        uint64_t val;
        val = strtoul(strtok(NULL, "="), NULL, 10);
        um_set_variable (dbg, buf, true, "ancien_main", val, 4);
      }

    /***** LOAD UPDATE *****/
    printf("Loading returned %d\n", um_load_code(dbg, "bin/update.so"));

    /***** SAFE REDEFINITION *****/
    um_redefine(dbg, "not_in_stack", "not_in_stack_v2");
    if (um_wait_out_of_stack(dbg, "sleep_and_print") == 0)
        um_redefine(dbg, "sleep_and_print", "sleep_and_print_2");

    /***** DEBUG *****/
    um_cont(pid);
    int status;
    waitpid(pid, &status, 0);
    if (WIFSIGNALED(status)) {
        struct user_regs_struct regs = {0};
        um_read_registers(dbg, &regs);
        printf("Killed by sig %d at 0x%lx\n", WTERMSIG(status), regs.rip);
    } else if (WIFSTOPPED(status)) {
        struct user_regs_struct regs = {0};
        um_read_registers(dbg, &regs);
        printf("Killed by sig %d at 0x%lx\n", WSTOPSIG(status), regs.rip);
    }

    /***** EXITING *****/

    um_destroy_stack(stack);
    um_end(dbg);

    sleep(1);
    um_detach(pid);
    return EXIT_SUCCESS;
  }
