/* threaded_manager.c This file is part of Cymoult */
/* Copyright (C) 2013 Sébastien Martinez, Fabien Dagnat, Jérémy Buisson */

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

Threaded Manager.

 */

#include "manager.h"
#include <stdio.h>

threaded_manager * global_threaded_manager;

static void * manager_main(void * arg){
  puts("manager started!");
  threaded_manager * self = (threaded_manager*) arg;
  manager * base = AS_BASE(self);
  while (self->alive){
    sleep(MANAGER_SLEEP);
    get_next_update(base);
    if (base->state == checking_requirements){
      req_ans req = base->current_update->check_requirements();
      if (req == yes){
        /* requirements are met */
        base->state = waiting_alterability;
        base->current_update->preupdate_setup();
        if (base->current_update->wait_alterability()){
          pause_threads(base);
          base->current_update->apply();
          base->state = applied;
          base->current_update->preresume_setup();
          resume_threads(base);
          base->current_update->wait_over();
          base->current_update->cleanup();
          finish_update(base);
        }else{
          base->current_update->clean_failed_alterability();
          postpone_update(base);
          sleep(MANAGER_SLEEP);
        }
      }else if (req = no){
        /* requirements are not met but may be met later */
        postpone_update(base);
        sleep(MANAGER_SLEEP);
      }else{
        /* requirements are not met and never will be */
        abort_update(base);
      }
    }
  }
}


threaded_manager * start_threaded_manager(char * name, dsuthread ** threads, int nthreads){
  threaded_manager * man = malloc(sizeof(threaded_manager));
  pthread_t thread;
  manager * base = AS_BASE(man);
  man->thread = &thread;
  man->alive = 1;
  base->name = name;
  base->threads = threads;
  base->nthreads = nthreads;
  base->updates = NULL;
  base->current_update = NULL;
  base->state = not_updating;
  pthread_create(&thread,NULL,&manager_main,(void*) man);
  global_threaded_manager = man;
  return man;
}

threaded_manager * request_threaded_manager(){
  return global_threaded_manager;
}

