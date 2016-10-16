#include "libama.h"
#include "variables.h"
#include "stdlib.h"
#include "stdio.h"

#include <pthread.h>

typedef struct _struct1{
  int age;
  char* name;
  char sex;
}person;

um_data* dbg;


int modify_struct(void* s1, void** s2, void (*transformer)(void* s1, void *s2)){

}

int _tmain(){

  const int max_tries = 10;

  const char* old_func_name = $old_function_name$;
  const char* new_func_name = $new_function_name$;

  const char * pid_file = "/home/leisurelyrcxf/cmoult/cmoult/libama/pid";
  FILE* file;
  if( (file = fopen(pid_file, "r") ) == NULL){
    fprintf(stderr, "cant' open file \"%s\"\n", pid_file);
    return -1;
  };
  char* buff = malloc(sizeof(char) * 1024);

  if(fgets(buff, 1024, file) == NULL){
    fprintf(stderr, "error while reading\n");
    return -1;
  };

  char* endptr;
  int pid = strtol(buff, &endptr, 10);
  printf("process id is %d\n", pid);

  if(pid <= 0){
    return -1;
  }

  free(buff);

  int res,fail;
  //Attach manager
  fail=um_attach(pid);
  if(fail != 0){
    perror("ptrace");
    return 1;
  }
  printf("Attaching on %d\n", pid);
  res = waitpid(pid,NULL,0);
  if(res != pid){
    printf("Unexpected wait result res %d",res);
    return 2;
  }
  printf("Attached on %d\n",res);
  /***** ALLOCATING DEBUG DATA *****/
  char *program_location = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
  sprintf(program_location, "%s/%s", $program_directory$, $program_name$);
  printf("program at \"%s/%s\"\n", $program_directory$, $program_name$);


  um_data* dbg;
  if ((fail = um_init(&dbg, pid, program_location)) != 0)
  {
    fprintf(stderr, "Could not fill out debug info for %s, error code %d\n", program_location, fail);
    return 3;
  }













//  /***** STACK UNWINDING *****/
  um_frame* stack = NULL;
//  um_unwind (dbg, NULL, &stack,0);


//  if(um_wait_out_of_stack(dbg, (char*)old_func_name) == 0){
//    um_redefine(dbg, (char*)old_func_name,(char*)new_func_name);
//  }




  uint64_t addr = -1;// um_get_var_addr(dbg, true, "*obj_copy", "print1");
//  printf("addr of *obj_copy is %p\n", (void*)addr);


    um_realloc_and_set_variable(dbg, true, "some_comment", "print1", 20, true, (void*)"new comments", strlen("new comments") + 1);


  if(addr != -1){
//    printf("addr of *obj_copy is %p\n", (void*)addr);

//    addr = um_get_var_addr(dbg, false, "*obj", "src/test.c");
//    printf("addr of *obj_copy is %p\n", (void*)addr);

//    um_set_variable(dbg, true, "age", "_struct1", 99, 4);
  }





  /*modify sex*/
  person per;
//  um_write_addr (dbg, (addr + ((uint64_t)(&per.sex) - (uint64_t)&per)), 'f', 1);


  /*modify name*/
//  uint64_t new_addr = add_memory(dbg->pid, 15);
//  const char* new_name = "xiaofan CHEN";
//  um_write_addr_n(dbg, new_addr, (void*)new_name, 13, 1);
//  um_write_addr (dbg, (addr + ((uint64_t)(&per.name) - (uint64_t)&per)), new_addr , 8);
//  getchar();
//
//
//
//
//  printf("addr is %llx\n", (unsigned long long )addr);
//
//  printf("next %llx\n", addr = um_read_addr(dbg, addr, 8));
//
////  printf("next %llx\n", addr = um_read_addr(dbg, addr, 8));
//
//
//um_write_addr (dbg, addr, 10, 8);



//  um_set_variable(dbg, false, var_name, "src/test.c", 10, 8);
//
//  um_set_variable(dbg, true, "*obj_copy", "print1", 100, 4);



  /***** LOAD UPDATE *****/
//  printf("Loading returned %d\n", um_load_code(dbg, "./testprogs/update.so"));


  um_destroy_stack(stack);
  um_end(dbg);

  //Detach manager
  um_detach(pid);
  printf("Detached from %d\n",pid);

//  //Delete Update File when over
//  char *update_file_path = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
//  sprintf(update_file_path, "%s/%s",ui->update_directory,update_file);
//  int rem_upd = remove(update_file_path);
//  if(rem_upd != 0){
//    printf("Could not delete update file %s \n",update_file);
//    return 4;
//  }
//  else{
//    printf("Update file %s deleted \n",update_file);
//  }

  return 0;
}


int main(){
  do{
    _tmain();
//    sleep(3);
  }while(0);
}
