#!/bin/bash
set -e
# For coverage build run a benchmark and check the coverage files
# appear where expected. Just test one test case for now.
if [ "X${C_COMPILER}" == "Xgcc" ]; then
  TESTCASE="${BUILD_DIR}/benchmarks/c/examples/simple_branch_non_klee_no_bug.x86_64"
  COVDIR="`pwd`/simple_branch_non_klee_no_bug.x86_64.cov"
  if [ ! -e "${TESTCASE}" ]; then
    echo "Failed to find \"${TESTCASE}\""
    exit 1
  fi
  if [ -d "${COVDIR}" ]; then
    echo "\"${COVDIR}\" should not exist"
    exit 1
  fi
  # Run test case
  ${TESTCASE}
  if [ ! -d "${COVDIR}" ]; then
    echo "\"${COVDIR}\" should exist"
    set +x
    ls -l "${BUILD_DIR}"
    find . -iname '*.gcda'
    find . -iname '*.gcno'
    exit 1
  fi
  # Check that the gcda files are present
  test "$((find ${COVDIR} -type f -iname '*.gcda' || echo '0') | wc -l)" -eq 1

  # Check that gcno information is present in the build
  test "$((find ${BUILD_DIR} -type f -iname '*.gcno' || echo '0') | wc -l)" -ne 0
else
  echo "Compiler ${C_COMPILER} not supported"
  exit 1
fi
