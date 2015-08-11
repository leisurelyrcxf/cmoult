#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>
#include <dlfcn.h>
#include <libconfig.h>
#include "common.h"

#define LISTENER_BUFF_SIZE 1024
#define LISTENER_PORT 4242
#define LISTENER_MAX_CONN 10
#define UPDATE_KEYWORD "update "

/*Socket listener*/
void start_socket_listener();
void stop_socket_listener();
pthread_t * access_socket_listener();

/*Common*/

/*Thread spawning*/
void extract_library_name(const char* str, char** libpath);
void load_update(char* path);
