#include <stdint.h>
#include <stddef.h>

// Functions that return non-determinstic values of a particular type
#define SVCOMP_NONDET_DECL_D(NAME,T) \
  T __VERIFIER_nondet_ ## NAME();

#define SVCOMP_NONDET_DECL(NAME) SVCOMP_NONDET_DECL_D(NAME,NAME)

// FIXME: Decide how to handle commented out types

SVCOMP_NONDET_DECL_D(bool,_Bool)
SVCOMP_NONDET_DECL(char)
SVCOMP_NONDET_DECL(double)
SVCOMP_NONDET_DECL(float)
SVCOMP_NONDET_DECL(int)
SVCOMP_NONDET_DECL(long)
//SVCOMP_NONDET_DECL(loff_t)
SVCOMP_NONDET_DECL_D(pointer,void*)
SVCOMP_NONDET_DECL_D(pchar,char*)
//SVCOMP_NONDET_DECL(pthread_t)
//SVCOMP_NONDET_DECL(sector_t)
SVCOMP_NONDET_DECL(short)
SVCOMP_NONDET_DECL(size_t)
SVCOMP_NONDET_DECL_D(u32, uint32_t)
SVCOMP_NONDET_DECL_D(uchar,unsigned char)
SVCOMP_NONDET_DECL_D(uint, unsigned int)
SVCOMP_NONDET_DECL_D(ulong, unsigned long)
SVCOMP_NONDET_DECL(unsigned)
SVCOMP_NONDET_DECL_D(ushort, unsigned short)

#undef SVCOMP_NONDET_D_DECL
#undef SVCOMP_NONDET_DECL

// TODO: Provide doxygen documentation
void __VERIFIER_assume(int condition);
void __VERIFIER_assert(int cond);
__attribute__ ((__noreturn__)) void __VERIFIER_error();
void __VERIFIER_atomic_begin();
void __VERIFIER_atomic_end();
