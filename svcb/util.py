from . import schema
import yaml

def loadBenchmarkSpecification(openFile):
  # FIXME: Use C loader implementation if available
  benchSpec = yaml.load(openFile)
  schema.validateBenchmarkSpecification(benchSpec)
  return benchSpec

