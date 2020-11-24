
/* Generate N bytes of random output.  */

/* When generating output this program uses the x86-64 RDRAND
   instruction if available to generate random numbers, falling back
   on /dev/random and stdio otherwise.

   This program is not portable.  Compile it with gcc -mrdrnd for a
   x86-64 machine.

   Copyright 2015, 2017, 2020 Paul Eggert

   This program is free software: you can redistribute it and/or
   modify it under the terms of the GNU General Public License as
   published by the Free Software Foundation, either version 3 of the
   License, or (at your option) any later version.

   This program is distributed in the hope that it will be useful, but
   WITHOUT ANY WARRANTY; without even the implied warranty of
   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
   General Public License for more details.

   You should have received a copy of the GNU General Public License
   along with this program.  If not, see <http://www.gnu.org/licenses/>.  */

// Module Imports
#include <errno.h>
#include <stdlib.h>
#include <stdio.h>
// Added headers
#include "./output.h"
#include "./options.h"
#include "./rand64-sw.h"
#include "./rand64-hw.h"

/* Main program, which outputs N bytes of random data.  */
int main (int argc, char **argv){
  /* Check arguments.  */
  bool valid = false;
  long long nbytes;
  struct opts options;
  checkOptions(argc, argv, &valid, &nbytes, &options);

  if (!valid) {
      fprintf (stderr, "%s: usage: %s NBYTES\n", argv[0], argv[0]);
      return 1;
    }

  /* If there's no work to do, don't worry about which library to use.  */
  if (nbytes == 0)
    return 0;

  /* Now that we know we have work to do, arrange to use the
     appropriate library.  */
  void (*initialize) (void);
  unsigned long long (*rand64) (void);
  void (*finalize) (void);

  if (rdrand_supported () && options.input != SLASH_F ) { // default
      initialize = hardware_rand64_init;
      if(options.input == MRAND48_R)
	rand64 = hardware_rand48;
      else
	rand64 = hardware_rand64;
      finalize = hardware_rand64_fini;
      
  }else{
    if(options.input == RDRAND){
      fprintf (stderr, "RDRAND not supported, use software\n");
      return 1;
    }else if(options.input == SLASH_F){
      software_rand64_setPath(options.r_src);
    }
    
    initialize = software_rand64_init;
    rand64 = software_rand64;
    finalize = software_rand64_fini;
  }
  initialize ();
  int wordsize = sizeof rand64 ();
  int output_errno = 0;
  if (options.output == N){
    const int all = options.block_size * 1024;
    unsigned long long *buf = malloc(all);
    if(buf == NULL){
      fprintf(stderr, "Error, make sure your N value is valid");
      return 1;
    }
    do{
      int out = nbytes < wordsize ? nbytes : wordsize;
      int block = all / sizeof rand64();
      for(int i = 0; i < block; i++){
	unsigned long long x = rand64();
	buf[i] = x;
      }
      int status = write(1, buf, out);
      nbytes -= status;
      if(status == -1){
	fprintf(stderr, "Error: unable to write\n");
	free(buf);
	return 1;
      }
    }while (0 < nbytes);
  }else{
  do {
      unsigned long long x = rand64 ();
      int outbytes = nbytes < wordsize ? nbytes : wordsize;
      if (!writebytes (x, outbytes)){
	  output_errno = errno;
	  break;
	}
      nbytes -= outbytes;
    }
  while (0 < nbytes);
  
  if (fclose (stdout) != 0)
    output_errno = errno;

  if (output_errno)
    {
      errno = output_errno;
      perror ("output");
    }
  }

  finalize ();
  return !!output_errno;
}
