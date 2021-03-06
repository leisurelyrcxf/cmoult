/* socket_listener.c This file is part of Cymoult */
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

Socket Listener.

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


static void* listener_main(void * arg){
  /*Initiate the socket */
  int conn_fd = 0;
  char buff[LISTENER_BUFF_SIZE];
  bool status;
  bool intern = *((bool*)arg);

  listener_socket_fd = socket(AF_INET,SOCK_STREAM,0);
  listener_serv_addr.sin_family = AF_INET;
  listener_serv_addr.sin_addr.s_addr = INADDR_ANY;
  listener_serv_addr.sin_port = htons(LISTENER_PORT);
  if(bind(listener_socket_fd,(struct sockaddr*) & listener_serv_addr,sizeof(listener_serv_addr)) < 0){
    printf("error in binding to port %d", LISTENER_PORT);
    return NULL;
  }
  listen(listener_socket_fd,LISTENER_MAX_CONN);
  while(continue_listener){
    conn_fd = accept(listener_socket_fd,(struct sockaddr*)NULL,NULL);
    int read_num = read(conn_fd, buff, LISTENER_BUFF_SIZE*sizeof(char));
    buff[read_num] = '\0';
    printf("receive command \"%s\"\n", buff);
    /* We got a command, parse it*/
    parse_and_run_command(buff,intern);
    close(conn_fd);
  }
}

void start_socket_listener(bool intern){
  pthread_create(&listener_thread,NULL,&listener_main,(void*) &intern);
}

void stop_socket_listener(){
  continue_listener = 0;
}
  
pthread_t * access_socket_listener(){
  return &listener_thread;
}
