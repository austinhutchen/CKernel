//-*-c++-*-
#ifndef _global_h_
#define _global_h_

/* Misc manifest constants */
#define MAXLINE    1024   /* max line size */
#define MAXARGS     128   /* max args on a command line */
#define MAXJOBS      16   /* max jobs at any point in time */
#define MAXJID    1<<16   /* max job ID */

/* Global variables */
extern int verbose;   // defined in tcsh.cc
//extern char sbuf[MAXLINE];         /* for composing sprintf messages */
/* End global variables */


#endif
