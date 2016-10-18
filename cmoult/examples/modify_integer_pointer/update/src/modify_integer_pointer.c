/* safe_redefine_update.c This file is part of Cymoult */
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
#include <pthread.h>
#include "variables.h"

pthread_t thread_array[] = {$thread_array_elements$};
pthread_t* threads = &thread_array[0];
int nthreads = sizeof(thread_array)/sizeof(thread_array[0]);
char* name = "modify_integer_pointer";

const int max_tries = 10;

const int new_size = 20;
int new_int_array[20] = {0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19};
int pid = $update_process_pid$;

um_data* dbg;

req_ans check_requirements(){
  return yes;
}

char preupdate_setup(){
  char *program_location = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
  sprintf(program_location, "%s/%s", $program_directory$, $program_name$);
  printf("program location is: \"%s\"\n", program_location);

  
  //  printf("Loading code from %s\n", $new_code_path$);
  //  printf("Loading returned %d\n", um_load_code(dbg, $new_code_path$));
  return init_dbg_and_attach_process(&dbg, pid, program_location);
}


char wait_alterability(){
  return um_wait_out_of_stack(dbg, "print_int_array") == 0;
}

//
//void clean_failed_alterability(){
//
//}

void apply(){
  uint64_t addr = um_get_var_addr(dbg, true, "p_int_array", "main");
  if(addr == (uint64_t)-1 || addr == 0){
    fprintf(stderr, "can't get address of p_int_array\n");
    return;
  }else{
    addr = um_set_pointer_to_values(dbg, addr, 10*sizeof(int), new_int_array, 20*sizeof(int), AUTO_REALLOC);
    if(addr == (uint64_t)-1){
      fprintf(stderr, "failed to write p_int_array\n");
      return;
    }
  }
  addr = um_get_var_addr(dbg, true, "size", "main");
  if(addr == (uint64_t)-1 || addr == 0){
    fprintf(stderr, "can't get address of size\n");
    return;
  }else{
    if(um_set_addr(dbg, addr, 20, sizeof(int)) != 0){
      fprintf(stderr, "failed to write size\n");
      return;
    }
  }
}

//void preresume_setup(){}
//char wait_over(){}
//char check_over(){}

void cleanup(){
  um_detach(pid);
  printf("Detached from %d\n",pid);
}

