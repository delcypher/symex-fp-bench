#!/bin/bash

set -e

: ${SOURCE_DIR:?SOURCE_DIR must be set to fp-bench source root}

if [ ! -e "${SOURCE_DIR}" ]; then
  echo "\"${SOURCE_DIR}\" does not exist"
  exit 1
fi

SVCB_SHOW_TARGETS="${SOURCE_DIR}/svcb/tools/svcb-show-targets.py"
SPEC_FILE_LIST="augmented_spec_files.txt"

test -f "${SPEC_FILE_LIST}"
LINES=0
while read l; do
  let LINES=${LINES}+1
  echo -n "Checking \"${l}\"..."
  if [ ! -e "${l}" ]; then
    echo "fail"
    exit 1
  else
    # Try to parse file
    set +e
    ${PYTHON_EXECUTABLE} ${SVCB_SHOW_TARGETS} "${l}" > /dev/null 2>&1
    if [ $? -ne 0 ]; then
      echo "fail"
      # Run again to show output
      set +x
      ${PYTHON_EXECUTABLE} ${SVCB_SHOW_TARGETS} "${l}"
      exit 1
    fi
    set -e
    echo "ok"
  fi
done < "${SPEC_FILE_LIST}"

if [ ${LINES} -lt 1 ]; then
  echo "${SPEC_FILE_LIST} is empty!"
  exit 1
fi

