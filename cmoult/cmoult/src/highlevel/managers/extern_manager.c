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

External Manager.

 */

#include "manager.h"
#include "listener.h"
#include <stdio.h>


const bool intern = false;

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
        printf("update requirements are met, ready to update\n");
        self->state = waiting_alterability;

        if(current_update->preupdate_setup() != 0){
          fprintf(stderr, "couldn't prepare update setup\n");
          postpone_update(self);
          dlclose(handle);
          continue;
        }

        if (current_update->wait_alterability()){
          printf("alterability waited\n");
          if(!intern){
            extern_pause_threads(self, update_threads, nupdate_threads);
          }else{
            pause_threads(self, update_threads, nupdate_threads);
          }
          current_update->apply();
          self->state = applied;
          current_update->preresume_setup();
          extern_resume_threads(self,update_threads,nupdate_threads);
          current_update->wait_over();
          current_update->cleanup();
          finish_update(self);
          dlclose(handle);
        }else{
          fprintf(stderr, "couldn't wait alterability, will clean failed alterablity , update postponed\n");
          current_update->clean_failed_alterability();
          postpone_update(self);
          dlclose(handle);
        }
      }else if (req == no){
        /* requirements are not met but may be met later */
        printf("update will be postponed\n");
        postpone_update(self);
        dlclose(handle);
      }else{
        /* requirements are not met and never will be */
        printf("udpate requirements will never meet, will be aborted\n");
        abort_update(self);
        dlclose(handle);
      }
    }
  }
}


manager * start_extern_manager(char * name){
  manager * man = malloc(sizeof(manager));
  man->alive = true;
  man->name = name;
  man->state = not_updating;
  man->tried = 0;
  init_update_queue(man);
  register_manager(man);
  pthread_create(&(man->thread),NULL,&manager_main,(void*) man);
  return man;
}

int manager_pid;
void main(int argc,char** argv){
  manager_pid = getpid();
  pthread_t manager_thread;
  manager * man = start_extern_manager("manager");
  cmoult_log_init();
  start_socket_listener(intern);
  pthread_join(man->thread,NULL);
  
  /*intend to load cmoult.so, otherwise cmoult_manager won't load cmoult lib*/
  init_dbg_and_attach_process(NULL, -1, NULL);
}
