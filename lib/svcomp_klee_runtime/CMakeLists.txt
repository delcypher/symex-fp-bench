if (KLEE_NATIVE_RUNTIME_FOUND)
  add_library(svcomp_klee_runtime OBJECT runtime.c)
  target_include_directories(svcomp_klee_runtime PRIVATE "${KLEE_NATIVE_RUNTIME_INCLUDE_DIR}")
else()
  message(WARNING "Can't build svcomp_klee_runtime without KLEE runtime")
endif()

if (HAS_STD_C11)
  # Needed for `static_assert()`
  target_compile_options(svcomp_klee_runtime
    PRIVATE ${SVCOMP_STD_C11})
else()
  message(FATAL_ERROR "C11 is required for SVCOMP runtime")
endif()

