/**
  This manager needs to launch the program through the manager.
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

pid_t pid;
char *program_update_directory;
char *program_name;
char *program_directory;
int update_state;

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
			printf("Unexpected wait result res %d \n",res);
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
void check_update_rep(){
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
}

void getInfos(char *program_cmd,pid_t cid){
	char *cwd = malloc(512*sizeof(char));
	memset(cwd,0,512);
	FILE* program_fp = NULL;
	char program_info_file[24] = {}; //Considering that pid won't be too big
	//prog infos
	program_name = malloc(512*sizeof(char));
	program_directory = malloc(512*sizeof(char));
	cwd = getcwd(NULL,512);
	printf("MANAGER: cwd is %s \n",cwd);
	sprintf(program_directory, "%s/%s",cwd,program_cmd);
	printf("MANAGER: prog cmd is %s \n",program_directory);
	//file name
	sprintf(program_info_file, "/proc/%d/comm",cid);
	program_fp = fopen(program_info_file,"r");
	if(program_fp == NULL){
		printf("MANAGER: Error while opening the file name\n");
		exit(EXIT_FAILURE);
	}
	program_name = malloc(128*sizeof(char));
	memset(program_name,0,128);
	if(fscanf(program_fp,"%s",program_name) == 0){
		printf("MANAGER: Error while reading the file name\n");
		exit(EXIT_FAILURE);
	}
	fclose(program_fp);
	printf("MANAGER: The file name is : %s\n", program_name);
	//file repository
	int name_len = strlen(program_name);
	int dir_len = strlen(program_directory);
	program_directory[dir_len-name_len-1]='\0';
	printf("MANAGER: File repository : %s \n",program_directory);
	
	//dsu repository
	program_update_directory = malloc(512*sizeof(char));
	memset(program_update_directory,0,512);
	sprintf(program_update_directory,"%s/dynamic_updates",program_directory);
	printf("MANAGER: DSU repository : %s \n",program_directory);
}

int main (int argc, char **argv){
	//Args checking
	if(argc < 2){
		printf("Usage : ./%s [program to launch] [args]* \n",argv[0]);
		exit(EXIT_FAILURE);
	}

	int child_exec;
	char *cargv [argc-1];
	pid=fork();
	if(pid<0){
		//Error
		exit(EXIT_FAILURE);
	}else if(pid==0){
		//Child = PROG
		for(int i=1;i<argc;i++){
			cargv[i-1]=argv[i];	
		}
		printf("My pid is : %d and my manager's is : %d \n",getpid(),getppid());
		child_exec = execv(argv[1],cargv);
		if(child_exec == -1){
			printf("Error while launching your program \n");
			exit(EXIT_FAILURE);
		}
	}else{
		//Parent = MANAGER
		//TODO: FIND A SOLUTION ON HOW TO WAIT THAT CHILD IS CREATED
		sleep(2);
		printf("MANAGER: Manager started \n");
		printf("MANAGER: child pid is %d \n",pid);
		getInfos(argv[1],pid);
		update_state = 0;
		while(1){
			sleep(5);
			check_update_rep();
		}
		exit(EXIT_SUCCESS);
	}
}
