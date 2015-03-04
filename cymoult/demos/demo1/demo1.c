#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int a;

void first(int *c){
	(*c)++;
	printf("a = %d\n",*c);
}

void second(int *c){
	(*c)--;
	printf("a = %d\n",*c);
}

void third(){
	printf("I don't want to do anything with a, I just wait 5 seconds\n");
	sleep(5);
	printf("I have slept !\n");
}

void fourth(int *c){
	(*c)*=2;
	printf("a = %d\n",*c);
}

void function_call(int *b){
	sleep(2);
	third();
}

int main(int argc, char **argv){
	//Args checking
	if(argc != 2){
		printf("Usage : ./%s [Start number]\n",argv[0]);
		exit(EXIT_FAILURE);
	}
	a=atoi(argv[1]);
	printf("a = %d\n",a);
	while(1){
		function_call(&a);
	}
	exit(EXIT_SUCCESS);
}

