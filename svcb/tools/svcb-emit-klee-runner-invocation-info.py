#!/usr/bin/env python
# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
"""
Reads a file containing a list of augmented spec files
and generate a corresponding invocation info file to
give to the klee-runner infrastructure.
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
  parser.add_argument("--program",
                      choices=['llvm_bc', 'exe'],
                      default='llvm_bc',
                      help='Select which program to instruct the infrastructure to run')
  parser.add_argument("-l","--log-level",type=str, default="info",
                      dest="log_level",
                      choices=['debug','info','warning','error'])
  parser.add_argument('augmented_spec_file_list',
                      help='Benchmark specification file',
                      type=argparse.FileType('r'))
  parser.add_argument('-o', '--output',
                      type=argparse.FileType('w'),
                      default=sys.stdout,
                      help='Output location (default stdout)')

  pargs = parser.parse_args()
  logLevel = getattr(logging, pargs.log_level.upper(),None)
  logging.basicConfig(level=logLevel)
  _logger = logging.getLogger(__name__)

  invocationInfos = { 'schema_version':0, 'jobs':[]}

  for path in pargs.augmented_spec_file_list:
    strippedPath = path.strip() # Remove trailing whitespace and newlines
    _logger.info('Loading "{}"'.format(strippedPath))
    # Load benchmark specification file.
    try:
      with open(strippedPath, 'r') as f:
        benchSpec = svcb.schema.loadBenchmarkSpecification(f)
    except svcb.schema.BenchmarkSpecificationValidationError as e:
      _logger.error('Failed to validate benchmark specification against schema')
      _logger.error(e.message)
      return 1
    except Exception as e:
      _logger.error('Exception raised whilst loading benchmark specification file')
      _logger.error(str(e))
      raise e
    benchmarkObjs = svcb.benchmark.getBenchmarks(benchSpec)
    assert len(benchmarkObjs) == 1 # Augmented spec files should contain no variants

    benchmarkObj = benchmarkObjs[0]

    programPath=None
    if pargs.program == 'llvm_bc':
      programPath = benchmarkObj.misc['llvm_bc_path']
    elif pargs.program == 'exe':
      programPath = benchmarkObj.misc['exe_path']
    else:
      raise Exception('Unreachable')

    # Make program path absolute
    programPath = os.path.join(os.path.dirname(strippedPath), programPath)

    job = {
      'command_line_arguments': benchmarkObj.runtimeEnvironment['command_line_arguments'],
      'environment_variables': benchmarkObj.runtimeEnvironment['environment_variables'],
      'program': programPath,
      'misc': {
        'augmented_spec_file': os.path.abspath(strippedPath),
      }
    }
    invocationInfos['jobs'].append(job)

  # Output as YAML
  pargs.output.write('# Automatically generated invocation info\n')
  pargs.output.write(yaml.dump(invocationInfos, default_flow_style=False))
  return 0

if __name__ == '__main__':
  sys.exit(main(sys.argv))
