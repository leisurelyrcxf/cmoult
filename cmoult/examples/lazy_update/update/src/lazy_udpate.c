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

int pid = $update_process_pid$;

um_data* dbg;

//test for modify struct structure
typedef struct _person{
  int age;
  char* name;
  char sex;
}person;

int update_person(um_data* dbg, void* p, size_t len){
  person* ppperson = (person*)p;
  ppperson->age = 33;
  ppperson->sex = 'm';
  uint64_t retval = um_write_str(dbg, (uint64_t)(ppperson->name), "Sebastien", AUTO_REALLOC);
  if(retval == 0 || retval == (uint64_t)-1){
    return -1;
  }
  ppperson->name = (char*)retval;
  return 0;
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
  return um_wait_var_access(dbg, true, "*person", "main", sizeof(person)) == 0;
}

//
//void clean_failed_alterability(){
//
//}

void apply(){
//  uint64_t addr = um_get_var_addr(dbg, true, "*person", "main");
//  size_t len = sizeof(person);
//  void* buffer = malloc(len);
//  if(um_memcpy(dbg, (uint64_t)buffer, addr, len, MEMCPY_REMOTE_TO_LOCAL) != 0){
//    free(buffer);
//    return;
//  }
//  if(update_person(dbg, buffer, len) != 0){
//    free(buffer);
//    return;
//  }
//  if(um_memcpy(dbg, addr, (uint64_t)buffer, len, MEMCPY_LOCAL_TO_REMOTE) != 0){
//    free(buffer);
//    return;
//  }
//  free(buffer);

  sleep(5);


//  um_lazy_update_variable(dbg, true, "*person", "main", sizeof(person), update_person);
}

//void preresume_setup(){}
//char wait_over(){}
//char check_over(){}

void cleanup(){
  uint64_t addr = um_get_var_addr(dbg, true, "*person", "main");
  cleanup_watchpoint(dbg, addr, sizeof(person), WP_TRAP_COND_DATA_ACCESS);
  um_detach(pid);
  printf("Detached from %d\n",pid);
}

