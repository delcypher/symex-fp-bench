import collections
import copy
import os
import pprint
import yaml
import jsonschema

class BenchmarkSpecificationValidationError(Exception):
  def __init__(self, message, absoluteSchemaPath=None):
    assert isinstance(message, str)
    if absoluteSchemaPath != None:
      assert isinstance(absoluteSchemaPath, collections.deque)
    self.message = message
    self.absoluteSchemaPath = absoluteSchemaPath

def getSchema():
  """
    Return the Schema for SV-COMP benchmark specification
    files.
  """
  yamlFile = os.path.join(os.path.dirname(__file__), 'schema.yml')
  schema = None
  with open(yamlFile, 'r') as f:
    schema = yaml.load(f)
  assert isinstance(schema, dict)
  assert '__version__' in schema
  return schema

def validateBenchmarkSpecification(benchSpec, schema=None):
  """
    Validate a benchmark specification ``benchSpec``.
    Will throw a ``BenchmarkSpecificationValidationError`` exception if
    something is wrong
  """
  assert isinstance(benchSpec, dict)
  if schema == None:
    schema = getSchema()
  assert isinstance(schema, dict)
  assert '__version__' in schema

  # Even though the schema validates this field in the benchSpec we need to
  # check them ourselves first because if the schema version we have doesn't
  # match then we can't validate using it.
  if 'schema_version' not in benchSpec:
    raise BenchmarkSpecificationValidationError(
      "'schema_version' is missing")
  if not isinstance(benchSpec['schema_version'], int):
    raise BenchmarkSpecificationValidationError(
      "'schema_version' should map to an integer")
  if not benchSpec['schema_version'] >= 0:
    raise BenchmarkSpecificationValidationError(
      "'schema_version' should map to an integer >= 0")
  if benchSpec['schema_version'] != schema['__version__']:
    raise BenchmarkSpecificationValidationError(
        ('Schema version used by benchmark ({}) does not match' +
        ' the currently support schema ({})').format(
          benchSpec['schema_version'],
          schema['__version__']))

  # Validate against the schema
  try:
    jsonschema.validate(benchSpec, schema)
  except jsonschema.exceptions.ValidationError as e:
    raise BenchmarkSpecificationValidationError(
        str(e),
        e.absolute_schema_path)

  # Do additional sanity checks if necessary

def upgradeBenchmarkSpecification(benchSpec, schema=None):
  # TODO:
  newBenchSpec = copy.deepcopy(benchSpec)
  if schema == None:
    schema = getSchema()
  assert '__version__' in schema
  assert 'schema_version' in benchSpec

  if schema['__version__'] == benchSpec['schema_version']:
    # Nothing to do
    pass
  else:
    raise NotImplementedException()

  # Check the upgraded benchmark spec
  validateBenchmarkSpecification(newBenchSpec, schema=schema)
  return newBenchSpec
