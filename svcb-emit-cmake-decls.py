#!/usr/bin/env python
"""
Reads a benchmark specification file and
emits CMake declarations for building the
bencmarks
"""
import argparse
import logging
import os
import pprint
import svcb
import svcb.benchmark
import svcb.build
import svcb.schema
import svcb.util
import sys
import yaml

_logger = None

def main(args):
  global _logger
  parser = argparse.ArgumentParser(description=__doc__)
  parser.add_argument("-l","--log-level",type=str, default="info",
                      dest="log_level",
                      choices=['debug','info','warning','error'])
  parser.add_argument('bench_spec_file',
                      help='Benchmark specification file',
                      type=argparse.FileType('r'))
  parser.add_argument('-o', '--output',
                      type=argparse.FileType('w'),
                      default=sys.stdout,
                      help='Output location (default stdout)')

  pArgs = parser.parse_args()
  logLevel = getattr(logging, pArgs.log_level.upper(),None)
  logging.basicConfig(level=logLevel)
  _logger = logging.getLogger(__name__)

  try:
    benchSpec = svcb.util.loadBenchmarkSpecification(pArgs.bench_spec_file)
  except svcb.schema.BenchmarkSpecificationValidationError as e:
    _logger.error('Failed to validate benchmark specification against schema')
    _logger.error(e.message)
    return 1
  except Exception as e:
    _logger.error('Exception raised whilst loading benchmark specification file')
    _logger.error(str(e))

  # Get absolute path to benchmark specification file
  bSpecPath = os.path.realpath(pArgs.bench_spec_file.name)
  sourceFileDirectory = os.path.dirname(bSpecPath)

  benchmarkObjs = svcb.benchmark.getBenchmarks(benchSpec)
  _logger.debug('Found {} benchmark(s)'.format(len(benchmarkObjs)))
  # FIXME: Get CMake to pass us the architectures it knows the compiler can build for
  cmakeDeclStr = svcb.build.generateCMakeDecls(benchmarkObjs,
                                               sourceRootDir=sourceFileDirectory,
                                               supportedArchitectures={'x86_64'})
  pArgs.output.write(cmakeDeclStr)

if __name__ == '__main__':
  sys.exit(main(sys.argv))