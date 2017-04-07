#ifdef KLEE
#include "klee/klee.h"
#endif
#include <assert.h>
#include <stdio.h>
#include "math.h"

int main() {
  float a = 0.0f;
#ifdef KLEE
  klee_make_symbolic(&a, sizeof(a), "a");
#endif
  if (isnan(a) || isinf(a)) {
    // assertion won't hold in these cases so exit early
    return 0;
  }
  float b = a - a;
  assert(sin(b) == 0.0f);
  return 0;
}
