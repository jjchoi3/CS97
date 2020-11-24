#include <stdio.h>
#include <stdbool.h>
#include <errno.h>
#include <unistd.h>
#include <stdlib.h>
#include <string.h>
#include "./options.h"

void checkOptions(char ca, char **v,  bool *val, long long *bytes, struct opts *opts){
  *val = false;
  int c;
  while((c = getopt(ca, v, ":i:o:")) != -1){
    switch(c){
    case 'i':
      if(strcmp("rdrand", optarg) == 0){
	opts->input = RDRAND;
      }else if (strcmp("mrand48_r", optarg) == 0){
	opts->input = MRAND48_R;
      }else if ('/' == optarg[0]){
	opts->input = SLASH_F;
	opts->r_src = optarg;
      }else{
	break;
      }
      *val = true;
      break;
      
    case 'o':
      if (strcmp("stdout", optarg) != 0){
	opts->output = N;
	opts->block_size = atoi(optarg);
      }
      *val = true;
      
    case ':':
      break;
    case '?':
      break;
    }
    
    if (optind >= ca){
      return;
    }
  }
    
    *bytes = atol(v[optind]);
    if(*bytes >=0){
      *val = true;
    }
}
