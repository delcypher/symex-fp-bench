#!/bin/bash

KLEE_SRC=${KLEE_SRC:-https://github.com/klee/klee/archive/v1.2.0.tar.gz}
BUILD_DIR=${BUILD_DIR:-_build}
WLLVM_SHA1=b61dd0fd1b9170cef84622e270d72909cd817d1f
WLLVM_GIT_URL=https://github.com/travitch/whole-program-llvm.git

# Exit if there is an error
set -e

# Show commands as they are executed
set -x

export SOURCE_DIR="$(dirname $(cd ${BASH_SOURCE[0]%/*} ; pwd))"

if [ ! -d "${SOURCE_DIR}" ]; then
  echo "\"${SOURCE_DIR}\" is not a directory"
  exit 1
fi

# Note we use ``C_COMPILER`` rather than ``CC`` because
# TravisCI overrides the ``CC`` variable
: ${C_COMPILER?C_COMPILER must be set}
  # Note we use ``CXX_COMPILER`` rather than ``CXX`` because
  # TravisCI overrides the ``CXX`` variable
: ${CXX_COMPILER?CXX_COMPILER must be set}

if [ "${C_COMPILER}" == "wllvm" ]; then
  echo "Using wllvm"
  if [ "${CXX_COMPILER}" != "wllvm++" ]; then
    echo "CXX_COMPILER must be wllvm++ if C_COMPILER is wllvm"
    exit 1
  fi
  git clone ${WLLVM_GIT_URL} wllvm_git && cd wllvm_git && git checkout ${WLLVM_SHA1} && cd ../
  export PATH=`pwd`/wllvm_git:$PATH
  export LLVM_COMPILER=clang
fi

export C_COMPILER
export CXX_COMPILER

echo "C Compiler:"
${C_COMPILER} -v --version
echo "C++ Compiler:"
${CXX_COMPILER} -v --version
echo "CMake"
cmake --version

: ${PROFILING?"PROFILING must be set to 0 or 1"}
if [ "X${PROFILING}" = "X0" ]; then
  CMAKE_PROFILING_BUILD_FLAG="-DBUILD_WITH_PROFILING=OFF"
else
  CMAKE_PROFILING_BUILD_FLAG="-DBUILD_WITH_PROFILING=ON"
fi

if [ -n "${PYTHON_EXECUTABLE}" ]; then
  CMAKE_PYTHON_FLAG="-DPYTHON_EXECUTABLE=${PYTHON_EXECUTABLE}"
  export PYTHON_EXECUTABLE
else
  CMAKE_PYTHON_FLAG=""
fi

mkdir -p ${BUILD_DIR} && cd ${BUILD_DIR}

# Make BUILD_DIR absolute
BUILD_DIR="$(cd ${BUILD_DIR}; pwd)"
export BUILD_DIR

# HACK:
# We need a KLEE header file and runtime library. KLEE's build system is
# stupidly fragile and complicated so just grab a release (for speed compared
# to grabbing from git) and build it manually.
wget ${KLEE_SRC} -O klee_src.tar.gz
tar -xvf klee_src.tar.gz
export KLEE_NATIVE_RUNTIME_INCLUDE_DIR="$(pwd)/klee-1.2.0/include"
# Build the KLEE runtime
${C_COMPILER} -I ${KLEE_NATIVE_RUNTIME_INCLUDE_DIR} -g -O2 -fpic -c $(pwd)/klee-1.2.0/runtime/Runtest/intrinsics.c -o runtest.o
${CXX_COMPILER} -I ${KLEE_NATIVE_RUNTIME_INCLUDE_DIR} -g -O2 -fpic -c $(pwd)/klee-1.2.0/lib/Basic/KTest.cpp -o ktest.o
${CXX_COMPILER} -shared runtest.o ktest.o -o $(pwd)/klee-1.2.0/runtime/Runtest/libkleeRuntest.so
export KLEE_NATIVE_RUNTIME_LIB_DIR="$(pwd)/klee-1.2.0/runtime/Runtest"

CC=${C_COMPILER} \
CFLAGS="${EXTRA_C_FLAGS}" \
CXX=${CXX_COMPILER} \
CXXFLAGS="${EXTRA_CXX_FLAGS}" \
cmake ${CMAKE_PYTHON_FLAG} "${CMAKE_PROFILING_BUILD_FLAG}" "${SOURCE_DIR}"
make check-svcb
make VERBOSE=1
make show-categories
make show-tasks
make show-correctness-summary

# Augmented spec files
make build-augmented-spec-files
make create-augmented-spec-file-list
"${SOURCE_DIR}/scripts/check_augmented_files.sh"

if [ "X${PROFILING}" != "X0" ]; then
  ${SOURCE_DIR}/scripts/check_coverage_build.sh
fi

# TODO: If wllvm build check the bitcode files exist and can be read.
