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



void call_manager(manager * self){
  if (self->current_update == NULL){
    self->current_update = pop_update(&(self->updates));
  }
  if (self->current_update != NULL){
    /* If the current update has not been applied */
    if (!(self->current_update->applied)){
      /*Suspend threads to check requirements and alterability */
      //TODO Actually suspend
      if ((*(self->current_update->requirements))()
          && (*(self->current_update->alterability))()){
        /*Apply the update*/
        (*(self->current_update->apply))();
        self->current_update->applied = 1;
      }
      /*Resume the execution*/
      //TODO Actually resume
      
      /* If it the current update has been applied */
    }else{
      /* If the update is over */
      if ((*(self->current_update->over))()){
        free(self->current_update);
        self->current_update = NULL;
        
      }
    }
  }
}


manager * start_manager(){
  manager * ntmanager = malloc(sizeof(manager));
  ntmanager->updates = NULL;
  ntmanager->current_update = NULL;
  return ntmanager;
}

void add_update_manager(manager * ntmanager, update * upd){
  push_update(&(ntmanager->updates),upd); 
}

manager * request_manager(){
  return global_manager;
}
