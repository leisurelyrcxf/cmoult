#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>



void __attribute__ ((noinline)) func1(){
  printf("func1()\n");
}

void __attribute__ ((noinline)) func2(){
  printf("func2()\n");
}

int main(){
  while(1){
    func1();
  }
  return 0;
}
