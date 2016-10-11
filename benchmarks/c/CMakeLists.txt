# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
add_subdirectory(examples)

# For now the benchmarks of each team will exist out of tree.
# However for convenience we have the build system pick up
# the directories of each team if they are present in the source tree.
if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/imperial")
  option(BUILD_IMPERIAL_BENCHMARKS "Build the Imperial team's benchmarks" ON)
  if (BUILD_IMPERIAL_BENCHMARKS)
    add_subdirectory(imperial)
  endif()
endif()

if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/aachen")
  option(BUILD_AACHEN_BENCHMARKS "Build the Aachen team's benchmarks" ON)
  if (BUILD_AACHEN_BENCHMARKS)
    add_subdirectory(aachen)
  endif()
endif()
