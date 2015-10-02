#include "manager.h"
#include "listener.h"

void main(int argc, char* argv[]){
  if (argc < 2){
    puts("Must give pid of target program");
  }else{
    pid_t target_id = atoi(argv[1]);
    char * name = "manager";
    if (argc > 2){
      name = argv[2];
    }
    manager * man = start_extern_manager(name,NULL,0);
    start_socket_listener();
    set_loglevel(2);
    pthread_join(man->thread,NULL);

    
    }
}

