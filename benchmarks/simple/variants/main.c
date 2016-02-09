#include "triangle_number.h"
#include "svcomp.h"

int main() {
  int result = triangle_number(LOOP_BOUND);
  __VERIFIER_assert(result == (LOOP_BOUND/2)*(LOOP_BOUND +1));
  return 0;
}
