#include "update_queue.h"

void init_queue(update_queue_t* queue){
  queue->first = NULL;
  queue->last = NULL;
}

void insert_queue(update_queue_t* queue, update_queue_element* element){
  element->next = NULL;
  if(queue->last == NULL){
    queue->first = element;
    queue->last = element;
  }else{
    queue->last->next = element;
    queue->last = element;
  }
}

update_queue_element* pop_out_queue(update_queue_t* queue){
  update_queue_element* head = queue->first;
  if(head != NULL)
    queue->first = head->next;
  if(queue->first == NULL){
    queue->last = NULL;
  }
  return head;
}
