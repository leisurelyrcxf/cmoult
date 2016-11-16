#Cmoult

Cmoult is the C couterpart of Pymoult. It provides DSU mechanisms
ready to be combined for designing dynamic updates.

Cmoult relies on libuminaty, provided in this repository, to read
DWARF informations and modify running binaries.

###Acknowledgement

The work on Pymoult, Cmoult and other derivatives is funded by the Brittany Regional Council in the context of project IMAJD.


##LICENCE

Cmoult is published under the GPLv2 license (see LICENSE.txt)


##Building

you should set the path of the project first. e.g. export CMOULT_PROJECT_HOME=ur_cmoult_project_home

Make a _build directory in the current folder and run cmake from here

`mkdir _build && cd _build && cmake ..`

##1, Introduction
The Cmoult project is a C version of Pymoult, which provides DSU ability for C langauge similar to Pymoult. In Pymoult, it provides the functionality of modify function, data types (classes), data values, etc. at runtime.

Thus the Cmoult project has the ambition to provide all those functionalities for the language C. Comparing to python, the implementation in C has a lot of difficulties, becuase python is a modern advanced dynamic language, but C is much closer to bottom machine level.

The current implementation still has some shortcomings, but it does have implemented the core functionalities of Pymoult in a prototype form. Below I am gonna the approaches that I used and other contributions which I have made to Cmoult.



##2, Approaches
###2.1, Tasks en Bref
&nbsp;&nbsp;The Pymoult project includes mainly three modules————listener, manager, update. The listener module provides the functionality of receving commands from a TCP session and transfer the corresponding commands including log related commands and especially the update commands, etc. to manager. The manager module provides the functionality of executing commands, managing updates, do updating, etc. The update module provides the infrastructure for implementing customized updates, e.g., the base classes, the low-level api to handling updates, etc.

&nbsp;&nbsp;While the modules listener and manager is much simpler in comparison to the module update, when I got involved into the prject, these two modules have bascially been done, but there are some bugs, which I will present in the later section.

&nbsp;&nbsp;For the update modules, the updates can be firstly classified into two catagories, namely updating function (or method) and updating data, which could be further devided into updating data type and data value. Another dimenstion of updating is the updating moment.

&nbsp;&nbsp;For function update, there are mainly three mechanisms for deciding the updating moment, namely 
* safe redefine update————periodically check the call stack and only apply the update when the function is not in the calling stack
* force quiescence update————apply the update exactly at the point when the function is poped out of stack
* updates with static update points————static update points could be assigned previously in the program, updates will be applied only at static update point to ensure safety.

&nbsp;&nbsp;For updating data, there are two acess strategies:
* progressive (data is accessed when it is used)
* immediate (data is accessed when the update is requested)

&nbsp;&nbsp;and transformation moment:
* delayed (the data is updated some time after the access) or
* instant (the data is updated when accessed).

&nbsp;&nbsp;Below I will present my approaches for implementing these updates seprately.

###2.2 Environments
&nbsp;&nbsp;Due to the time and hardware limitation, All these approaches are implemented and tested under Ubuntu 16.04 and some of these approaches will only work under X86-64.

###2.3, Update function
####2.3.1, Update Approach
&nbsp;&nbsp;Cmoult uses the X86 near jump instruction (0xeb) and long jump instruction (0xe9) to implement this update. To do this, we need to get the addresses of the old function and the new function. This is done with libdw by searching the Dwarf_Die tree.

The code used for updating is as below.

```CPP
int um_redefine(um_data* dbg, char* name1, char* name2){
  uint64_t f1, f2;
  f1 = um_get_function_addr(dbg, name1);
  f2 = um_get_function_addr(dbg, name2);
  if (f1 == 0 || f2 == 0)
      return -1;
  insert_jump(dbg->pid, f1, f2);
  return 0;
}
```

####2.3.2, Dicide the Right Update Moment
&nbsp;&nbsp;There are mainly threee approaches, namely safe redefine update, force quiescence update and static update points. I will explain them in the coming section.
####2.3.2.1, Safe Redefine Update
&nbsp;&nbsp;This is done by periodically checking the call stack and only applying the update when the function is not in the calling stack.
&nbsp;&nbsp;The key API's used to check a whether a function is in stack or not are as below.

```CPP
bool is_function_in_stack(um_data* dbg, char* name){
    um_frame* cache = NULL;
    if (!name)
        return false;
    if(um_unwind(dbg, name, &cache, UM_UNWIND_STOPWHENFOUND) == NULL){
      return false;
    }
    return true;
}
```

