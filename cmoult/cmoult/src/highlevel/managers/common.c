#include "manager.h"
#include <stdio.h>


/* Managers storage */

manager ** managers;
char ** manager_names; 
int nmanagers = 0;
int managers_size = 0;
pthread_mutex_t register_lock;

//man queue for manual
void init_update_queue(manager * man){
  pthread_mutex_lock(MAN_LOCK(man));
  update_queue_t* queue = (update_queue_t*)malloc(sizeof(update_queue_t));
  init_queue(queue);
  man->updates = queue;
  man->nupdate = 0;
  man->current_update = NULL;
  pthread_mutex_unlock(MAN_LOCK(man));
}

static void push_update(manager * man, char * update){
  update_queue_element * u = malloc(sizeof(update_queue_element));
  char* buff = malloc(sizeof(char) * (strlen(update) + 1));
  strcpy(buff, update);
  u->update = buff;
  man->nupdate++;
  insert_queue(man->updates,u);
}

static void pop_update(manager * man){
  update_queue_element * u;
  char * update;
  u = pop_out_queue(man->updates);
//  printf("update file \"%s\"\n",u->update);
  man->current_update = u;
  man->nupdate--;
}

void postpone_update(manager * man){
  pthread_mutex_lock(MAN_LOCK(man));
  push_update(man,man->current_update->update);
  free(man->current_update->update);
  free(man->current_update);
  man->state = not_updating;
  pthread_mutex_unlock(MAN_LOCK(man));
}

void abort_update(manager *man){
  pthread_mutex_lock(MAN_LOCK(man));
  man->state = not_updating;
  free(man->current_update->update);
  free(man->current_update);
  man->current_update = NULL;
  pthread_mutex_unlock(MAN_LOCK(man));
}

void finish_update(manager* man){
  /* TODO : log the update */
  pthread_mutex_lock(MAN_LOCK(man));
  man->state = not_updating;
  free(man->current_update->update);
  free(man->current_update);
  man->current_update = NULL;
  pthread_mutex_unlock(MAN_LOCK(man));
}

void manager_add_update(manager * man, char * update){
  pthread_mutex_lock(MAN_LOCK(man));
  push_update(man,update);
  pthread_mutex_unlock(MAN_LOCK(man));
}

/* Life-cycle bases */

static char load_from_module(manager * man, void * handle,const char * symbol, const char* module, void ** pointer, void * default_value){
  (* pointer) = dlsym(handle,symbol);
  char * error = dlerror();
  if (error != NULL){
    if ((strstr(error,"undefined symbol") != NULL) && (default_value != NULL)){
      (* pointer) = default_value;
      cmoult_log(2,"Symbol %s not found in %s, using default value instead",symbol,module);
      (*pointer) = default_value;
    }else{
      cmoult_log(1,"Error when looking up symbol \"%s\" in \"%s\", error: \"%s\"",symbol,module,error);
      return 0;
    }
  }
  return 1;
}

void * load_next_update(manager * man, update_functions * upd, pthread_t ** threads, int * nthreads, int * max_tries, char** name){
  pthread_mutex_lock(MAN_LOCK(man));
  if ((man->state == not_updating) && (man->nupdate > 0)){
    pop_update(man);
    char * module = man->current_update->update;
    printf("update module: \"%s\"\n",module);
    void * handle = dlopen(module,RTLD_LAZY);
    if (handle == NULL){
      //An error happened when loading
      char * error = dlerror();
      cmoult_log(1,"Error when loading script %s : %s. Aborting",module,error);
      //Abort the update
      abort_update(man);
    }else{
      dlerror();
      char ok = 1;
      ok = ok && load_from_module(man,handle,"threads",module, (void**) &threads, NULL);      
      ok = ok && load_from_module(man,handle,"nthreads",module, (void**) &nthreads, NULL);      
      ok = ok && load_from_module(man,handle,"max_tries",module, (void**) &max_tries, NULL);      
      ok = ok && load_from_module(man,handle,"name",module, (void**) &name, NULL);      
      //Load functions
      ok = ok && load_from_module(man,handle,"check_requirements",module, (void**) &(upd->check_requirements), &req_ans_empty_step);      
      ok = ok && load_from_module(man,handle,"preupdate_setup",module, (void**) &(upd->preupdate_setup), &char_empty_step);
      ok = ok && load_from_module(man,handle,"check_alterability",module, (void**) &(upd->check_alterability), &char_empty_step);
      ok = ok && load_from_module(man,handle,"wait_alterability",module, (void**) &(upd->wait_alterability), &char_empty_step);
      ok = ok && load_from_module(man,handle,"clean_failed_alterability",module, (void**) &(upd->clean_failed_alterability),&void_empty_step);
      ok = ok && load_from_module(man,handle,"apply",module, (void**) &(upd->apply),&void_empty_step);
      ok = ok && load_from_module(man,handle,"preresume_setup",module, (void**) &(upd->preresume_setup),&void_empty_step);
      ok = ok && load_from_module(man,handle,"wait_over",module, (void**) &(upd->wait_over),&char_empty_step);
      ok = ok && load_from_module(man,handle,"check_over",module, (void**) &(upd->check_over),&char_empty_step);
      ok = ok && load_from_module(man,handle,"cleanup",module, (void**) &(upd->cleanup),&void_empty_step);
      if (ok){
        man->state = checking_requirements;
        cmoult_log(2,"Script %s loaded successfully",name);
      }else{
        cmoult_log(1,"Error when loading symbols from %s. Aborting",module);
        pop_update(man);
      }
    }
    pthread_mutex_unlock(MAN_LOCK(man));
    return handle;
  }
  pthread_mutex_unlock(MAN_LOCK(man));
  return NULL;
}


