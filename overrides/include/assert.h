// Undefine our assert macro just in case this header is included multiple times.
#undef assert
// GCC preprocessor specific behaviour to find next header in search path
#if __GNUC__
#include_next <assert.h>
#else
#error "Require gcc/clang"
#endif

#undef assert
#ifdef NDEBUG
#define assert(ignore) ((void)0)
#else

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

// Modified version of assert() macro that flushes gcov coverage files first.
#define assert(expr)                                          \
	do {                                                        \
		if(!(expr)) {                                             \
			__gcov_flush();                                         \
			__assert_fail(#expr, __FILE__, __LINE__, __func__);     \
		}                                                         \
	} while(0)
#endif
