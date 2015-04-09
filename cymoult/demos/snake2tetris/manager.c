#include "../../libama/libama.h"

//Infos structures
ama_program_infos pi;
ama_update_infos ui;

//Functions to update
char *functions_to_update[1] = {"getDirection"};
char *new_functions_to_update[1] = {"getDirectionTetris"};

void update_signal_handler(int signum){
	if (ama_check_updates_from_repository(&pi,&ui))
		exit(EXIT_FAILURE);
	signal(SIGUSR1, &update_signal_handler);
}

int main (int argc, char **argv){
	//Args checking
	if(argc != 2){
		printf("Usage : ./%s [PID of the program to dynamically update]\n",argv[0]);
		exit(EXIT_FAILURE);
	}

	//Infos init
	ama_init_program_infos_from_pid(&pi,atoi(argv[1]));
	ama_init_update_infos_from_program_infos(&ui,&pi);
	ama_set_update_functions_list(&ui,functions_to_update,new_functions_to_update,1);	

	//Register signal to listen while waiting for an update.
	signal(SIGUSR1, &update_signal_handler);
	while(1){
		sleep(1000);
	}
}
