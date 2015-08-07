#ifndef MANAGER_H
#define MANAGER_H

#include <pthread.h>
#include <unistd.h>
#include "update.h"

#define MANAGER_SLEEP 5
#define MIN_ARRAY_SIZE 32

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
  dsuthread ** threads;
  int nthreads;
  char ** updates;
  int front_update;
  int back_update;
  int update_array_size;
  update_state state;
  int tried;
  char alive;
  pthread_t * thread;
} manager;


/* general manager functions */

void manager_add_update(manager * man, char * update_name, char * update);
void get_next_update(manager * man);
void postpone_update(manager * man);
void abort_update(manager * man);
void finish_update(manager * man);
void pause_threads(manager * man);
void resume_threads(manager * man);
void pause_thread(dsuthread * dthread);
void resume_thread(dsuthread * dthread);


/* threaded manager functions */


threaded_manager * start_threaded_manager(char * name, dsuthread ** threads, int nthreads);
threaded_manager * request_threaded_manager();

/*non threaded manager functions */

manager * start_manager(char * name, dsuthread ** threads, int nthreads);
void manager_apply_next_update(manager * ntmanager);
manager * request_manager();


#endif /* End ifndef MANAGER_H */
