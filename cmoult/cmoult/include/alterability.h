#ifndef ALTERABILITY_H
#define ALTERABILITY_H

#include <signal.h>
#include <errno.h>
#include <time.h>
#include "api.h"

char preupdate_setup_static_update_point(int pid);

char wait_static_update_point();

void cleanup_static_update_point(int pid);



/*functions for applications*/

void pre_setup_static_update_point();

void static_update_point();

#endif
