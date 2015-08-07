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

static void * manager_main(void * arg){
  manager * self = (manager*) arg;
  //Current update
  update_functions * current_update = malloc(sizeof(update_functions));
  //Pointers to data of the update
  dsuthread ** update_threads;
  int nupdate_threads;
  int max_tries;
  char * current_update_name;
  //Handle on the loaded script
  void * handle;
  //Life cycle
  while (self->alive){
    sleep(MANAGER_SLEEP);
    handle = load_next_update(self,current_update,&update_threads,&nupdate_threads,&max_tries,&current_update_name);
    if (man->state == checking_requirements){
      req_ans req = man->current_update->check_requirements();
      if (req == yes){
        /* requirements are met */
        man->state = waiting_alterability;
        man->current_update->preupdate_setup();
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
  free(current_update);
}


manager * start_extern_manager(char * name, dsuthread ** threads, int nthreads){
  manager * man = malloc(sizeof(manager));
  pthread_t thread;
  man->thread = &thread;
  man->alive = 1;
  man->name = name;
  man->threads = threads;
  man->nthreads = nthreads;
  man->updates = (char**) malloc(MIN_ARRAY_SIZE*sizeof(size_t));
  man->front_update = -1;
  man->back_update = -1;
  man->update_array_size = MIN_ARRAY_SIZE;
  man->state = not_updating;
  man->tried = 0;
  pthread_create(&thread,NULL,&manager_main,(void*) man);
  return man;
}