/* Manager registering */

void register_manager(manager * man){
  pthread_mutex_lock(&register_lock);
  if (managers_size == 0){
    managers = malloc(MANAGER_REGSITER_MIN_SIZE*sizeof(size_t));
    manager_names = malloc(MANAGER_REGSITER_MIN_SIZE*sizeof(size_t));
    managers_size = MANAGER_REGSITER_MIN_SIZE;
  }else if (nmanagers >= (managers_size-1)){
    managers_size *= 2;
    managers = realloc(managers,managers_size*sizeof(size_t));
    manager_names = realloc(manager_names,managers_size*sizeof(size_t));
  }
  manager_names[nmanagers] = man->name;
  managers[nmanagers] = man;
  nmanagers++;
  pthread_mutex_unlock(&register_lock);
}

manager * lookup_manager(const char * request){
  manager * man;
  for (int i=0;i<nmanagers;i++){
    if (strcmp(manager_names[i],request) == 0){
      return managers[i];
    }
    
  }
  return NULL;
}


/* Thread suspension */

static void pause_thread(pthread_t thread){
}

static void resume_thread(pthread_t thread){
}


static void extern_pause_thread(pthread_t thread){
  ptrace(PTRACE_ATTACH, (pid_t) thread, NULL, NULL);
  waitpid((pid_t) thread, NULL, 0);
}

static void extern_resume_thread(pthread_t thread){
  ptrace(PTRACE_DETACH, (pid_t) thread, NULL, NULL);
}


void pause_threads(manager* man, pthread_t * update_threads, int nupdate_threads){
  if (update_threads!=NULL){
    //Update defined its own threads
    for (int i=0;i<nupdate_threads;i++){
      pause_thread(update_threads[i]);
    }
  }else{
    //Using managerthreads
    for (int i=0;i<(man->nthreads);i++){
      pause_thread((man->threads)[i]);
    }
  }
}

void resume_threads(manager* man, pthread_t * update_threads, int nupdate_threads){
  if (update_threads!=NULL){
    //Update defined its own threads
    for (int i=0;i<nupdate_threads;i++){
      resume_thread(update_threads[i]);
    }
  }else{
    //Using managerthreads
    for (int i=0;i<(man->nthreads);i++){
      resume_thread((man->threads)[i]);
    }
  }
}


void extern_pause_threads(manager* man, pthread_t * update_threads, int nupdate_threads){
  if (update_threads!=NULL){
    //Update defined its own threads
    for (int i=0;i<nupdate_threads;i++){
      extern_pause_thread(update_threads[i]);
    }
  }else{
    //Using managerthreads
    for (int i=0;i<(man->nthreads);i++){
      extern_pause_thread((man->threads)[i]);
    }
  }
}

void extern_resume_threads(manager* man, pthread_t * update_threads, int nupdate_threads){
  if (update_threads!=NULL){
    //Update defined its own threads
    for (int i=0;i<nupdate_threads;i++){
      extern_resume_thread(update_threads[i]);
    }
  }else{
    //Using managerthreads
    for (int i=0;i<(man->nthreads);i++){
      extern_resume_thread((man->threads)[i]);
    }
  }
}
