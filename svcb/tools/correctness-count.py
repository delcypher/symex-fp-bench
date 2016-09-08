#!/usr/bin/env python
# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
"""
Traverse a directory looking for benchmarks
and group them by expected correctness
"""
from load_svcb import add_svcb_to_module_search_path
add_svcb_to_module_search_path()
import svcb.schema
import svcb.benchmark
import argparse
import logging
import os
import sys

_logger = None

def main(args):
  global _logger
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("-l","--log-level",type=str, default="info",
                      dest="log_level",
                      choices=['debug','info','warning','error'])
  parser.add_argument("directory",
                      type=str,
                      help="Directory to traverse")
  pargs = parser.parse_args(args)
  logLevel = getattr(logging, pargs.log_level.upper(),None)
  logging.basicConfig(level=logLevel)
  _logger = logging.getLogger(__name__)

  if not os.path.isdir(pargs.directory):
    _logger.error('"{}" is not a directory'.format(pargs.directory))
    return 1

  # Stats
  benchmarkFileParseSuccess = set()
  benchmarkFileParseFailures = set()
  benchmarkNames = set()
  verificationTaskMap = { }

  # Traverse directory
  for dirpath, dirnames, filenames in os.walk(pargs.directory):
    for fname in filenames:
      if fname == 'spec.yml':
        fullFileName = os.path.join(dirpath, fname)
        _logger.debug('Found file "{}"'.format(fullFileName))

        benchSpec = None
        try:
          with open(fullFileName, 'r') as f:
            benchSpec = svcb.schema.loadBenchmarkSpecification(f)
        except svcb.schema.BenchmarkSpecificationValidationError as e:
          _logger.error('Failed to validate "{}"'.format(fullFileName))
          benchmarkFileParseFailures.add(fullFileName)
          continue

        _logger.debug('Successfuly parsed and validated "{}"'.format(fullFileName))
        benchmarkFileParseSuccess.add(fullFileName)
        sys.stdout.write("Loaded {} file(s)\r".format(len(benchmarkFileParseSuccess)))

        # Convert to BenchmarkObjects. This also handles variants by giving
        # back multiple BenchmarkObjects
        benchmarkObjs = svcb.benchmark.getBenchmarks(benchSpec)
        assert len(benchmarkObjs) > 0
        for benchmarkObj in benchmarkObjs:
          assert benchmarkObj.name not in benchmarkNames
          benchmarkNames.add(benchmarkObj.name)

          # Verification tasks
          for (task, taskProperties) in benchmarkObj.verificationTasks.items():
            if task not in verificationTaskMap:
              verificationTaskMap[task] = { True: [], False: [], None: [] }
            verificationTaskMap[task][taskProperties['correct']].append(benchmarkObj)

  # Show statistics
  print("")
  print("# of file(s) successfully parsed: {}".format(len(benchmarkFileParseSuccess)))
  print("# of file(s) unsuccessfully parsed: {}".format(len(benchmarkFileParseFailures)))
  print("# of benchmarks: {}".format(len(benchmarkNames)))
  print("")
  print("Verification Tasks")
  for (task, expectedResult) in verificationTaskMap.items():
    print("Task {}:".format(task))
    print("# of tasks expected to be correct: {}".format(len(expectedResult[True])))
    print("# of tasks expected to be incorrect: {}".format(len(expectedResult[False])))
    print("# of tasks with unknown correctness: {}".format(len(expectedResult[None])))
    print("")
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
