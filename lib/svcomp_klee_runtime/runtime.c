/* Copyright (c) 2016, Daniel Liew
   This file is covered by the license in LICENSE-SVCB.txt
*/

// This provides a basic implementation of the SV-COMP
// runtime functions that calls into KLEE's runtime functions.
#include "svcomp/svcomp.h"
#include "klee/klee.h"
#include <inttypes.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>

#define SVCOMP_NONDET_DEFN_D(NAME,T) \
T __VERIFIER_nondet_ ## NAME() { \
  static uint64_t counter = 0; \
  char name[] = "symbolic_xxxxxxxxxxxxxxxxxxxx_TTTTTTTT"; \
  char* offsetStr = name + 9; \
  sprintf(offsetStr, "%" PRIu64 "_%s", counter, #T); \
  T initialValue; \
  klee_make_symbolic(&initialValue, sizeof(T), name); \
  return initialValue; \
}

#define SVCOMP_NONDET_DEFN(NAME) SVCOMP_NONDET_DEFN_D(NAME, NAME)

SVCOMP_NONDET_DEFN_D(bool,_Bool)
SVCOMP_NONDET_DEFN(char)
SVCOMP_NONDET_DEFN(double)
SVCOMP_NONDET_DEFN(float)
SVCOMP_NONDET_DEFN(int)
SVCOMP_NONDET_DEFN(long)
//SVCOMP_NONDET_DEFN(loff_t)
SVCOMP_NONDET_DEFN_D(pointer,void*)
SVCOMP_NONDET_DEFN_D(pchar,char*)
//SVCOMP_NONDET_DEFN(pthread_t)
//SVCOMP_NONDET_DEFN(sector_t)
SVCOMP_NONDET_DEFN(short)
SVCOMP_NONDET_DEFN(size_t)
SVCOMP_NONDET_DEFN_D(u32, uint32_t)
SVCOMP_NONDET_DEFN_D(uchar,unsigned char)
SVCOMP_NONDET_DEFN_D(uint, unsigned int)
SVCOMP_NONDET_DEFN_D(ulong, unsigned long)
SVCOMP_NONDET_DEFN(unsigned)
SVCOMP_NONDET_DEFN_D(ushort, unsigned short)

void __VERIFIER_assume(int expression) {
  klee_assume(expression);
}


// Provide proto-type to suppress -Werror=implicit-function-declaration
void __assert_fail(const char*, const char*, unsigned int, const char*);

void __VERIFIER_assert(int expression) {
  klee_assert(expression);
}

SVCOMP_NO_RETURN void __VERIFIER_error() {
  // FIXME: klee_report_error is not implemented in libkleeRuntest.
  // klee_report_error(__FILE__, __LINE__, "__VERIFIER_error reached","");
  abort();
}

// FIXME: We can probably do better than this
void __VERIFIER_atomic_begin() {
  fprintf(stderr, "__VERIFIER_atomic_begin() is a no-op\n");
}

// FIXME: We can probably do better than this
void __VERIFIER_atomic_end() {
  fprintf(stderr, "__VERIFIER_atomic_end() is a no-op\n");
}
