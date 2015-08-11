#include "manager.h"
#include <dlfcn.h>

static void queue_push(char *** queue, char * item, int * size, int * back, int * front){
  //Detect if the queue is full. It is full if the front is at 0 and back is at size - 1
  //It is also full if back is at front -1
  if (((*front) == 0) && ((*back) == (*size) -1)){
    (*size) = (*size)*2;
    (*queue) = (char**) realloc((*queue),(*size)*sizeof(size_t));
  }else if ((*front - *back) == 1){
    //Bad luck! We have to flatten the queue
    int newsize = (*size)*2;
    char ** tmp = (char**) malloc(newsize*2*sizeof(size_t));
    int i = 0;
    int f = *front;
    int b = *back;
    while (f != b+1){
      tmp[i] = (*queue)[f];
      f = (f+1) % (*size);
      i++;
    }
    *front = 0;
    *back = (i-1);
    *size = newsize;
    free(*queue);
    queue = &tmp;
  }
  (*back) = ((*back)+1) % (*size);
  (*queue)[(*back)] = item;
}

static char * queue_pop(char ** queue, int * queue_front, const int size){
  char * item = queue[(*queue_front)];
  (*queue_front) = ((*queue_front) +1) % size;
  return item;
}

static void pop_update(manager * man){
  char * module = queue_pop(man->updates,&(man->front_update),man->update_array_size);
  free(module);
}

static char load_from_module(manager * man, void * handle,const char * symbol, const char* module, void ** pointer){
  (* pointer) = dlsym(handle,symbol);
  char * error = dlerror();
  if (error != NULL){
    cmoult_log(1,"Error when looking up symbol %s in %s : %s",symbol,module,error);
    pop_update(man);
    return 0;
  }
  return 1;
}

void * load_next_update(manager * man, update_functions * upd, pthread_t ** threads, int * nthreads, int * max_tries, char** name){
  if ((man->state == not_updating) && (man->front_update >= 0)){
    char * module = man->updates[man->front_update];
    void * handle = dlopen(module,RTLD_LAZY);
    char * message = malloc(2048*sizeof(char)); //For potential errors
    if (handle == NULL){
      //An error happened when loading
      char * error = dlerror();
      cmoult_log(1,"Error when loading script %s : %s. Aborting",module,error);
      //Remove that script from the list
      pop_update(man);
    }else{
      dlerror();
      char ok = 1;
      ok = ok && load_from_module(man,handle,"threads",module, (void**) &threads);      
      ok = ok && load_from_module(man,handle,"nthreads",module, (void**) &nthreads);      
      ok = ok && load_from_module(man,handle,"max_tries",module, (void**) &max_tries);      
      ok = ok && load_from_module(man,handle,"name",module, (void**) &name);      
      //Load functions
      ok = ok && load_from_module(man,handle,"check_requirements",module, (void**) upd->check_requirements);      
      ok = ok && load_from_module(man,handle,"preupdate_setup",module, (void**) upd->preupdate_setup);
      ok = ok && load_from_module(man,handle,"check_alterability",module, (void**) upd->check_alterability);
      ok = ok && load_from_module(man,handle,"wait_alterability",module, (void**) upd->wait_alterability);
      ok = ok && load_from_module(man,handle,"clean_failed_alterability",module, (void**) upd->clean_failed_alterability);
      ok = ok && load_from_module(man,handle,"apply",module, (void**) upd->apply);
      ok = ok && load_from_module(man,handle,"preresume_setup",module, (void**) upd->preresume_setup);
      ok = ok && load_from_module(man,handle,"wait_over",module, (void**) upd->wait_over);
      ok = ok && load_from_module(man,handle,"check_over",module, (void**) upd->check_over);
      ok = ok && load_from_module(man,handle,"cleanup",module, (void**) upd->cleanup);
      if (ok){
        man->state = checking_requirements;
      }else{
        cmoult_log(1,"Error when loading symbols from %s. Aborting",module);
        pop_update(man);
      }
    }
    return handle;
  }
  return NULL;
}

void postpone_update(manager * man){
  char * update = queue_pop(man->updates,&(man->front_update),man->update_array_size);
  manager_add_update(man,update);
  man->state = not_updating;
}

void abort_update(manager *man){
  man->state = not_updating;
  pop_update(man);
}

void finish_update(manager* man){
  /* TODO : log the update */
  man->state = not_updating;
  pop_update(man);
}

void manager_add_update(manager * man, char * update){
  queue_push(&(man->updates),update,&(man->update_array_size),&(man->back_update),&(man->front_update));
}


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







