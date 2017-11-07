#ifndef API_H
#define API_H

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <syscall.h>
#include <dirent.h>
#include <string.h>
#include <sys/ptrace.h>

#include "libuminati.h"

char init_dbg_and_attach_process(um_data** dbg, int pid, char* program_location);













#endif
