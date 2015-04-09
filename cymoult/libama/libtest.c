#include "libama.h"

int main (int argc, char **argv){
	//Args checking
	if(argc != 2){
		printf("Usage : ./%s [PID of the program to dynamically update]\n",argv[0]);
		exit(EXIT_FAILURE);
	}
	//Infos structures
	ama_program_infos pi;
	ama_update_infos ui;
	
	//Infos loading
	ama_init_program_infos_from_pid(&pi,atoi(argv[1]));
	printf("pid : %d\n",pi.program_pid);
	printf("pname : %s\n",pi.program_name);
	printf("pdir : %s\n",pi.program_directory);

	ama_init_update_infos_from_program_infos(&ui,&pi);
	printf("ustate : %d\n",ui.update_state);
	printf("udir : %s\n",ui.update_directory);
}
