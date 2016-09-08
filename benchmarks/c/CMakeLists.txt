# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
add_subdirectory(examples)

# For now the benchmarks of each team will exist out of tree.
# However for convenience we have the build system pick up
# the directories of each team if they are present in the source tree.
if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/imperial")
  add_subdirectory(imperial)
endif()

if (EXISTS "${CMAKE_CURRENT_SOURCE_DIR}/aachen")
  add_subdirectory(aachen)
endif()
