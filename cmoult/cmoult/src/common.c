#include "common.h"
#include <stdio.h>
#include <time.h>
#include <sys/types.h>
#include <dirent.h>
#include <errno.h>
#include <pthread.h>
#include <stdarg.h>

/*Log level : 0 : Nothing, 1 : Only errors, 2: Everything! */


int loglevel = 1;
char * logpath = ".";
pthread_mutex_t log_lock;
pthread_mutexattr_t log_attr;


void cmoult_log_init(){
  pthread_mutexattr_init(&log_attr);
  pthread_mutexattr_settype(&log_attr,PTHREAD_MUTEX_RECURSIVE);
  pthread_mutex_init(&log_lock,&log_attr);
}

void cmoult_log(const int level,const char * format, ...){
  struct tm *date;
  char date_str[15];
  va_list args;

  pthread_mutex_lock(&log_lock);

  if (level <= loglevel){
    char * path = (char*) malloc((strlen(logpath)+13)*sizeof(char));
    strcpy(path,logpath);
    strcat(path,"/cmoult.log");
    FILE * logFile = fopen(path,"a");
    if (logFile == NULL){
      //Could not open file
      printf("Critical Error! Could not write log entry : does %s even exist?\n",path);
    }else{
      time_t t = time(NULL);
      date = localtime(&t);
      strftime(date_str,sizeof(date_str), "%m/%d,%Hh%M:%S",date);
      fprintf(logFile,"[%s]\t",date_str);
      va_start(args,format);
      vfprintf(logFile,format,args);
      va_end(args);
      fputs("\n",logFile);
      fclose(logFile);
    }
    free(path);
  }
  pthread_mutex_unlock(&log_lock);
}

void set_loglevel(const int level){
  pthread_mutex_lock(&log_lock);
  if ((loglevel >= 0) && (loglevel <= 2)){
    loglevel = level;
  }else{
    cmoult_log(1,"Could not set loglevel to a value less than 0 or greater 2");
  }
  pthread_mutex_unlock(&log_lock);
}

void set_logpath(char * path){
  pthread_mutex_lock(&log_lock);
  DIR * d = opendir(path);
  if (d != NULL){
    //Path exists and everything is OK
    logpath = path;
    closedir(d);
  }else{
    //Dir could not be opend
    switch (errno)
      {
      case EACCES:
        cmoult_log(1,"Permission denied when accessing %s",path);
        break;
      case ENOENT:
        cmoult_log(1,"Path %s does not exist",path);
        break;
      case ENOTDIR:
        cmoult_log(1,"Path %s does not lead to a directory",path);
        break;
      default:
        cmoult_log(1,"Unknown error when trying to set log path to %s",path);
      }
  }
  pthread_mutex_unlock(&log_lock);
}