The function ` um_frame* um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags) ` is implemented with the libdw api `dwfl_getthread_frames`. The old function in libuminati has some bugs, thus I decided to write my own version of this function, but I still backed up the old function.

```CPP
static int frame_callback (Dwfl_Frame *dwfl_frame, void *callback_arg){
  frame_callback_struc *args = (frame_callback_struc*)callback_arg;
  if(args->has_error){
    return DWARF_CB_ABORT;
  }

  if(args->finished){
    return DWARF_CB_OK;
  }

  Dwarf_Addr pc;
  bool isactivation;
  um_frame* previous;

  if (!dwfl_frame_pc(dwfl_frame, &pc, &isactivation)){
    args->has_error = true;
    dwarf_error("failed to get pc in dwfl_frame_pc()");
    return DWARF_CB_ABORT;
  }
  Dwarf_Addr pc_adjusted = pc - (isactivation ? 0 : 1);

  /* get dwfl by thread, which is not needed in our case currently, may be useful in future work*/
  //  Dwfl_Thread *thread = dwfl_frame_thread (dwfl_frame);
  //  Dwfl *dwfl = dwfl_thread_dwfl (thread);
  Dwfl_Module *mod = dwfl_addrmodule (args->dbg->debug_raw, pc_adjusted);

  if(mod == NULL){
    dwarf_error("Failed in dwfl_addrmodule()");
    args->has_error = true;
    return DWARF_CB_ABORT;
  }



  char *symname = NULL;
  if(mod){
    symname = dwfl_module_addrname (mod, pc_adjusted);
  }



  if(args->stack == NULL){
    args->stack = (um_frame*)malloc(sizeof(um_frame));
    memset(args->stack, 0, sizeof(um_frame));
    args->current = args->stack;
    previous = NULL;
  }else{
    args->current->next = (um_frame*)malloc(sizeof(um_frame));
    memset(args->current->next, 0, sizeof(um_frame));
    previous = args->current;
    args->current = args->current->next;
  }

  if(args->current == args->stack){
    struct user_regs_struct regs = {0};
    if (_um_read_registers(args->dbg->pid, &regs) != 0){
      fprintf(stderr, "can't read registers\n");
      args->has_error = true;
      goto ppp;
    }else{
      args->current->rip = regs.rip;
      args->current->regs[REG_RSP] = regs.rsp;
      args->current->regs[REG_RBP] = regs.rbp;
      if(get_cfa_from_dwfl_module(mod, args->current->rip, args->current, args->dbg) != 0){
//        dwarf_error("Failed in get_cfa_from_dwfl_frame()");
        args->finished = true;
        goto ppp;
      }else{
        if(get_register_from_dwfl_module(REG_RA, mod, args->current->rip, args->current, args->dbg) != 0){
//          dwarf_error("Failed in get_register_from_dwfl_frame()");
          args->finished = true;
          goto ppp;
        }
      }
    }
  }else{
    args->current->rip = pc;//um_read_addr(args->dbg, previous->regs[REG_RA], 8);
    if(args->current->rip == 0 || args->current->rip == 0xffffffffffffffff){
      args->finished = true;
      goto ppp;
    }

    args->current->regs[REG_RSP] = previous->cfa;
    if (get_cfa_from_dwfl_module(mod, args->current->rip, args->current, args->dbg) == 0) {
      int temp_result;
      if ((temp_result = get_register_from_dwfl_module(REG_RBP, mod, args->current->rip, args->current, args->dbg)) > 0){
        args->current->regs[REG_RBP] = _um_read_addr(args->dbg->pid, previous->regs[REG_RBP], 8);
      }else if(temp_result < 0){
//        dwarf_error("Failed in get_register_from_dwfl_frame()");
        args->finished = true;
        goto ppp;
      }
    }else{
      args->current->regs[REG_RBP] = _um_read_addr(args->dbg->pid, previous->regs[REG_RBP], 8);
      if (get_cfa_from_dwfl_module(mod, args->current->rip, args->current, args->dbg) != 0){
//        dwarf_error("Failed in get_cfa_from_dwfl_frame()");
        args->finished = true;
        goto ppp;
      }
    }

    if (get_register_from_dwfl_module(REG_RA, mod, args->current->rip, args->current, args->dbg) != 0){
//      dwarf_error("Failed in get_register_from_dwfl_frame()");
      args->finished = true;
      goto ppp;
    }

  }

ppp:
  //if this um_frame corresponds to the wanted scope, we set res
  if(args->target){
    if (symname) {
      if (strcmp(args->target, symname) == 0){
        args->found = true;
        if (!args->result || args->return_last)
          args->result = args->current;
        if (args->stop_when_found){
          args->finished = true;
        }
      }
    }
  }



  if(args->print){
    Dwarf_Addr start, end;
    const char* module_name;
    module_name = dwfl_module_info (mod, NULL, &start, &end, NULL, NULL, NULL, NULL);
    symname[6] = '\0';
    printf("#%p\t%4s\t%s\t%p\t%p\t%p\t%p\t%p\n", (void*)((uint64_t) pc),
      ! isactivation ? "-1" : "top", symname, (void*)mod, (void*)args->current->cfa, (void*)args->current->regs[REG_RSP],
          (void*)args->current->regs[REG_RBP], (void*)args->current->regs[REG_RA]);
  }
  return DWARF_CB_OK;
}

um_frame* _um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags, bool print) {

  frame_callback_struc args = {
      .dbg = dbg,
      .stack = NULL,
      .current = NULL,
      .result = NULL,
      .target = target,
      .stop_when_found = flags & 0x01,
      .return_last = flags & 0x02,
      .found = 0,
      .finished = false,
      .print = print,
      .has_error = false
  };



  if(args.print){
    printf("pc\t'active'\tfunc_name\tmod_name\tcfa\trsp\trbp\tra\n");
  }
  if(dwfl_getthread_frames(dbg->debug_raw, dbg->pid, &frame_callback, (void*)(&args)) != 0){
      dwarf_error("dwfl_getthread_frames");
      return NULL;
  }
  if(args.print){
    printf("\n\n\n");
  }
  *cache = args.stack;

  if(args.has_error || (target && !args.found)){
    return NULL;
  }

  return args.result;
}

um_frame* um_unwind (um_data* dbg, const char* target, um_frame** cache, int flags) {
  _um_unwind(dbg, target, cache, flags, 1);
}
```
&nbsp;&nbsp;The implementation of safe redefine update is something similar to below
```CPP
int um_wait_safe_redefine_update_point(um_data* dbg, char* func_name, unsigned long mseconds){
  while(is_function_in_stack(dbg, func_name)){
    um_cont(dbg->pid);

    struct timespec spec = {.tv_sec = mseconds/1000, .tv_nsec = (mseconds%1000)*1000000};
    nanosleep(&spec, NULL);
    um_stop(dbg->pid);
    int res = waitpid(dbg->pid,NULL,0);
    if(res != dbg->pid){
      return -1;
    }
  }
  return 0;
}

int um_safe_redefine(um_data* dbg, char* name1, char* name2, unsigned long mseconds){
  if(um_wait_safe_redefine_update_point(dbg, name1, mseconds) == 0)
    return um_redefine(dbg, name1, name2);
}
```
####2.3.2.2, Force Quiescence Update
&nbsp;&nbsp;Apply the update exactly at the point when the function has just been poped out of calling stack. This is done by unwind the stack and add a breakpoint at the entrance of the next function in the call stack.

