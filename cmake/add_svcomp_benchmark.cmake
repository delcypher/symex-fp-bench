macro(add_svcomp_benchmark BENCHMARK_DIR)
  # FIXME: Check timestamp so we don't have to regenerate every file
  # for incremental builds
  # FIXME: We need to pass ``svcb-emit-cmake-decls.py`` the targets we know the
  # compiler can support building
  set(INPUT_FILE ${CMAKE_CURRENT_SOURCE_DIR}/${BENCHMARK_DIR}/spec.yml)
  set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${BENCHMARK_DIR}_targets.cmake)
  execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/svcb-emit-cmake-decls.py
                          ${INPUT_FILE}
                          --output ${OUTPUT_FILE}
                  RESULT_VARIABLE RESULT_CODE
                 )
  if (NOT ${RESULT_CODE} EQUAL 0)
    message(FATAL_ERROR "Failed to process benchmark ${BENCHMARK_DIR}. With error ${RESULT_CODE}")
  endif()
  # Include the generated file
  include(${OUTPUT_FILE})
  # Let CMake know that configuration depends on the benchmark specification file
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS ${INPUT_FILE})
endmacro()
