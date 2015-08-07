#include "common.h"
#include <stdio.h>


int main(){
  set_loglevel(2);
  set_logpath("/home/garrik");
  cmoult_log(2,"coucou %s, %d","moi",3);
  set_logpath("/lama");
  cmoult_log(1,"tutu %d",95);
  return 0;
}




