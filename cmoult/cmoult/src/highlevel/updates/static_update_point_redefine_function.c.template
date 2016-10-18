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
#include "update_common_header.h"

pthread_t thread_array[] = {$thread_array_elements$};
pthread_t* threads = &thread_array[0];
int nthreads = sizeof(thread_array)/sizeof(thread_array[0]);
char* name = "safeRedefineUpdate";

const int max_tries = 10;

const char* old_func_name = $old_function_name$;
const char* new_func_name = $new_function_name$;
int pid = $update_process_pid$;

um_data* dbg;

req_ans check_requirements(){
  return yes;
}

char preupdate_setup(){
  return preupdate_setup_static_update_point(pid);
}


/*wait static update point*/
char wait_alterability(){
  return wait_static_update_point();
//    return  um_wait_out_of_stack(dbg, (char*)old_func_name);
//    return 0;
//  }
}

//
//void clean_failed_alterability(){
//
//}

void apply(){
  char *program_location = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
  sprintf(program_location, "%s/%s", $program_directory$, $program_name$);
  printf("program location is: \"%s\"\n", program_location);
  if(init_dbg_and_attach_process(&dbg, pid, program_location) != 0){
    fprintf(stderr, "failed to update\n");
    fprintf(stderr, "can't redefine function \"%s\" to \"%s\"\n", old_func_name, new_func_name);
    return;
  }

//  um_cont(pid);
  if(um_redefine(dbg, (char*)old_func_name,(char*)new_func_name) != 0){
    printf("can't redefine function \"%s\" to \"%s\"\n", old_func_name, new_func_name);
  }else{
    printf("successfully update function \"%s\" to \"%s\"\n", old_func_name, new_func_name);
  }
}

//void preresume_setup(){}
//char wait_over(){}
//char check_over(){}

void cleanup(){
  cleanup_static_update_point(pid);
}

