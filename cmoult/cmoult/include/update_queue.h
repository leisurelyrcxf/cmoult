#ifndef UPDATE_QUEUE_H
#define UPDATE_QUEUE_H

#include <stdlib.h>

typedef struct update_q {
  char * update;
  struct update_q* next;
}update_queue_element;

typedef struct update_queue{
  update_queue_element* first;
  update_queue_element* last;
}update_queue_t;


void init_queue(update_queue_t* queue);

void insert_queue(update_queue_t* queue, update_queue_element* element);

update_queue_element* pop_out_queue(update_queue_t* queue);


#endif
