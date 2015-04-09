#include <pthread.h>
#include <unistd.h>
#include <stdlib.h>

#define LISTENER_BUFF_SIZE 1024
#define LISTENER_PORT 4242
#define LISTENER_MAX_CONN 10
#define LISTENER_MAX_SPAWNS 512
#define UPDATE_KEYWORD "update "

/*Threaded listener*/
void start_threaded_listener();
void stop_threaded_listener();
pthread_t * access_threaded_listener();

/*Common*/

/* List of threads */
typedef struct ll_spawned{
  pthread_t thread;
  char finished;
  char * libpath;
  struct ll_spawned * next;
} ll_spawned;


/*Thread spawning*/
//void spawn_thread(pthread_t* threads,void** libs,int* nthreads,char* libpath);
void spawn_thread(ll_spawned** threads,char* libpath);
/*Parsing command*/
void extract_library_name(const char* str, char** libpath);
/* Cleaning dead threads*/
void clean_threads(ll_spawned ** threads);
