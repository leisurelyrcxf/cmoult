/* dsuthread.c This file is part of Cymoult */
/* Copyright (C) 2015 Sébastien Martinez, Fabien Dagnat, Jérémy Buisson */

/* This program is free software; you can redistribute it and/or modify */
/* it under the terms of the GNU General Public License as published by */
/* the Free Software Foundation; either version 2 of the License, or */
/* (at your option) any later version. */

/* This program is distributed in the hope that it will be useful, */
/* but WITHOUT ANY WARRANTY; without even the implied warranty of */
/* MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the */
/* GNU General Public License for more details. */

/* You should have received a copy of the GNU General Public License along */
/* with this program; if not, write to the Free Software Foundation, Inc., */
/* 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA. */

/*

DSU thread

 */

#include "dsuthread.h"


static void * dsu_thread_main(void * arg){
  dsuthread * dthread = (dsuthread *) arg;
  dthread->pid = syscall(SYS_gettid);
  return dthread->main(dthread->thread_args);
}

dsuthread * dsuthread_create(const pthread_attr_t *attr, void *(*main)(void* targs), void * args){
  dsuthread * dthread = malloc(sizeof(dsuthread));
  pthread_t thread;
  dthread->thread = &thread;
  dthread->thread_args = args;
  dthread->main = main;
  pthread_create(&thread,attr,&dsu_thread_main,(void*) dthread);
  return dthread;
}