The code is as below.
```CPP
int um_wait_out_of_stack(um_data* dbg, char* name){
    um_frame* cache = NULL;
    if (!name)
        return -1;
    if ((cache = um_unwind(dbg, name, &cache, UM_UNWIND_RETURNLAST))) {
        if (!(cache->next))
            return -2;

        //Set a breakpoint after the function's return
        uint64_t old_value = add_breakpoint(dbg->pid, cache->next->rip);
        //Let the function run
        um_cont(dbg->pid);
        waitpid(dbg->pid, 0, 0);
        //Delete the breakpoint and fix RIP
        _um_write_addr(dbg->pid, cache->next->rip, old_value, 1);
        struct user_regs_struct regs;
        _um_read_registers(dbg->pid, &regs);
        regs.rip = cache->next->rip;
        _um_write_registers(dbg->pid, &regs);
    }
    return 0;
}
```
####2.3.2.3, Static Update Point
The static update point is implemented using the linux signal system.

The manager firstly sends a SIGUSR1 to the process to be updated, if then the manager receives a SIGUSR1 back from the application then the manager will be ready to doing update. By calling `char wait_static_update_point(unsigned int)`, the manager will block itself until receiving a SIGUSR2 from the application which indiates that the application has entered a static update point or the timeout is expired which indicates what the application doesn't enter any static update point within the given timeout.

The application firstly registers functions for handling signal SIGUSR1 and SIGUSR2. If it receives a SIGUSR1 from manager, it will be aware of that there is a coming update event. Then it will store the pid of the manager and send a SIGUSR1 back to the manager. When it reaches its *static_update_point* function, it will send a SIGUSR2 to the manager, and block itself until the manager finished the update and sending back a SIGUSR2.

