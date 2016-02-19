#include "listener.h"
#include <ctype.h>
#include <stdio.h>

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
  if ((strncmp(trimedstr,UPD_STR,UPD_LEN) == 0) && (trimedsize > UPD_LEN)){
    *libpath = (char*) malloc((trimedsize-UPD_LEN+1)*sizeof(char));
    strcpy(*libpath,&(trimedstr[UPD_LEN]));
    free(trimedstr);
  }else{
    *libpath = NULL;
  }
}


void load_update(char* path){
  config_t update;
  config_setting_t * set;
  config_setting_t * script;
  const char * name;
  const char * code;
  char * buff;
  int n;
  manager * man;

  config_init(&update);
  if (! config_read_file(&update,path)){
    //could not read file
    cmoult_log(1,"Error : Could not read update file"); 
    return;
  }
  if (!config_lookup_string(&update,"code",&code)){
    //could not find name of code
    cmoult_log(1,"Warning : Could find code field in update file");
  }else{
    //Load code. We assume that the update is loaded from inside here
    //TODO, trigger loading from outside
    //load_code(code);
    cmoult_log(2,"Loading code : %s\n",code);
  }
  set = config_lookup(&update,"scripts");
  if (set != NULL){
    //Parse the updates
    n = config_setting_length(set);
    for (int i=0;i<n;i++){
      const char * name_s, *script_s, *manager_s;
      script = config_setting_get_elem(set,i);
      if (config_setting_lookup_string(script,"name",&name_s) && config_setting_lookup_string(script,"script",&script_s) && config_setting_lookup_string(script,"manager",&manager_s)){
        //One script parsed
        man = lookup_manager(manager_s);
        if (man == NULL){
          cmoult_log(1,"Error : Request <<%s>> did not correspond to a manager",manager_s);
        }else{
          buff = malloc(strlen(script_s)*sizeof(char));
          strcpy(buff,script_s);
          manager_add_update(man,buff);
        }
      }else{
        //Could not par an update
        cmoult_log(1,"Error : Could not parse update instance number %d",i);
      }
    }
  }
  config_destroy(&update);
}


void ext_load_update(char* path, int pid){

}


/* Parses a command and calls the proper function for running it */

void parse_and_run_command(const char* command, bool intern){
  char * trimed_command;
  int command_size;
  int intarg;
  char * chararg;
  char * token;
  //First, trim the command
  strtrim(command,&trimed_command,&command_size);
  //check if it is a "set" command
  if ((strncmp(trimed_command,SET_STR,SET_LEN) ==0) && (command_size > SET_LEN)){
    //the command can be "set loglevel <lvl>" or "set logpath <path>"
    if ((strncmp(trimed_command+SET_LEN,LOGLVL_STR,LOGLVL_LEN) ==0) && (command_size > LOGLVL_LEN)){
      //We are setting the loglevel
      intarg = strtol(trimed_command+SET_LEN+LOGLVL_LEN,&token,10);
      if (token != NULL){
        set_loglevel((int) intarg);
        return;
      }
    }
    if ((strncmp(trimed_command+SET_LEN,LOGPATH_STR,LOGPATH_LEN) ==0) && (command_size > LOGPATH_LEN)){
      chararg = trimed_command+SET_LEN+LOGPATH_LEN+1;
      if (strlen(chararg) > 0){
        set_logpath(chararg);
        return;
      }
    }
  }
  //check if it is an update command
  if ((strncmp(trimed_command,UPD_STR,UPD_LEN)==0) && (command_size > UPD_LEN)){
    //The command can be either "update <update file>" (internal listner) or "update <pid> <update file>" (external listener)
    intarg = strtol(trimed_command+UPD_LEN,&token,10);
    if (intarg != 0){
      //We found a pid
      chararg = token+1;
      if (intern){
        //Load update from inside
        load_update(chararg);
      }else{
        ext_load_update(chararg,intarg);
      }
    }else{
      //We did not find a pid
      chararg = trimed_command+UPD_LEN;
      if (intern){
        //Load update from inside
        load_update(chararg);
      }else{
        //We cannot load update from outside because we didn't find a pid
        cmoult_log(1,"Error, cannot load update from ouside without a target pid");
      }
    }
    return;
  }
  //If we reach here, the command could not be parsed
  cmoult_log(1,"Error, could not parse command <<%s>>",trimed_command);
}
