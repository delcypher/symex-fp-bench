# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt

# List of additional files that generation of target
# include files should depend on. This ensures that if these
# files change the files containing the benchmark targets
# get regenerated (i.e. OUTPUT_FILE in add_svcomp_benchmark())
set(SVCOMP_ADDITIONAL_GEN_CMAKE_INC_DEPS
  "${SVCB_DIR}/svcb/benchmark.py"
  "${SVCB_DIR}/svcb/build.py"
  "${SVCB_DIR}/svcb/schema.py"
  "${SVCB_DIR}/svcb/schema.yml"
  "${SVCB_DIR}/svcb/util.py"
  "${SVCB_DIR}/tools/svcb-emit-cmake-decls.py"
  "${SVCB_DIR}/tools/svcb-emit-cmake-augmented-spec.py"
)

set(SVCOMP_DEPENDENCY_HANDLERS "")

# Tell the build system about an additional dependency handler declared in
# `pythonFile`.  Subsequent calls to `add_benchmark()` in the directory (and
# sub directories) `add_cmake_dependency_handler()` is called in will use
# the additional dependency handler.
macro(add_cmake_dependency_handler pythonFile)
  if ("${pythonFile}" STREQUAL "")
    message(FATAL_ERROR "pythonFile argument cannot be empty")
  endif()
  set(_HANDLER_FILE "${CMAKE_CURRENT_SOURCE_DIR}/${pythonFile}")
  if (NOT EXISTS "${_HANDLER_FILE}")
    message(FATAL_ERROR "Dependency handler file \"${_HANDLER_FILE}\" does not exist")
  endif()
  list(APPEND SVCOMP_DEPENDENCY_HANDLERS "${_HANDLER_FILE}")
  list(APPEND SVCOMP_ADDITIONAL_GEN_CMAKE_INC_DEPS "${_HANDLER_FILE}")
  unset(_HANDLER_FILE)
endmacro()

macro(add_benchmark BENCHMARK_DIR)
  set(INPUT_FILE ${CMAKE_CURRENT_SOURCE_DIR}/${BENCHMARK_DIR}/spec.yml)
  set(OUTPUT_FILE ${CMAKE_CURRENT_BINARY_DIR}/${BENCHMARK_DIR}_targets.cmake)
  # Only re-generate the file if necessary so that re-configure is as fast as possible
  set(_should_force_regen FALSE)
  foreach (dep ${SVCOMP_ADDITIONAL_GEN_CMAKE_INC_DEPS})
    if (NOT EXISTS "${dep}")
      message(FATAL_ERROR "Dependency \"${dep}\" does not exist")
    endif()
    if ("${dep}" IS_NEWER_THAN "${OUTPUT_FILE}")
      set(_should_force_regen TRUE)
    endif()
  endforeach()
  if (("${INPUT_FILE}" IS_NEWER_THAN "${OUTPUT_FILE}") OR ${_should_force_regen})
    message(STATUS "Generating \"${OUTPUT_FILE}\"")
    get_filename_component(OUTPUT_DIR "${OUTPUT_FILE}" DIRECTORY)
    file(MAKE_DIRECTORY ${OUTPUT_DIR})

    # If there are additional dependency handlers construct the command line
    # to request them to be loaded.
    set(_handler_args "")
    list(LENGTH SVCOMP_DEPENDENCY_HANDLERS SVCOMP_DEPENDENCY_HANDLERS_LENGTH)
    if ("${SVCOMP_DEPENDENCY_HANDLERS_LENGTH}" GREATER 0)
      list(APPEND _handler_args "--load-dependency-handlers")
      foreach (handler ${SVCOMP_DEPENDENCY_HANDLERS})
        list(APPEND _handler_args "${handler}")
      endforeach()
    endif()

    execute_process(COMMAND ${PYTHON_EXECUTABLE} "${SVCB_DIR}/tools/svcb-emit-cmake-decls.py"
                            ${INPUT_FILE}
                            --architecture ${SVCOMP_ARCHITECTURE}
                            --output ${OUTPUT_FILE}
                            ${_handler_args}
                    RESULT_VARIABLE RESULT_CODE
                   )
    if (NOT ${RESULT_CODE} EQUAL 0)
      # Remove the generated output file because it is broken and if we don't
      # the next time configure runs it will succeed.
      file(REMOVE "${OUTPUT_FILE}")
      message(FATAL_ERROR "Failed to process benchmark ${BENCHMARK_DIR}. With error ${RESULT_CODE}")
    endif()
    unset(_handler_args)
  endif()
  # Include the generated file
  include(${OUTPUT_FILE})

  # Iterate over the declared targets and perform any necessary action
  foreach (benchmark_target ${_benchmark_targets})
    if (WLLVM_RUN_EXTRACT_BC)
      add_custom_command(TARGET ${benchmark_target}
        POST_BUILD
        COMMAND ${WLLVM_EXTRACT_BC_TOOL} "$<TARGET_FILE:${benchmark_target}>" -o "$<TARGET_FILE:${benchmark_target}>.bc"
        COMMENT "Running ${WLLVM_EXTRACT_BC_TOOL} on ${benchmark_target}"
        ${ADD_CUSTOM_COMMAND_USES_TERMINAL_ARG}
      )
      # Make sure the output file gets removed when the `clean` target is invoked
      set_property(DIRECTORY
        APPEND
        PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "$<TARGET_FILE:${benchmark_target}>.bc"
      )
    endif()

    if (EMIT_AUGMENTED_BENCHMARK_SPECIFICATION_FILES)
      if (WLLVM_RUN_EXTRACT_BC)
        set(_extract_bc_arg "--llvm-bc-path" "$<TARGET_FILE:${benchmark_target}>.bc")
      endif()
      add_custom_command(TARGET ${benchmark_target}
        POST_BUILD
        COMMAND "${PYTHON_EXECUTABLE}" "${SVCB_DIR}/tools/svcb-emit-cmake-augmented-spec.py"
          "${INPUT_FILE}"
          "${benchmark_target}"
          "-o" "$<TARGET_FILE:${benchmark_target}>.yml"
          "--exe-path" "$<TARGET_FILE:${benchmark_target}>"
          ${_extract_bc_arg}
        COMMENT "Generating augmented benchmark specification file for ${benchmark_target}"
      )
      # Make sure the output file gets removed when the `clean` target is invoked
      set_property(DIRECTORY
        APPEND
        PROPERTY ADDITIONAL_MAKE_CLEAN_FILES "$<TARGET_FILE:${benchmark_target}>.yml"
      )
    set_property(GLOBAL APPEND PROPERTY
      SVCB_AUGMENTED_BENCHMARK_SPECIFICATION_FILES
      "$<TARGET_FILE:${benchmark_target}>.yml"
    )
    endif()
  endforeach()
  unset(_extract_bc_arg)

  if ("${CMAKE_VERSION}" VERSION_LESS "3.0")
    message(FATAL_ERROR "Need CMake >= 3.0 to support CMAKE_CONFIGURE_DEPENDS property on directories")
  endif()

  # Let CMake know that configuration depends on the benchmark specification file
  set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${INPUT_FILE}")
  foreach (dep ${SVCOMP_ADDITIONAL_GEN_CMAKE_INC_DEPS})
    set_property(DIRECTORY APPEND PROPERTY CMAKE_CONFIGURE_DEPENDS "${dep}")
  endforeach()
  unset(_should_force_regen)
endmacro()
