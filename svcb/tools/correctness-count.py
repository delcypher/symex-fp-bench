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
  parser.add_argument("--categories", type=str, nargs='+', default=None, help='Only gather process benchmarks belonging to the specified categories')
  parser.add_argument("--mode", choices=['tasks','benchmark'], default='tasks', help='Group by tasks or by benchmark')
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
  benchmarksSkipped = set()
  verificationTaskMap = { }

  # Prepare verificationTaskMap
  if pargs.mode == 'tasks':
    # FIXME: Refactor to do preparation here
    pass
  elif pargs.mode == 'benchmark':
    verificationTaskMap[0] = set() # All correct
    verificationTaskMap[1] = set() # At least one incorrect task
    verificationTaskMap[2] = set() # Mixture of correct and unknown verification tasks.
    verificationTaskMap[3] = set() # All tasks are unknown
  else:
    raise Exception('Unreachable')

  onlyProcessCategories = set(pargs.categories) if pargs.categories != None else set()

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
          if pargs.categories != None:
            if len(onlyProcessCategories.intersection(benchmarkObj.categories)) == 0:
              # Skip
              benchmarksSkipped.add(benchmarkObj)
              continue

          # Verification tasks
          if pargs.mode == 'tasks':
            for (task, taskProperties) in benchmarkObj.verificationTasks.items():
                if task not in verificationTaskMap:
                  verificationTaskMap[task] = { True: [], False: [], None: [] }
                verificationTaskMap[task][taskProperties['correct']].append(benchmarkObj)
          elif pargs.mode == 'benchmark':
            group = determineGroup(benchmarkObj)
            verificationTaskMap[group].add(benchmarkObj)
          else:
            raise Exception('Unreachable')

  # Show statistics
  print("")
  print("# of file(s) successfully parsed: {}".format(len(benchmarkFileParseSuccess)))
  print("# of file(s) unsuccessfully parsed: {}".format(len(benchmarkFileParseFailures)))
  print("# of benchmarks: {}".format(len(benchmarkNames)))
  print("# of benchmarks: {}".format(len(benchmarkNames)))
  print("# of benchmarks skipped for further processing: {}".format(len(benchmarksSkipped)))
  print("")
  if pargs.mode == 'tasks':
    print("Verification Tasks")
    for (task, expectedResult) in verificationTaskMap.items():
      print("Task {}:".format(task))
      print("# of tasks expected to be correct: {}".format(len(expectedResult[True])))
      print("# of tasks expected to be incorrect: {}".format(len(expectedResult[False])))
      print("# of tasks with unknown correctness: {}".format(len(expectedResult[None])))
      print("")
  elif pargs.mode == 'benchmark':
    print("Grouped by benchmark")
    print("# of benchmarks that expect all tasks to be correct: {}".format(len(verificationTaskMap[0])))
    print("# of benchmarks that expect at least one task to be incorrect: {}".format(len(verificationTaskMap[1])))
    print("# of benchmarks that expect tasks to be a mixture of correct and unknown: {}".format(len(verificationTaskMap[2])))
    print("# of benchmarks that expect all tasks to be unknown: {}".format(len(verificationTaskMap[3])))
    print("")
  else:
    raise Exception('Unreachable')
  return 0


def determineGroup(benchmarkObj):
  """
    Returns 0 if benchmark expects all verification tasks to be correct.
    Returns 1 if benchmark expects at least one verification task to be incorrect.
    Returns 2 if benchmark expects a mixture of correct and unknown verification tasks.
    Return  3 if benchmarks expect all tasks to be unknown.
  """
  foundAllCorrect=True # Assume to be true until we discover to be false
  foundAllUnknown=True # Assume to be true until we discover to be false
  foundIncorrect=False # Assume to be false until we discover to be true
  foundMixedCorrectAndUnknown=True # Assume to be true until we discover to be false
  correctCount = 0
  for (taskName, properties) in benchmarkObj.verificationTasks.items():
    correct = properties['correct']
    if correct == False:
      foundIncorrect = True
      foundAllCorrect = False
      foundAllUnknown = False
      foundMixedCorrectAndUnknown = False
      break
    elif correct == None:
      foundAllCorrect = False
    elif correct == True:
      correctCount += 1
      foundAllUnknown = False

  if (correctCount == 0 and foundMixedCorrectAndUnknown) or foundAllUnknown:
    # We need to have seen at least one verification task expected to be
    # correct.
    foundMixedCorrectAndUnknown = False

  if foundAllCorrect:
    return 0

  if foundIncorrect:
    return 1

  if foundMixedCorrectAndUnknown:
    assert not foundAllUnknown
    return 2

  assert foundAllUnknown
  return 3


if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