The key APIs come as below:
```CPP
static bool flag_wait_static_update_point = 0;
static bool flag_application_ready_to_update = 0;
static void manager_signal_handler_wait_static_update_point(int sig){
  switch(sig){
    case SIGUSR1:
      flag_application_ready_to_update = 1;
      break;
    case SIGUSR2:
      printf("recevie SIGUSR1\n");
      flag_wait_static_update_point = 0;
      break;
    default:
      break;
  }
}

char preupdate_setup_static_update_point(int pid){
  flag_application_ready_to_update = 0;
  flag_wait_static_update_point = 1;
  if(signal(SIGUSR1, manager_signal_handler_wait_static_update_point) == SIG_ERR){
    fprintf(stderr, "Unable to create signal handler\n");
    return -1;
  }

  kill(pid, SIGUSR1);
  //wait application to response
  sleep(2);
  printf("send SIGUSR1 to process %d, send the pid of manager and makes the application ready for coming update\n", pid);
  return 0;
}



char wait_static_update_point(unsigned int timeout){
  //application is not ready to updates
  if(!flag_application_ready_to_update){
    return -1;
  }
  const struct timespec rqtp = {0, 100000000};
  float time_consumed = 0;
  while(flag_wait_static_update_point){
    nanosleep(&rqtp, NULL);
    time_consumed += 0.1;
    if(time_consumed > timeout){
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
}








/*functions for application*/

extern int manager_pid = 0;

static bool application_static_update_point_update_finished;

static void application_signal_handler_wait_static_update_point(int sig, siginfo_t *info, void *ctx){
  printf("\nreceive a sig %d\n", sig);
  switch(sig){
    case SIGUSR1:
      manager_pid = info->si_pid;
      printf("manager pid is %d\n\n", info->si_pid);
      //tell manager the application is ready for the coming update
      kill(manager_pid, SIGUSR1);
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
    kill(manager_pid, SIGUSR2);
    manager_pid = 0;

    application_static_update_point_update_finished = 0;
    while(!application_static_update_point_update_finished){
      sleep(1);
    }
  }
}
```

Below is an example to use these functions.

Manager side (the updates)
```CPP
char preupdate_setup(){
  return preupdate_setup_static_update_point(pid);
}


/*wait static update point*/
char wait_alterability(){
  return wait_static_update_point(1800) == 0;
}

//
//void clean_failed_alterability(){
//
//}

void apply(){
  char *program_location = malloc(PROGRAM_DIRECTORY_MAXLENGTH*sizeof(char));
  sprintf(program_location, "%s/%s", $program_directory$, $program_name$);
  printf("program location is: \"%s\"\n", program_location);
  if(init_dbg_and_attach_process(&dbg, pid, program_location) != 0){
    fprintf(stderr, "failed to update\n");
    fprintf(stderr, "can't redefine function \"%s\" to \"%s\"\n", old_func_name, new_func_name);
    return;
  }

//  um_cont(pid);
  if(um_redefine(dbg, (char*)old_func_name,(char*)new_func_name) != 0){
    printf("can't redefine function \"%s\" to \"%s\"\n", old_func_name, new_func_name);
  }else{
    printf("successfully update function \"%s\" to \"%s\"\n", old_func_name, new_func_name);
  }
}

//void preresume_setup(){}
//char wait_over(){}
//char check_over(){}

void cleanup(){
  cleanup_static_update_point(pid);
}
```

Application side
```CPP
void __attribute__ ((noinline)) func1(){
  printf("func1()\n");
}

void __attribute__ ((noinline)) func2(){
  printf("func2()\n");
}

int manager_pid = 0;

int main(){
  pre_setup_static_update_point();
  while(1){
    static_update_point();
    func1();
    sleep(1);
  }
  return 0;
}
```

###2.4, Update Data
####2.4.1, Update Approach
Update data involves updating data in heap and data in stack.
#####2.4.1.1 Key APIs
Some of the key APIs are as following.
```CPP
//write value to given address
int um_set_addr (um_data* dbg, uint64_t addr, uint64_t val, size_t size){
  if(addr == 0xffffffffffffffff){
    return -1;
  }

  return _um_write_addr (dbg->pid, addr, val, size);
}
```

```CPP
//find variable adddress and write new value (only used for basic types)
int um_set_variable (um_data* dbg, bool is_local, char* name, char* scope, uint64_t val, size_t size){
  return um_set_addr(dbg, um_get_var_addr(dbg, is_local, name, scope), val, size);
}
```

