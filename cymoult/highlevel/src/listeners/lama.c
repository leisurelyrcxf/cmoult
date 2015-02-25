#include <stdio.h>

__attribute__((__constructor__)) void update_func(){

  puts("Hello world!");

}


