#include <pthread.h>
#include <unistd.h>
#include "update.h"

#define MANAGER_SLEEP 5


/*Common*/

/*List of updates*/

typedef struct ll_updates{
  update * update;
  struct ll_updates * next;
} ll_updates;

update* pop_update(ll_updates **ll);
void push_update(ll_updates **ll,update* upd);



/*Threaded Manager*/

typedef struct{
  pthread_t * thread;
  ll_updates * updates;
  update * current_update;
  char alive;
} threaded_manager;

void add_update_threaded_manager(threaded_manager * tmanager, update * upd);
threaded_manager * start_threaded_manager();
threaded_manager * request_threaded_manager();


/*Non Threaded Manager*/

typedef struct{
  ll_updates * updates;
  update * current_update;
} manager;

void add_update_manager(manager * ntmanager, update * upd);
manager * start_manager();
void call_manager(manager * ntmanager);
manager * request_manager();


