#include "manager.h"


update* pop_update(ll_updates **ll){
  ll_updates * item = *ll;
  ll_updates * item2;
  update * res;
  if (item == NULL){
    return NULL;
  }
  item2 = item->next;
  if (item2 == NULL){
    /*single element*/
    res = item->update;
    free(item);
    (*ll) = NULL;
  }else{
    while(item2->next != NULL){
      item = item2;
      item2 = item->next;
    }
    item->next = NULL;
    res = item2->update;
    free(item2);
  }
  return res;
}

void push_update(ll_updates **ll,update *upd){
  ll_updates * new = malloc(sizeof(ll_updates));
  new->update = upd;
  new->next = (*ll);
  (*ll) = new;
}


void manager_add_update(manager* man, update* upd){
  push_update(&(man->updates),upd);
}

void get_next_update(manager * man){
  if (man->state == not_updating){
    update * next_update = pop_update(&(man->updates));
    if (next_update != NULL){
      man->current_update = next_update;
      man->state = checking_requirements;
    }
    
  }
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





