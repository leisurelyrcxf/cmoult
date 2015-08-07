#include "manager.h"

static void queue_push(char *** queue, const char * item, int * size, int * back, int * front){
  //Detect if the queue is full. It is full if the front is at 0 and back is at size - 1
  //It is also full if back is at front -1
  if ((*front == 0) && (*back == size -1)){
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

static char load_from_module(void * handle,const char * symbol, const char* module, void ** pointer){
  (* pointer) = dlsym(handle,symbol);
  char * error = dlerror();
  if (error != NULL){
    log(1,"Error when looking up symbol %s in %s : %s",symbol,module,error);
    pop_update();
    return 0;
  }
  return 1;
}

void * load_next_update(manager * man, update_functions * upd, dsuthread *** threads, int * nthreads, int * max_tries, char** name){
  if ((man->state == not_updating) && (man->front_update >= 0)){
    char * module = man->updates[man->front_update];
    void * handle = dlopen(module,RTLD_LAZY);
    char * message = malloc(2048*sizeof(char)); //For potential errors
    if (handle == NULL){
      //An error happened when loading
      char * error = dlerror();
      log(1,"Error when loading script %s : %s. Aborting",module,error);
      //Remove that script from the list
      pop_update(man);
    }else{
      dlerror();
      char ok = 1;
      ok = ok && load_from_module(handle,"threads",module, (void**) &threads);      
      ok = ok && load_from_module(handle,"nthreads",module, (void**) &nthreads);      
      ok = ok && load_from_module(handle,"max_tries",module, (void**) &max_tries);      
      ok = ok && load_from_module(handle,"name",module, (void**) &name);      
      //Load functions
      


      
      if (ok){
        man->state = checking_requirements;
      }else{
        log(1,"Error when loading symbols from %s. Aborting",module);
        pop_update(man);
      }
    }
    return handle;
  }
  return NULL;
}

void postpone_update(manager * man){
  manager_add_update(man,man->current_update);
  man->current_update = NULL;
  man->state = not_updating;
}

void abort_update(manager *man){
  man->state = not_updating;
  free(man->current_update);
  man->current_update = NULL;
}

void finish_update(manager* man){
  /* TODO : log the update */
  man->state = not_updating;
  free(man->current_update);
  man->current_update = NULL;
}

void pause_threads(manager* man){
  size_t nthreads = man->current_update->nthreads;
  dsuthread ** threads = man->current_update->threads;
  if (nthreads > 0){
    for (int i=0;i<nthreads;i++){
      pause_thread(threads[i]);
    }
  }else{
    nthreads = man->nthreads;
    threads = man->threads;
    for (int i=0;i<nthreads;i++){
      pause_thread(threads[i]);
    }
  }
}

void resume_threads(manager* man){
  size_t nthreads = man->current_update->nthreads;
  dsuthread ** threads = man->current_update->threads;
  if (nthreads > 0){
    for (int i=0;i<nthreads;i++){
      resume_thread(threads[i]);
    }
  }else{
    nthreads = man->nthreads;
    threads = man->threads;
    for (int i=0;i<nthreads;i++){
      resume_thread(threads[i]);
    }
  }
}


void pause_thread(dsuthread * dthread){
}

void resume_thread(dsuthread * dthread){
}





