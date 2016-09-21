#!/usr/bin/env python
# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
"""
Reads a benchmark specification file and a CMake target name
and emit the corresponding benchmark specification file
(variants removed) optionally augmented with paths to
files built by the CMake build system.
"""
from load_svcb import add_svcb_to_module_search_path
add_svcb_to_module_search_path()
import argparse
import logging
import os
import pprint
import re
import svcb
import svcb.benchmark
import svcb.build
import svcb.schema
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
  parser.add_argument('--exe-path', dest='exe_path', type=str, default=None)
  parser.add_argument('--llvm-bc-path', dest='llvm_bc_path', type=str, default=None)
  parser.add_argument('-o', '--output',
                      type=argparse.FileType('w'),
                      default=sys.stdout,
                      help='Output location (default stdout)')
  parser.add_argument('cmake_target_name', type=str)

  pArgs = parser.parse_args()
  logLevel = getattr(logging, pArgs.log_level.upper(),None)
  logging.basicConfig(level=logLevel)
  _logger = logging.getLogger(__name__)

  # Extract the benchmark name and architecture.
  matchResult = re.match(r'^(.+)\.(.+)$', pArgs.cmake_target_name)
  if matchResult == None:
    _logger.error('cmake_target_name not in valid format')
    return 1
  benchmarkName = matchResult.group(1)
  assert isinstance(benchmarkName, str) and len(benchmarkName) > 0
  benchmarkArchitecture = matchResult.group(2)
  assert isinstance(benchmarkArchitecture, str) and len(benchmarkArchitecture) > 0

  # Load benchmark specification file.
  try:
    benchSpec = svcb.schema.loadBenchmarkSpecification(pArgs.bench_spec_file)
  except svcb.schema.BenchmarkSpecificationValidationError as e:
    _logger.error('Failed to validate benchmark specification against schema')
    _logger.error(e.message)
    return 1
  except Exception as e:
    _logger.error('Exception raised whilst loading benchmark specification file')
    _logger.error(str(e))
    raise e

  # Get absolute path to benchmark specification file
  bSpecPath = os.path.realpath(pArgs.bench_spec_file.name)
  sourceFileDirectory = os.path.dirname(bSpecPath)

  # Extract the benchmark objects
  benchmarkObjs = svcb.benchmark.getBenchmarks(benchSpec)
  _logger.debug('Found {} benchmark(s)'.format(len(benchmarkObjs)))

  # Find the relevant benchmark object
  _logger.debug('Looking for benchmark with name "{}"'.format(benchmarkName))
  filteredBenchmarkObjs  = list(filter(lambda b: b.name == benchmarkName, benchmarkObjs))

  if len(filteredBenchmarkObjs) != 1:
    _logger.error('Failed to find requested benchmark {} in file {}'.format(benchmarkName, bSpecPath))
    return 1

  benchmarkObj = filteredBenchmarkObjs[0]

  # Augment the benchmark with additional data
  if pArgs.exe_path:
    benchmarkObj.getInternalRepr()['misc']['exe_path'] = pArgs.exe_path

  if pArgs.llvm_bc_path:
    benchmarkObj.getInternalRepr()['misc']['llvm_bc_path'] = pArgs.llvm_bc_path

  # Output as YAML
  pArgs.output.write('# Automatically generated from "{}"\n'.format(bSpecPath))
  pArgs.output.write(yaml.dump(benchmarkObj.getInternalRepr(), default_flow_style=False))
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
