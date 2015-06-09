/* update.c This file is part of Cymoult */
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

Basic update.

 */

#include "update.h"

/* Default empty update functions */


req_ans req_ans_empty_step(){
  return yes;
}

void void_empty_step(){
}

char char_empty_step(){
  return 1;
}


/* Intialize an empty update */

update * create_empty_update(char* name, dsuthread ** threads, int nthreads){
  update * up = malloc(sizeof(update));
  up->name = name;
  up->threads = threads;
  up->nthreads = nthreads;
  up->max_tries = 5;
  up->check_requirements = req_ans_empty_step;
  up->preupdate_setup = void_empty_step;
  up->check_alterability = char_empty_step;
  up->wait_alterability = char_empty_step;
  up->clean_failed_alterability = void_empty_step;
  up->apply = void_empty_step;
  up->preresume_setup = void_empty_step;
  up->wait_over = char_empty_step;
  up->check_over = char_empty_step;
  up->cleanup = void_empty_step;
  up->applied = 0;
}

  
