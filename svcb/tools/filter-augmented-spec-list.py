#!/usr/bin/env python
"""
Loads a list of augmented spec files. Parses
them and optionally filters them based on
some criteria.
"""
from load_svcb import add_svcb_to_module_search_path
add_svcb_to_module_search_path()
import svcb
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
  parser.add_argument("augmented_spec_file_list",
                      type=argparse.FileType('r'))
  parser.add_argument("-o", "--output", type=argparse.FileType('w'), default=sys.stdout)
  parser.add_argument("--categories", type=str, nargs='+', default=None, help='Only gather process benchmarks belonging to the specified categories')
  pargs = parser.parse_args(args)
  logLevel = getattr(logging, pargs.log_level.upper(),None)
  logging.basicConfig(level=logLevel)
  _logger = logging.getLogger(__name__)

  benchmarkFileParseFailures = set()
  benchmarkFilesToKeep = set()
  for line in pargs.augmented_spec_file_list.readlines():
    filePath = line.strip() # Remove newlines
    if not os.path.exists(filePath):
      _logger.error('File "{}" does not exist'.format(filePath))
      return 1
    # Parse as spec file
    benchSpec = None
    try:
      with open(filePath, 'r') as f:
        _logger.debug('Parsing "{}"'.format(filePath))
        benchSpec = svcb.schema.loadBenchmarkSpecification(f)
    except svcb.schema.BenchmarkSpecificationValidationError as e:
      _logger.error('Failed to validate "{}"'.format(fullFileName))
      benchmarkFileParseFailures.add(fullFileName)
      continue
    # Get benchmark object
    benchmarkObjs = svcb.benchmark.getBenchmarks(benchSpec)
    assert len(benchmarkObjs) == 1
    benchmark = benchmarkObjs[0]

    if pargs.categories != None:
      allowedCategories = set(pargs.categories)
      if len(allowedCategories.intersection(benchmark.categories)) == 0:
        _logger.info('Dropping "{}"'.format(benchmark.name))
        continue
    benchmarkFilesToKeep.add(filePath)

  # Write output
  _logger.info('Keeping {} benchmarks'.format(len(benchmarkFilesToKeep)))
  for fileName in sorted(benchmarkFilesToKeep):
    pargs.output.write('{}\n'.format(fileName))

  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv[1:]))
