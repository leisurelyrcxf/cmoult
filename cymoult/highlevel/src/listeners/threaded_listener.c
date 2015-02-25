/* threaded_listener.c This file is part of Cymoult */
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

Threaded Socket Listener.

 */

#include <stdio.h>
#include <arpa/inet.h>
#include <sys/types.h>
#include <sys/socket.h>
#include "listener.h"

/* Listener thread */ 
pthread_t listener_thread;
/* Listener socket */
int listener_socket_fd;
struct sockaddr_in listener_serv_addr;
/* Listener will continue until this values 0 */
char continue_listener = 1;


static void * listner_main(void * arg){
  puts("listener started");
  /*Initiate the socket */
  int conn_fd = 0;
  char buff[LISTENER_BUFF_SIZE];
  char * libpath = NULL;
  /* Listener spwaned threads */
  ll_spawned * spawns =NULL;
  /* update handles for spanwees */
  //void ** spawns_libs = malloc(LISTENER_MAX_SPAWNS*sizeof(size_t));

  listener_socket_fd = socket(AF_INET,SOCK_STREAM,0);
  listener_serv_addr.sin_family = AF_INET;
  listener_serv_addr.sin_addr.s_addr = INADDR_ANY;
  listener_serv_addr.sin_port = htons(LISTENER_PORT);
  bind(listener_socket_fd,(struct sockaddr*) & listener_serv_addr,sizeof(listener_serv_addr));
  listen(listener_socket_fd,LISTENER_MAX_CONN);
  while(continue_listener){
    conn_fd = accept(listener_socket_fd,(struct sockaddr*)NULL,NULL);
    read(conn_fd,buff,(LISTENER_BUFF_SIZE-1)*sizeof(char));
    /* We got a command,we extract the library name from it*/
    extract_library_name(buff,&libpath);
    /* If the command was invalid, libpath will be NULL */
    if (libpath != NULL){
      //      spawn_thread(spawns,spawns_libs,&spawned_threads,libpath);
      spawn_thread(&spawns,libpath);
    }
    close(conn_fd);
    clean_threads(&spawns);
  }
  /* We clean everything */
  free(spawns);
  //  free(spawns_libs);
}

void start_threaded_listener(){
  pthread_create(&listener_thread,NULL,&listner_main,NULL);
}

void stop_threaded_listener(){
  continue_listener = 0;
}
  
pthread_t * access_threaded_listener(){
  return &listener_thread;
}






