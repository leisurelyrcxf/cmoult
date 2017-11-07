#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include "lowlevel.h"

void __attribute__ ((noinline)) func1(){
  printf("func1()\n");
}

void __attribute__ ((noinline)) func2(){
  printf("func2()\n");
}

int main(){
  pre_setup_static_update_point();
  while(1){
    func1();
    sleep(10);
    static_update_point(60); //timeout 60s
  }
  return 0;
}
