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

manager * global_manager;

void manager_apply_next_update(manager * self){
  get_next_update(self);
  if (self->current_update != NULL){
    if (self->state == checking_requirements){
      /* First, check requirements */
      self->tried = 0;
      req_ans req = self->current_update->check_requirements();
      if (req == yes){
        /* requirements are met */
        self->current_update->preupdate_setup();
        self->state = waiting_alterability;
      }else if (req == no){
        /* requirements are not met but may be met later */
        postpone_update(self);
      }else{
        /* requirements are not met and never will be */
        abort_update(self);
      }
    }
    if (self->state == waiting_alterability){
      if (self->current_update->check_alterability()){
        pause_threads(self);
        self->current_update->apply();
        self->current_update->preresume_setup();
        resume_threads(self);
        self->state = applied;
      }else{
        self->tried++;
        if (self->tried >= self->current_update->max_tries){
          self->current_update->clean_failed_alterability();
          postpone_update(self);
        }
      }
    }
    if (self->state == applied){
      if (self->current_update->check_over()){
        self->current_update->cleanup();
        finish_update(self);
      }
    }
  }
}


manager * start_manager(char * name, dsuthread * threads, int nthreads){
  manager * man = malloc(sizeof(manager));
  man->name = name;
  man->threads = threads;
  man->nthreads = nthreads;
  man->updates = NULL;
  man->current_update = NULL;
  man->state = not_updating;
  global_manager = man;
  return man;
}

manager * request_manager(){
  return global_manager;
}
