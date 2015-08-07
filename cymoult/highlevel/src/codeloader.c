/* codeloader.c This file is part of Cymoult */
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

Code Loader. Launched in the application so it can load code later.

 */

#include "loader.h"

pthread_t code_loader;
char code_loader_keep_alive = 1;
long load_switch = 0; //boolean encoded on a long to be changeable with ptrace
char * load_path; //Path to the code to be loaded (will be malloc'ed when strating the code loader

static void * code_loader_main(void * arg){
  char* dlerr;

  while (code_loader_keep_alive){
    sleep(SLEEP_TIME);
    if (load_swicth){
      char * message = malloc((strlen(load_path)+256)*sizeof(char));
      if (access(load_path,F_OK) == 0){
        dlopen(load_path,RTLD_NOW|RTLD_GLOBAL);
        dlerr = dlerror();
        if (dlerr != NULL){
          //An error was met when loading the code
          sprintf(message,"Error met when loading code %s : %s",load_path,dlerr);
          log(1,message);
          free(message);
        }else{
          //Code loaded succesfully
          sprintf(message,"Code loaded successfully from path %s",load_path);
          log(2,message);
        }
      }else{
        //Could not access code path
        spprintf(message,"Error met when loading code %s : could not access the code file",load_path);
        log(1,message);
      }
      load_switch = 0;          
    }
    free(message);
  }
  //The code loader is terminating, free the load_path
  free(load_path);
}

void start_code_loader(){
  load_path = malloc(PATH_SIZE*sizeof(char));
  pthread_create(&code_loader,NULL,&code_loader_main,NULL);  
}

void stop_code_loader(){
  code_loader_keep_alive = 0;
}

pthread_t * access_code_loader(){
  return &code_loader;
}

/* Functions for adding a code to load from the inside */

void load_code(char * path){
  if (strlen(path) > PATH_SIZE){
    log(1,sprintf("Cannot load code from path %s : path string is too long!",path));
  }else{
    strcpy(load_path,path);
    load_switch = 1;
  }

}


