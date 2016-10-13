#include <assert.h>
#include <stdio.h>
#include "svcomp/svcomp.h"
#include "toy_library.h"

int main() {
  toy_library_hello();

  int a = __VERIFIER_nondet_int();
  if (a == 0) {
    printf("a is zero\n");
#ifdef BUG
    __VERIFIER_error();
#endif
  } else {
    printf("a is non-zero\n");
  }
  return 0;
}
