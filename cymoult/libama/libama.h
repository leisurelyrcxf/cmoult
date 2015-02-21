#ifndef LIBAMA
#define LIBAMA

#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>
#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <syscall.h>
#include <dirent.h>
#include <string.h>
#include <sys/ptrace.h>
#include "libuminati.h"

/* String length considering they won't be too big */
#define PROGRAM_PROC_MAXLENGTH 24
#define PROGRAM_NAME_MAXLENGTH 128
#define PROGRAM_DIRECTORY_MAXLENGTH 512

/**
Structures
**/

/* Program infos */
typedef struct ama_program_infos {
	char *program_name;
	char *program_directory;
	pid_t program_pid;
} ama_program_infos;

/* Update infos */
typedef struct ama_update_infos {
	char *program_update_directory;//TODO: To be changed to update_checking --> opaque type ? Cases : directory/socket
	//TODO : update_triggering automatic/manual
	int update_state;
} ama_update_infos;

/**
Data access
**/

/* Get/Set program infos */
int set_program_infos_from_pid(ama_program_infos *pi, pid_t pid);
int get_program_name_from_pid(char **program_name, pid_t pid);
int get_program_directory_from_pid_name(char **program_directory, pid_t pid,char **name);

/* Get/Set update infos */

/* Get/Set update file */

/**
DSU functions
**/

/* Start update */

/* Update a function */

/* Manual triggering */

#endif
