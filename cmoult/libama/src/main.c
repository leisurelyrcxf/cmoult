#include "libama.h"
#include "VARIABLES.h"
#include "stdlib.h"
#include "stdio.h"

#include <pthread.h>
#include "lazy_update.h"

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
  person2->sex = person1->sex;
  person2->comment = NULL;

  person2->age = 11;
  person2->sex = 'f';
  person2->name = (char*)um_write_str(dbg, (uint64_t)(person2->name), "CPF", flag);

  char* old_name = malloc(1024);
  um_read_str_at_address(dbg, (uint64_t)(person2->name), old_name, 1024);
  char* comment = malloc(1024);
  sprintf(comment, "name: %s, age: %d, sex: %c", old_name, person2->age, person2->sex);
  free(old_name);

  person2->comment = (char*)um_write_str(dbg, (uint64_t)0, comment, flag);
  free(comment);
  return 0;
}

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




  uint64_t addr = -1;






//  //modify array test, passed
//  uint64_t paddr = um_get_var_addr(dbg, true, "person1", "print1");
//  printf("\n\n\naddr %p\n", (void*)paddr);
//
//
//  paddr = um_get_var_addr(dbg, true, "*person1", "print1");
//  printf("addr %p\n", (void*)paddr);
//
//
//
//  person per;
//  addr = um_get_var_addr(dbg, true, "*person1", "print1");
//  if(addr == -1 || addr == 0){
//    fprintf(stderr, "can't get address of *person1\n");
//  }else{
//    um_set_addr(dbg, (addr + offsetof(person, age)), 1111, 4);
//    um_set_str_pointer(dbg, (addr + offsetof(person, name)), "GUO1234456", AUTO_REALLOC);
//    um_set_addr(dbg, (addr + ((char*)(&per.sex) - (char*)&per)), 'f', 1);
//  }
//  int new_int_array[20];
//  for(int i = 0; i < 20; i++){
//    new_int_array[i] = i;
//  }
//  addr = um_get_var_addr(dbg, true, "p_int_array", "print1");
//  if(addr == -1 || addr == 0){
//    fprintf(stderr, "can't get address of p_int_array\n");
//  }else{
//    um_set_pointer_to_values(dbg, addr, 10*sizeof(int), new_int_array, 20*sizeof(int), AUTO_REALLOC);
//  }
//  addr = um_get_var_addr(dbg, true, "size", "print1");
//  if(addr == -1 || addr == 0){
//    fprintf(stderr, "can't get address of size\n");
//  }else{
//    um_set_addr(dbg, addr, 20, sizeof(int));
//  }






  addr = um_get_var_addr(dbg, true, "person", "main");

//    addr = um_get_var_addr(dbg, true, "person", "main");
    printf("person at addr %p\n", (void*)addr);
//    um_transform_struct_pointer(dbg, addr, sizeof(person), sizeof(person_v2), &transform_person_to_person_v2, AUTO_REALLOC);
    if(um_wait_out_of_stack(dbg, "print1") == 0){
      addr = um_get_var_addr(dbg, true, "person", "main");
      printf("person at addr %p\n", (void*)addr);
//      um_transform_struct_pointer(dbg, addr, sizeof(person), sizeof(person_v2), &transform_person_to_person_v2, AUTO_REALLOC);
//      um_redefine(dbg, "print1", "print1_v2");
    }















//    //load code test, failed
//    um_print_stack(dbg);
//    printf("function %s %s in stack\n", "print1", is_function_in_stack(dbg, "print1") ? "is" : "isn't");
//    printf("\n-------------------------------------------\n\n");
//    if(um_load_code(dbg, "/home/leisurelyrcxf/cmoult/cmoult/libama/test/update/lib/libupdate.so") != 0){
//      printf("can't load code\n");
//      return -1;
//    }
//    if(um_wait_out_of_stack(dbg, "print1") == 0){
//      um_print_stack(dbg);
//      printf("function %s %s in stack\n", "print1", is_function_in_stack(dbg, "print1") ? "is" : "isn't");
//      um_redefine(dbg, "print1", "print1_v2");
//    }







//  //test um_get_var_size, pass
//  size_t size1 = um_get_var_size(dbg, "person1", "main");
//  printf("size of person1 in main %u\n", size1);
//  size_t size2 = um_get_var_size(dbg, "person_array", "main");
//  printf("size of person_array in main %u\n", size2);

//  printf("Loading returned %d\n", um_load_code(dbg, "./testprogs/update.so"));









  //test wait data access

//  if(um_wait_out_of_stack(dbg, "print1") == 0){
//    um_lazy_update_variable(dbg, true, "*person", "main", sizeof(person), update_person);
//  }












//  um_destroy_stack(stack);
  um_end(dbg);

  //Detach manager
  um_detach(pid);
  printf("Detached from %d\n",pid);

  return 0;
}


int main(){
  do{
    _tmain();
//    sleep(3);
  }while(0);
}
