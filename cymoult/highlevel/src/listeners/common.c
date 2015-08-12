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
  int keyword_size = sizeof(UPDATE_KEYWORD)/sizeof(char) -1;
  if ((strncmp(trimedstr,UPDATE_KEYWORD,keyword_size) == 0) && (trimedsize > keyword_size)){
    *libpath = (char*) malloc((trimedsize-keyword_size+1)*sizeof(char));
    strcpy(*libpath,&(trimedstr[keyword_size]));
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
  //  if (!(config_lookup_string(&update,"name",name) && config_lookup_string(&update,"code",code))){
  if (!config_lookup_string(&update,"code",&code)){
    //could not find name of code
    cmoult_log(1,"Warning : Could find code field in update file");
  }else{
    //Load code. We assume that the update is loaded from inside here
    //TODO, trigger loading from outside
    //load_code(code);
    printf("Loading code : %s\n",code);
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


