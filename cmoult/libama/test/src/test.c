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

char* comment;

void __attribute__ ((noinline)) print1(person* person1){
//  sleep(3);
//  char array[] = {'s', 'o', 'm', 'e', ' ', 'c', 'o', 'm', 'm', 'e', 'n', 't', '\0'};
//  char* some_comment = array;
  printf("person1 of type person1 at %p\n", (void*)person1);
  printf("person1->name: \"%s\"\n", person1->name);
  printf("person1->age: %d\n", person1->age);
  printf("person1->sex: \'%c\'\n", person1->sex);
  printf("finished print1()\n\n");

  sleep(5);

  printf("person1 of type person1 at %p\n", (void*)person1);
  printf("person1->name: \"%s\"\n", person1->name);
  printf("person1->age: %d\n", person1->age);
  printf("person1->sex: \'%c\'\n", person1->sex);
  printf("finished print1()\n\n");
//  free(some_comment);
}


void print2(person_v2* person2){
  printf("person2 of type person_v2 at %llx\n", (unsigned long long)person2);
  printf("person2->name: \"%s\"\n", person2->name);
  printf("person2->age: %d\n", person2->age);
  printf("person2->sex: \'%c\'\n", person2->sex);
  printf("person2->comment: \"%s\"\n", person2->comment);
  printf("finished print2\n\n");

  sleep(5);

  printf("person2 of type person_v2 at %llx\n", (unsigned long long)person2);
  printf("person2->name: \"%s\"\n", person2->name);
  printf("person2->age: %d\n", person2->age);
  printf("person2->sex: \'%c\'\n", person2->sex);
  printf("person2->comment: \"%s\"\n", person2->comment);
  printf("finished print2\n\n");
}

void jmp(){
  sleep(1);
}



int main(){
//  comment = malloc(sizeof(char)*1024);
//  const char* some_text = "some comment";
//  memcpy(comment, some_text, strlen(some_text) + 1);
//  ptrace(PTRACE_TRACEME,0,NULL,NULL);

//  person person1;
//  person1.age = 24;
//  person1.name = "Xiaofan";
//  person1.sex = 'm';

  person person_array[] = {{0,0,0},{0,0,0},{0,0,0}};

  person* person1 = malloc(sizeof(person));
  person1->age = 24;
  person1->name = "Xiaofan";
  person1->sex = 'm';
  while(1){
    print1(person1);
  }
  free(person1);
  return 0;
}