```CPP
//get the address pointed by a pointer
uint64_t um_get_addr_by_pointer_addr(um_data* dbg, uint64_t pointer_addr){
  return um_read_addr(dbg, pointer_addr, 8);
}
```

```CPP
//repoint pointer to a new address
int um_repoint_pointer_to_addr(um_data* dbg, uint64_t pointer_addr, uint64_t addr){
  return um_write_addr(dbg, pointer_addr, addr, 8);
}
```

```CPP
//like malloc in C, but in Cmoult way
uint64_t um_malloc(um_data* dbg, size_t malloc_size){
  uint64_t malloc_addr = add_memory(dbg->pid, malloc_size);
  if(malloc_addr == (uint64_t)-1 || malloc_addr == 0){
    fprintf(stderr, "can't malloc memory of %lu bytes\n", malloc_size);
    return 0;
  }
  return malloc_addr;
}
```

```CPP
//like realloc in C, but in Cmoult way
uint64_t um_realloc(um_data* dbg, uint64_t old_addr, size_t old_size, size_t new_size){
  if(old_addr == 0 || old_addr == -1 || new_size > old_size){
    return um_malloc(dbg, new_size);
  }
  return old_addr;
}
```

```CPP
//like memcpy in C, but in Cmoult way
int um_memcpy(um_data* dbg, uint64_t dest, uint64_t src, size_t n, int memcpy_flag){
  if(dest == 0 || dest == -1 || src == 0 || src == -1){
    return -1;
  }

  switch(memcpy_flag){
    //manager to manger
    case MEMCPY_LOCAL_TO_LOCAL:
      memcpy((void*)dest, (void*)src, n);
      return 0;
    //application to manager
    case MEMCPY_REMOTE_TO_LOCAL:
    {
      if(um_read_addr_n(dbg, src, (void*)dest, n, 1) != 0){
        return -1;
      }
      return 0;
    }
    //manager to application
    case MEMCPY_LOCAL_TO_REMOTE:
    {
      if(um_write_addr_n(dbg, dest, (void*)src, n, 1) != 0){
        return -1;
      }
      return 0;
    }
    //application to application
    case MEMCPY_REMOTE_TO_REMOTE:
    {
      void* temp_buf = malloc(n);
      int result = um_memcpy(dbg, (uint64_t)temp_buf, src, n, MEMCPY_REMOTE_TO_LOCAL);
      if(result != 0){
        free(temp_buf);
        return result;
      }
      result = um_memcpy(dbg, dest, (uint64_t)temp_buf, n, MEMCPY_LOCAL_TO_REMOTE);
      if(result != 0){
        free(temp_buf);
        return result;
      }
      return 0;
    }
    default:
      return -1;
  }
}
```
#####2.4.1.2 Basic Update
Simple updates can be done by simply calling the all-in-one function
`int um_set_variable (um_data* dbg, bool is_local, char* name, char* scope, uint64_t val, size_t size)`
More complicated updates can be done using the combination of the aboved APIs.

#####2.4.1.3 Update Non-Pointed values
Non pointed values can only be updated in an in-place way, e.g.,
```CPP
struct some_struct s; //here s can only be updated in place.
char* p; //here the pointer p itself can only be updated in place
```

#####2.4.1.4 Update Pointer
######2.4.1.4.1 Update Pointer Itself
Pointer itself can only be updated in place as updating non-pointed values.
######2.4.1.4.2 Update Pointer Values
Firstly calculate the address of the pointed values by reading the content of pointer address, then write a new address to the pointer address.
######2.4.1.4.3 Allocate New Memory and Redirect Pointer
Allocate New Memory and Redirect Pointer can be used to write new values which have bigger size than the old values and couldn't be written in the in-place way. In this case, firstly, new memory is allocated, new values are written to the new address, and then the pointer is redirected to the new address.

#####2.4.1.5 Update String
Cause in C a string is usually a char* variable in heap or const memory, update string can either be done in place or by allocating new moemory and using pointer redirection.

The API **um_write_str** and **um_set_str_pointer** are for this purpose. These two functions both accept a parameter **flag**, which is used to decide whether new memory need be allocated. Curretly there are four kinds of flags which are described as below
* FORCE_REALLOC————force allocate new memory
* NOT_REALLOC————force not allocate new memory
* AUTO_REALLOC————let Cmoult decide whether to allocate memoery or not (recommended). Cmoult will get the length of the old string and the length of the new string, then use them to decide whether allocating new momery is needed

