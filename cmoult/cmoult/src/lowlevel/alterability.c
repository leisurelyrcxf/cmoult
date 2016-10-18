#include "alterability.h"


static bool flag_wait_static_update_point;

static void manager_signal_handler_wait_static_update_point(int sig){
  switch(sig){
    case SIGUSR1:
      printf("recevie SIGUSR1\n");
      flag_wait_static_update_point = 0;
      break;
    default:
      break;
  }
}

char preupdate_setup_static_update_point(int pid){
  flag_wait_static_update_point = 1;
  if(signal(SIGUSR1, manager_signal_handler_wait_static_update_point) == SIG_ERR){
    fprintf(stderr, "Unable to create signal handler\n");
    return -1;
  }

  kill(pid, SIGUSR1);
  printf("send SIGUSR1 to process %d, send the pid of manager and makes the application ready for coming update\n", pid);
  return 0;
}



char wait_static_update_point(){
  const struct timespec rqtp = {0, 100000000};
  while(flag_wait_static_update_point){
    nanosleep(&rqtp, NULL);
  }
  return 0;
}


void cleanup_static_update_point(int pid){
  um_detach(pid);
  printf("Detached from %d\n",pid);

  kill(pid, SIGUSR2);
  printf("send SIGUSR2 to process %d, pull the process out of the static point\n", pid);
}








/*functions for application*/

extern int manager_pid;

static bool application_static_update_point_update_finished;

static void application_signal_handler_wait_static_update_point(int sig, siginfo_t *info, void *ctx){
  printf("\nreceive a sig %d\n", sig);
  switch(sig){
    case SIGUSR1:
      manager_pid = info->si_pid;
      printf("manager pid is %d\n\n", info->si_pid);
      break;
    case SIGUSR2:
      application_static_update_point_update_finished = 1;
      break;
    default:
      break;
  }
}



void pre_setup_static_update_point(){
  struct sigaction act;
  act.sa_sigaction = application_signal_handler_wait_static_update_point; //sa_sigaction与sa_handler只能取其一

  sigemptyset(&act.sa_mask);
  act.sa_flags = SA_SIGINFO; // set flag to enable sa_sigaction

  if (sigaction(SIGUSR1, &act, NULL) < 0){
    fprintf(stderr, "fail to register sigaction\n");
    exit(-1);
  }

  if (sigaction(SIGUSR2, &act, NULL) < 0){
    fprintf(stderr, "fail to register sigaction\n");
    exit(-1);
  }
}

void static_update_point(){
  if(manager_pid != 0){
    printf("trapping into static update point, send SIGUSR1 to manager of pid %d\n", manager_pid);
    kill(manager_pid, SIGUSR1);
    manager_pid = 0;

    application_static_update_point_update_finished = 0;
    while(!application_static_update_point_update_finished){
      sleep(1);
    }
  }
}
