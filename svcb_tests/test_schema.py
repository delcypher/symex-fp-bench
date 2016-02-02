import svcb
from svcb import schema
import unittest

class TestSchema(unittest.TestCase):
  def setUp(self):
    self.persistentSchema = schema.getSchema()

  def appendSchemaVersion(self, d):
    d['schema_version'] = self.persistentSchema['__version__']

  def testLoadSchema(self):
    schemas = [ schema.getSchema(), self.persistentSchema ]
    for s in schemas:
      self.assertIsInstance(s, dict)
      self.assertIn('__version__', s)

  def testValidateSimpleCorrect(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'foo',
      'sources': ['a_is_a_good_name.c', 'b-IS-also-A-good-name.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    schema.validateBenchmarkSpecification(s)
    schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateSimpleIncorrect(self):
    s = {
      'architecture': 'foo',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"'foo' is not one of"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateIncorrectSchemaVersion(self):
    s = {
      'architecture': 'foo',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
      'schema_version': 123456
    }
    msgRegex= r"Schema version used by benchmark \(\d+\) does not match the currently support schema \(\d+\)"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateIncorrectSoureFilePath(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a bad name.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"'a bad name.c' does not match"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateIncorrectName(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'my bad benchmark name',
      'sources': ['a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"'my bad benchmark name' does not match"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateSimpleWithDefines(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'defines': { 'config1': ['FOO' 'BAR=BAZ', 'NUM=0'] },
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    schema.validateBenchmarkSpecification(s)
    schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateIncorrectDefine(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'defines': { 'config1': ['foo=bad value'] },
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"'foo=bad value' does not match"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)


