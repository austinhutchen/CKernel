//-*-c++-*-
#ifndef _helper_routines_h_
#define _helper_routines_h_

#include <signal.h>
#include <sys/types.h>
#include <sys/wait.h>

/* Here are helper routines that we've provided for you */
int parseline(const char *cmdline, char **argv); 
void sigquit_handler(int sig);
void usage(void);
void unix_error(const char *msg);
void app_error(const char *msg);
typedef void handler_t(int);
handler_t *Signal(int signum, handler_t *handler);

#endif
