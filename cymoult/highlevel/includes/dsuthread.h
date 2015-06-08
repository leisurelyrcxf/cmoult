#ifndef DSUTHREAD_H
#define DSUTHREAD_H

#include <pthread.h>
#include <unistd.h>
#include <setjmp.h>

#define DSUTHREAD_SLEEP 1


typedef enum ti{
  reboot,
  suspend,
  resume,
  nothing
} thread_interupt;


typedef struct dsuthread{
  pthread_t * thread;
  void * thread_args;
  void *(*main)(void *args) main;
  thread_interupt tsignal;
} dsuthread;

dsuthread * dsuthread_create(const pthread_attr_t *attr, void* (*main)(void* targs), void * args);
void pause_thread(dsuthread thread);
void resume_thread(dsuthread thread);








#endif /* End ifndef DSUTHREAD_H */
