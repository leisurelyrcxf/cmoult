#include <stdlib.h>
#include <string.h>
#include <stdbool.h>

#define SLEEP_TIME 5

//Logging

void cmoult_log(const int level,const char* format,...);
void set_loglevel(const int level);
void set_logpath(char* path);
void cmoult_log_init();
