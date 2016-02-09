import copy
import pprint

class Benchmark(object):
  def __init__(self, data):
    assert isinstance(data, dict)
    # Just store the dict internally
    self._data = data

  def __str__(self):
    return pprint.pformat(self._data)

  def getInternalRepr(self):
    return self._data

  # TODO: Provide a nice interface


def getBenchmarks(benchSpec):
  assert isinstance(benchSpec, dict)
  benchmarkObjs = []
  if 'variants' in benchSpec:
    # Create a ``Benchmark`` object from each variant
    globalDefines = []
    if 'defines' in benchSpec:
      globalDefines.extend(benchSpec['defines'])
    globalName = benchSpec['name']
    for variantName, defines in benchSpec['variants'].items():
      # Make a copy to work with
      benchSpecCopy = copy.deepcopy(benchSpec)
      # Modify the copied benchmark specification so it looks
      # like a single benchmark
      benchmarkDefines = list(globalDefines)
      benchmarkDefines.extend(defines)
      benchmarkName = "{}_{}".format(globalName, variantName)
      del benchSpecCopy['variants']
      benchSpecCopy['defines'] = benchmarkDefines
      benchSpecCopy['name'] = benchmarkName
      benchmarkObjs.append(Benchmark(benchSpecCopy))
  else:
    # Single benchmark
    # Make a copy to work with
    benchSpecCopy = copy.deepcopy(benchSpec)
    benchmarkObjs.append(Benchmark(benchSpecCopy))
  return benchmarkObjs
