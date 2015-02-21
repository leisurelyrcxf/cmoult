#include "libama.h"

//Infos structures
ama_program_infos pi;
ama_update_infos ui;

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

	//Register signal to listen while waiting for an update.
	signal(SIGUSR1, &update_signal_handler);
	while(1){
		sleep(1000);
	}
}
