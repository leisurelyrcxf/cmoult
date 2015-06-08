#ifndef MANAGER_H
#define MANAGER_H


#include <pthread.h>
#include <unistd.h>
#include "update.h"

#define MANAGER_SLEEP 5
#define AS_BASE(x) (&(x->base))

/*Common*/

/* state of updates */

typedef enum us {
  not_updating,
  checking_requirements,
  waiting_alterability,
  applied
} update_state;

/*List of updates*/

typedef struct ll_updates{
  update * update;
  struct ll_updates * next;
} ll_updates;

update* pop_update(ll_updates **ll);
void push_update(ll_updates **ll,update* upd);

/*Non Threaded Manager (also base to threaded manager)*/

typedef struct{
  char * name;
  dsuthread * threads;
  size_t nthreads;
  ll_updates * updates;
  update * current_update;
  update_state state;
  int tried;
} manager;

/*Threaded Manager*/

typedef struct{
  manager base;
  pthread_t * thread;
  char alive;
} threaded_manager;


/* general manager functions */

void manager_add_update(manager * man, update * upd);
void get_next_update(manager * man);
void postpone_update(manager * man);
void abort_update(manager * man);
void finish_update(manager * man);
void pause_threads(manager * man);
void resume_threads(manager * man);


/* threaded manager functions */


threaded_manager * start_threaded_manager();
threaded_manager * request_threaded_manager();

/*non threaded manager functions */

manager * start_manager();
void manager_apply_next_update(manager * ntmanager);
manager * request_manager();


#endif /* End ifndef MANAGER_H */
