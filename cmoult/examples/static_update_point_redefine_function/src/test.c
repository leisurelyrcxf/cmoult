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

int manager_pid = 0;

int main(){
  pre_setup_static_update_point();
  while(1){
    static_update_point();
    func1();
    sleep(1);
  }
  return 0;
}
