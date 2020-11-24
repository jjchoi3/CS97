#include <stdio.h>
#include <stdlib.h>

/* Input stream containing random bytes.  */
static FILE *urandstream;
static char *path;

void software_rand64_setPath(char *loc){
  path = loc;
  printf("%s", path);
 }
/* Initialize the software rand64 implementation.  */
void software_rand64_init (void){
  if(!path)
    path = "/dev/random";
  
  urandstream = fopen(path, "r");
  if (!urandstream)
    abort ();
}


/* Return a random value, using software operations.  */
unsigned long long software_rand64 (void){
  unsigned long long int x;
  if (fread (&x, sizeof x, 1, urandstream) != 1)
    abort ();
  return x;
}

/* Finalize the software rand64 implementation.  */
void software_rand64_fini (void){
  fclose (urandstream);
}
