#include "libama.h"

pid_t pid;

//Infos structures
ama_program_infos pi;
ama_update_infos ui;

//Functions to update
char *functions_to_update[1] = {"not_in_stack"};
char *new_functions_to_update[1] = {"not_in_stack_v2"};

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
		//TODO: FIND A BETTER SOLUTION ON HOW TO WAIT THAT CHILD IS CREATED
		sleep(2);
		printf("MANAGER: Manager started \n");
		printf("MANAGER: child pid is %d \n",pid);
		
		//Infos init
		ama_init_program_infos_from_pid(&pi,pid);
		ama_init_update_infos_from_program_infos(&ui,&pi);
		ama_set_update_functions_list(&ui,functions_to_update,new_functions_to_update,1);	
		
		while(1){
			sleep(5);
			if (ama_check_updates_from_repository(&pi,&ui)>0)
				exit(EXIT_FAILURE);
		}
		exit(EXIT_SUCCESS);
	}
}
