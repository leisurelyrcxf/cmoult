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
#define FUNCTION_NAME_MAXLENGTH 128

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
	char *update_directory;//TODO: To be changed to update_checking --> opaque type ? Cases : directory/socket
	//TODO : update_triggering automatic/manual
	char **update_functions_list;
	char **update_new_functions_list;
	int update_functions_list_size;
	int update_state;
} ama_update_infos;

/**
Data access
**/

/* Get/Set program infos */
int ama_init_program_infos_from_pid(ama_program_infos *pi, pid_t pid);
int ama_get_program_name_from_pid(char **program_name, pid_t pid);
int ama_get_program_directory_from_pid_name(char **program_directory, pid_t pid,char **name);

/* Get/Set update infos */
int ama_init_update_infos_from_program_infos(ama_update_infos *ui, ama_program_infos *pi);
void ama_get_update_directory_from_program_directory_udirname(char **update_directory, char **program_directory, char *udirname);
void ama_set_update_functions_list(ama_update_infos *ui, char **functions_list, char **new_functions_list, int list_size);

/* Get/Set update file */
int ama_check_updates_from_repository(ama_program_infos *pi, ama_update_infos *ui);

/**
DSU functions
**/

/* Start update */
int ama_start_update_from_file(char * update_file, ama_program_infos *pi, ama_update_infos *ui);

/* Update a function */
int ama_update_function(um_data* dbg,um_frame* stack,int l,ama_program_infos *pi, ama_update_infos *ui);

#endif
