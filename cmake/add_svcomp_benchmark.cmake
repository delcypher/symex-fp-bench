macro(add_svcomp_benchmark BENCHMARK_DIR)
  set(INPUT_FILE ${CMAKE_CURRENT_SOURCE_DIR}/${BENCHMARK_DIR}/spec.yml)
  set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${BENCHMARK_DIR}_targets.cmake)
  # Only re-generate the file if necessary so that re-configure is as fast as possible
  if ("${INPUT_FILE}" IS_NEWER_THAN "${OUTPUT_FILE}")
    message(STATUS "Generating \"${OUTPUT_FILE}\"")
    execute_process(COMMAND ${PYTHON_EXECUTABLE} ${CMAKE_SOURCE_DIR}/svcb-emit-cmake-decls.py
                            ${INPUT_FILE}
                            --architecture ${SVCOMP_ARCHITECTURE}
                            --output ${OUTPUT_FILE}
                    RESULT_VARIABLE RESULT_CODE
                   )
    if (NOT ${RESULT_CODE} EQUAL 0)
      message(FATAL_ERROR "Failed to process benchmark ${BENCHMARK_DIR}. With error ${RESULT_CODE}")
    endif()
  endif()
  # Include the generated file
  include(${OUTPUT_FILE})
  # Let CMake know that configuration depends on the benchmark specification file
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${INPUT_FILE}")
endmacro()
