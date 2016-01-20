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


static void * manager_main(void * arg){
  manager * self = (manager*) arg;
  //Current update
  update_functions * current_update = malloc(sizeof(update_functions));
  //Pointers to data of the update
  pthread_t * update_threads;
  int nupdate_threads;
  int max_tries;
  char * current_update_name;
  //Handle on the loaded script
  void * handle;
  //Life cycle
  while (self->alive){
    sleep(MANAGER_SLEEP);
    handle = load_next_update(self,current_update,&update_threads,&nupdate_threads,&max_tries,&current_update_name);
    if (self->state == checking_requirements){
      req_ans req = current_update->check_requirements();
      if (req == yes){
        /* requirements are met */
        self->state = waiting_alterability;
        current_update->preupdate_setup();
        if (current_update->wait_alterability()){
          pause_threads(self,update_threads,nupdate_threads);
          current_update->apply();
          self->state = applied;
          current_update->preresume_setup();
          extern_resume_threads(self,update_threads,nupdate_threads);
          current_update->wait_over();
          current_update->cleanup();
          finish_update(self);
          dlclose(handle);
        }else{
          current_update->clean_failed_alterability();
          postpone_update(self);
          dlclose(handle);
        }
      }else if (req == no){
        /* requirements are not met but may be met later */
        postpone_update(self);
        dlclose(handle);
      }else{
        /* requirements are not met and never will be */
        abort_update(self);
        dlclose(handle);
      }
    }
  }
}


manager * start_extern_manager(char * name, pthread_t * threads, int nthreads){
  manager * man = malloc(sizeof(manager));
  man->alive = 1;
  man->name = name;
  man->threads = threads;
  man->nthreads = nthreads;
  man->updates = (char**) malloc(MIN_ARRAY_SIZE*sizeof(size_t));
  man->front_update = 0;
  man->nupdate = 0;
  man->update_array_size = MIN_ARRAY_SIZE;
  man->state = not_updating;
  man->tried = 0;
  register_manager(man);
  pthread_create(&(man->thread),NULL,&manager_main,(void*) man);
  return man;
}








