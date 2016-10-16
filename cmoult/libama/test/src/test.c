#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <sys/ptrace.h>

typedef struct _struct1{
  int age;
  char* name;
  char sex;
}person;

typedef struct _struct2{
  int age;
  char* name;
  char* comment;
  char sex;
}person_with_comment;

person* obj;
char* comment;

void __attribute__ ((noinline)) print1(person* obj){
//  sleep(3);
  char* some_comment = malloc(sizeof(char)*1024);
  const char* some_text = "some comment";
  memcpy(some_comment, some_text, strlen(some_text) + 1);
  person* obj_copy = obj;
  printf("obj of type person at %p\n", (void*)obj_copy);
  printf("obj->name: \"%s\"\n", obj_copy->name);
  printf("obj->age: %d\n", obj->age);
  printf("obj->sex: \'%c\'\n", obj->sex);
  printf("char* some_comment at %p\n", (void*)some_comment);
  printf("comment: %s\n", some_comment);
  printf("finished print1()\n\n");


  sleep(5);
  printf("obj of type person at %p\n", (void*)obj_copy);
  printf("obj->name: \"%s\"\n", obj_copy->name);
  printf("obj->age: %d\n", obj->age);
  printf("obj->sex: \'%c\'\n", obj->sex);
  printf("char* some_comment at %p\n", (void*)some_comment);
  printf("comment: %s\n", some_comment);
  printf("finished print1()\n\n");
//  free(some_comment);
}


void print2(person_with_comment* obj){
  printf("obj of type person_with_comment at %llx\n", (unsigned long long)obj);
  printf("obj->name: \"%s\"\n", obj->name);
  printf("obj->age: %d\n", obj->age);
  printf("obj->sex: \'%c\'\n", obj->sex);
  printf("obj->comment: \"%s\"\n", obj->comment);
  printf("finished print2\n\n");
}

void jmp(){
  sleep(1);
}

int main(){
  comment = malloc(sizeof(char)*1024);
  const char* some_text = "some comment";
  memcpy(comment, some_text, strlen(some_text) + 1);
  person* obj_copy = obj;
  obj = (person*)malloc(sizeof(person));
  obj->age = 24;
  obj->name = "Xiaofan";
  obj->sex = 'm';
//  ptrace(PTRACE_TRACEME,0,NULL,NULL);
  int i = 0;
  while(1){
    print1(obj);
    return 0;
  }
  return 0;
}
