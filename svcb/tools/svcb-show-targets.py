#!/usr/bin/env python
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
"""
Reads a benchmark specification file and
prints the benchmarks it declares
"""
from load_svcb import add_svcb_to_module_search_path
add_svcb_to_module_search_path()
import argparse
import logging
import svcb
import svcb.util
import svcb.schema
import svcb.benchmark
import pprint
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

  pArgs = parser.parse_args()
  logLevel = getattr(logging, pArgs.log_level.upper(),None)
  logging.basicConfig(level=logLevel)
  _logger = logging.getLogger(__name__)

  try:
    benchSpec = svcb.schema.loadBenchmarkSpecification(pArgs.bench_spec_file)
  except svcb.schema.BenchmarkSpecificationValidationError as e:
    _logger.error('Failed to validate benchmark specification against schema')
    _logger.error(e.message)
    return 1
  except Exception as e:
    _logger.error('Exception raised whilst loading benchmark specification file')
    _logger.error(str(e))

  benchmarkObjs = svcb.benchmark.getBenchmarks(benchSpec)
  _logger.debug('Found {} benchmark(s)'.format(len(benchmarkObjs)))
  # Emit as a stream of YAML documents
  for index, benchmark in enumerate(benchmarkObjs):
    print("---")
    print("# benchmark {} of {}".format(index+1, len(benchmarkObjs)))
    print(yaml.dump(benchmark.getInternalRepr()))
if __name__ == '__main__':
  sys.exit(main(sys.argv))
