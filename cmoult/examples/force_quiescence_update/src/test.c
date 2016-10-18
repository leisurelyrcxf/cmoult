#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>



void func1(){
  printf("func1()\n");
}

void func2(){
  printf("func2()\n");
}

int main(){
  while(1){
    func1();
    sleep(1);
  }
  return 0;
}
