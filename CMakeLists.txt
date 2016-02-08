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
# Runtime libraries
###############################################################################
add_subdirectory(lib)

###############################################################################
# Benchmarks
###############################################################################
add_subdirectory(benchmarks)
