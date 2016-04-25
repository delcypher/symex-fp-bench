# Copyright 2016 Daniel Liew
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
add_custom_target(docs)
option(BUILD_DOXYGEN_DOCS "Build Doxygen documentation" ON)
find_package(Doxygen)
if (DOXYGEN_FOUND)
  message(STATUS "Doxygen found")

  # Configure the Doxyfile
  configure_file(Doxyfile.in Doxyfile @ONLY)

  # Add rule to build doxygen documentation
  add_custom_target(doc-doxygen
    COMMAND "${DOXYGEN_EXECUTABLE}" "${CMAKE_CURRENT_BINARY_DIR}/Doxyfile"
    COMMENT "Generating Doxygen documentation"
		${ADD_CUSTOM_COMMAND_USES_TERMINAL_ARG}
  )
	add_dependencies(docs doc-doxygen)
else()
  message(WARNING "Doxygen not found. Can't build Doxygen documentation")
  set(BUILD_DOXYGEN_DOCS OFF CACHE BOOL "Build Doxygen documentation" FORCE)
endif()
