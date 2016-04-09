# This overrides the default flags for the different CMAKE_BUILD_TYPEs
set(CMAKE_USER_MAKE_RULES_OVERRIDE "${CMAKE_CURRENT_SOURCE_DIR}/cmake/c_flags_override.cmake")
project(SVCOMP_C_BENCHMARKS C CXX)
cmake_minimum_required(VERSION 2.8.12)

###############################################################################
# Set useful variables depending on CMake version
###############################################################################
if (("${CMAKE_VERSION}" VERSION_EQUAL "3.2") OR ("${CMAKE_VERSION}" VERSION_GREATER "3.2"))
  # In CMake >= 3.2 add_custom_command() supports a ``USES_TERMINAL`` argument
  set(ADD_CUSTOM_COMMAND_USES_TERMINAL_ARG "USES_TERMINAL")
else()
  set(ADD_CUSTOM_COMMAND_USES_TERMINAL_ARG "")
endif()
# Detect target supported by compiler
include(${CMAKE_SOURCE_DIR}/cmake/target_arch_detect.cmake)
detect_target_architecture(SVCOMP_ARCHITECTURE)
if (NOT SVCOMP_ARCHITECTURE)
  message(FATAL_ERROR "Failed to detect target architecture")
endif()

###############################################################################
# Set default project BUILD_TYPE
###############################################################################
if(NOT CMAKE_BUILD_TYPE)
  set(CMAKE_BUILD_TYPE "Release" CACHE STRING
      "Choose the type of build, options are: Debug Release RelWithDebInfo MinSizeRel." FORCE)
endif()
message(STATUS "CMAKE_BUILD_TYPE:${CMAKE_BUILD_TYPE}")

###############################################################################
# Find Python
###############################################################################
find_package(PythonInterp REQUIRED)
if ("${PYTHON_VERSION_STRING}" VERSION_LESS "2.7.0")
  message(FATAL_ERROR "Detected version of Python is too old (need >= 2.7)."
    " You can pass -DPYTHON_EXECUTABLE=/path/python to use a different version"
    " of Python")
endif()

###############################################################################
# Setup global include directory
###############################################################################
include_directories("${CMAKE_SOURCE_DIR}/include")

###############################################################################
# Documentation
###############################################################################
option(BUILD_DOCS "Build documentation" ON)
if (BUILD_DOCS)
  add_subdirectory(docs)
endif()

###############################################################################
# Setup variables used by auto generated CMake files
###############################################################################
# FIXME: Detect these and set them
set(SVCOMP_STD_C89 "-std=c89")
set(SVCOMP_STD_C99 "-std=c99")
set(SVCOMP_STD_C11 "-std=c11")
set(SVCOMP_STD_GNUC89 "-std=gnu89")
set(SVCOMP_STD_GNUC99 "-std=gnu99")
set(SVCOMP_STD_GNUC11 "-std=gnu11")
set(SVCOMP_STD_CXX98 "-std=c++98")
set(SVCOMP_STD_CXX03 "-std=c++03")
set(SVCOMP_STD_CXX11 "-std=c++11")
set(SVCOMP_STD_CXX14 "-std=c++14")
set(SVCOMP_STD_GNUCXX98 "-std=gnu++98")
set(SVCOMP_STD_GNUCXX03 "-std=gnu++03")
set(SVCOMP_STD_GNUCXX11 "-std=gnu++11")
set(SVCOMP_STD_GNUCXX14 "-std=gnu++14")

###############################################################################
# Detect supported warning flags
###############################################################################
# FIXME: Do this properly
set(SVCOMP_WARNING_FLAGS
    -Wall
    -Werror=main
    -Werror=implicit
   )
# Set flags globally
add_compile_options(${SVCOMP_WARNING_FLAGS})

###############################################################################
# Detect libraries that benchmarks may depend on
###############################################################################
# Pthreads
set(CMAKE_THREAD_PREFER_PTHREAD TRUE)
find_package(Threads)
find_package(OpenMP)

###############################################################################
# Add add_svcomp_benchmark() macro
###############################################################################
include(cmake/add_svcomp_benchmark.cmake)

###############################################################################
# Runtime libraries
###############################################################################
add_subdirectory(lib)

###############################################################################
# Python tests
###############################################################################
add_custom_target(check-svcb ALL
                  COMMAND ${PYTHON_EXECUTABLE} -m unittest discover
                  WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                  COMMENT "Running svcb unit tests"
                 )

###############################################################################
# Benchmarks
###############################################################################
add_subdirectory(benchmarks)
