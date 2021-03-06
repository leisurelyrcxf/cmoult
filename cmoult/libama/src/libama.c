#include "libama.h"

/**
Data access
**/

/* Get/Set program infos */
int ama_init_program_infos_from_pid(ama_program_infos *pi, pid_t pid){
	pi->program_pid = pid;
	pi->program_name = malloc(PROGRAM_NAME_MAXLENGTH*sizeof(char));
	pi->program_directory = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	if(ama_get_program_name_from_pid(&pi->program_name,pid)>0)
		return 1;
	if(ama_get_program_directory_from_pid_name(&pi->program_directory,pid,&pi->program_name)>0)
		return 2;
	return 0;
}

int ama_get_program_name_from_pid(char **program_name, pid_t pid){
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
	return 0;
}

int ama_get_program_directory_from_pid_name(char **program_directory, pid_t pid,char ** name){
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
	//TODO : FIX READLINK IMPLICIT DECLARATION
	program_cmd_read = readlink(program_info_file,program_cmd_dir,PROGRAM_DIRECTORY_MAXLENGTH);
	if(!program_cmd_read){
		printf("Error while reading the file working directory\n");
		return 2;
	}
	fclose(program_fp);
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
	//file repository
    if(program_cmd[0] == '/')
            sprintf(*program_directory,"%s",program_cmd);
    else
    	sprintf(*program_directory,"%s/%s",program_cmd_dir,program_cmd);
	int name_len = strlen(*name);
	int dir_len = strlen(*program_directory);
	(*program_directory)[dir_len-name_len-1]='\0';
	return 0;
}

/* Get/Set update infos */
int ama_init_update_infos_from_program_infos(ama_update_infos *ui, ama_program_infos *pi){
	ui->update_state = 0;
	//from a repository by default
	ui->update_directory = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	ama_get_update_directory_from_program_directory_udirname(&ui->update_directory,&pi->program_directory,"dynamic_updates");
	return 0;
}

void ama_get_update_directory_from_program_directory_udirname(char **update_directory, char **program_directory, char *udirname){
	//dsu repository
	sprintf(*update_directory,"%s/%s",*program_directory,udirname);
}

void ama_set_update_functions_list(ama_update_infos *ui, char **functions_list, char **new_functions_list, int list_size){
	ui->update_functions_list_size = list_size;
	ui->update_functions_list = malloc(list_size*sizeof(char*));
	ui->update_new_functions_list = malloc(list_size*sizeof(char*));
	for(int i=0;i<list_size;i++){
		ui->update_functions_list[i]=functions_list[i];
		ui->update_new_functions_list[i]=new_functions_list[i];
	}
}

/* Get/Set update file */
int ama_check_updates_from_repository(ama_program_infos *pi, ama_update_infos *ui){
	if(ui->update_state != 1){
		ui->update_state = 1;
		//Check for update files
		DIR* dp = opendir(ui->update_directory);
		if( dp == NULL ){
			ui->update_state = 0;
			printf("Error while opening the directory %s\n",ui->update_directory);
			return 1;
		}
		struct dirent* dir_infos;
		while( ( dir_infos = readdir(dp) ) ){
			if( ( strcmp(dir_infos->d_name,".") != 0 ) && ( strcmp(dir_infos->d_name,"..") != 0 )){
				printf("%s is available for update\n", dir_infos->d_name);
				if(ama_start_update_from_file(dir_infos->d_name, pi, ui)>0){
					return 2;
				}else{
					printf("%s has been successfully updated\n",dir_infos->d_name);
				}
			}
		}
		if( closedir(dp) < 0 ){
			printf("Error while closing the directory %s\n",ui->update_directory);
			return 3;
		}
		ui->update_state = 0;
	}
	return 0;
}

/**
DSU functions
**/

/* Start update */
int ama_start_update_from_file(char * update_file, ama_program_infos *pi, ama_update_infos *ui){
	int res,fail;
	//Attach manager
	fail=um_attach(pi->program_pid);
	if(fail != 0){
		perror("ptrace");
		return 1;
	}
	printf("Attaching on %d\n", pi->program_pid);
	res = waitpid(pi->program_pid,NULL,0);
	if(res != pi->program_pid){
		printf("Unexpected wait result res %d",res);
		return 2;
	}
	printf("Attached on %d\n",res);
	/***** ALLOCATING DEBUG DATA *****/
	char *program_location = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	sprintf(program_location, "%s/%s",pi->program_directory,pi->program_name);
	um_data* dbg;
	if ((fail = um_init(&dbg, pi->program_pid, program_location)) != 0)
	{
		fprintf(stderr, "Could not fill out debug info for %s, error code %d\n", pi->program_name, fail);
		return 3;
	}
	/***** STACK UNWINDING *****/
	um_frame* stack = NULL;
	um_unwind (dbg, NULL, &stack,0);

	/***** MODIFYING VARIABLES *****/
	//TODO: understand why working on arch and not ubuntu
	/*char test[4]="n=3";
        char* buf = strtok(test, "=");
	printf("var %s\n",buf);
        uint64_t val;
        val = strtoul(strtok(NULL, "="), NULL, 10);
	char *fun = malloc(12*sizeof(char));
	sprintf(fun,"ancien_main");
        printf("changing %s by %d in %s\n",buf,val,fun);
	int errorcode;
	if(errorcode = um_set_variable(dbg, buf, true, fun , val, 4)<0){
		printf("Could not change variable : Error %d\n",errorcode);
		return 4;
	}*/

	/***** LOAD UPDATE *****/
	//TODO: use code injection
	printf("Loading returned %d\n", um_load_code(dbg, "./testprogs/update.so"));

	/***** CHECKING FOR FUNCTIONS IN STACK AND REDEFINITION *****/
	int upd_fail;
	for(int i=0;i<ui->update_functions_list_size;i++){
		if ( (upd_fail=ama_update_function(dbg,stack,i,pi,ui)) > 0 )
			return upd_fail;
	}

	/***** EXITING *****/
	um_destroy_stack(stack);
	um_end(dbg);

	//Detach manager
	um_detach(pi->program_pid);
	printf("Detached from %d\n",pi->program_pid);
	
	//Delete Update File when over
	char *update_file_path = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
	sprintf(update_file_path, "%s/%s",ui->update_directory,update_file);
	int rem_upd = remove(update_file_path);
	if(rem_upd != 0){
		printf("Could not delete update file %s \n",update_file);
		return 4;
	}
	else{
		printf("Update file %s deleted \n",update_file);
	}
	return 0;
}

/* Update a function */
int ama_update_function(um_data* dbg,um_frame* stack,int l,ama_program_infos *pi, ama_update_infos *ui){
	if (um_wait_out_of_stack(dbg, ui->update_functions_list[l]) == 0){
		um_redefine(dbg, ui->update_functions_list[l],ui->update_new_functions_list[l]);
	}
	return 0;
}


