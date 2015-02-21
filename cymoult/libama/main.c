#include "libama.h"

int main (int argc, char **argv){
	//Args checking
	if(argc != 2){
		printf("Usage : ./%s [PID of the program to dynamically update]\n",argv[0]);
		exit(EXIT_FAILURE);
	}
	//Infos loading
	ama_program_infos pi;
	set_program_infos_from_pid(&pi,atoi(argv[1]));
	printf("%d\n",pi.program_pid);
	printf("%s\n",pi.program_name);
	printf("%s\n",pi.program_directory);
}
