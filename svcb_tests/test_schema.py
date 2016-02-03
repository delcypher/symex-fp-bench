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

  def testValidateIncorrectArchitecture(self):
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

  def testValidateIncorrectLanguage(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c++11',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"'c\+\+11' is not one of"
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

  def testValidateIncorrectSourceFilePath(self):
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

  def testValidateIncorrectRelativeSourcePath(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['../a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"not allowed for '\.\./a.c'"
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
      'defines': ['FOO', 'BAR=0'],
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    schema.validateBenchmarkSpecification(s)
    schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateSimpleWithIncorrectDefines(self):
    s = {
      'architecture': 'x86_64',
      'defines': ['badmacro name', 'BAR=0'],
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex = r"'badmacro name' does not match"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateSimpleWithVariants(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'variants': { 'config1': ['FOO' 'BAR=BAZ', 'NUM=0'],
                   'config2' : ['NUM=1']},
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    schema.validateBenchmarkSpecification(s)
    schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateIncorrectVariantDefine(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'variants': { 'config1': ['foo=bad value'] },
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"'foo=bad value' does not match"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)

  def testValidateIncorrectBuildVariantName(self):
    s = {
      'architecture': 'x86_64',
      'language': 'c99',
      'name': 'mybenchmark',
      'sources': ['a.c', 'b.c'],
      'variants': { 'bad build variant name': ['FOO=1'] },
      'verification_tasks': [
        'CHECK( init(main()), LTL(G ! call(__VERIFIER_error())) )'],
    }
    self.appendSchemaVersion(s)
    msgRegex= r"Additional properties are not allowed \('bad build variant name'"
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s)
    with self.assertRaisesRegex(schema.BenchmarkSpecificationValidationError, msgRegex):
      schema.validateBenchmarkSpecification(s, schema=self.persistentSchema)


