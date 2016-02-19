#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <libconfig.h>
#include "common.h"
#include "manager.h"

#define LISTENER_BUFF_SIZE 1024
#define LISTENER_PORT 4242
#define LISTENER_MAX_CONN 10

//Keywords for commands
#define SET_STR "set "
#define SET_LEN 4
#define LOGLVL_STR "loglevel "
#define LOGLVL_LEN 8
#define LOGPATH_STR "logpath "
#define LOGPATH_LEN 7
#define UPD_STR "update "
#define UPD_LEN 7

/*Socket listener*/
void start_socket_listener(bool intern);
void stop_socket_listener();
pthread_t * access_socket_listener();

/*Common*/

/*Parsing and running commands*/
void parse_and_run_command(const char* command, bool intern);
