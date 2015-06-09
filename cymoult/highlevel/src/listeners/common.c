#include "listener.h"
#include <string.h>
#include <dlfcn.h>
#include <stdio.h>
#include <ctype.h>

static void * spawn_main(void *args){
  ll_spawned * sargs = (ll_spawned*) args;
  if (access(sargs->libpath,F_OK) == 0){
    dlopen(sargs->libpath,RTLD_NOW);
    printf("error : %s\n",dlerror());
    //When the thread is finished, we tell it
    sargs->finished = 1;
  }else{
    fprintf(stderr,"Warning! Listener could not find library %s\n",sargs->libpath); 
  }
}

void spawn_thread(ll_spawned** threads,char* libpath){
  //Create the thread element
  ll_spawned * new_spawned = (ll_spawned*) malloc(sizeof(ll_spawned));
  new_spawned->next = *threads;
  new_spawned->finished = 0;
  new_spawned->libpath = libpath;
  *threads = new_spawned;
  pthread_create(&(new_spawned->thread),NULL,&spawn_main,(void*) new_spawned);
}


/* Trims str and copies the result in trimedstr. Allocates the
   string. trimedsize recieves the new size of the strin */

static void strtrim(const char * str, char ** trimedstr, int * trimedsize){
  int strsize = (int) strlen(str);
  int newsize = strsize;
  for (int i=strsize-1;i>0;i--){
    if (isspace(str[i])){
      newsize--;
    }else{
      break;
    }
  }

  *trimedstr = (char*) malloc((newsize+1)*sizeof(char));
  strncpy(*trimedstr,str,newsize);
  (*trimedstr)[newsize]='\0';
  *trimedsize = newsize;
}

/* Extratcts the library name from a command recieved. 
   The library name will be allocated since this function calls strtrim. */

void extract_library_name(const char* str, char** libpath){
  char * trimedstr;
  int trimedsize;
  strtrim(str,&trimedstr,&trimedsize);
  int keyword_size = sizeof(UPDATE_KEYWORD)/sizeof(char) -1;
  if ((strncmp(trimedstr,UPDATE_KEYWORD,keyword_size) == 0) && (trimedsize > keyword_size)){
    *libpath = (char*) malloc((trimedsize-keyword_size+1)*sizeof(char));
    strcpy(*libpath,&(trimedstr[keyword_size]));
    free(trimedstr);
  }else{
    *libpath = NULL;
  }
}


void clean_threads(ll_spawned ** threads){
  ll_spawned * item = *threads;
  ll_spawned * item2;
  //First, clean the head
  if (item->finished){
    item2 = item->next;
    free(item->libpath);
    free(item);
    item = item2;
    while((item!=NULL) && (item->finished)){
      item2 = item->next;
      free(item->libpath);
      free(item);
      item = item2;
    }
    //item is either NULL (all threads have finished)
    //or the first non-finished thread
    *threads = item;
  }
  if(item != NULL){ 
    item2 = item;
    item = item->next;
    while (item!=NULL){
      if (item->finished){
        item2->next = item->next;
        free(item->libpath);
        free(item);
        item = item2->next;
      }else{
        item2 = item;
        item = item->next;
      }
    }
  }
}




