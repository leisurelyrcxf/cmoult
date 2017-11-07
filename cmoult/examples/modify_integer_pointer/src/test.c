#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>

int array_for_test[10] = {1,2,3,4,5,6,7,8,9,10};

void print_int_array(int* p, size_t size){
  for(size_t i = 0; i < size; i++){
    printf("%d", p[i]);
    printf(",");
  }
  printf("\n");
}



int main(){
  int* p_int_array = array_for_test;
  const size_t size = 10;
  do{
    print_int_array(p_int_array, size);
    sleep(1);
  }while(1);
  return 0;
}
