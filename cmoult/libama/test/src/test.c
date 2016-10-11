#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>

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

void print1(person* obj){
  printf("obj of type person at %p\n", (void*)obj);
  printf("obj->name: \"%s\"\n", obj->name);
  printf("obj->age: %d\n", obj->age);
  printf("obj->sex: \'%c\'\n", obj->sex);
  printf("finished print1()\n\n");
  sleep(1);
}


void print2(person_with_comment* obj){
  printf("obj of type person_with_comment at %llx\n", (unsigned long long)obj);
  printf("obj->name: \"%s\"\n", obj->name);
  printf("obj->age: %d\n", obj->age);
  printf("obj->sex: \'%c\'\n", obj->sex);
  printf("obj->comment: \"%s\"\n", obj->comment);
  printf("finished print2\n\n");
  sleep(1);
}

int main(){
  obj = (person*)malloc(sizeof(person));
  obj->age = 24;
  obj->name = "Xiaofan";
  obj->sex = 'm';
  while(1){
    print1(obj);
  }
  return 0;
}
