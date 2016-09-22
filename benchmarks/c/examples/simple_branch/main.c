#ifdef KLEE
#include "klee/klee.h"
#endif
#include <assert.h>
#include <stdio.h>

int main() {
  int a;
#ifdef KLEE
  klee_make_symbolic(&a, sizeof(a), "a");
#endif

  if (a == 0) {
    printf("a is zero\n");
#ifdef BUG
    assert(0);
#endif
  } else {
    printf("a is non-zero\n");
  }
  return 0;
}
