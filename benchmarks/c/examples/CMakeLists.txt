# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt

# This is a toy library that is used to demonstrate
# handling external dependencies.
option(BUILD_TOY_LIBRARY "Build the toy library" ON)
if (BUILD_TOY_LIBRARY)
  add_library(toy_library STATIC toy_library/toy_library.c)
  set(TOY_LIBRARY_LIBS toy_library)
  set(TOY_LIBRARY_INCLUDES "${CMAKE_CURRENT_SOURCE_DIR}/toy_library")
endif()
add_cmake_dependency_handler(toy_library/toy_dependency_handler.py)

add_benchmark(simple_branch)
add_benchmark(simple_svcomp)
add_benchmark(simple_math)
