#include "alterability.h"


static bool flag_wait_static_update_point = 0;
static bool flag_application_ready_to_update = 0;
static int app_pid = -1;

static void manager_signal_handler_wait_static_update_point(int sig, siginfo_t *info, void *ctx){
  switch(sig){
    case SIGUSR1:
      printf("recevie SIGUSR1\n");
      if(info->si_pid == app_pid)
        flag_application_ready_to_update = 1;
      break;
    case SIGUSR2:
      printf("recevie SIGUSR2\n");
      if(info->si_pid == app_pid)
        flag_wait_static_update_point = 1;
      break;
    default:
      break;
  }
}

char preupdate_setup_static_update_point(int pid){
  flag_application_ready_to_update = 0;
  flag_wait_static_update_point = 0;
  app_pid = pid;

  struct sigaction act;
  act.sa_sigaction = manager_signal_handler_wait_static_update_point; //sa_sigaction与sa_handler只能取其一

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

  kill(pid, SIGUSR1);
  printf("send SIGUSR1 to process %d\n", pid);
  //wait application to response
  sleep(2);
  return 0;
}



char wait_static_update_point(unsigned timeout_in_seconds){
  //application is not ready to updates
  if(!flag_application_ready_to_update){
    return -1;
  }
  const struct timespec rqtp = {0, 100000000};
  float time_consumed = 0;
  while(!flag_wait_static_update_point){
    nanosleep(&rqtp, NULL);
    time_consumed += 0.1;
    if(time_consumed > timeout_in_seconds){
      //can't wait static update point in timeout, may due to maybe the application is down or the application
      //can't get into static update point, etc.
      return -1;
    }
  }
  return 0;
}


void cleanup_static_update_point(int pid){
  um_detach(pid);
  printf("Detached from %d\n",pid);

  kill(pid, SIGUSR2);
  printf("send SIGUSR2 to process %d, pull the process out of the static point\n", pid);
  app_pid = -1;
}








/*functions for application*/

static int manager_pid = -1;

static bool application_static_update_point_update_finished = 0;

static void application_signal_handler_wait_static_update_point(int sig, siginfo_t *info, void *ctx){
  switch(sig){
    case SIGUSR1:
      manager_pid = info->si_pid;
      printf("recevie SIGUSR1\n");
      printf("manager pid is %d\n\n", info->si_pid);
      //tell manager the application is ready for the coming update
      kill(manager_pid, SIGUSR1);
      break;
    case SIGUSR2:
      printf("recevie SIGUSR2\n");
      if(info->si_pid == manager_pid)
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

void static_update_point(unsigned timeout_in_seconds){
  if(manager_pid != -1){
    printf("trapping into static update point, send SIGUSR1 to manager of pid %d\n", manager_pid);
    kill(manager_pid, SIGUSR2);

    application_static_update_point_update_finished = 0;
    unsigned time_passed = 0;
    while(!application_static_update_point_update_finished){
      sleep(1);
      time_passed += 1;
      if(time_passed > timeout_in_seconds) {
        break;
      }
    }
    manager_pid = -1;
  }
}
