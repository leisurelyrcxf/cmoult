#ifndef MANAGER_H
#define MANAGER_H

#include <pthread.h>
#include <unistd.h>
#include <sys/ptrace.h>
#include <sys/wait.h>
#include <sys/queue.h>
#include <dlfcn.h>
#include "common.h"
#include "update.h"

#define MANAGER_SLEEP 5
#define MIN_ARRAY_SIZE 32
#define MANAGER_REGSITER_MIN_SIZE 10
#define MAN_LOCK(x) (&(x->lock))


/*Common*/

/* Update queue of managers */

typedef STAILQ_HEAD(queuehead,update_q) update_queue_t; 
struct update_q {
  char * update;
  STAILQ_ENTRY(update_q) updates;
};

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
  update_queue_t* updates;
  int nupdate;
  char * current_update;
  update_state state;
  int tried;
  bool alive;
  pthread_t thread;
  pthread_mutex_t lock;
} manager;


/* general manager functions */

void init_update_queue(manager * man);
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


#endif /* End ifndef MANAGER_H */
