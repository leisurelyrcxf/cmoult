#include "libama.h"

/**
Data access
**/

/* Get/Set program infos */
int set_program_infos_from_pid(ama_program_infos *pi, pid_t pid){
	pi->program_pid = pid;
	pi->program_name = malloc(PROGRAM_NAME_MAXLENGTH*sizeof(char));
	pi->program_directory = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	if(get_program_name_from_pid(&pi->program_name,pid)>0)
		return 1;
	if(get_program_directory_from_pid_name(&pi->program_directory,pid,&pi->program_name)>0)
		return 2;
	return 0;
}

int get_program_name_from_pid(char **program_name, pid_t pid){
	FILE* program_fp;
	char program_info_file[PROGRAM_PROC_MAXLENGTH];
	sprintf(program_info_file, "/proc/%d/comm",pid);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("Error while opening the file name\n");
		return 1;
	}
	if(fscanf(program_fp,"%s",*program_name) == 0){
		printf("Error while reading the file name\n");
		return 2;
	}
	fclose(program_fp);
	printf("The file name is : %s\n", *program_name);
	return 0;
}

int get_program_directory_from_pid_name(char **program_directory, pid_t pid,char ** name){
	FILE* program_fp;
	char program_info_file[PROGRAM_PROC_MAXLENGTH];
	//cmd working directory
	sprintf(program_info_file, "/proc/%d/cwd",pid);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("Error while opening the file working directory\n");
		return 1;
	}
	size_t program_cmd_read;
	char* program_cmd_dir = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	program_cmd_read = readlink(program_info_file,program_cmd_dir,PROGRAM_DIRECTORY_MAXLENGTH);
	if(!program_cmd_read){
		printf("Error while reading the file working directory\n");
		return 2;
	}
	fclose(program_fp);
	printf("The cmd working directory is : %s\n", program_cmd_dir);
	//cmd
	sprintf(program_info_file, "/proc/%d/cmdline",pid);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("Error while opening the cmd file\n");
		return 3;
	}
	char* program_cmd = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	if(fscanf(program_fp,"%s",program_cmd) == 0){
		printf("Error while reading the cmd file\n");
		return 4;
	}
	fclose(program_fp);	
	printf("The cmd is : %s\n", program_cmd);
	//file repository
	sprintf(*program_directory,"%s/%s",program_cmd_dir,program_cmd);
	int name_len = strlen(*name);
	int dir_len = strlen(*program_directory);
	(*program_directory)[dir_len-name_len-1]='\0';
	printf("File repository : %s\n",*program_directory);
	return 0;
}

/* Get/Set update infos */

/* Get/Set update file */

/**
DSU functions
**/

/* Start update */

/* Update a function */

/* Manual triggering */
