#ifndef MANAGER_H
#define MANAGER_H

#include <pthread.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <dlfcn.h>
#include "common.h"
#include "update.h"

#define MANAGER_SLEEP 5
#define MIN_ARRAY_SIZE 32
#define MANAGER_REGSITER_MIN_SIZE 10
#define MAN_LOCK(x) (&(x->lock))


/*Common*/

/* state of updates */

typedef enum us {
  not_updating,
  checking_requirements,
  waiting_alterability,
  applied
} update_state;

/*Manager data structure*/

typedef struct{
  char * name;
  pthread_t * threads;
  int nthreads;
  char ** updates;
  int front_update;
  int nupdate;
  int update_array_size;
  update_state state;
  int tried;
  char alive;
  pthread_t thread;
  pthread_mutex_t lock;
} manager;


/* general manager functions */

void manager_add_update(manager * man, char * update);
void get_next_update(manager * man);
void postpone_update(manager * man);
void abort_update(manager * man);
void finish_update(manager * man);
void pause_threads(manager * man, pthread_t * update_threads, int nupdate_threads);
void resume_threads(manager * man, pthread_t * update_threads, int nupdate_threads);
void extern_pause_threads(manager * man, pthread_t * update_threads, int nupdate_threads);
void extern_resume_threads(manager * man, pthread_t * update_threads, int nupdate_threads);
void * load_next_update(manager * man, update_functions * upd, pthread_t ** threads, int * nthreads, int * max_tries, char** name);

manager * lookup_manager(const char * request);
void register_manager(manager * man);


/* extern manager */

manager * start_extern_manager(char * name, pthread_t * threads, int nthreads);


/* threaded manager functions */


/* threaded_manager * start_threaded_manager(char * name, dsuthread ** threads, int nthreads); */
/* threaded_manager * request_threaded_manager(); */

/*non threaded manager functions */

/* manager * start_manager(char * name, dsuthread ** threads, int nthreads); */
/* void manager_apply_next_update(manager * ntmanager); */
/* manager * request_manager(); */


#endif /* End ifndef MANAGER_H */