```CPP
/**
 * write new str at str_addr, allocate new memory is possible
 * str_addr: the address of the old string (not pointer)
 * new_str: a manager-side string
 * return value: the address of the new string
*/
uint64_t um_write_str(um_data* dbg, uint64_t str_addr, char* new_str, int flag){
  if(new_str == NULL){
    return -1;
  }
  size_t new_len = strlen(new_str);
  uint64_t new_size = new_len + 1;

  uint64_t addr;
  //force allocate new memory
  if(flag == FORCE_REALLOC){
    addr = um_malloc(dbg, new_size);
  //force not allocate new memory
  }else if(flag == NOT_REALLOC){
    if(str_addr == 0 || str_addr == -1){
      return -1;
    }
    addr = str_addr;
  //decide alllocate or not in an antomatical way
  }else if(flag == AUTO_REALLOC){
    size_t old_len = um_get_str_len_at_address(dbg, str_addr);
    if(old_len == -1){
      addr = um_malloc(dbg, new_size);
    }else{
      uint64_t old_size = old_len + 1;
      addr = um_realloc(dbg, str_addr, old_size, new_size);
    }
  }else{
    return -1;
  }
  if(um_memcpy(dbg, addr, (uint64_t)new_str, new_size, MEMCPY_LOCAL_TO_REMOTE) != 0){
    return -1;
  }
  return addr;
}
```

```CPP
/**
 * set string pointer to a new string, allocate new momory is possible (depends on flag)
 */
uint64_t um_set_str_pointer(um_data* dbg, uint64_t str_pointer_addr, char* new_str, int flag){
  uint64_t str_addr = um_get_addr_by_pointer_addr(dbg, str_pointer_addr);
  if(str_addr == 0 || str_addr == -1){
    return -1;
  }

  uint64_t addr = um_write_str(dbg, str_addr, new_str, flag);
  if(addr == 0 || addr == -1){
    return -1;
  }

  if(um_repoint_pointer_to_addr(dbg, str_pointer_addr, addr) != 0){
    return -1;
  }
  return addr;
}
```
#####2.4.1.6 Update Buffer

Similar to updating string, but for generic purpose and generic types, unlike update string, Cmoult can't deduct the size of the size of the old buffer and new buffer, thus two additional parameters (**old_size** and **new_size**) are needed.
```CPP
/**
 * like uint64_t um_write_str(um_data* dbg, uint64_t str_addr, char* new_str, int flag), but in a more generic way for generic types
 */
uint64_t um_write_values(um_data* dbg, uint64_t exisiting_addr, size_t old_size, void* new_values, size_t new_size, int flag){
  if(new_values == NULL){
    return -1;
  }

  uint64_t addr;
  if(flag == FORCE_REALLOC){
    addr = um_malloc(dbg, new_size);
  }else if(flag == NOT_REALLOC){
    if(exisiting_addr == 0 || exisiting_addr == -1){
      return -1;
    }
    addr = exisiting_addr;
  }else if(flag == AUTO_REALLOC){
    addr = um_realloc(dbg, exisiting_addr, old_size, new_size);
  }else{
    return -1;
  }
  if(um_memcpy(dbg, addr, (uint64_t)new_values, new_size, MEMCPY_LOCAL_TO_REMOTE) != 0){
    return -1;
  }
  return addr;
}
```

```CPP
/**
 * uint64_t um_set_str_pointer(um_data* dbg, uint64_t str_pointer_addr, char* new_str, int flag), but in a more generic way for generic types
 */
uint64_t um_set_pointer_to_values(um_data* dbg, uint64_t pointer_addr, size_t old_size, void* new_values, size_t new_size, int flag){
  uint64_t target_addr = um_get_addr_by_pointer_addr(dbg, pointer_addr);
  if(target_addr == 0 || target_addr == -1){
    return -1;
  }

  uint64_t addr = um_write_values(dbg, target_addr, old_size, new_values, new_size, flag);
  if(addr == 0 || addr == -1){
    return -1;
  }

  if(um_repoint_pointer_to_addr(dbg, pointer_addr, addr) != 0){
    return -1;
  }
  return addr;
}
```

#####2.4.1.7 Update Struct
Similar to update buffer, but instead providing new values, a transform function pointer is provided as a parameter to do the transformation.

In the pointer case, cause new memory could be allocated and pointer redirection is used, thus increasing the size of the struct is possible, i.e., add or remove member from struct is also possible. Otherwise, increasing or keeping the size of the struct is not possible, but descreasing it is possible.

