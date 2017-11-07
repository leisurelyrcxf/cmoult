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

void __attribute__ ((noinline)) print_person(person* person){
  printf("Begin print_person()\n\n");

  printf("person of type person at %p\n", (void*)person);
  printf("pointer to person at %p\n", (void*)&person);
  printf("person->name: \"%s\"\n", person->name);
  printf("person->age: %d\n", person->age);
  printf("person->sex: \'%c\'\n", person->sex);


  printf("\nFinished print_person()\n\n\n\n");
}


int main(){
  person person1;
  person1.age = 24;
  person1.name = "Xiaofan";
  person1.sex = 'm';
  do{
    print_person(&person1);
//    sleep(1);
  }while(1);
  return 0;
}
