/** 
  This manager knows the PID of the program to update. It is waiting for a SIGUSR1 signal, which is a trigger from the developper who wants to do an update.
  Once trigger is activated, the manager is looking for update files in the /dynamic_updates repository of the program to update.
 */

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

char *program_update_directory;
char *program_name;
char *program_directory;
pid_t pid;
int update_state;

/*TODO: NEED TO BE TESTED WITH A NEW TEST PROG THAT FIND A FUNC IN STACK
Only replacing functions by functions_v2 */
int update_func(um_data* dbg,um_frame* stack,char* fname){
	if (um_unwind (dbg, fname, &stack)){
		printf("Found %s on the stack!\n",fname);
		//Detach manager
		um_detach(pid);
		sleep(10);
		int res,fail;
		//Attach manager
		fail=um_attach(pid);
		if( fail != 0 ){
			perror("ptrace");
			return 1;
		}
		printf("Attaching on %d\n", pid);	
		res = waitpid(pid,NULL,0);
		if(res != pid){
			printf("Unexpected wait result res %d",res);
			return 2;
		}
		printf("Attached on %d\n",res);
		return update_func(dbg,stack,fname);
	}
	else{
		printf("Did not find %s on the stack!\n",fname);
		char* fakename = malloc(128*sizeof(char));
		memset(fakename,0,128);
		sprintf(fakename,"%s_v2",fname);
		um_safe_redefine(dbg, fname, fakename);
	}
	return 0;
}

//TODO ? Add state to know that we are already updating (just in case several signal sent at the same time)
int update_safe(char* dname){
	int res,fail;
	//Attach manager
	fail=um_attach(pid);
	if(fail != 0){
		perror("ptrace");
		return 1;
	}
	printf("Attaching on %d\n", pid);	
	res = waitpid(pid,NULL,0);
	if(res != pid){
		printf("Unexpected wait result res %d",res);
		return 2;
	}
	printf("Attached on %d\n",res);
	/***** ALLOCATING DEBUG DATA *****/
	char *program_location = malloc(512*sizeof(char));
	sprintf(program_location, "%s/%s",program_directory,program_name);
	um_data* dbg;
	if ((fail = um_init(&dbg, pid, program_location)) != 0)
	{
		fprintf(stderr, "Could not fill out debug info for %s, error code %d\n", program_name, fail);
		return 3;
	}
	/***** STACK UNWINDING *****/
	um_frame* stack;
	um_unwind (dbg, NULL, &stack);
	/***** CHECKING FOR FUNCTIONS IN STACK AND REDEFINITION *****/
	int upd_fail;
	if ( (upd_fail=update_func(dbg,stack,"not_in_stack")) > 0 )
		return upd_fail;

	/***** EXITING *****/
	um_destroy_stack(stack);
	um_end(dbg);

	//Detach manager
	um_detach(pid);
	printf("Detached from %d\n",pid);
	
	//Delete Update File when over
	char *update_file_path = malloc(512*sizeof(char));
	sprintf(update_file_path, "%s/%s",program_update_directory,dname);
	int rem_upd = remove(update_file_path);
	if(rem_upd != 0){
		printf("Could not delete update file %s \n",dname);
		return 4;
	}
	else{
		printf("Update file %s deleted \n",dname);
	}
	return 0;
}
//SIGUSR1 handler : On signal, launch update
void update_signal_handler(int signum){
	if(update_state != 1){
		update_state = 1;
		//Check for update files
		DIR* dp = opendir(program_update_directory);
		if( dp == NULL ){
			update_state = 0;
			printf("Error while opening the directory %s\n",program_update_directory);
			return;
		}
		struct dirent* dir_infos;
		while( ( dir_infos = readdir(dp) ) ){
			if( ( strcmp(dir_infos->d_name,".") != 0 ) && ( strcmp(dir_infos->d_name,"..") != 0 )){
				printf("%s is available for update\n", dir_infos->d_name);
				if(update_safe(dir_infos->d_name)>0){
					return;
				}else{
					printf("%s has been successfully updated\n",dir_infos->d_name);
				}
			}
		}
		if( closedir(dp) < 0 ){
			printf("Error while closing the directory %s\n",program_update_directory);
			return;
		}
		printf("Update SUCCESS \n");
		update_state = 0;
	}
	signal(SIGUSR1, &update_signal_handler);
}

int main (int argc, char **argv){
	//Args checking
	if(argc != 2){
		printf("Usage : ./%s [PID of the program to dynamically update]\n",argv[0]);
		exit(EXIT_FAILURE);
	}

	update_state = 0;

	//Get program infos to know the update repository
	pid = atoi(argv[1]);
	FILE* program_fp;
	char program_info_file[24]; //Considering that pid won't be too big

	//cmd working directory
	sprintf(program_info_file, "/proc/%s/cwd",argv[1]);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("Error while opening the file working directory\n");
		exit(EXIT_FAILURE);
	}
	size_t program_cmd_read;
	char* program_cmd_dir = malloc(512*sizeof(char));
	memset(program_cmd_dir,0,512);
	program_cmd_read = readlink(program_info_file,program_cmd_dir,512);
	if(!program_cmd_read){
		printf("Error while reading the file working directory\n");
		exit(EXIT_FAILURE);
	}
	fclose(program_fp);
	printf("The cmd working directory is : %s\n", program_cmd_dir);

	//cmd
	sprintf(program_info_file, "/proc/%s/cmdline",argv[1]);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("Error while opening the cmd file\n");
		exit(EXIT_FAILURE);
	}
	char* program_cmd = malloc(512*sizeof(char));
	memset(program_cmd,0,512);
	if(fscanf(program_fp,"%s",program_cmd) == 0){
		printf("Error while reading the cmd file\n");
		exit(EXIT_FAILURE);
	}
	fclose(program_fp);	
	printf("The cmd is : %s\n", program_cmd);

	//file name
	sprintf(program_info_file, "/proc/%s/comm",argv[1]);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("Error while opening the file name\n");
		exit(EXIT_FAILURE);
	}
	program_name = malloc(128*sizeof(char));
	memset(program_name,0,128);
	if(fscanf(program_fp,"%s",program_name) == 0){
		printf("Error while reading the file name\n");
		exit(EXIT_FAILURE);
	}
	fclose(program_fp);
	printf("The file name is : %s\n", program_name);

	//file repository
	program_directory = malloc(512*sizeof(char));
	sprintf(program_directory,"%s/%s",program_cmd_dir,program_cmd);
	int name_len = strlen(program_name);
	int dir_len = strlen(program_directory);
	program_directory[dir_len-name_len-1]='\0';
	printf("File repository : %s\n",program_directory);
	
	//dsu repository
	program_update_directory = malloc(512*sizeof(char));
	memset(program_update_directory,0,512);
	sprintf(program_update_directory,"%s/dynamic_updates",program_directory);

	//Register signal to listen while waiting for an update.
	signal(SIGUSR1, &update_signal_handler);
	while(1){
		sleep(1000);
	}
}