E.g., for variable like `struct some_struct s`, if we modify `some_struct` to `some_struct_2`, if size of `some_struct_2` is bigger than `some_struct`, then the update is not doable (if size of `some_struct_2` is smaller than or equal to `some_struct`, then it's still doable). But for variable like `struct some_struct* s`, no matter what the size of the new struct `some_struct_2` is, the udpate is always doable. So if users want to use this version of Cmoult and want to add member to exsiting struct at runtime, it must program in a more Cmoult way, i.e., for struct variable, always allocate it in heap other than stack.
```CPP
/**
 * Transform struct, both values and structure (types) are possible
 */
uint64_t um_transform_struct(um_data* dbg, uint64_t obj_addr, size_t old_size, size_t new_size, int (*transform)(um_data*, void*, void*, int flag), int flag){
  if(obj_addr == -1 || obj_addr == 0){
    return -1;
  }

  void* old_values = malloc(old_size);
  memset(old_values, 0, old_size);
  if(um_memcpy(dbg, (uint64_t)old_values, obj_addr, old_size, MEMCPY_REMOTE_TO_LOCAL) != 0){
    free(old_values);
    return -1;
  }

  void* new_values = malloc(new_size);
  memset(new_values, 0, new_size);
  if(transform(dbg, old_values, new_values, flag) != 0){
    fprintf(stderr, "Failed to transform\n");
    free(old_values);
    free(new_values);
    return -1;
  }

  uint64_t addr;
  if(flag == FORCE_REALLOC){
    addr = um_malloc(dbg, new_size);
  }else if(flag == NOT_REALLOC){
    if(new_size > old_size){
      fprintf(stderr, "new struct size bigger than old, must realloc\n");
      addr = -1;
    }else{
      addr = obj_addr;
    }
  }else if(flag == AUTO_REALLOC){
    addr = um_realloc(dbg, obj_addr, old_size, new_size);
  }else{
    return -1;
  }
  if(addr == 0 || addr == -1){
    free(old_values);
    free(new_values);
    return -1;
  }


  if(um_memcpy(dbg, addr, (uint64_t)new_values, new_size, MEMCPY_LOCAL_TO_REMOTE) != 0){
    return -1;
  }

  return addr;
}
```

```CPP
//redirect pointer address
uint64_t um_transform_struct_pointer(um_data* dbg, uint64_t pointer_addr, size_t old_size, size_t new_size, int (*transform)(um_data*, void*, void*, int flag), int flag){
  uint64_t obj_addr = um_get_addr_by_pointer_addr(dbg, pointer_addr);
  if(obj_addr == 0 || obj_addr == -1){
    return -1;
  }

  uint64_t addr = um_transform_struct(dbg, obj_addr, old_size, new_size, transform, flag);
  if(addr == 0 || addr == -1){
    return -1;
  }

  if(um_repoint_pointer_to_addr(dbg, pointer_addr, addr) != 0){
    return -1;
  }
  return addr;
}
```
#####2.4.1.7 Update Array
Cause arrays are allocated in stack, and the array variable can't be redirected (it is kindly equivalenet to a const pointer). Update an array is always in place.
```CPP
//all-in-one function for updating an array in place
uint64_t um_set_by_array_variable(um_data* dbg, bool is_local, char* name, char* scope, void* new_values, size_t new_size){
  uint64_t addr = um_get_var_addr(dbg, is_local, name, scope);
  if(addr == -1 || addr == 0){
    fprintf(stderr, "failed to get address of variable %s in %s\n", name, scope);
    return -1;
  }

  if(um_write_addr_n(dbg, addr, new_values, new_size, 1) != 0){
    return -1;
  }
  return 0;
}
```

####2.4.2 Access Strategy
#####2.4.2.1 Progressive
I implement a basic version of progressive access strategy using the X86 debug registers. The X86 debug registers can monitor access to specific sections of memory and cause process to interrupt when access is monitored. Such kind of memory breakpoint is called watchpoint in a gdb way. The description of the format of the X86 debug registers could be found in wikipedia, see [x86 debug resiters](https://en.wikipedia.org/wiki/X86_debug_register).

But this approach has some obvious limitations, such as,
* The memory monitored concurrently is limited, in a X86-64 case, maximum 32 Bytes.
* Platform dependency. Have to recode for each architecture. Some architectures don't provide debug registers.

Below is the code of the key API of add a watchpoint in Cmoult.

```CPP
static int um_add_aligned_watchpoint(um_data* dbg, uint64_t addr_to_watch, uint8_t len,
    uint8_t break_cond, uint8_t break_ctrl){
  if(addr_to_watch == 0 || addr_to_watch == (uint64_t)-1){
    return -1;
  }

  if(len != 1 && len != 2 && len != 4 && len != 8){
    fprintf(stderr, "len must be 1, 2, 4 or 8\n");
    return -1;
  }

  if(addr_to_watch % len != 0){
    fprintf(stderr, "not aligned\n");
    return -1;
  }

  if(break_cond < 0 || break_cond > 3){
    fprintf(stderr, "break condition invalid\n");
    return -1;
  }

  if(break_ctrl < 0 || break_ctrl > 1){
    fprintf(stderr, "break control invalid\n");
    return -1;
  }

  int i = 0;
  for(; i < DR_NUM; i++){
    if(um_is_dr_available(i)){
      break;
    }
  }
  if(i >= DR_NUM){
    fprintf(stderr, "no debug register available\n");
    return -1;
  }

  uint64_t dri = addr_to_watch;
  uint64_t break_len_bits_mask = (((uint64_t)break_cond) | ((uint64_t)um_get_len_bits(len))) << (16 + i * 4);
  uint64_t local_global_bits_mask = (1 << (break_ctrl ? 1 : 0) ) << (i * 2);
  uint64_t dr7 = um_read_dr(dbg, 7);
  uint64_t clear_bits_mask = ~((0b1111 << (16 + i * 4)) | (0b11 << (i * 2)));

  dr7 = ((dr7 & clear_bits_mask ) | break_len_bits_mask ) | local_global_bits_mask;
  if(um_write_dr(dbg, i, dri) != 0){
    char buff[1024];
    sprintf(buff, "write dr%d", i);
    perror(buff);
    return -1;
  }

  if(um_write_dr(dbg, 7, dr7) != 0){
    perror("write dr7");
    return -1;
  }
  wp_dr_used[i] = 1;
  wp_dr_mem_addr[i] = dri;
  wp_dr_mem_len[i] = len;
  wp_dr_cond[i] = break_cond;
  wp_dr_ctrl[i] = break_ctrl;
  return 0;
}
```


#####2.4.2.2 Immediate
Data is accessed when the update is requested————the basic case which has nothing to say.

####2.4.3 Transformation Moment
#####2.4.3.1 Delayed
The data is updated some time after the access. The delayed update can be fulfilled in several way such as setting a time to wait, use `um_wait_out_of_stack` of certain functions, use static update point, etc.
#####2.4.3.2 Instant
The data is updated when accessed. This is the basic case.

#3 Other Work
The original Cmoult project and the libuminati all have a lot of bugs, which stuck me hard at certain point. Here I listed some of the bugs or enhancement below.

##3.1 Bug Fix
#3.1.1 Unwind Stack
The original unwind_stack doesn't work if a system call exists. This is probably due to the problems below
* Reading registers to get all the PC for all frames is not reliable.
* The original API `int get_cfa_from_frame(um_frame* context, um_data* dbg)` doesn't work in a system call case, cause the cfi is not always the same for different modules.
* Other potential reasons.

#3.1.2 Get Local Variable Address
Dwarf_Attribute can't be directly assigned, e.g., `Dwarf_Attribute a = b;` seems to result in segmenation error.

#3.1.3 Segmentation Fault in Cmoult Manager
Due to wrong use of `<system/queue>` and when malloc for string, forget to plus 1 for the ending character. I replace the system queue with my own queue implementation because using system queue macros is not easy reading and easy to make error.

#3.1.4 Other Bugs
May still have some bugs which are not listed above.

#3.2 Enhancement
I added a lot of API to libuminati to enhance its functionality, including but not limited to read/write facilities, watchpoint supports, etc.

#3.3 Demos
I implement demos for different kinds of update for demostrating how to use Cmoult, including 
* eager_conversion_update
* modify_integer_pointer
* force_quiescence_update
* safe_redefine_update
* lazy_update
* static_update_point_redefine_function


#4 Future Work
#4.1 Bug Fix
There are some bugs which I have payed a lot of time and attention and still can't resolve, which I list below.
* The API in libuminati `um_load_code` seems not work properly. I have tried to load the new function at runtime and then do an insert jump to the new function address but this always results in segmentation fault.
* The `um_unwind` function is still not perfect, in some special case, the result is not reliable.
Resolving these bugs requires stepping more deeply into the libdw library and understanding more of the call stack implementation in X86, apparently it is goint to be hard and a long term work.

#4.2 Potential Enhancement
* For non-pointed variables, such as `struct some_struct s`, increasing the size of the struct is not possible, which limits the usage of Cmoult. Need read more papers to find out if it is doable, and if yes one possible solution.


#5 Remerciement
Thanks for Fabien Dagnat and Sebastien Martinez for their help during this project.