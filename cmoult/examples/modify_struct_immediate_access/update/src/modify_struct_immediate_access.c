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

typedef struct _person_v2{
  int age;
  char* name;
  char sex;
  char* comment;
}person_v2;

int transform_person_to_person_v2(um_data* dbg, void * p1, void * p2, int flag){
  person* person1 = (person*)p1;
  person_v2* person2 = (person_v2*)p2;
  person2->age = person1->age;
  person2->name = person1->name;
  //  person2->name = (char*)um_write_str(dbg, (uint64_t)(person2->name), "Sebastien", flag); //modify person name
  person2->sex = person1->sex;
  person2->comment = NULL;


  char* old_name = malloc(1024);
  um_read_str_at_address(dbg, (uint64_t)(person2->name), old_name, 1024);
  char* comment = malloc(1024);
  sprintf(comment, "name: %s, age: %d, sex: %c", old_name, person2->age, person2->sex);
  free(old_name);

  person2->comment = (char*)um_write_str(dbg, (uint64_t)0, comment, flag);
  free(comment);
  return 0;
}

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
  return um_wait_out_of_stack(dbg, "print_person") == 0;
}

//
//void clean_failed_alterability(){
//
//}

void apply(){
  uint64_t addr = um_get_var_addr(dbg, true, "*person", "main");
  if(addr == (uint64_t)-1 || addr == 0){
    fprintf(stderr, "can't get address of *person\n");
    return;
  }

  /*modify person variable*/
  um_set_addr(dbg, (addr + offsetof(person, age)), 30, 4);
  um_set_str_pointer(dbg, (addr + offsetof(person, name)), "Sebastien", AUTO_REALLOC);
  um_set_addr(dbg, (addr + offsetof(person, sex)), 'f', 1);


  addr = um_get_var_addr(dbg, true, "person", "main");
  if(addr == (uint64_t)-1 || addr == 0){
    fprintf(stderr, "can't get address of person\n");
    return;
  }


  /*transfrom person from struct person to struct person_v2*/
  um_transform_struct_pointer(dbg, addr, sizeof(person), sizeof(person_v2), &transform_person_to_person_v2, AUTO_REALLOC);
  um_redefine(dbg, "print_person", "print_person_v2");
}

//void preresume_setup(){}
//char wait_over(){}
//char check_over(){}

void cleanup(){
  um_detach(pid);
  printf("Detached from %d\n",pid);
}

