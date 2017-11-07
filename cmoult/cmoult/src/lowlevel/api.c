#include "api.h"

/*stop pid, attach tracer, init dbg*/
char init_dbg_and_attach_process(um_data** dbg, int pid, char* program_location){
  int res,fail;
  //Attach manager
  printf("Attaching on process %d\n", pid);
  fail=um_attach(pid);
  if(fail != 0){
    perror("ptrace");
    return -1;
  }
  res = waitpid(pid,NULL,0);
  if(res != pid){
    printf("Unexpected wait result res %d",res);
    return -1;
  }
  printf("Attached on process %d\n",res);
  if ((fail = um_init(dbg, pid, program_location)) != 0)
  {
    fprintf(stderr, "Could not fill out debug info for %s, error code %d\n", program_location, fail);
    return -1;
  }

  if(!(*dbg)){
    printf("cound't get debug info\n");
    return -1;
  }

  return 0;
}
