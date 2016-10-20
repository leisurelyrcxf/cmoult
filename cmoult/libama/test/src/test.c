#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <sys/ptrace.h>

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

//char* comment;

int array_for_test[10] = {1,2,3,4,5,6,7,8,9,10};

void* print_int_array(int* p, size_t size){
  for(int i = 0; i < size; i++){
    printf("%d", p[i]);
    printf(",");
  }
  printf("\n");
}

void __attribute__ ((noinline)) print1(person* person){
//  sleep(3);
//  char array[] = {'s', 'o', 'm', 'e', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't', '\0'};
//  char* some_comment = array;
  printf("Begin print1()\n\n");

  int* p_int_array = array_for_test;
  int size = 10;

  printf("Before:\n");
  printf("person of type person at %p\n", (void*)person);
  printf("pointer person at %p\n", (void*)&person);
  printf("print1 at %p\n", (void*)print1);
  printf("person->name: \"%s\"\n", person->name);
  printf("person->age: %d\n", person->age);
  printf("person->sex: \'%c\'\n", person->sex);
  print_int_array(p_int_array, size);
  printf("\n");

//  sleep(5);

  printf("After:\n");
  printf("person of type person at %p\n", (void*)person);
  printf("pointer person at %p\n", (void*)&person);
  printf("person->name: \"%s\"\n", person->name);
  printf("person->age: %d\n", person->age);
  printf("person->sex: \'%c\'\n", person->sex);
  print_int_array(p_int_array, size);
//  free(some_comment);


  printf("\nFinished print1()\n\n");
}


void print1_v2(person_v2* person){
  printf("person of type person_v2 at %llx\n", (unsigned long long)person);
  printf("person->name: \"%s\"\n", person->name);
  printf("person->age: %d\n", person->age);
  printf("person->sex: \'%c\'\n", person->sex);
  printf("person->comment: \"%s\"\n", person->comment);
  printf("finished print2\n\n");

//  sleep(5);

  printf("person of type person_v2 at %llx\n", (unsigned long long)person);
  printf("person->name: \"%s\"\n", person->name);
  printf("person->age: %d\n", person->age);
  printf("person->sex: \'%c\'\n", person->sex);
  printf("person->comment: \"%s\"\n", person->comment);
  printf("finished print2\n\n");
}



int main(){
//  comment = malloc(sizeof(char)*1024);
//  const char* some_text = "some comment";
//  memcpy(comment, some_text, strlen(some_text) + 1);
//  ptrace(PTRACE_TRACEME,0,NULL,NULL);

//  person person;
//  person.age = 24;
//  person.name = "Xiaofan";
//  person.sex = 'm';

  person person_array[] = {{0,0,0},{0,0,0},{0,0,0}};

  person* person = malloc(sizeof(person));
  person->age = 24;
  person->name = "Xiaofan";
  person->sex = 'm';
  do{
    print1(person);
//    sleep(5);
  }while(1);
  free(person);
  return 0;
}
