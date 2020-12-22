#include <stdbool.h>
#include <stdio.h>

enum Input {DEFAULT, RDRAND, MRAND48_R, SLASH_F};
enum Output {STDOUT, N};

struct opts{
  enum Input input;
  char *r_src;
  enum Output output;
  unsigned int block_size;
};
  

void checkOptions(char ca, char **v,  bool *val, long long *bytes, struct opts *opts);
