# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
#
# FindKLEENativeRuntime
# ---------------------
#
# Tries to find KLEE's native runtime that allows running
# programs designed to use KLEE's API natively.
#
# If the runtime is found `KLEE_NATIVE_RUNTIME_FOUND` will be set to TRUE
# and the following will be defined:
#
# KLEE_NATIVE_RUNTIME_FOUND - System has KLEE's native runtime
# KLEE_NATIVE_RUNTIME_INCLUDE_DIR - KLEE runtime include directory
# KLEE_NATIVE_RUNTIME_LIB
include(FindPackageHandleStandardArgs)

# Try to find libraries
find_library(KLEE_NATIVE_RUNTIME_LIB
  NAMES libkleeRuntest.so libkleeRuntest.dylib
  PATHS ENV KLEE_NATIVE_RUNTIME_LIB_DIR
  DOC "KLEE native runtime library"
)
if (KLEE_NATIVE_RUNTIME_LIB)
  message(STATUS "Found KLEE native runtime library: \"${KLEE_NATIVE_RUNTIME_LIB}\"")
else()
  message(STATUS "Could not find KLEE native runtime library.\n"
		"Try setting the KLEE_NATIVE_RUNTIME_LIB_DIR environment variable to the directory"
    " containing \"libkleeRuntest.so\""
  )
endif()

# Try to find headers
find_path(KLEE_NATIVE_RUNTIME_INCLUDE_DIR
  NAMES klee/klee.h
  PATHS ENV KLEE_NATIVE_RUNTIME_INCLUDE_DIR
  DOC "KLEE runtime header"
)
if (KLEE_NATIVE_RUNTIME_INCLUDE_DIR)
  message(STATUS "Found KLEE runtime include path: \"${KLEE_NATIVE_RUNTIME_INCLUDE_DIR}\"")
else()
  message(STATUS "Could not find KLEE runtime include path.\n"
    "Try setting the KLEE_NATIVE_RUNTIME_INCLUDE_DIR environment variable to the KLEE include directory"
  )
endif()

if (KLEE_NATIVE_RUNTIME_LIB AND KLEE_NATIVE_RUNTIME_INCLUDE_DIR)
  message(STATUS "Found KLEE native runtime")
else()
  message(STATUS "Could not find KLEE native runtime.")
endif()

# TODO: We should check we can link some simple code against KLEE's native runtime library

# Handle QUIET and REQUIRED and check the necessary variables were set and if so
# set ``KLEENativeRuntime_FOUND``
find_package_handle_standard_args(KLEE_NATIVE_RUNTIME DEFAULT_MSG KLEE_NATIVE_RUNTIME_INCLUDE_DIR KLEE_NATIVE_RUNTIME_LIB)
