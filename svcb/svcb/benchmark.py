# Copyright (c) 2016, Daniel Liew
# This file is covered by the license in LICENSE-SVCB.txt
import copy
import pprint
import re

# This declares dictionary of verification tasks
# that is merged into to the loaded verification
# tasks of a `spec.yml` file. This serves to facilitate
# verification properties being implicitly assumed to be
# correct unless otherwise stated.
# This should be kept consistent with `schema.yml`.
DefaultVerificationTaskStatuses = {
  "no_assert_fail": { "correct": True },
  "no_reach_error_function": { "correct": True },
  "no_invalid_free": { "correct": True },
  "no_invalid_deref": { "correct": True },
  "no_integer_division_by_zero": { "correct": True },
  "no_overshift": { "correct": True},
}

class Benchmark(object):
  def __init__(self, data):
    assert isinstance(data, dict)
    # Just store the dict internally
    self._data = data
    assert 'variants' not in self._data
    # TODO: Add all implicit empty fields
    if 'description' not in self._data:
      self._data['description'] = ""
    if 'defines' not in self._data:
      self._data['defines'] = {}
    if 'dependencies' not in self._data:
      self._data['dependencies'] = {}
    if 'misc' not in self._data:
      self._data['misc'] = {}

  def __str__(self):
    return pprint.pformat(self._data)

  def getInternalRepr(self):
    return self._data

  @property
  def name(self):
    return self._data['name']

  @property
  def sources(self):
    return self._data['sources']

  @property
  def architectures(self):
    return self._data['architectures']

  @property
  def defines(self):
    return self._data['defines']

  @property
  def language(self):
    return self._data['language']

  @property
  def dependencies(self):
    return self._data['dependencies']

  @property
  def categories(self):
    return set(self._data['categories'])

  @property
  def description(self):
    return self._data['description']

  @property
  def verificationTasks(self):
    return self._data['verification_tasks']

  def isLanguageC(self):
    return not self.isLanguageCXX()

  def isLanguageCXX(self):
    return self.language.find('++') != -1

  @property
  def misc(self):
    return self._data['misc']

def getBenchmarks(benchSpec, addImplicitVerificationTasks=True):
  # FIXME: addImplicitVerificationTasks should always be set to True by clients.
  # It should only ever be set to False in unittests where we want to test
  # without the implicit tasks being added.
  #
  # We should probably remove this option entirely and fix up the tests to
  # prevent abuse.
  assert isinstance(benchSpec, dict)
  benchmarkSpecs = []
  benchmarkObjs = []
  if 'variants' in benchSpec:
    # Create a ``Benchmark`` object from each variant
    globalDefines = {}
    if 'defines' in benchSpec:
      globalDefines.update(benchSpec['defines'])
    globalDependencies = {}
    if 'dependencies' in benchSpec:
      globalDependencies.update(benchSpec['dependencies'])
    globalCategories = []
    if 'categories' in benchSpec:
      globalCategories = benchSpec['categories']
      # Ensure the categories are always sorted so clients can rely on this behaviour
      globalCategories.sort()
    globalDescription = ""
    if 'description' in benchSpec:
      globalDescription += benchSpec['description']
    globalName = benchSpec['name']
    for variantName, variantProperties in benchSpec['variants'].items():
      # Make a copy to work with
      benchSpecCopy = copy.deepcopy(benchSpec)
      # Modify the copied benchmark specification so it looks
      # like a single benchmark
      benchmarkDefines = dict(globalDefines)
      benchmarkDependencies = dict(globalDependencies)
      benchmarkCategories = list(globalCategories)
      benchmarkDescription = str(globalDescription)
      if 'defines' in variantProperties:
        benchmarkDefines.update(variantProperties['defines'])
      if 'dependencies' in variantProperties:
        benchmarkDependencies.update(variantProperties['dependencies'])
      if 'categories' in variantProperties:
        benchmarkCategories.extend(variantProperties['categories'])
        # Make categories unique and sorted.
        benchmarkCategories = set(benchmarkCategories)
        benchmarkCategories = list(benchmarkCategories)
        benchmarkCategories.sort()
      if 'description' in variantProperties:
        # Make the description for the benchmark be the concatenation
        # of the global and variant description.
        benchmarkDescription += "\n{}".format(variantProperties['description'])
      benchmarkName = "{}_{}".format(globalName, variantName)
      del benchSpecCopy['variants']
      benchSpecCopy['defines'] = benchmarkDefines
      benchSpecCopy['name'] = benchmarkName
      benchSpecCopy['dependencies'] = benchmarkDependencies
      benchSpecCopy['categories'] = benchmarkCategories
      benchSpecCopy['description'] = benchmarkDescription

      if 'verification_tasks' in variantProperties:
        assert 'verification_tasks' not in benchSpecCopy
        benchSpecCopy['verification_tasks'] = copy.deepcopy(variantProperties['verification_tasks'])
      else:
        assert 'verification_tasks' in benchSpecCopy

      benchmarkSpecs.append(benchSpecCopy)
  else:
    # Single benchmark
    # Make a copy to work with
    benchSpecCopy = copy.deepcopy(benchSpec)
    benchmarkSpecs.append(benchSpecCopy)

  # Make the benchmark objects from the specs
  for benchSpecCopy in benchmarkSpecs:
    # Add implicit verification tasks
    if addImplicitVerificationTasks:
      verificationTasks = benchSpecCopy['verification_tasks']
      for (task, properties) in DefaultVerificationTaskStatuses.items():
        if task not in verificationTasks:
          verificationTasks[task] = copy.deepcopy(properties)

    # Add implicit `exhaustive_counter_examples` field.
    for (task, properties) in benchSpecCopy['verification_tasks'].items():
      if properties['correct'] is False and not 'exhaustive_counter_examples' in properties:
        if 'counter_examples' in properties:
          properties['exhaustive_counter_examples'] = True
        else:
          properties['exhaustive_counter_examples'] = False

    # Finally build the object
    benchmarkObjs.append(Benchmark(benchSpecCopy))

  return benchmarkObjs
