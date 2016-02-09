# This overrides the default flags for the different CMAKE_BUILD_TYPEs
set(CMAKE_USER_MAKE_RULES_OVERRIDE "${CMAKE_CURRENT_SOURCE_DIR}/cmake/c_flags_override.cmake")
project(SVCOMP_C_BENCHMARKS LANGUAGES C)
cmake_minimum_required(VERSION 2.8.12)

# TODO: Detect target(S) supported by compiler

# TODO: Setup warning flags

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

###############################################################################
# Setup global include directory
###############################################################################
include_directories("${CMAKE_SOURCE_DIR}/include")

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
set(SVCOMP_TARGET_X86_64_FLAGS "-m64")
set(SVCOMP_TARGET_i686_FLAGS "-m32")

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
