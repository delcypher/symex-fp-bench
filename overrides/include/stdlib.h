// Undefine our abort macro just in case this header is included multiple times.
#undef abort
// GCC preprocessor specific behaviour to find next header in search path
#if __GNUC__
#include_next <stdlib.h>
#else
#error "Require gcc/clang"
#endif

#ifdef __cplusplus
extern "C" {
#endif

#ifndef SVCB_GCOV_FLUSH_DECL
extern void __gcov_flush();
#define SVCB_GCOV_FLUSH_DECL
#endif

#ifdef __cplusplus
}
#endif

// Wrapper macro that makes sure __gcov_flush() is called
// first.
#undef abort
#define abort() do {__gcov_flush(); abort();} while(0)
