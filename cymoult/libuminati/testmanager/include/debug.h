#include <stdlib.h>
#include <stdio.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <unistd.h>
#include <syscall.h>
#include <string.h>
#include <dwarf.h>
#include "libuminati.h"

void print_variables (um_frame *stack, um_data *dbg);
