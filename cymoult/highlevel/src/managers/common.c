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

