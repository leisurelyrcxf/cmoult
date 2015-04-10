#include<stdio.h>
#include<stdlib.h>
#include<unistd.h>

int a;

void not_in_stack(int* b) {
    *b++;
}

void sleep_and_print(int* i) {
    sleep(1);
		printf("i = %d\n", *i);
}

void sleep_and_print_2(int* i) {
    sleep(1);
		printf("i is %d\n", *i);
}

void ancien_main(int n){
	int i=0;
	while(1){
    sleep_and_print(&i);
		i+=n;
    if (i == 42)
        printf("a = %d\n", a);
    not_in_stack(&a);
	}
}

void main(){
  int n = 2;
  a = 0;
  ancien_main(n);
}

