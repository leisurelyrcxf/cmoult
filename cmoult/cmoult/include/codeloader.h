#include "common.h"
#include <pthread.h>
#include <unistd.h>
#include <dlfcn.h>
#include <sys/ptrace.h>
#include <sys/wait.h>


#define PATH_SIZE 1024


/*Functions*/
void start_code_loader();
void stop_code_loader();
pthread_t * access_code_loader();
