if (KLEE_NATIVE_RUNTIME_FOUND)
  add_library(svcomp_klee_runtime OBJECT runtime.c)
  target_include_directories(svcomp_klee_runtime PRIVATE "${KLEE_NATIVE_RUNTIME_INCLUDE_DIR}")
else()
  message(WARNING "Can't build svcomp_klee_runtime without KLEE runtime")
endif()

