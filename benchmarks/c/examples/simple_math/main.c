#ifdef KLEE
#include "klee/klee.h"
#endif
#include <assert.h>
#include <stdio.h>
#include "math.h"

int main() {
  float a;
#ifdef KLEE
  klee_make_symbolic(&a, sizeof(a), "a");
#endif
  float b = a - a;
  assert(sin(b) == 0.0f);
  return 0;
}
